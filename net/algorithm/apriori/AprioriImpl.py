'''
Created on 2017年5月3日

@author: Magister
'''
from itertools import chain


class Apriori(object):
    '''
    classdocs
    '''
    def __init__(self, rawData, minSup):
        '''
        Constructor
        '''
        self.minSup = minSup
        self.data = rawData
        self.freqItemSet = {}
        self.execute(self.data, self.minSup, self.freqItemSet)

            
    def findFreqOneItemSet(self, rawData, minSup, freqOneSet):
        if rawData is not None:
            for trans in rawData:
                for item in trans:
                    freqOneSet[item] = freqOneSet.get(item, 0) + 1
#     print("candidate one item set: ", freqOneSet)
        if freqOneSet is not None:
            keyList = list(freqOneSet.keys())
            for item in keyList:
                if freqOneSet[item] < minSup:
                    del(freqOneSet[item])
    
        return freqOneSet
    

    def myMerge(self, set1, set2):
        '''This method help us to merge two sets whose length are equal'''
        
        pass
    
    
    def connect(self, count, lastItemSet, tempSet):
        for items in lastItemSet:
            if isinstance(items, frozenset):
                idx = lastItemSet.index(set(items))
            else:
                idx = lastItemSet.index(items)
            while idx < len(lastItemSet) - 1:
                tempTuple = set()
                if isinstance(items, frozenset):
                    tempTuple = self.myMerge(set(items),set(lastItemSet[idx + 1]))
                    if len(tempTuple) == count:
                        tempSet.add(tempTuple)
                #create candidate two items set
                else:
                    tempTuple.add(items)
                    tempTuple.add(lastItemSet[idx + 1])
                    tempSet.add(frozenset(tempTuple))                    
                idx += 1
        pass
    
    
    def findSubset(self, items, subSet):
        if len(items) == 2:
            for item in items:
                subSet.append(item)
        else:
            for item in items:
                temp = items.copy()
                temp.remove(item)
                subSet.append(temp)
        
    
    def pruning(self, lastItemSet, tempSet):
        for items in tempSet:
            subSet = []
            #find temp_set's i-1 items subset.
            self.findSubset(items, subSet)
            for mSet in subSet:
                if mSet not in lastItemSet:
                    tempSet.remove(items)
    
    
    def findSubTransSet(self, count, trans):
        subSet = []
        if len(trans) < count:
            return None
        for item in trans:
            temp = set(trans)
            temp.remove(item)
            if len(temp) > count:
                subSet.append(self.findSubTransSet(count, temp))
            if len(temp) == count:
                subSet.append(temp)
            if len(temp) + 1 == count:
                subSet.append(set(trans))
                break
        return subSet
    
    def findSubSet(self, waitingSet):
        rtnVal = set([])
        for items in waitingSet:
            if isinstance(items, list):
                for item in items:
                    rtnVal.add(frozenset(item))
            else:
                rtnVal = waitingSet.copy()
                break
        return rtnVal
    
    def filter(self, count, rawData, minSup, candidate):
        rtnSet = {}
        for trans in rawData:
            subTransSet = self.findSubSet(self.findSubTransSet(count, trans))
#             print('subTransSet: ', subTransSet)
            if subTransSet is None:
                continue
            for item in candidate:
                if item in subTransSet:
                    rtnSet[frozenset(item)] = rtnSet.get(frozenset(item), 0) + 1
#         for item in rtnSet.items():
#             print(item)
        keyList = list(rtnSet.keys())
        i = 1
        for key in keyList:
            print(i)
            i += 1
            if rtnSet[key] < minSup:
                del(rtnSet[key])
        return rtnSet
    
    
    def generateItemSet(self, count, rawData, minSup, lastFreqSet):
        lastItemSet = list(v[0] for v in sorted(lastFreqSet.items(), key = lambda p : p[1]))
        tempSet = set([])
        #connect step
        self.connect(count, lastItemSet, tempSet)
#         for item in tempSet:
#             print(item)
        ''' According to the property of Apriori,
         all subsets of frequent item set are frequent.
         So in this step, we would prune temp_set by checking 
         whether its all i-1 items subsets belong to frequent item set'''
        #pruning step
        self.pruning(lastItemSet, tempSet)
#         print(tempSet)
#         for item in tempSet:
#             print(item)
        '''After pruning step, tempSet evolves that we called Candidate item set 
        during the next step, we would filter the items in Candidate item set.'''
        #filter the candidate item set
        freqSet = self.filter(count, rawData, minSup, tempSet)
#         print(freqSet)
        return freqSet
    
    
    def findFreqItemSet(self, count, rawData, minSup, lastFreqSet, freqItemSet):
        count += 1
        if lastFreqSet is None:
            return None
        freqItemSet.update(lastFreqSet)
        ''' The first step to find ith frequent item set
         is generating the ith frequent item set.'''
        lastFreqSet = self.generateItemSet(count, rawData, minSup, lastFreqSet)
        self.findFreqItemSet(count, rawData, minSup, lastFreqSet, freqItemSet)
#         return freqItemSet
#         return freqItemSet
    
    
    
    def execute(self, rawData, minSup, freqItemSet):
        freqOneSet = {}     #frequent one item set
        #find frequent_one_itemset.
        self.findFreqOneItemSet(rawData, minSup, freqOneSet)
#     print("frequent one item set: ", freqOneSet)
        '''After we find out frequent_one_item_set, we should find 
        frequent_i_item_set in iteration or recursion with it. '''
        #find all frequent item set by recursion
        self.findFreqItemSet(1, rawData, minSup, freqOneSet, freqItemSet)
        print('freqItemSet: ', freqItemSet)
        for items in freqItemSet:
            print(items)
#         pass
    

