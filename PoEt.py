from time import sleep
from random import uniform
import asyncio

# The source code for the Proof of Elapsed Time consensus algorithm.
# In this algorithm, all the nodes of the network are put to sleep for a given duration allotted to them through a random lottery.
# The first node to wake up is the winner of the block and has mining rights.
# Since the nodes go to sleep concurrently, we simulate this using async functions in python using the inbuilt asyncio library.


# The wait function
async def NodeWait(node:str,delay:float):
    await asyncio.sleep(delay)
    print(node," done waiting.")

async def PoEt(nodes:dict):
    time_map = {}

    winner = ""
    wait_min=8

    for node in nodes:
        time_map[node]=uniform(1, 7)
        
        #Evaluating the winner
        if time_map[node]<wait_min:
            wait_min=time_map[node]
            winner=node

    
    for node in time_map:
        print(node," will wait for: ",time_map[node]," seconds.\n")

    print("Waiting...\n")

    WaitList= []
    
    for node in time_map:
        WaitTask = asyncio.create_task(NodeWait(node,time_map[node])) # RUns the function passed as argument asynchronously.
        WaitList.append(WaitTask)
    
    for W in WaitList:
        await W  # Using the await call, all the tasks run concurrently.
   
    return winner



