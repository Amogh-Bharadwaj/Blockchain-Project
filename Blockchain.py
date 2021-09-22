#A module for blockchains which are lists consisting of the Block class.

from Block import Block, Genesis
from Transaction import Transaction
from hashlib import sha256
import sys
import uuid
import json

class Blockchain:
    
    #Constructing a new blockchain for use.
    #Following parameters are specified:
    #   weight_for_validate: minimum voting weight required to validate a transaction.
    #   max_block_capacity: maximum number of transactions that can fit into a block.
    #   difficulty: number of leading zeros in the winning SHA256 hash [similar to how Bitcoin operates]
    #
    #A unique identifier is generated for each block upon creation.
    def __init__(self, weight_for_validate: int, max_block_capacity: int, difficulty: int):
        if difficulty <= 0 or difficulty > 64:
            raise ValueError("Difficulty needs to be between 1 and 64.")
        self.blockchain = [Genesis()]
        self.weight_for_validate = weight_for_validate
        self.max_block_capacity = max_block_capacity
        self.difficulty = difficulty
        self.verified_transaction_pool = {}
        self.unverified_transaction_pool = {}

        self.uuid = uuid.uuid4().hex

    def ProofOfWork(self, prev_hash: str, block_data: str):
        nonce = 1
        to_compare = '0' * self.difficulty
        merged_data = str(prev_hash) + block_data
        while True:
            test = merged_data + str(nonce)
            test_hash = sha256(test.encode('utf-8')).hexdigest()[:self.difficulty]
            if test_hash == to_compare:
                break
            else:
                nonce += 1
        return [sha256(test.encode('utf-8')).hexdigest(), nonce]


    def AddTransaction(self, transaction: Transaction):
        #Checking for key conflicts, so other transactions are not overwritten.
        if self.unverified_transaction_pool.get(transaction.uuid, None) != None:
            raise KeyError("Transaction already added or UUID collision detected.")
        self.unverified_transaction_pool[transaction.uuid] = transaction
    

    def UpdateTransactionVote(self, transaction_uuid: str, weight: int):
        if weight <= 0:
            raise ValueError("Weight needs to be a positive integer.")

        #Locate transaction using its uuid.
        if transaction_uuid in self.unverified_transaction_pool.keys():
            transaction = self.unverified_transaction_pool.pop(transaction_uuid)

            #Update its weight based on the voter.
            transaction.current_weight = transaction.current_weight + weight

            if transaction.current_weight >= self.weight_for_validate:
                print("[NOTICE] Transaction " + transaction_uuid + " just reached consensus. Moving to verified pool.\n")

                self.verified_transaction_pool[transaction_uuid] = transaction
            else:
                self.unverified_transaction_pool[transaction_uuid] = transaction 

        elif transaction_uuid in self.verified_transaction_pool.keys():
            
            transaction = self.verified_transaction_pool.pop(transaction_uuid) 
            transaction.current_weight = transaction.current_weight + weight

            self.verified_transaction_pool[transaction_uuid] = transaction
        else:
            raise KeyError("Transaction not currently tracked by blockchain.")    


    #Method for adding a new block.
    def AddBlock(self, block_data: str):
        print("Mining block at height " + str(len(self.blockchain)) + "...")
        new_hash, nonce = self.ProofOfWork(self.blockchain[-1].proof_of_work, block_data)
        print("Block added. Proof(hex): ", new_hash)
        sys.stdout.flush()

        self.blockchain.append(Block(block_data, new_hash, nonce))
    

    def ChainValidity(self):
        #All chains start with the same genesis block.
        chain = self.blockchain
        if chain[0].block_data != "{}":
            print("Error: First block is not the genesis block.\n")
            return False
        
        for i in range(1,len(chain)): 
            proof_test = sha256((str(chain[i - 1].proof_of_work) + chain[i].block_data + str(chain[i].nonce)).encode('utf-8')).hexdigest()

            #Checking the proof of work puzzle as well as the proof itself.
            if proof_test[:self.difficulty]!='0'*self.difficulty and proof_test==chain[i].proof_of_work:
                print("\n Blockchain is invalid! Corrupt block was created at timestamp ",chain[i].timestamp,".")
                return False

        print("No discrepancies found. The blockchain has been reverified successfully.\n")
        return True


    #Keep replacing the current chain with a longer chain, if there is one.
    def UpdateChain(self,newChain):
        if len(newChain) <= len(self.blockchain):
            return "updateError: New chain is not longer than current chain."
           
        elif not self.ChainValidity():
            return "validityError: New chain is invalid."
           
        else:
            self.blockchain = newChain
    

    #Carrying out block creation upon finishing transaction validations
    def finalize_verified(self):
         verified_list = list(self.verified_transaction_pool.values())
         cache = []

         for transaction in verified_list:
             cache.append(transaction.serialize())
             self.verified_transaction_pool.pop(transaction.uuid)
              
             #Once transaction threshold is reached, create a block. 
             if len(cache) == self.max_block_capacity:
                 self.AddBlock(json.dumps(cache))
                 cache.clear()
         #Create a block for the remaining transactions.
         if len(cache) > 0:
                 self.AddBlock(json.dumps(cache))
                 cache.clear() 







