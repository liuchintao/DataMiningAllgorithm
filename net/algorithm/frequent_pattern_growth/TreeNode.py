'''
Created on 2017年4月18日

@author: Magister
'''

class TreeNode:
    def __init__(self, name, numOccur, parentNode):
        self.name = name
        self.count = numOccur
        self.parent = parentNode
        self.nodeLink = None
        self.children = {}
    
    def inc(self,numOccur):
        self.count += numOccur
    
#     def disp(self, ind=1):
#         print(" "*ind, self.name, " ", self.count)
#         for cheld in self.cheldren.values():
#             cheld.disp(ind+1)