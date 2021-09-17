#Simple node class with wallet for each node.
class Node:
    def __init__(self,cash):
        self.wallet = cash
         
    def updateWallet(self,exchange):
        self.wallet+=exchange
    