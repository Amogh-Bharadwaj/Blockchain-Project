
#A module for blockchains which are lists consisting of the Block class.

from Block import Block,GetNewBlock,Genesis
from MerkleRoot import MerkleHash

class Blockchain:
    
    #Default constructor for this class
    def __init__(self):
        self.blockchain = [Genesis()]
        

    #[INCOMPLETE] Method for adding a new block. Will need to be modified to also include the validator and his/her signature.
    def AddBlock(self,data):
        self.blockchain.append(GetNewBlock(self.blockchain[-1],data))
    

    # Method to check if the blockchain hasn't been tampered.
    def ChainValidity(self,chain):
        #All chains start with the same genesis block.
        if(chain[0]!=Genesis()):
            return False

        #Checking if hash of the previous block is equal to the previous hash of the current block.
        for i in range(1,len(chain)):
            if (chain[i-1].blockHash != chain[i].previousHash) or (chain[i].blockHash != MerkleHash(chain[i].data)): #Checking hash of each block as well.
                return False 
            return True


    #Keep replacing the current chain with a longer chain, if there is one.
    def UpdateChain(self,newChain):
        if len(newChain)<=len(self.blockchain):
            return "updateError: New chain is not longer than current chain."
           
        elif not self.ChainValidity(newChain):
            return "validityError: New chain is invalid."
           
        else:
            self.blockchain=newChain







