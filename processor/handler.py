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
from protobuf.item_pb2 import Item, AgentContainer
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

def _create_agent(payload, signer, timestamp, state):
    # agents have names, get it from the payload and check its existence
    name = payload.name
    # the public key is the signer, make a variable public_key and assign to it
    public_key = signer
    # verify a name was provided
    if not name:
        raise InvalidTransaction(
            'Must provide agent name.'
        )

    # verify a public_key was provided, just check its existence, don't use _verify_agent
    if not public_key:
        raise InvalidTransaction(
            'Public key is required.')

    # an address in the merkel tree is required. refer to addressing.py, the identifier
    # is the public_key created above
    address = addressing.make_agent_address(public_key)
    # grab a container of any potential agents in state given the address provided above
    container = _get_container(state,address)
    # view docs on any(x)
    # check to see if an agent public_key that matches the public_key above exists in 
    # in the container entries
    if any(agent.public_key ==  public_key for agent in container.entries):  # fill me in
        raise InvalidTransaction(
                'Agent already exists.')

    # create a new agent object with a public key and name
    agent = Agent(public_key = public_key, name = name)
    # extend the current container to include the agent created above
    container.entries.extend([agent])
    # do this crazy thing
    container.entries.sort(key=lambda ag: ag.public_key)

    # call set container to put the agent container into state at the address 
    _set_container(state, address, container)

# Utility functions

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


def _get_item(state, address):
    
    entries = state.get_state([address])    # API call, entries 

    if entries:
        data = entries[0].data          # get the first address in a list of them
        container.ParseFromString(data) # it looks like some encoded data

    return container    


def _set_item(state, address, container):
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


def _verify_agent(state, public_key):
    ''' Verify that public_key has been registered as an agent '''
    # given the public_key, generate address 
        # the public key is the identifier in addressing.py

    # get the container which is very likely just one agent

    # iterate through the container to see if any of the agents
    # in the container have a public_key that matches the one
    # passed in


TYPE_TO_ACTION_HANDLER = { 
    Payload.CREATE_AGENT: ('create_agent', _create_agent),
} 