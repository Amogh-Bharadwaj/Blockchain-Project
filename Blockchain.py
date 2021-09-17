
#A module for blockchains which are lists consisting of the Block class.

from Block import Block,GetNewBlock,Genesis
from MerkleRoot import MerkleHash
from hashlib import sha256

class Blockchain:
    
    #Default constructor for this class
    def __init__(self):
        self.blockchain = [Genesis()]
    

    def ProofOfWork(self,prev_proof):
        newProof = 1
        while True:
            test = hex(newProof + int(prev_proof,16))[2:]
            test_hash = sha256(bytes.fromhex(test)).hexdigest()[0:5]
            if test_hash=="00000":

                break
            else:
                newProof+=1
        return test

    #Method for adding a new block.
    def AddBlock(self,data):
        lastProof = self.blockchain[-1].proof
        print("Mining block.. \n")
        newproof = self.ProofOfWork(lastProof)
        print("Block added. Proof(hex): ", newproof,"\n")

        self.blockchain.append(GetNewBlock(self.blockchain[-1],data,newproof))
    

    # Method to check if the blockchain hasn't been tampered.
    def ChainValidity(self,chain):
        #All chains start with the same genesis block.
        if(chain[0].timestamp!="GENESIS_TIME"):
            return False

        #Checking if hash of the previous block is equal to the previous hash of the current block.
        for i in range(1,len(chain)):
            if (chain[i-1].blockHash != chain[i].previousHash) or (chain[i].blockHash != MerkleHash(chain[i].transactions).Hashed()) or (sha256(bytes.fromhex(chain[i].proof)).hexdigest()[0:5]!="00000"): #Checking hash and proof of each block as well.
                print("Invalid block!\n")
                return False 
        print("Chain is valid.\n")
        return True


    #Keep replacing the current chain with a longer chain, if there is one.
    def UpdateChain(self,newChain):
        if len(newChain)<=len(self.blockchain):
            return "updateError: New chain is not longer than current chain."
           
        elif not self.ChainValidity(newChain):
            return "validityError: New chain is invalid."
           
        else:
            self.blockchain=newChain







