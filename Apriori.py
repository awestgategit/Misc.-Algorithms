"""
Adam Westgate
A simplistic implementation of the Apriori algorithm. 
"""

def run( transactions, minSupport ):
"""
Inputs:
    transactions - A "list of lists" where each x is an index containing a list (transacton) of y items that compose a single transaction.
    minSupport - The support threshold for itemsets
Outputs:
    -A list of all of the frequent itemsets
"""

    #a list of single items that occur in the dataset with no duplicates
    uniqueSingleItems = findUniqueItems(transactions)

    #Itemset containing all of the frequent itemsets generated over the course of the algorithm's run
    totalFrequents = []

    #generate the first set of two-item itemsets. The initial single item list must be changed to a list of lists for this (so it doesn't iterate through characters).
    for i in range(0, len(uniqueSingleItems)):
        uniqueSingleItems[i] = [uniqueSingleItems[i]]
    
    #remove infrequent single itemsets
    uniqueSingleItems = eliminateItemsets(uniqueSingleItems, transactions, minSupport)

    totalFrequents += uniqueSingleItems

    #generate first set of candidate/frequent pairs
    candidateList = generateCandidateList(uniqueSingleItems, uniqueSingleItems)
    frequentList = eliminateItemsets(candidateList, transactions, minSupport)

    totalFrequents += frequentList

    #loop to extract frequent itemsets of a size greater than 2
    while len(frequentList) > 0:
        candidateList = generateCandidateList(uniqueSingleItems, frequentList)
        frequentList = eliminateItemsets(candidateList, transactions, minSupport)

        if len(frequentList) > 0:
            totalFrequents += frequentList

    return totalFrequents

def findUniqueItems( inData ):
"""
Pulls unique items from the input transactions. This will be used to assemble the initial list of items.
"""
    uniqueItemList = []
    
    for i in range(0, len(inData)):
        #check the word against other words already in the array of words (aka items)
        for j in range (0, len(inData[i])):
            if checkIfUnique( uniqueItemList, inData[i][j] ) == True:
                uniqueItemList.append(inData[i][j])

    return uniqueItemList

def checkIfUnique( inList, checkWord ):
"""
Checks a word against the items in the array to see if it is unique. 
"""
    
    for i in range(0, len(inList)):
        if inList[i] == checkWord:
            return False
    return True

def checkSupport( itemset, dataset ):
"""
A function that returns the support value of an itemset. Note: All itemsets(even itemsets of size 1) passed to this function must be passed as the entire list.
"""
    
    supportCount = 0

    #checkString is the string being checked against lineString which is the row of the dataset collapsed into one string
    lineString = ''
    checkString = ''.join(itemset)

    for i in range(0,len(dataset)):
        lineString = ''.join(dataset[i])
        supportCount += lineString.count(checkString)

    return supportCount

def eliminateItemsets( itemset, dataset, minSupport ):
"""
Eliminates itemsets from a list of multiple itemsets if they don't meet minimum support. Returns the set with all the infrequent itemsets removed.
"""
    i = 0

    #The new itemset with all the infrequent itemsets removed
    filteredItemset = []
    
    #used to convert each individual item to a single item array... this is a lazy fix for using checkSupport on single item lists
    while i < len(itemset):
        if checkSupport( itemset[i], dataset ) < minSupport:
            itemset[i] = None
            
        i+=1

    for i in range(0,len(itemset)):
        if itemset[i] != None:
            filteredItemset.append(itemset[i])

    return filteredItemset

def generateCandidateList( firstList, secondList ):
"""
Returns a list that is made from joining firstList and secondList. In the case of this algorithm it will be used to join two of the same list
"""

    newlyJoinedList = []

    for i in range(0, len(firstList)):
        for j in range(0, len(secondList)):
            #to ensure no duplicates in the itemsets
            if firstList[i] != secondList[j] and secondList[j] not in firstList[i] and firstList[i] not in secondList[j]:
                newlyJoinedList.append(list(firstList[i] + secondList[j]))

    return newlyJoinedList


