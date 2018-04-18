import Apriori
import Sampling

"""
Adam Westgate
An of Toivonen's algorithm for association rule mining.
Note: If used on a small dataset the difference in support between MIN_SUPPORT and MIN_SUPPORT_SAMPLE should be no less than 2. Also on a small dataset the algorithm gets screwy if the MIN_SUPPORT_SAMPLE is >= 4
"""
SAMPLE_SIZE = 6
MIN_SUPPORT_SAMPLE = 2
MIN_SUPPORT = 4

def main():

    #Temporary thing that holds all the possible items in the itemsets. Might change later to a function that finds them instead.
    potentialSingleItems = [['Blouse'],['Jeans'],['Shoes'],['Shorts'],['Skirt'],['TShirt']]

    #grab first random sample
    sample = []
    while len(sample) == 0:
        sample = Sampling.getRandomSample("dataset.txt",SAMPLE_SIZE)

    #run apriori on sample
    frequentSampleItemsets = Apriori.run(sample,MIN_SUPPORT_SAMPLE)

    #get negative border
    negativeBorder = getNegativeBorder( potentialSingleItems, frequentSampleItemsets )

    #get the frequents for Negative Border U Frequent Sample Itemsets
    allFrequentItemsets = sorted(getFrequentItemsets(negativeBorder + frequentSampleItemsets , "dataset.txt", MIN_SUPPORT))

    while len(getFrequentItemsets(negativeBorder, "dataset.txt", MIN_SUPPORT)) > 0:

        #first pass, get sample and generate negative border
        sample = Sampling.getRandomSample("dataset.txt",SAMPLE_SIZE)
        frequentSampleItemsets = Apriori.run(sample, MIN_SUPPORT_SAMPLE)
        negativeBorder = getNegativeBorder( potentialSingleItems, frequentSampleItemsets )
        
        #second pass, get frequents of all itemsets
        allFrequentItemsets = sorted(getFrequentItemsets(negativeBorder + frequentSampleItemsets , "dataset.txt", MIN_SUPPORT))

    print("Final Result (all frequents): ")
    print(allFrequentItemsets)
    

def getNegativeBorder( possibleItems, sampleItemsets ):
"""
Finds all possible combinations that weren't in the sample itemsets and returns them as a list. This is the negative border.
"""
    
    negativeBorder = []

    #add the missing single items that compose all the other itemsets
    for i in range(0,len(possibleItems)):
        if possibleItems[i] not in sampleItemsets:
            negativeBorder.append(possibleItems[i])

    #add all the possible frequent itemsets whose subsets are in the frequent itemsets from the sample
    index = 0
    while index < len(sampleItemsets):
        for j in range(0,len(sampleItemsets)):
            #create the itemsets by joining the frequents. j must be greater than index so that the items at the index do not add anything before. This is to avoid creating itemsets of the same elements in different orders.
            #Converting to a set removes duplicates and sorting them makes sure that itemsets of the same elements do not slip into the negative border because the order of their elements is different
            if j > index and sampleItemsets[index] != sampleItemsets[j] and sampleItemsets[index] not in sampleItemsets[j] and sampleItemsets[j] not in sampleItemsets[index] and list(sorted(set(sampleItemsets[index] + sampleItemsets[j]))) not in negativeBorder and list(sorted(set(sampleItemsets[index] + sampleItemsets[j]))) not in sampleItemsets:
                negativeBorder.append(list(sorted(set(sampleItemsets[index] + sampleItemsets[j]))))
            
        index+=1

    return negativeBorder

def getFrequentItemsets( itemsets, fileName, minSupport ):
"""
Returns the frequent itemsets from a set that is a union of the negative border and the potential frequents
"""

    supportCounts = [0] * len(itemsets)

    readFile = open(fileName,'r')

    line = readFile.readline()
    while line:
        for i in range(0,len(itemsets)):
            supportCounts[i] += line.count(','.join(itemsets[i]))

        line = readFile.readline()

    frequentItemsets = []
    #remove all the items that don't meet minimum support
    for i in range(0,len(itemsets)):
        if supportCounts[i] >= minSupport:
            frequentItemsets.append(itemsets[i])

    readFile.close()

    return frequentItemsets
    
main()

