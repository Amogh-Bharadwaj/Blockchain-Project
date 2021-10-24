from random import uniform
import asyncio


# Proof of Elapsed Time is a consensus algorithm in which nodes are given a time to wait based on a lottery. 
# The code for this algorithm is usually downloaded by all the nodes and run in a secure enclave using Intel's Secure Guard Extensions (SGX) hardware. 
# We stored this code in an Amazon S3 bucket, from which the nodes shall download it (see Launch.py)
# All nodes wait concurrently of course, and to simulate this, we use Python's inbuilt asyncio library which facilitiates asynchronous functions.
# Using async and await calls, we can simulate nodes waiting for their given durations, and the first node to finish waiting is declared as the winner. 


# Uses a sleep() function to simulate "waiting".
async def NodeWait(node:str,delay:float):
    await asyncio.sleep(delay)
    print(node," done waiting.")

async def PoEt(nodes:dict):
    time_map = {} # A dictionary to store nodes and the wait times they receive.
    winner = ""
    wait_min=11
    for node in nodes:
        time_map[node]=uniform(1, 10) # A random lottery
        

        # Evaluating the winner
        if time_map[node]<wait_min:
            wait_min=time_map[node]
            winner=node

    
    for node in time_map:
        print(node," will wait for: ",time_map[node]," seconds.\n")

    print("Waiting...\n")

    WaitList= []
    
    for node in time_map:
        WaitTask = asyncio.create_task(NodeWait(node,time_map[node])) # Runs the function passed as argument asynchronously.
        WaitList.append(WaitTask)
    
    for W in WaitList:
        await W # Concurrently running all the nodes' waiting tasks. 
   
    return winner



