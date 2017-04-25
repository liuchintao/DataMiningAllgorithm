'''
Created on 2017年4月24日

@author: Magister
'''
import sys
from net.algorithm.decision_tree_id3 import DecisionTree, TestClassifier



def loadData():
    print("Please enter full file name:")
    fileName = sys.stdin.readline().strip()
    print("reading file......")
    try:
        f = open(fileName,'r')
        print("start loading data.")
        data = [[]]
        for line in f:
            line = line.strip()
            data.append(line.split(','))
        data.remove([])
        print("Complete.")
        return data
    except IOError:
        print("Error: Could not find the test file specified or unable to open it" %fileName)
        sys.exit(0)


def printTree(tree, indent):
    loc = indent
    if isinstance(tree, dict):
        for treeNode in tree.items():
            print("    " * loc, treeNode[0])
            if isinstance(treeNode[1], dict):
                indent += 1
                printTree(treeNode[1], indent)
            else:
                print("    " * (loc+1), treeNode[1])


def main():
    #load train data set
    trainDataSet = loadData()
#     for mtuple in trainDataSet:
#         print(mtuple)
    attributes_list = trainDataSet[0]
#     print(attributes_list)
    trainDataSet.remove(attributes_list)
    target = 'class'
    
    #create decision tree
    tree = DecisionTree.makeTree(trainDataSet, attributes_list, target, 0)
#     print(tree)
#     printTree(tree, 0)
    TestClassifier.testProcess(tree, attributes_list)
    pass


if __name__ == '__main__':
    main()