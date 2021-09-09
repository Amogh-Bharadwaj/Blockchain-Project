
# A module for individual blocks.

from MerkleRoot import MerkleHash
from datetime import datetime

class Block:
    
    #Constructor for this class
    def __init__(self,timestamp,prev_hash,block_hash,data,validator,digital_signature):
        self.timestamp = timestamp #Data type: datetime.datetime class. Output is of the form 2021-09-09 18:23:34.624497

        self.previousHash = prev_hash #Hash of the previous block.
        self.blockHash = block_hash #Hash of this block.

        self.transaction = data #Transactions of the block. Data type: Python List.

        self.validator = validator #Validator decided via  a consensus mechanism
        self.signature = digital_signature #Digital signature for this block,
    

# Method to initialise a new block
def GetNewBlock(prev_block,data):
    stamp = datetime.now()

    blockHash= MerkleHash(data).Hashed() #Getting the hash (merkle root) of this block based on the transactions in it.
    prevHash = prev_block.previousHash #Getting hash of the previous block

    return Block(stamp,prevHash,blockHash,data,"NONE","NONE")
    

# A basic genesis block which all chains start from.
def Genesis():
    return Block("GENESIS_TIME","NONE","GENESIS_HASH","NONE","NONE","NONE")

