# A module for individual blocks.

import time
import json

class Block:
    #Constructor for a new block. Takes the following parameters:
    # block_data: the transaction data to be stored in the block.
    # proof_of_work: the hash of [prev_block_hash + block_data + nonce] generated via Proof of Work.
    # nonce: the same nonce as the one used in the PoW algorithm.
    #
    # A timestamp is autogenerated, and a merkle tree hash is also computed upon Block construction.

    def __init__(self, block_data: str, proof_of_work: str, nonce: int):
        self.timestamp = int(time.time()) 
        self.block_data = block_data 
        self.proof_of_work = proof_of_work 
        self.nonce = nonce

    def serialize(self):
        
        output = {"timestamp": self.timestamp, "block_data": json.loads(self.block_data), \
        "proof_of_work": self.proof_of_work, "nonce": self.nonce}
        return json.dumps(output)        
    
# A basic genesis block which all chains start from.
def Genesis():
    return Block("{}","NONE", 0)


