'''
Created on 2017年5月3日

@author: Magister
'''

'''可以考虑下frozenset'''
def findSubTransSet(count, trans):
    subSet = []
    if len(trans) < count:
        return None
    for item in trans:
        temp = set(trans)
        temp.remove(item)
        if len(temp) > count:
            subSet.append(findSubTransSet(count, temp))
        if len(temp) == count:
            subSet.append(temp)
    return subSet

if __name__ == '__main__':
    data = [1,2,3]
    result = findSubTransSet(2, data)
    val = set([])
    for items in result:
        if isinstance(items, list):
            for item in items:
                val.add(frozenset(item))
        else:
            val = result.copy()
    for i in val:
        print(i)