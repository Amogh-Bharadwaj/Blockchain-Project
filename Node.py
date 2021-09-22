#Simple node class with a private wallet for each node.
class Node:
    # Each node is given a weight and a cash value when it is created.
    # This weight comes into play when a transaction needs to be voted upon.
    # Currently, all nodes except Dexter have a weight of 0. [they cannot vote upon any transactions]
    def __init__(self, amount: int, weight: int):
        if amount < 0 or weight < 0:
            raise ValueError("We can't have negative cash or weights for a node.")   
        self.amount = amount
        self.weight = weight
       
    def __repr__(self):
        return "Amount: " + str(self.amount) + "  Weight: " + str(self.weight) 

    def updateWallet(self, exchange: int) -> None:
        self.amount = self.amount + exchange
    