'''
Created on 2017年4月19日

@author: Magister
'''
from net.algorithm.frequent_pattern_growth.TreeNode import TreeNode
from itertools import count





class MyFpGrowth(object):
    

    def __createHeaderTab(self, dataset, headerTab, minsup):
        if dataset is None:
            return
        #Create a candidate items set.
        for trans in dataset:
            for items in trans:
                if items != 'null':
                    headerTab[items] = headerTab.get(items,0) + dataset[trans]
        #Remove items that do not meet minimum support
        keys = list(headerTab.keys())
        for key in keys:
            if headerTab[key] < minsup or headerTab[key] == 'null':
                del(headerTab[key])
                continue
            headerTab[key] = [headerTab[key],None]
            
    def __updateHeader(self, nodeToUpdate, targetNode):
        while nodeToUpdate.nodeLink != None:
            nodeToUpdate = nodeToUpdate.nodeLink
        nodeToUpdate.nodeLink = targetNode
    
    def __insertTreeNode(self, items, inTree, headerTab, count):
        '''if item has been in tree node's children set, execute child.inc()
            else add new child to the tree root node
        '''

        if items[0] in inTree.children:
            inTree.children[items[0]].inc(count)
        else:
            inTree.children[items[0]] = TreeNode(items[0], count, inTree)
            #Update header table
            if headerTab[items[0]][1] is None:
                headerTab[items[0]][1] = inTree.children[items[0]]
            else:
                self.__updateHeader(headerTab[items[0]][1], inTree.children[items[0]])
        if len(items) > 1:
            self.__insertTreeNode(items[1::], inTree.children[items[0]], headerTab, count)
    
    def __createTree(self, inTree, rawDataset, headerTab, minsup = 1):
        for trans,count in rawDataset.items():
            localD = {}
            for item in trans:
                if item in headerTab:
                    localD[item] = headerTab[item][0]
#             print(localD)
            if len(localD) > 0:
                orderItems = [v[0] for v in sorted(localD.items(), key = lambda p : p[1], reverse = True)]
#                 print(orderItems)
                self.__insertTreeNode(orderItems, inTree, headerTab, count)
    

    def __initRawDataset(self, dataset):
        rtnSet = {}
        for trans in dataset:
            if frozenset(trans) in rtnSet:
                rtnSet[frozenset(trans)] += 1
            else:
                rtnSet[frozenset(trans)] = 1
        return rtnSet
    
    
    def __init__(self, dataset, frequentItemsSet, minsup = 1):
        self.rawDataset  = dataset
        self.frequentItemsSet = frequentItemsSet
        self.minsup = minsup
        self.headerTab = {}
        self.fpTree = TreeNode('null', 1, None)
        
        '''this algorithm will scan raw data set twice.
        it is the first time scan raw data set, initializing header table.  
        extract value from rawDataset to headerTab.'''
        
        self.formatDataset = self.__initRawDataset(dataset)
#         print('format: ', self.formatDataset)
        self.__createHeaderTab(self.formatDataset, self.headerTab, self.minsup)
#         print(self.headerTab)
        #convert raw data set to FP-Tree
        self.__createTree(self.fpTree, self.formatDataset, self.headerTab, self.minsup)
#         self.fpTree.disp()
        self.__mine(self.frequentItemsSet, self.headerTab, self.fpTree)
        

    def __ascendTree(self, treeNode, prefixPath):
        if treeNode is not None:
            prefixPath.append(treeNode.name)
            self.__ascendTree(treeNode.parent, prefixPath)
        pass
    
    
    def __findPrefixPath(self, basePat, treeNode):
        condPat = {}
        while treeNode is not None:
            prefixPath = []
            self.__ascendTree(treeNode, prefixPath)
            if len(prefixPath) > 1:
                condPat[frozenset(prefixPath[1::])] = treeNode.count
            treeNode = treeNode.nodeLink
        return condPat
    
    
    def __mine(self, frequentItemsSet, headerTab, inTree, prefix = set([])):
        suffixList = [v[0] for v in sorted(headerTab.items(), key = lambda p : p[1][0])]
#         print(suffixList)
        for basePat in suffixList:
            newFreqSet = prefix.copy()
            newFreqSet.add(basePat)
            frequentItemsSet.append(newFreqSet)
            
            condPatBase = self.__findPrefixPath(basePat, headerTab[basePat][1])
#             print(condPatBase)
            #conditional FPTree & FPHeaderTab
            condFPTree = TreeNode('null', 1, None)
            condFPheaderTab = {}
            self.__createHeaderTab(condPatBase, condFPheaderTab, self.minsup)
            self.__createTree(condFPTree, condPatBase, condFPheaderTab, self.minsup)
#             print(condFPheaderTab)
            if condFPheaderTab != None:
                self.__mine(frequentItemsSet, condFPheaderTab, condFPTree, newFreqSet)
                
        pass