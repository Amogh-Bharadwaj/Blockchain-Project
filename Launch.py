# BITS F452 - Blockchain Technology
# Amogh Bharadwaj,

from Node import Node
from Blockchain import Blockchain
from random import choice,randint

#Maximum number of transactions per block.
TRANSACTION_THRESHOLD=7

# Getting sender and amount from the transaction
def parse_transaction(transaction):
    trans_list = list(transaction.split())  # "M sends 4 coins to J" -> ["M","sends","4","coins","to","J"]

    sender = trans_list[0]
    amount = -1*int(trans_list[2])

    return sender,amount

# Nodes for demonstration purpose.
Dexter = Node(10) #Dexter has 10 coins in his bank account.
Kevin = Node(50)
Anish = Node(50)
Amogh = Node(6)


# Some data structures just for convenience.
customers = ["Kevin","Anish","Amogh"]
customer_map = {"Kevin":Kevin,"Anish":Anish,"Amogh":Amogh}

#Pool of unverified transactions.
unverified_pool = []

#Populating pool of transactions with sample transactions for demonstration purpose.
for i in range(7):
    new_transaction = choice(customers)+" sends "+str(randint(1,60))+" coins to Dexter"
    unverified_pool.append(new_transaction)

# Pool of confirmed transactions.
verified_pool = []

#Initialising blockchain
blockChain = Blockchain()


print("Welcome, Dexter. Please validate the following transactions(sorted by timestamp): \n")
print("-"*170)
print("\n")

#Iterating through unverified pool, 7 at a time.
for i in range(0,len(unverified_pool)-TRANSACTION_THRESHOLD+int(len(unverified_pool)==7),TRANSACTION_THRESHOLD):
    print("BLOCK ",(i//7)+1,"\n")
    current_pool=[]
    
    for j in range(i+7):
        currTrans = unverified_pool[j]
        print(currTrans,"\n")
        
        sendr,amnt = parse_transaction(unverified_pool[j])
        Sender = customer_map[sendr]
        print(sendr+"'s balance before this transaction: ", Sender.wallet,"\n")

        response = input("Confirm this transaction? y/n \n")
        while "y" not in response and "n" not in response:
            print("Invalid response. Please yes or no.\n")
            response = input("Confirm this transaction? y/n \n")
        
        if "n" in response:
            #Rejected transactions are discarded.
            print("Rejected this transaction.\n ")
        else:
            print("Adding transaction to verified pool.\n")
            
            #Transaction is confirmed hence we add to pool.
            verified_pool.append(currTrans)
            current_pool.append(currTrans)

            #Executing the transactions.
            Sender.updateWallet(amnt)
            Dexter.updateWallet(-1*amnt)
        
        print("-"*70)
        print("\n")

    
    #Mining using PoW
    blockChain.AddBlock(current_pool)
    
    print("Verified pool: ",verified_pool,"\n")

    print("-"*170)
    print("\n")

#Checking if chain is valid.
print("All transactions processed. Checking chain validity.... \n")
blockChain.ChainValidity(blockChain.blockchain.copy())

print("Thank you.")


        
        










    



