from hashlib import sha256
from random import randint

# In bitcoin, block information is stored as a hash. To achieve this, the transactions of the block
# are run through an algorithm to get a merkle root. In this process, each transactions is hashed 
# and the hashed transactions make up the leaves of the merkle tree.
# The leaves are then paired up and hashed to form the next nodes. This happens recursively.
# In the end we will end up with one node (the parent of the binary merkle tree) which is known as the merkle root.
# The merkle root represents the hashed block.

class MerkleTree:
    def __init__(self, transactions: list):
        hashed_transactions = []

         #Hashing the transactions  to form the leaves.
        for t in transactions:
            hashed_transactions.append(self.nodeHash(t.encode()))
        
        #If number of leaves is odd, the last leaf is duplicated.
        if len(hashed_transactions)%2==1:
            hashed_transactions.append(hashed_transactions[-1])

        self.leaves=hashed_transactions

    #SHA256 hash function. Output is a bytes object.
    def nodeHash(self,node):
        return sha256(node).digest()

    #Recursive hashing to get merkle root.
    def BuildMerkleTree(self,state):
        state_size=len(state)
        
        #Reject empty states.
        if state_size==0:
            return "stateError: Empty leaf state."
        
        # All leaves converged to one parent which is the merkle root.
        if state_size==1:
            #print("Merkle root computed.")
            return state[0]
            
        node_state=[]

        for i in range(0,state_size-1,2):
            node_state.append(self.nodeHash(state[i]+state[i+1]))
        
        return self.BuildMerkleTree(node_state)
    
    def MerkleHashRoot(self):
        return self.BuildMerkleTree(self.leaves)












