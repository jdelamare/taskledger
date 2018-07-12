# Copyright Capstone Team B
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import logging
import hashlib

# Sawtooth SDK
from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

# Skltn protos
from protobuf.task_pb2 import *
from protobuf.payload_pb2 import *
from protobuf.project_node_pb2 import *
from protobuf.sprint_node_pb2 import *

# Skltn addressing specs
import addressing


LOGGER = logging.getLogger(__name__)


class SkltnTransactionHandler(TransactionHandler):
    @property
    def family_name(self):
        return addressing.FAMILY_NAME

    @property
    def family_versions(self):
        return ['0.1']

    @property
    def namespaces(self):
        return [addressing.NAMESPACE] # how to determine address prefix

    def apply(self, transaction, state):
        '''
        A Payload consists of a timestamp, an action tag, and
        attributes corresponding to various actions (create_asset,
        touch_asset, etc).  The appropriate attribute will be selected
        depending on the action tag, and that information plus the 
        timestamp and the public key with which the transaction was signed
        will be passed to the appropriate handler function
        unpack_transaction gets the signing key, the timestamp, and the 
        appropriate payload attribute and handler function
        '''
        # TO DO : check that timestamp is valid before calling handler.
        signer, timestamp, payload, handler = _unpack_transaction(transaction, state)

        # note that handler will be chosen by what was given to unpack
        handler(payload, signer, timestamp, state)


# Handler functions
def _create_task(payload, signer, timestamp, state):
    if not payload.task_name:
        raise InvalidTransaction(
            'Task must have a name.'
    )

    if not payload.description:
         raise InvalidTransaction(
            'Task must have a description.'
    )
    current_sprint = None

    # check if pk is authorized 
    project_address = addressing.make_project_node_address(payload.project_name)
    project_container = _get_container(state, project_address) 

    # inside a list of projects there is a list of keys. check 'em
    for project_node in project_container.entries: 
        if project_node.project_name == payload.project_name:
            _verify_contributor(state,signer, payload.project_name)
            current_sprint = project_node.current_sprint
    
    # check that the task doesn't already exist
    sprint_address = addressing.make_sprint_node_address(payload.project_name,str(current_sprint))

    sprint_container = _get_container(state, sprint_address)

    for sprint_node in sprint_container.entries: 
        if sprint_node.project_name == payload.project_name:
            if any(task == payload.task_name for task in sprint_node.task_names):
                raise InvalidTransaction(
                    "This task name is already in use.")
            sprint_node.task_names.extend([payload.project_name])

            _set_container(state, sprint_address, sprint_container)

    # we made it here, it's all good. create the object
    task = Task (
        project_name = payload.project_name,
        task_name = payload.task_name,
        description = payload.description,
        timestamp = timestamp)
 
    # create the task
    address = addressing.make_task_address(payload.project_name, current_sprint, payload.task_name)

    container = _get_container(state, address)

    container.entries.extend([task])       

    _set_container(state, address, container)

""" creating a project involves creating a first sprint"""
def _create_project(payload, signer, timestamp, state):
    # raise InvalidTransaction('this is not working')
    FIRST_SPRINT = '0'
    # check for complete payload
    if not payload.project_name:
        raise InvalidTransaction(
            "Project must have a name")

    project_address = addressing.make_project_node_address(payload.project_name)
    project_container = _get_container(state,project_address)

    if not project_container: #if no container exists, create one
        project_container = ProjectNodeContainer(entries=[])

    #check to see if a project already exists under the same name
    if any(project_node.project_name == payload.project_name
        for project_node in project_container.entries):
            raise InvalidTransaction(
                'Project with this name already exists.')

    # create the metanode protobuf object
    project_node = ProjectNode(
        project_name = payload.project_name,
        public_keys = [signer], #add creator of project to authorized public key list
        current_sprint = int(FIRST_SPRINT))

    #add project to container
    project_container.entries.extend([project_node])
    #set state with new project included
    _set_container(state,project_address,project_container)

    # initialize first sprint node
    sprint_node_address = addressing.make_sprint_node_address(payload.project_name, FIRST_SPRINT)
    sprint_container = _get_container(state, sprint_node_address)

    if not sprint_container:  # if no container exists, create one
        sprint_container = SprintNodeContainer(entries=[])
    
    sprint_node = SprintNode(
        project_name=payload.project_name,
        task_names=[])
    
    sprint_container.entries.extend([sprint_node])
    
    _set_container(state,sprint_node_address,sprint_container)


