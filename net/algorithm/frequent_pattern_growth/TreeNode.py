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
    
    def inc(self,numOccur = 1):
        self.count += numOccur
    
    def disp(self, ind=1):
        if not isinstance(self.parent, TreeNode):
            print("Parent:", self.parent, '___', self.name, " ", self.count)
        else:
            print("Parent:", self.parent.name, '___', self.name, " ", self.count)
        for child in self.children.values():
            child.disp(ind+1)
    
    def getChildByName(self, name):
        for child in self.children:
            if child.name == name:
                return child
    
    def add(self, child):
        if not isinstance(child, TreeNode):
            raise TypeError("Can only add other FPNodes as children")
        if not child in self.children:
            self.children[child.name] = child
            child.parent = self