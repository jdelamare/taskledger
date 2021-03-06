# MIT License
#
# Copyright (c) 2018 Nicholas Springer & Jeffrey De La Mare
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Utilities

import hashlib
import subprocess
import sys
import secp256k1
import base64
import time
import uuid
import requests
import json
import random
from random import randint
import sys
import urllib.request, json


# Sawtooth SDK
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import BatchList

from protobuf.payload_pb2 import *
from protobuf.project_node_pb2 import *
from protobuf.sprint_node_pb2 import *
from protobuf.task_pb2 import *
import addressing

def _get_batcher_public_key(signer):
    return signer.pubkey.serialize().hex()

def _get_time():
    return int(time.time())

def _create_signer(private_key):
    signer = secp256k1.PrivateKey(privkey=bytes.fromhex(str(private_key+'00000000')))
    return signer
    

class Todo():
    def __init__(self):
        self.txns = []

    def create_project(self, args):
        ''' Creates a transaction that includes a create_project payload

            args: [password/signer, project_name]
        '''
        if not len(args) == 2: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()
        #create signer using given private key
        #private_key = args[0]
        #signer = _create_signer(private_key)
        signer = args[0]

        # bundle the action information
        action = CreateProjectAction(
                project_name = args[1],
        )
        # bundle the payload
        payload = Payload(
            action = 0,
            timestamp = _get_time(),
            create_project = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def create_task(self, args):
        ''' Creates a transaction that includes a create_task payload

            args: [password/signer, project_name, task_name, description]
        '''
        if not len(args) == 4: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        #private_key = args[0]
        #signer = _create_signer(private_key)
        signer = args[0]
        # bundle the action information
        action = CreateTaskAction(
                project_name = args[1],
                task_name = args[2],
                description = args[3]
        )
        # bundle the payload
        payload = Payload(
            action = 1,
            timestamp = _get_time(),
            create_task = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def progress_task(self, args):
        ''' Creates a transaction that includes a progress_task payload

            args: [password/signer, project_name, task_name]
        '''
        if not len(args) == 3: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        signer = args[0]

        # bundle the action information
        action = ProgressTaskAction(
                project_name=args[1],
                task_name=args[2],
        )
        # bundle the payload
        payload = Payload(
            action = 2,
            timestamp = _get_time(),
            progress_task = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def edit_task(self, args):
        ''' Creates a transaction that includes a create_project payload

            args: [password/signer, project_name, task_name, description]
        '''
        if not len(args) == 4: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        signer = args[0]
        # bundle the action information
        action = EditTaskAction(
                project_name = args[1],
                task_name = args[2],
                description = args[3]
        )
        # bundle the payload
        payload = Payload(
            action = 3,
            timestamp = _get_time(),
            edit_task = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def increment_sprint(self, args):
        ''' Creates a transaction that includes an increment_sprint payload

            args: [password/signer, project_name]
        '''
        if not len(args) == 2: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        signer = args[0]

        # bundle the action information
        action = IncrementSprintAction(
                project_name = args[1],
        )
        # bundle the payload
        payload = Payload(
            action = 4,
            timestamp = _get_time(),
            increment_sprint = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def add_user(self, args):
        ''' Creates a transaction that includes an add_user payload

            args: [password/signer, project_name, public_key]
        '''
        if not len(args) == 3: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        signer = args[0]

        # bundle the action information
        action = AddUserAction(
                project_name = args[1],
                public_key = args[2],
        )
        # bundle the payload
        payload = Payload(
            action = 5,
            timestamp = _get_time(),
            add_user = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def remove_user(self, args):
        ''' Creates a transaction that includes a remove_user payload

            args: [password/signer, project_name, public_key]
        '''
        if not len(args) == 3: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()

        #create signer using given private key
        signer = args[0]

        # bundle the action information
        action = RemoveUserAction(
                project_name = args[1],
                public_key = args[2],
        )
        # bundle the payload
        payload = Payload(
            action = 6,
            timestamp = _get_time(),
            remove_user = action,
        )

        # serialize/encode before sending
        payload_bytes = payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)
        batch_list_bytes = self.create_batch(signer)
        send_it(batch_list_bytes)

    def create_transaction(self, signer, payload_bytes):
        '''Bundles together a transaction that includes the given payload and is signed by given signer'''
        txn_header_bytes = TransactionHeader(
            family_name='todo',
            family_version='0.1',
            inputs=[addressing.NAMESPACE],
            outputs=[addressing.NAMESPACE],
            signer_public_key = signer.pubkey.serialize().hex(),
            # In this example, we're signing the batch with the same private key,
            # but the batch can be signed by another party, in which case, the
            # public key will need to be associated with that key.          # make a global batch_public_key
            batcher_public_key = signer.pubkey.serialize().hex(), # must have been generated from the private key being used to sign the Batch, or validation will fail
            # batcher_public_key = _get_batcher_public_key(signer),
            # In this example, there are no dependencies.  This list should include
            # an previous transaction header signatures that must be applied for
            # this transaction to successfully commit.
            # For example,
            # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
            dependencies=[],
            payload_sha512=hashlib.sha512(payload_bytes).hexdigest()
        ).SerializeToString()

        # Ecdsa signing standard, then remove extra ecdsa bytes using compact.
        txn_signature = signer.ecdsa_sign(txn_header_bytes)
        txn_signature_bytes = signer.ecdsa_serialize_compact(txn_signature)
        signature = txn_signature_bytes.hex()

        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=payload_bytes
        )

        self.txns.append(txn)

    def create_batch(self, signer):
        '''Bundles together a batch that includes self.txns and is signed by given signer'''
        batch_header_bytes = BatchHeader(
            signer_public_key = signer.pubkey.serialize().hex(),
            transaction_ids=[txn.header_signature for txn in self.txns],
        ).SerializeToString()

        batch_signature = signer.ecdsa_sign(batch_header_bytes)
        batch_signature_bytes = signer.ecdsa_serialize_compact(batch_signature)
        signature = batch_signature_bytes.hex()

        batch = Batch(
            header=batch_header_bytes,
            header_signature=signature,
            transactions=self.txns
        )

        batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
        
        return batch_list_bytes

    def print_project(self, args):
        ''' Prints all information about a given project

            args: [password (not validated; can be anything), project_name]
        '''
        if not len(args) == 2: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()
        # queries state
        with urllib.request.urlopen("http://localhost:8008/state") as url:
            state = json.loads(url.read().decode())['data']
        project_name = args[1]
        # gets project node from state
        project_node = getProjectNode(state,project_name)
        print('+++++++++++++++++++++Project:' + project_name + '+++++++++++++++++++++')
        print("<<<<<<<<<<<<Public Keys:>>>>>>>>>>>>")
        # print all authorized public keys
        for public_key in project_node.public_keys:
            print(public_key)
        print("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>")
        current_sprint = project_node.current_sprint
        # print all sprints and tasks in the sprints
        for sprint in range(0,current_sprint+1):
            print('=================Sprint '+ str(sprint) + '=================')
            sprint_node = getSprintNode(state,project_name,sprint)
            for task_name in sprint_node.task_names:
                task = getTask(state,project_name,sprint,task_name)
                print("------------Task------------")
                print("Task_name: " + task.task_name)
                print('Description: ' + task.description)
                print('Progress: ' + str(task.progress))
                print('---------------------------')
            print ("====================================================")
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    def add_password(self, args):
        ''' Takes authorized signer and new password to be added to auth users.
            
            args: [password (is a signer), new_password]
        '''
        if not len(args) == 3: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()
        #creates public key from password
        new_pass = args[2]
        priv_key = hashlib.sha224(new_pass.encode('utf-8')).hexdigest()
        args[2] = _create_signer(priv_key).pubkey.serialize().hex()
        self.add_user(args)

    def remove_password(self, args):
        ''' Takes authorized signer and password to be removed from auth users.
            
            args: [password (is a signer), removed_password]
        '''
        if not len(args) == 3: # make sure correct number of arguments are present for desired transaction
            print("\nIncorrect number of arguments for desired command.\n")
            quit()
        #creates public key from password
        new_pass = args[2]
        priv_key = hashlib.sha224(new_pass.encode('utf-8')).hexdigest()
        args[2] = _create_signer(priv_key).pubkey.serialize().hex()
        self.remove_user(args)


def send_it(batch_list_bytes):
    '''Sends batch to REST API where it'''
    # ship it out and scrape
    url = "http://localhost:8008/batches"
    headers = { 'Content-Type' : 'application/octet-stream' }
    payload = batch_list_bytes
    resp = requests.post(url, data=payload, headers=headers)
    json_url = json.loads(resp.text)
    # print("Batch status link: \n\n" + json_url["link"] + "\n") # DEBUG
    resp = requests.get(json_url["link"])
    json_batch_status = json.loads(resp.text)
    status = json_batch_status["data"][0]["status"]
    print("PENDING")
    while not (status == "COMMITTED" or status == "INVALID"):
        resp = requests.get(json_url["link"])
        json_batch_status = json.loads(resp.text)
        status = json_batch_status["data"][0]["status"]
    print(status)

def getProjectNode(state,project_name):
    ''' Given a project name and sprint name get a sprint node. '''

    # make address of project metanode
    project_node_address = addressing.make_project_node_address(project_name)
    project_node_container = ProjectNodeContainer()
    data = getData(state,project_node_address)
    project_node_container.ParseFromString(data)  # decode data and store in container

    for project_node in project_node_container.entries:  # find project with correct name
        if project_node.project_name == project_name:
            return project_node
    return None

def getSprintNode(state,project_name,sprint):
    ''' Given a project name and sprint name get a sprint node. '''

    # make address of sprint metanode
    sprint_node_address = addressing.make_sprint_node_address(project_name, str(sprint))
    sprint_node_container = SprintNodeContainer()
    data = getData(state,sprint_node_address)
    sprint_node_container.ParseFromString(data)  # decode data and store in container

    for sprint_node in sprint_node_container.entries:  # find project with correct name
        if sprint_node.project_name == project_name:
            return sprint_node
    return None

def getTask(state,project_name,sprint,task_name):
    ''' Given a project name, sprint, and task name get a task node. '''

    # make address of task node
    task_address = addressing.make_task_address(project_name,sprint,task_name)
    task_container = TaskContainer()
    data = getData(state,task_address)
    task_container.ParseFromString(data)  # decode data and store in container

    for task in task_container.entries:  # find task with correct name
        if task.task_name == task_name:
            return task
    return None


def getData(state, address):
    ''' Gets the data from a provided address.

        State has two fields address and data.  We can create the
        address using functions in addressing.py.  The data field
        is encoded with base64 encoding.
    '''

    for location in state:
        if location['address'] == address:
            encoded_data = location['data']
            return base64.b64decode(encoded_data)
    return None



#subprocess.run(["docker-compose", "-f" "../sawtooth-default.yaml", "up", "-d"])

todo = Todo()

args = sys.argv[1:]
passcode = args[1]

priv_key = hashlib.sha224(passcode.encode('utf-8')).hexdigest()
args[1] = _create_signer(priv_key)
# run desired function
getattr(todo, args[0])(args[1:])

#subprocess.run(["docker-compose", "-f" "../sawtooth-default.yaml", "down"])