def _progress_task(payload, signer, timestamp, state):
    # check for complete payload
    if not payload.project_name:
        raise InvalidTransaction(
            "a project name must be provided")
    if not payload.task_name:
        raise InvalidTransaction(
            "a task name must be provided")
    # verify transaction is signed by authorized key
    _verify_contributor(signer, payload.project_name)

    # make task address
    task_address = addressing.make_task_address(payload.project_name,
                                                _get_project_node(payload.project_name).current_sprint,
                                                payload.task_name)
    # get the container with tasks at this address
    task_container = _get_container(state, task_address)
    # check if it doesn't exist
    if not task_container:
        raise InvalidTransaction(
            "task with specified name does not exist")
    # find the task with the correct name
    for task in task_container.entries:
        if task.task_name == payload.task_name:
            # check if the task is already complete
            if task.progress==task.DONE:
                raise InvalidTransaction(
                    "task already complete")
            # increase progression level of task
            task.progress += 1
            # set the new state
            _set_container(state,task_address,task_container)
            return
    # if task with specified name not found, reject transaction
    raise InvalidTransaction(
        "task with specified name does not exist")


def _edit_task(payload, signer, timestamp, state):
    # check for complete payload
    if not payload.project_name:
        raise InvalidTransaction(
            "a project name must be provided")
    if not payload.task_name:
        raise InvalidTransaction(
            "a task name must be provided")
    # verify transaction is signed by authorized key
    _verify_contributor(signer, payload.project_name)
    # make task address
    task_address = addressing.make_task_address(payload.project_name,
                                                _get_project_node(payload.project_name).current_sprint,
                                                payload.task_name)
    # get the container with tasks at this address
    task_container = _get_container(state,task_address)
    # check if it doesn't exist
    if not task_container:
        raise InvalidTransaction(
            "task with specified name does not exist")
    # find the task with the correct name
    for task in task_container.entries:
        if task.task_name == payload.task_name:
            # set the new description and put it in state
            task.description = payload.description
            _set_container(state, task_address, task_container)
            return
    # if task with specified name not found, reject transaction
    raise InvalidTransaction(
        "task with specified name does not exist")


def _increment_sprint(payload, signer, timestamp, state):
    # check for complete payload
    if not payload.project_name:
        raise InvalidTransaction(
            "a project name must be provided")
    # verify transaction is signed by authorized key
    _verify_contributor(signer, payload.project_name)

    # find the current sprint number
    current_sprint = _get_project_node(state, payload.project_name).current_sprint
    # get past task names list from previous sprint node
    task_names = _get_current_sprint_node(state, payload.project_name).task_names
    # new list of unfinished tasks to be transferred
    new_task_names = []
    for task_name in task_names:
        # get task container
        task_address = addressing.make_task_address(payload.project_name,current_sprint,task_name)
        task_container = _get_container(state, task_address)
        #find task with correct name
        for task in task_container.entries:
            if task.task_name == task_name:
                # if task is not complete, copy to new sprint
                if task.progress != task.DONE:
                    new_task_names.extend([task_name])
                    new_task_address = addressing.make_task_address(payload.project_name, current_sprint + 1,task_name)
                    new_task_container = _get_container(state, new_task_address)
                    # if the container does not exist, create it
                    if not new_task_container:
                        new_task_container = TaskContainer(entries=[])
                    # add the task to the new sprint and set state
                    new_task_container.entries.extend([task])
                    _set_container(state,new_task_address,new_task_container)


    # make address of new sprint metanode
    new_sprint_node_address = addressing.make_sprint_node_address(payload.project_name,current_sprint + 1)
    sprint_container = _get_container(state, new_sprint_node_address)
    # if no container exists, create one
    if not sprint_container:
        sprint_container = SprintNodeContainer(entries=[])
    # create the new sprint node
    sprint_node = SprintNode(
        project_name = payload.project_name,
        task_names = new_task_names)
    # add sprint to container and set state
    sprint_container.entries.extend([sprint_node])
    _set_container(state,new_sprint_node_address,sprint_container)

    # make address of project metanode
    project_node_address = addressing.make_project_node_address(payload.project_name)

    # get the container
    project_container = _get_container(state, project_node_address)
    # find project with correct name
    for project_node in project_container.entries:
        if project_node.project_name == payload.project_name:
            # increment the sprint and set the state
            project_node.current_sprint += 1
            _set_container(state,project_node_address,project_container)

# add a public key to the list of those allowed to edit the project
def _add_user(payload, signer, timestamp, state):
    if not payload.project_name:
        raise InvalidTransaction(
            "a project name must be provided")

    if not payload.public_key:
        raise InvalidTransaction(
            "a pk must be provided")

    _verify_owner(signer, payload.project_name)

    address = addressing.make_project_node_address(payload.project_name)
    container = _get_container(state, address)
    
    project_node = None
    
    for entry in container.entries:
        if entry.project_name == payload.project_name:
            project_node = entry 

    # verify user is legit
    if any(existing.public_key == payload.public_key 
        for existing in container.entries.public_keys):
            raise InvalidTransaction(
                "This user's public key is already registered")
            
    project_node.public_keys.extend([payload.public_key])

    _set_container(state, address, container)


