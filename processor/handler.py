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
    if not payload.name:
        raise InvalidTransaction(
            'Task must have a name.'
    )

    if not payload.description:
         raise InvalidTransaction(
            'Task must have a description.'
    )
 
    project_name = payload.project_name 
    project_node = get_project_node(project_name)
    container = get_container(project_node) 

    if all(legit_users.public_key != public_key for legit_users in container.entries):
        raise InvalidTransaction(
            "User must be authorized to make changes to this project")

    sprint = _get_current_sprint_node(project_name)
    if any(task == payload.name for task in sprint.task_names)
        raise InvalidTransaction(
            "This task name is already in use.")
        
    # we made it here, it's all good. create the object
    task = Task (
        project_name = project_name,
        name = payload.name 
        description = payload.description
        timestamp = timestamp
    )
 
    # can we pass `NOT_STARTED` here or must this be `0`?
    address = make_task_address(project_name, project_node.current_sprint, payload.name, task.NOT_STARTED)
    container = _get_container(state, address)

    container.entries.extend([task])       

    set_container(state, address, container)


def _create_project(payload, signer, timestamp, state):
    project_name = payload.project_name
    # make address of project metanode
    project_node_address = addressing.make_project_node_address(project_name)

    # get the current projects
    project_container = _get_container(state,project_node_address)
    if not project_container: #if no container exists, create one
        project_container = ProjectNodeContainer(entries=[])

    #check to see if a project already exists under the same name
    if any(project_node.project_name == project_name
           for project_node in container.entries):
        raise InvalidTransaction(
            'Project with this name already exists.')

    # create the metanode protobuf object
    project_node = ProjectNode(
        project_name = project_name,
        public_keys = [signer], #add creator of project to authorized public key list
        current_sprint = 0)
    #add project to container
    project_container.entries.append(project_node)
    #set state with new project included
    _set_container(state,project_node_address,project_container)

    # initialize first sprint node
    sprint_container = _get_container(state, sprint_node_address)
    if not sprint_container:  # if no container exists, create one
        sprint_container = SprintNodeContainer(entries=[])


def _progress_task(payload, signer, timestamp, state):
    project_name = payload.project_name
    # verify transaction is signed by authorized key
    _verify_contributor(signer, project_name)

def _edit_task(payload, signer, timestamp, state):
    project_name = payload.project_name
    # verify transaction is signed by authorized key
    _verify_contributor(signer, project_name)

def _increment_sprint(payload, signer, timestamp, state):
    project_name = payload.project_name
    # verify transaction is signed by authorized key
    _verify_contributor(signer, project_name)

    current_sprint = _get_project_node(state, project_name).current_sprint
    # make address of sprint metanode
    sprint_node_address = addressing.make_sprint_node_address(project_name,current_sprint+1)

    # get the current sprint nodes at the address
    sprint_container = _get_container(state, sprint_node_address)
    if not sprint_container:  # if no container exists, create one
        sprint_container = SprintNodeContainer(entries=[])
    #get past task names list from previous metanode
    task_names = _get_current_sprint_node(state,project_name).task_names
    # create the metanode protobuf object
    sprint_node = SprintNode(
        project_name = project_name,
        task_names = task_names)  # add tasks added in past
    # add sprint to container
    sprint_container.entries.append(sprint_node)
    # set state with new project included
    _set_container(state, sprint_node_address, sprint_container)

    for name in task_names: # go through every task in previous sprint
        #get container where task would be if it is done
        task_container = _get_container(state,addressing.make_task_address(project_name,current_sprint,name,3))
        if not task_container: #if container doesn't exist, copy over all copies of task
            copy_task_new_sprint(state, project_name, current_sprint, name)
        elif not any(name == task.name for task in task_container.entries): #if container exists, but
            copy_task_new_sprint(state, project_name, current_sprint, name)



# add a public key to the list of those allowed to edit the project
def _add_user(payload, signer, timestamp, state):
    _verify_owner(signer,payload.project_name)
    project_node = _get_project_node(state,payload.project_name)
    project_node.public_keys.extend([payload.public_key]) 


# remove a public key from the list of those allowed to edit the project
def _remove_user(payload, signer, timestamp, state):
    _verify_owner(signer, payload.project_name)
    project_node = _get_project_node(state,payload.project_name)
    project_node.public_keys.remove([payload.public_key])


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


def _get_sprint_node(state,project_name,sprint):
    # make address of project metanode
    sprint_node_address = addressing.make_sprint_node_address(project_name,sprint)

    # get the current projects
    sprint_container = _get_container(state, sprint_node_address)


    for sprint_node_temp in sprint_container.entries:  # find project with correct name
        if sprint_node_temp.project_name == project_name:
            return sprint_node_temp

    return None


def _get_current_sprint_node(state,project_name):
    project_node = _get_project_node(state,project_name)
    if project_node:
        sprint_node = _get_sprint_node(state,project_name, project_node.current_sprint)
        return sprint_node

    return None

def _verify_contributor(signer, project_name):
    # check to see that the signer is in the project node's list of authorized signers
    auth_keys = _get_project_node(project_name).public_keys
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

def copy_task_new_sprint(state, project_name,current_sprint,name):
    for progress in range(0, 3):
        copy_container = _get_container(state,
            addressing.make_task_address(project_name, current_sprint, name, progress))
        if copy_container:
            for task in copy_container.entries:  # if copy container exists, copy task with desired name to new location
                if task.name == name:
                    _set_container(state,
                        addressing.make_task_address(project_name, current_sprint + 1, name, task.stage),
                        TaskContainer(entries=[task]))

TYPE_TO_ACTION_HANDLER = { 
    Payload.CREATE_PROJECT: ('create_project', _create_project),
    Payload.CREATE_TASK: ('create_task', _create_task),
    Payload.PROGRESS_TASK: ('progress_task', _progress_task),
    Payload.EDIT_TASK: ('edit_task', _edit_task),
    Payload.INCREMENT_SPRINT: ('increment_sprint', _create_project),
    Payload.ADD_USER: ('add_user', _add_user),
    Payload.REMOVE_USER: ('remove_user', _remove_user),
} 
