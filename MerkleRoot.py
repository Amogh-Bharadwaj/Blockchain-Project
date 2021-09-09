from hashlib import sha256
from random import randint

# In bitcoin, block information is stored as a hash. To achieve this, the transactions of the block
# are run through an algorithm to get a merkle root. In this process, each transactions is hashed 
# and the hashed transactions make up the leaves of the merkle tree.
# The leaves are then paired up and hashed to form the next nodes. This happens recursively.
# In the end we will end up with one node (the parent of the binary merkle tree) which is known as the merkle root.
# The merkle root represents the hashed block.


class MerkleHash:

    def __init__(self,data):
        processedData = []

        #Hashing the transactions to form the leaves.
        for d in data:
            processedData.append(self.NodeHash(d.encode())) 

        #If number of leaves is odd, the last leaf is duplicated.
        if len(processedData)%2==1:
            processedData.append(processedData[-1])

        self.leaves = processedData
        
    #SHA256 hash function. Output is a bytes object.
    def NodeHash(self,node):
        return sha256(node).digest()

    #Recursive hashing to get merkle root.
    def ConstructRoot(self,state):
        state_size=len(state)
        
        #Reject empty states.
        if state_size==0:
            return "stateError: Empty leaf state."
        
        # All leMerkleRootaves converged to one parent which is the merkle root.
        if state_size==1:
            #print("Merkle root computed: ")
            return state[0]
            
        node_state=[]

        for i in range(0,state_size-1,2):
            node_state.append(self.NodeHash(state[i]+state[i+1]))
        
        return self.ConstructRoot(node_state)
    
    def Hashed(self):
        return self.ConstructRoot(self.leaves)