# remove a public key from the list of those allowed to edit the project
def _remove_user(payload, signer, timestamp, state):
    if not payload.project_name:
        raise InvalidTransaction(
            "a project name must be provided")

    if not payload.public_key:
        raise InvalidTransaction(
            "a pk must be provided")

    _verify_owner(signer, payload.project_name)

    address = addressing.make_project_node_address(payload.project_name)
    container = _get_container(state, address)
    
    project_node = None 

    for entry in container.entries:
        if entry.task_name == payload.project_name:
            project_node = entry

    if any(existing.public_key != payload.public_key
        for existing in container.entries.public_keys):
            raise InvalidTransaction(
                "The user's public key does not exist to be removed.")

    project_node.public_keys.remove(payload.public_key)

    _set_container(state, address, container)

def _unpack_transaction(transaction, state):
    '''Return the transaction signing key, the SCPayload timestamp, the
    appropriate SCPayload action attribute, and the appropriate
    handler function (with the latter two determined by the constant
    TYPE_TO_ACTION_HANDLER table.
    '''

    # identify who signed the transaction 
    signer = transaction.header.signer_public_key

    # create an empty Payload object defined in protos/payload.proto
    payload_header = Payload()
    
    # convert from the binary format
    payload_header.ParseFromString(transaction.payload)

    # define the desired action indicated by the payload
    action = payload_header.action

    # define the desired timestamp indicated by the payload
    timestamp = payload_header.timestamp

    try:
        # using a dictionary, dynamically choose the function we'd like
        # 'create_agent', _create_agent
        attribute, handler = TYPE_TO_ACTION_HANDLER[action]
    except KeyError:
        raise Exception('Specified action is invalid')

    # view docs on getattr(x,x)
    # view protos/payload.proto this makes a CreateAgentAction object
    payload = getattr(payload_header, attribute)

    # go back to apply
    return signer, timestamp, payload, handler


def _get_container(state, address):
    tag = address[6:8] # tag bits that designate the type of node

    containers = {
        addressing.PROJECT_METANODE : ProjectNodeContainer,
        addressing.SPRINT_METANODE : SprintNodeContainer,
        addressing.TODO_TASK : TaskContainer,
    }
    container = containers[tag]() #initialize the correct type of container based on the tag
    entries = state.get_state([address]) # get the state using the address

    if entries:
        data = entries[0].data          # extract the data from the state
        container.ParseFromString(data) # decode data and store in container

    return container    


def _set_container(state, address, container):
    try:
        addresses = state.set_state({
        address: container.SerializeToString()
        })
        if not addresses:
            raise InternalError(
                'State error, failed to set state entities')
    except:
        raise InternalError(
            'State error, likely using wrong in/output fields in tx header.')


def _get_project_node(state, project_name):
    # make address of project metanode
    project_node_address = addressing.make_project_node_address(project_name)

    # get the current projects
    project_container = _get_container(state, project_node_address)

    for project_node in project_container.entries: #find project with correct name
        if project_node.project_name == project_name:
            return project_node 

    return None 


def _get_sprint_node(state, project_name,sprint):
    # make address of project metanode
    sprint_node_address = addressing.make_sprint_node_address(project_name,sprint)

    # get the current projects
    sprint_container = _get_container(state, sprint_node_address)


    for sprint_node_temp in sprint_container.entries:  # find project with correct name
        if sprint_node_temp.project_name == project_name:
            return sprint_node_temp

    return None


def _get_current_sprint_node(state, project_name):
    project_node = _get_project_node(state,project_name)
    if project_node:
        sprint_node = _get_sprint_node(state,project_name, project_node.current_sprint)
        return sprint_node

    return None


def _verify_contributor(state,signer, project_name):
    # check to see that the signer is in the project node's list of authorized signers
    auth_keys = _get_project_node(state,project_name).public_keys
    if not any(signer == key for key in auth_keys):
        raise InvalidTransaction(
            'Signer not authorized as a contributor')

def _verify_owner(signer,project_name):
    # check to see that the signer is the creator of the project
    # i.e. they are the first in the list of authorized signers
    auth_keys = _get_project_node(project_name).public_keys
    if not signer == auth_keys[1]:
        raise InvalidTransaction(
            'Signer not authorized as a contributor')



TYPE_TO_ACTION_HANDLER = { 
    Payload.CREATE_PROJECT: ('create_project', _create_project),
    Payload.CREATE_TASK: ('create_task', _create_task),
    Payload.PROGRESS_TASK: ('progress_task', _progress_task),
    Payload.EDIT_TASK: ('edit_task', _edit_task),
    Payload.INCREMENT_SPRINT: ('increment_sprint', _create_project),
    Payload.ADD_USER: ('add_user', _add_user),
    Payload.REMOVE_USER: ('remove_user', _remove_user),
} 
