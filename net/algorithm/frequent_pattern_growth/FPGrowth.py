'''
Created on 2017年4月18日

@author: Magister
'''
from net.algorithm.frequent_pattern_growth.TreeNode import TreeNode



def loadDat():
    rtnData = [[1,2,5],
               [2,4],
               [2,3],
               [1,2,4],
               [1,3],
               [2,3],
               [1,3],
               [1,2,3,5],
               [1,2,3]
        ]
    return rtnData

def initDataset(simpleDat):
    rtnSet = {}
    for trans in simpleDat:
        if frozenset(trans) in rtnSet:
            rtnSet[frozenset(trans)] += 1
        else:
            rtnSet[frozenset(trans)] = 1
    return rtnSet


def createTree(initSet, minsup = 1):
    headerTab = {}
    #go over dataset twice
    #first step go over dataset once and get candidate set C1
    for trans in initSet:
        for item in trans:
            headerTab[item] = headerTab.get(item,0) + initSet[trans]
    #remove items that not matching min_sup
    keys = list(headerTab.keys())
    for item in keys:
        if headerTab[item] < minsup:
            del(headerTab[item])
            
    #create FP-Tree
    #create frequent items set 
    freqItemSet = set(headerTab.keys())
#     print(freqItemSet)
    if len(freqItemSet) == 0:
        #if there is no item meets min_sup, go out
        return None
    for item in headerTab:
        #refactor the value of dic-type headerTab to use None link
        headerTab[item] = [headerTab[item],None]
#     print(headerTab)
    
    #create root tree-node
    rtnTree = TreeNode('null_item', 1, None)
    #go through data set twice
    for trans, count in initSet.items():
        print('trans: ', trans, 'count:', count)
        localD = {}
        for item in trans:
            if item in freqItemSet:
                localD[item] = headerTab[item][0]
        print('localD',localD)
        if len(localD) > 0:
            orderItems = [v[0] for v in sorted(localD.items(), key=lambda p:p[1],reverse=True)]
#             print('orderItems', orderItems)
            #create tree with ordered items
            insertTree(orderItems, rtnTree, headerTab, count)
    return rtnTree, headerTab

def updateHeader(nodeToUpdate, targetNode):
    while(nodeToUpdate.nodeLink != None):
        nodeToUpdate = nodeToUpdate.nodeLink
    nodeToUpdate.nodeLink = targetNode

def insertTree(items, inTree, headerTab, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = TreeNode(items[0],count,inTree)
        if headerTab[items[0]][1] is None:
            headerTab[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTab[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        insertTree(items[1::], inTree.children[items[0]], headerTab, count)  


def ascendTree(treeNode, prefixPath):
    if treeNode.parent != None:
        prefixPath.append(treeNode)
        ascendTree(treeNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPat = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            condPat[frozenset(prefixPath[1:])] = treeNode.count
#             print("condPat: ", condPat)
        treeNode = treeNode.nodeLink
    return condPat


def mineTree(inTree, headeerTab, freqItemList, minsup, prefix=set([])):
    #asc order headerTab's key
    bigL = [v[0] for v in sorted(headeerTab.items(), key = lambda p : p[1][0])]
    for basePat in bigL:
#         print('basePat: ', basePat)
        newFreqSet = prefix.copy()
        newFreqSet.add(basePat)
#         print('newFreqSet: ', newFreqSet)
        freqItemList.append(newFreqSet)
        condPatBases = findPrefixPath(basePat,headeerTab[basePat][1])
#         print(condPatBases)
        condTree, condHead = createTree(condPatBases, minsup)
        if condHead != None:
            print("conditional tree for: ", newFreqSet)
            mineTree(condTree, condHead, freqItemList, minsup, newFreqSet)
def main():
    simpleDat = loadDat()
#     print(simpleDat)
    
    initSet = initDataset(simpleDat)
#     print(initSet)
#     create FP-tree with initSet and min_sup
    fpTree, headerTab = createTree(initSet, 2)
#  print('headerTab:',headerTab)
    freqItem = []
    mineTree(fpTree, headerTab, freqItem, 2)
    print(freqItem)
if __name__ == '__main__':
    main()