''' to use this test one must already know the private key.  on the cli
input usr0_prv_key, usr1_prv_key, or usr2_prv_key.  This distinction would
exist depending on who holds keys and has access to the form from which a 
transaction is created.  

When testing, create_agent should be run with one of the aforementioned 
users, then we can see if assets can be created and touched repeatedly.

It can also be seen that a bogus private key is the default case when an
invalid input is provided from the cli. We'd like to see that not every 
user can touch an asset.'''


# Utilities
import hashlib
import subprocess
import sys
import secp256k1
import time
import uuid
import requests
import json
import random
from random import randint

# Sawtooth SDK
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import BatchList


from protobuf.payload_pb2 import Payload, CreateAssetAction
from protobuf.payload_pb2 import CreateAgentAction, TouchAssetAction
import addressing


def _get_prv_key():
    return priv_key 


def _get_batcher_public_key():
    signer = _create_signer(_get_prv_key())
    return signer.pubkey.serialize().hex()


def _get_time():
    return int(time.time())

def _create_signer(private_key):
    signer = secp256k1.PrivateKey()
    signer.set_raw_privkey(bytes.fromhex(str(private_key)))
    return signer
    

class Todo():
    def __init__(self):
        self.txns = []

    def create_item(self, args):       # args [create_agent, private_key, name]
        if len(args) < 1:
            print("\nA private key is required to create an item.\n")
            return

        private_key = args[1]
        signer = _create_signer(private_key)

        if 2 < len(args):
            name = args[2]
        else:
            print("\nA name is required to create an item.\n")
            return

        # make the agent_payload, and specific attributes
        agent_action = CreateAgentAction(
                public_key = signer.pubkey.serialize().hex(),
                name = name,
        )

        agent_payload = Payload(
            action = 1,
            timestamp = _get_time(),
            create_agent = agent_action,
        )

        # serialize before sending
        payload_bytes = agent_payload.SerializeToString()

        # Pack it all up and ship it out
        self.create_transaction(signer, payload_bytes)


    def create_transaction(self, signer, payload_bytes):
        #private_key = _get_prv_key()
        #signer2 = _create_signer(private_key)
        #batch_pubkey = signer.pubkey.serialize().hex()
        txn_header_bytes = TransactionHeader(
            family_name='skltn',
            family_version='0.1',
            inputs=[addressing.NAMESPACE],
            outputs=[addressing.NAMESPACE],
            signer_public_key = signer.pubkey.serialize().hex(),
            # In this example, we're signing the batch with the same private key,
            # but the batch can be signed by another party, in which case, the
            # public key will need to be associated with that key.          # make a global batch_public_key
            # batcher_public_key = signer.pubkey.serialize().hex(), # must have been generated from the private key being used to sign the Batch, or validation will fail
            batcher_public_key = _get_batcher_public_key(),
            # In this example, there are no dependencies.  This list should include
            # an previous transaction header signatures that must be applied for
            # this transaction to successfully commit.
            # For example,
            # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
            dependencies=[],
            payload_sha512=sha512(payload_bytes).hexdigest()
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


    def create_batch(self, args):   # args [create_batch, private_key]
        private_key = args[1]
        signer = _create_signer(private_key)

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


def send_it(batch_list_bytes):
    # ship it out and scrape
    url = "http://localhost:8008/batches"
    headers = { 'Content-Type' : 'application/octet-stream' }
    payload = batch_list_bytes
    resp = requests.post(url, data=payload, headers=headers)
    json_url = json.loads(resp.text)
    # print("Batch status link: \n\n" + json_url["link"] + "\n") # DEBUG
    time.sleep(2)
    resp = requests.get(json_url["link"])
    json_batch_status = json.loads(resp.text)
    print(json_batch_status["data"][0]["status"])

#subprocess.run(["docker-compose", "-f" "../sawtooth-default.yaml", "up", "-d"])


todo = Todo()

passcode = "hello"
priv_key = hashlib.sha224(passcode.encode('utf-8')).hexdigest()

name = "John Doe"

//create item
args = ["create_item", priv_key, name, description]

//edit description
args = ["edit_description", priv_key,name, description]

//set status
args = ["set_status", priv_key,name, is_done]

//run desired function
getattr(todo, args[0])(args)

args = ["create_batch", priv_key]        
batch_list_bytes = getattr(skltn, args[0])(args)

send_it(batch_list_bytes)

#subprocess.run(["docker-compose", "-f" "../sawtooth-default.yaml", "down"])
