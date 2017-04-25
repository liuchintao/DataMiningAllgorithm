'''
Created on 2017年4月24日

@author: Magister
'''
import math



def majority(valFre):
    max = 0
    major = ''
    for val in valFre.items():
        if val[1] > max:
            max = val[1]
            major = val[0]
#     print(major,': ', max)
    return major


def entropy(attributes, data, target):
    #Calculate the frequency of target values' kinds
    valFre = {}
    entropy = 0.0
    idx = attributes.index(target)
    for rec in data:
        valFre[rec[idx]] = valFre.get(rec[idx], 0) + 1
    for val in valFre.values()():
        if val == 0:
            entropy += 0
        else:
            entropy += (-val/len(data)) * math.log(val/len(data), 2)
    return entropy


def gain(data, attributes, attr, target, infoD):
    '''
    Calculate the information gain(reduction in entropy) that would be 
    resulted by splitting the data set on the chosen attribute(attr)
    '''
    attrValFre = {}
    subsetEntropy = 0.0
#     count the frequency of the values of attr
    idx = attributes.index(attr)
    for entry in data:
        attrValFre[entry[idx]] = attrValFre.get(entry[idx], 0) + 1
    # Calculate the sum of the entropy for each subset of records 
    # weighted by their probability of occuring in the training set.
    for key in attrValFre.keys():
        attrValProp = attrValFre[key] / sum(attrValFre.values())
        subDataSet = [entry for entry in data if entry[idx] == key]
        subsetEntropy += attrValProp * entropy(attributes, subDataSet, target)
    return (infoD - subsetEntropy)
    pass


def chooseAttrByID3(data, attributes, target):
    best = attributes[0]
    maxgain = 0
    infoD = entropy(attributes, data, target)
#     find best attribute as splitting criterion by calculating 
#     information gain of each attributes.
    for attr in attributes:
        attrGain = gain(data, attributes, attr, target, infoD)
        if attrGain > maxgain:
            maxgain = attrGain
            best = attr
    return best


def getValues(data, attributes, attr):
    values = set()
    idx = attributes.index(attr)
    for rec in data:
        values.add(rec[idx])
    return values


def getExamples(data, attributes, attr, val):
    examples = [[]]
    idx = attributes.index(attr)
    for rec in data:
        if rec[idx] == val:
            newEntry = []
            for i in range(0,len(rec)):
                if i != idx:
                    newEntry.append(rec[i])
            examples.append(newEntry)
    examples.remove([])
    return examples


def makeTree(data, attributes, target, recursion):
    recursion += 1
    tarIdx = attributes.index(target)
    valFre = {}
    vals = []
    for rec in data: 
        #get target's kinds of values
        vals.append(rec[tarIdx])
        #get target's frequency of value kinds
        valFre[rec[tarIdx]] = valFre.get(rec[tarIdx], 0) + 1
#     for rec in valFre.items():
#         print(rec)
#     print(vals)
    #find majority value that was tagged as 'default class.'
    default = majority(valFre)
#     print(default)
#     if the attributes list except target attribute or the 
#     (sub)data set is empty, return the default value.
    
    if not data or len(attributes) -1 < 0:
        return default
#         if the (sub)data set is pure, return the target value
#         in other words, the records in the data set have 
#        the same classification 
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
#         find out the next best splitting_criterion by using 
#         attribute_selece_method
        bestAttr = chooseAttrByID3(data, attributes, valFre, target)
#         Create a new decision tree/node with the best attribute 
#         and an empty dictionary object--we'll fill that up next.
        tree = {bestAttr:{}}
#         Create a new decision tree/sub-node for each of the values 
#         in the best attribute field
        for val in getValues(data, attributes, bestAttr):
            examples = getExamples(data, attributes, bestAttr, val)
            newAttrList = attributes[:]
            newAttrList.remove(bestAttr)
            subTree = makeTree(examples, newAttrList, target, recursion)
            tree[bestAttr][val] = subTree
    return tree


