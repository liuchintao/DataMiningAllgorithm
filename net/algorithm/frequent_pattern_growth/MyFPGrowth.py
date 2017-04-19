'''
Created on 2017年4月19日

@author: Magister
'''
from net.algorithm.frequent_pattern_growth.TreeNode import TreeNode




class MyFpGrowth(object):
    

    def __createHeaderTab(self, rawDataset, headerTab, minsup):
        if rawDataset is None:
            return
        #Create a candidate items set.
        for trans in rawDataset:
            for items in trans:
                headerTab[items] = headerTab.get(items,0) + 1
        #Remove items that do not meet minimum support
        keys = list(headerTab.keys())
        for key in keys:
            if headerTab[key] < minsup:
                del(headerTab[key])
            headerTab[key] = [headerTab[key],None]
            

    def __updateHeader(self, nodeToUpdate, targetNode):
        while nodeToUpdate.nodeLink != None:
            nodeToUpdate = nodeToUpdate.nodeLink
        nodeToUpdate.nodeLink = targetNode
    
    
    
    def __insertTreeNode(self, items, inTree, headerTab):
        '''if item has been in tree node's children set, execute child.inc()
            else add new child to the tree root node
        '''

        if items[0] in inTree.children:
            inTree.children[items[0]].inc()
        else:
            inTree.children[items[0]] = TreeNode(items[0], 1, inTree)
            #Update header table
            if headerTab[items[0]][1] is None:
                headerTab[items[0]][1] = inTree.children[items[0]]
            else:
                self.__updateHeader(headerTab[items[0]][1], inTree.children[items[0]])
        if len(items) > 1:
            self.__insertTreeNode(items[1::], inTree.children[items[0]], headerTab)
    
    
    def __createTree(self, inTree, rawDataset, headerTab, minsup = 1):
        for trans in rawDataset:
            localD = {}
            for item in trans:
                localD[item] = localD.get(item, 0) + headerTab[item][0]
#             print(localD)
            if len(localD) > 0:
                orderItems = [v[0] for v in sorted(localD.items(), key = lambda p : p[1], reverse = True)]
                print(orderItems)
                self.__insertTreeNode(orderItems, inTree, headerTab)
    
    def __init__(self, dataset, frequentItemsSet, minsup = 1):
        self.rawDataset  = dataset
        self.frequentItemsSet = frequentItemsSet
        self.minsup = minsup
        self.headerTab = {}
        self.fpTree = TreeNode('null_item', 1, None)
        
        '''this algorithm will scan raw data set twice.
        it is the first time scan raw data set, initializing header table.  
        extract value from rawDataset to headerTab.'''
        
        self.__createHeaderTab(self.rawDataset, self.headerTab, self.minsup)
#         print(self.headerTab)
        #convert raw data set to FP-Tree
        self.__createTree(self.fpTree, self.rawDataset, self.headerTab, self.minsup)
#         self.fpTree.disp()
        
