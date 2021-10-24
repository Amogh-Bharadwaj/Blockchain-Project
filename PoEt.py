from time import sleep
from random import uniform
import asyncio


async def NodeWait(node:str,delay:float):
    await asyncio.sleep(delay)
    print(node," done waiting.")

async def PoEt(nodes:dict):
    time_map = {}
    winner = ""
    wait_min=11
    for node in nodes:
        time_map[node]=uniform(1, 10)

        if time_map[node]<wait_min:
            wait_min=time_map[node]
            winner=node

    
    for node in time_map:
        print(node," will wait for: ",time_map[node]," seconds.\n")

    print("Waiting...\n")

    WaitList= []
    
    for node in time_map:
        WaitTask = asyncio.create_task(NodeWait(node,time_map[node]))
        WaitList.append(WaitTask)
    
    for W in WaitList:
        await W
   
    return winner



