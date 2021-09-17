
# A module for individual blocks.

from MerkleRoot import MerkleHash
from datetime import datetime

class Block:
    
    #Constructor for this class
    def __init__(self,timestamp,prev_hash,block_hash,data,proof):
        self.timestamp = timestamp #Data type: datetime.datetime class. Output is of the form 2021-09-09 18:23:34.624497

        self.previousHash = prev_hash #Hash of the previous block.
        self.blockHash = block_hash #Hash of this block.
        self.proof=proof
        self.transactions = data #Transactions of the block. Data type: Python List.

    

# Method to initialise a new block
def GetNewBlock(prev_block,data, new_proof):
    stamp = datetime.now()
    prevHash = prev_block.blockHash #Getting hash of the previous block
    to_hash = data
    blockHash= MerkleHash(to_hash).Hashed() #Getting the hash (merkle root) of this block based on the transactions in it.

    return Block(stamp,prevHash,blockHash,data,new_proof)
    

# A basic genesis block which all chains start from.
def Genesis():
    return Block("GENESIS_TIME","NONE","GENESIS_HASH","NONE",hex(10231023)[2:])

