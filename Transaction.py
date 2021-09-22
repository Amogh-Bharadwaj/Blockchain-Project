#A module for handling transaction information.

from hashlib import sha256
import uuid
import time 
import json

class Transaction:
    #Constructor for a transaction. A transaction UUID is generated to track it.
    def __init__(self, sender_node: str, receiver_node: str, amount: int):
        if amount <= 0:
            raise ValueError("Transaction amount needs to be a positive integer.")
        self.sender_node = sender_node
        self.receiver_node = receiver_node
        self.amount = amount

        self.current_weight = 0
        self.timestamp = int(time.time())
        self.uuid = uuid.uuid4().hex

    def __repr__(self):
        return self.sender_node + " pays " + str(self.amount) + " to " + self.receiver_node + " at " + str(self.timestamp) + "."         

    #Prepares the transaction for storage into a block. Hashes sender and receiver nodes, 
    #and outputs a string representing the transaction.
    def serialize(self) -> str:
        self.sender_node = sha256(self.sender_node.encode('utf-8')).hexdigest()
        self.receiver_node = sha256(self.receiver_node.encode('utf-8')).hexdigest()
        output = {"uuid": self.uuid, "sender": self.sender_node, "receiver": self.receiver_node, \
        "amount": self.amount, "timestamp": self.timestamp}
        return json.dumps(output)

