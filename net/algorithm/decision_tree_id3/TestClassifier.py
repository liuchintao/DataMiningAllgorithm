'''
Created on 2017年4月25日

@author: Magister
'''
import sys
from net.algorithm.decision_tree_id3 import Node

def testProcess(dTree, attributes):
    print("Please enter test file name:")
    testFile = sys.stdin.readline().strip()
    tf = open(testFile,'r')
    data = [[]]
    for line in tf:
        line = line.strip()
        data.append(line.split(','))
    data.remove([])
    count = 0
    for entry in data:
        count += 1
        tempDict = dTree.copy()
        result = ""
        while(isinstance(tempDict, dict)):
            l = list(tempDict.keys())
            root = Node.Node(l[0], tempDict[l[0]])
            tempDict = tempDict[l[0]]
            index = attributes.index(root.value)
            value = entry[index]
            if(value in tempDict.keys()):
                result = tempDict[value]
                tempDict = tempDict[value]
            else:
                print("can't process input %s" % count)
                result = "?"
                break
        print("entry%s = %s" % (count, result))
    
    