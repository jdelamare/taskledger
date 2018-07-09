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
from protobuf.item_pb2 import Item
from protobuf.payload_pb2 import Payload

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

# TODO: how many handler functions, these need prototypes
# address h(public key + project name) for the main part

# Utility functions
def _create_task(payload, signer, timestamp, state):
    verification?
    
    needs name, if not name it cannot be made
    
    needs description if not desc than cannot make

    
    task = Task (
        name = payload.name # ?
        description = payload.description
        timestamp = timestamp
    )


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
        current_sprint = -1)
    #add project to container
    project_container.entries.append(project_node)
    #set state with new project included
    _set_container(state,project_node_address,project_container)
    # calls increment sprint to go from sprint -1 to 0 and initalize sprint metanode
    _incremenet_sprint(IncrementSprintAction(project_name = project_name),signer,timestamp,state)

def _edit_task(payload, signer, timestamp, state):

def _incremenet_sprint(payload, signer, timestamp, state):

def _add_user(payload, signer, timestamp, state):

def _remove_user(payload, signer, timestamp, state):

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
    
    entries = state.get_state([address])    # API call, entries 

    if entries:
        data = entries[0].data          # get the first address in a list of them
        container.ParseFromString(data) # it looks like some encoded data
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


# Any potential verification functions

TYPE_TO_ACTION_HANDLER = { 
    Payload.CREATE_PROJECT: ('create_project', _create_project),
    Payload.CREATE_TASK: ('create_task', _create_task),
    Payload.PROGRESS_TASK: ('progress_task', _progress_task),
    Payload.EDIT_TASK: ('edit_task', _edit_task),
    Payload.INCREMENT_SPRINT: ('increment_sprint', _create_project),
    Payload.ADD_USER: ('add_user', _add_user),
    Payload.REMOVE_USER: ('remove_user', _remove_user),
} 
