'''
Created on 2017年4月19日

@author: Magister
'''
from net.algorithm.frequent_pattern_growth.MyFPGrowth import MyFpGrowth


def loadData():
    rtnVal = [[1,2,5],
               [2,4],
               [2,3],
               [1,2,4],
               [1,3],
               [2,3],
               [1,3],
               [1,2,3,5],
               [1,2,3]
        ]
    return rtnVal



if __name__ == '__main__':
    dataset = loadData()#raw data set
    frequentItemsSet = []#result list
    minsup = 2#minimum support
    #create FP-Tree & FP-HeaderTab
    myFpGrowthImpl = MyFpGrowth(dataset, frequentItemsSet, minsup)
    for items in frequentItemsSet:
        print(items)
    #mining step