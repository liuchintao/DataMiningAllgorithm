'''
Created on 2017年4月24日

@author: Magister
'''
import sys


def loadData():
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


def main():
    #load train data set
    trainDataSet = loadData()
#     for mtuple in trainDataSet:
#         print(mtuple)
    attributes_list = trainDataSet[0]
#     print(attributes_list)
    trainDataSet.remove(attributes_list)
    target = 'class'
    
    pass


if __name__ == '__main__':
    main()