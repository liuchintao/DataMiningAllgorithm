'''
Created on 2017年5月3日

@author: Magister
'''
from net.algorithm.apriori import AprioriImpl

def loadData():
    rtnVal = [
        ['i1','i2','i3','i5'],
        ['i2','i4'],
        ['i1','i2','i5'],
        ['i2','i3'],
        ['i1','i2','i4'],
        ['i1','i3'],
        ['i2','i3'],
        ['i1','i3'],
        ['i1','i2','i3']]
    minSup = 2
    return rtnVal, minSup



if __name__ == '__main__':
    #load raw data and minimum support by loadData method.
    rawData, minSup = loadData()
    #execute apriori algorithm
    AprioriImpl.Apriori(rawData, minSup)