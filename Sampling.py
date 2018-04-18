import Apriori
import linecache
import random

"""
Adam Westgate
An implementation of the Random Sampling algorithm for association rules. This is used to obtain relevant random samples from databases that are too large to analyze in their entirety.
"""

def getRandomSample( fileName, size ):

    #this is because the first row of the list will always be none -- there is no "line 0"
    size += 1
    sample = [None] * size

    for i in range(1,len(sample)):
        sample[i] = lineToList( linecache.getline( fileName, i ).rstrip() ) 

    #clear the line cache when its not being used
    linecache.clearcache()

    #pop off the first item because it will always be a useless value (there is no line 0)
    sample.pop(0)

    
    dataFile = open( fileName,'r' )
    replaceIndex = 0
    currentLine = len(sample)+1

    #this is here so that when the next loop runs it will start at a line number equal to size+1
    for i in range(0,currentLine):
        dataFile.readline()

    random.seed()

    # loop to replace lines in the sample based on an ever diminishing probability.
    # The loop continues until there are no more lines to read because the sampling is supposed to work even if there were an unknown number of lines for some crazy reason.
    while dataFile.readline():

        #this is used to create a random chance of replacing the line in the sample. If this number is smaller than the size of the sample then it will be the index of a line to be replaced.
        replaceIndex = random.randint(0,currentLine)

        #the chance of a line being replaced is: samplesize/currentLine -- if the current line being read is line 14 then the chance of it replacing an existing index will be 7/14 or 50%
        if replaceIndex < len(sample):
            sample[replaceIndex] = lineToList( linecache.getline( fileName, currentLine ).rstrip() )
        
        currentLine+=1

    dataFile.close()
    linecache.clearcache()
    
    return sample
        
    
def lineToList( readString ):
"""
Converts a read string line into a list for use in the transaction array
"""

    itemList = []

    readString.replace(' ','')
    itemList = readString.split(',')

    return itemList
