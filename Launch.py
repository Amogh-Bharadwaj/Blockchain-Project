# BITS F452 - Blockchain Technology
# Amogh Bharadwaj, Kevin Biju Kizhake Kanichery

import sys
import pprint
import requests
from Node import Node
from Transaction import Transaction
from Blockchain import Blockchain
import asyncio

#Initializing a new blockchain for demonstration.
blockchain = Blockchain(7, 7, 5)    

#[NOT ANYMORE] Setting up nodes, ensure that Dexter is the only node with weight for voting purposes.
Dexter = Node(10, 7)

node_map = {"Dexter": Dexter}

print("BITS F452 Blockchain Assignment 1 Demonstration")
print("Project by:")
print("\t1. Anish Kacham [2019A7PS0091H]")
print("\t2. Amogh Bharadwaj [2019A7PS0086H]")
print("\t3. Kevin Biju Kizhake Kanichery [2019A7PS0045H]\n")

print("Phase #1: We begin add one or more nodes representing customers of Dexter's shop.")
print("By definition, these nodes shouldn't be able to verify the transactions. Therefore we give all these nodes a voting weight of 0.\n")

user_input = 'y'
while user_input != 'n':
    node_name = input("Enter name of new node: ")
    if node_name in node_map.keys():
        print("Node with this name already exists!", file = sys.stderr)
    else:
        node_amount = int(input("Number of coins with node: "))

        # All nodes have same weightage for consensus.
        node_map[node_name] = Node(node_amount, 7)
    user_input = input("Add another node? [Any key for yes or n to skip] ")    

print("Current list of nodes:\n")
pprint.pprint(node_map)
print()

print("All nodes in the network download the code for the Proof of Elapsed Time consensus algorithm  from a secure server at the time of joining.")
print("Downloading consensus algorithm....")

algorithm_url = "https://nightingalebucket.s3.ap-south-1.amazonaws.com/PoEt.py"
algorithm_source = requests.get(algorithm_url, allow_redirects=True)
print("Obtained source code..")
open("PoEt.py",'wb').write(algorithm_source.content)
print("Consensus algorithm installed. Moving to Phase 2.\n")

from PoEt import PoEt, NodeWait

print("Phase #2: We now add one or more transactions from the customer to Dexter.")
print("The system automatically checks if the customer can pay the amount mentioned.")
print("Each transaction has a unique UUID assigned to it.\n")

user_input = 'y'
while user_input != 'n':
    node_name = input("Enter node name: ")
    if node_name not in node_map.keys():
        print("Node doesn't exist!", file = sys.stderr)
    else:
        amount = int(input("Number of coins sent to Dexter: "))
        if amount <= 0 or amount > node_map[node_name].amount:
            print("Invalid transaction amount!", file = sys.stderr)
        else:
            node_map[node_name].updateWallet(-amount)
            node_map["Dexter"].updateWallet(amount)
            transaction = Transaction(node_name, "Dexter", amount)
            blockchain.AddTransaction(transaction)
            print("Transaction successfully added with UUID " + transaction.uuid + ". Current state is UNVERIFIED.\n")
    user_input = input("Add another transaction? [Any key for yes or n to skip] ")   

print("Current list of unverified transactions:\n")
pprint.pprint(blockchain.unverified_transaction_pool)    
print()

print("Current list of nodes:\n")
pprint.pprint(node_map)
print()

print("Phase #3: We iterate over all the unverified transactions in the Blockchain.")
print("The Proof of Elapsed Time consensus algorithm will be performed and the winner will get to mine the block.")

#print("Currently, Dexter is the only voting node in the blockchain.")
#print("The blockchain is therefore setup to consider the transaction verified as soon as Dexter votes for it.\n")

winner=asyncio.run(PoEt(node_map))
print(winner+" is the winner as they finished waiting first.\n")
print("Behaving as if we were "+winner+", we can choose to vote for a transaction's validity.")
print("Minimum voting weight for the blockchain to verify transaction: " + str(blockchain.weight_for_validate))
print(winner+"'s voting weight: " + str(node_map[winner].weight) + "\n")

temp = list(blockchain.unverified_transaction_pool.keys())

for transaction_uuid in temp:

    print(blockchain.unverified_transaction_pool[transaction_uuid])
    while True:
        user_input = input("Approve transaction? [y/n] ")
        if user_input == 'y':
            blockchain.UpdateTransactionVote(transaction_uuid, node_map[winner].weight)
            break
        elif user_input == 'n':
            print("[NOTICE] Transaction has been discarded. \n")
            break
    

print()
print("Final Phase: All verified transactions are finalized and stored in the blockchain.")
print("Each block has a maximum capacity. So verified transactions are split into multiple blocks as needed.")
print("They are mined using a Proof of Work algorithm using Bitcoin.\n")
print("Finally, the blockchain is reverified.")


blockchain.finalize_verified()
blockchain.ChainValidity()

for block in blockchain.blockchain:
    pprint.pprint(block.serialize())
print()

print("Thank You!")


    



