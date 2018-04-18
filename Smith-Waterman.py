"""
Adam Westgate
An implementation of the Smith-Waterman algorithm for solving local sequence alignment problems.
"""

class ScoreNode:

    score = -1 #score held within the node
    prev = None #reference to the previous node
    i = 0
    j = 0
    
    def __init__(self):
        pass

    def set_indices(self,i,j):
        self.i = i
        self.j = j

MATCH = 1
MISMATCH = -1
INDEL = -0.5

#initializes the score matrix. Inputs are the lengths of sequence 1 and 2
def init_matrix(seq1_len, seq2_len):

    score_matrix = [[ScoreNode() for i in range(seq1_len+1)] for j in range(seq2_len+1)]

    for i in range(seq1_len+1):
        score_matrix[0][i].score = 0

    for j in range(seq2_len+1):
        score_matrix[j][0].score = 0

    #print_matrix(score_matrix, seq1_len, seq2_len)

    return score_matrix

#fill the score matrix with the appropriate scores and pointers
def fill_matrix(matrix, seq1, seq2):

    for i in range(1,len(seq2)+1):
        for j in range(1,len(seq1)+1):
            matrix[i][j].set_indices(i,j) #store location of the node in the matrix
            if(seq1[j-1] == seq2[i-1]):
                matrix[i][j].score = matrix[i-1][j-1].score + MATCH
                matrix[i][j].prev = matrix[i-1][j-1]
            else:
                matrix[i][j].score = max([matrix[i-1][j-1].score + MISMATCH,
                                          matrix[i-1][j].score + INDEL,
                                          matrix[i][j-1].score + INDEL,
                                          0])

            if(matrix[i][j].score == matrix[i-1][j-1].score + MISMATCH):
                matrix[i][j].prev = matrix[i-1][j-1]
            elif(matrix[i][j].score == matrix[i-1][j].score + INDEL):
                matrix[i][j].prev = matrix[i-1][j]
            elif(matrix[i][j].score == matrix[i][j-1].score + INDEL):
                matrix[i][j].prev = matrix[i][j-1]

#gets the optimal alignment path by backtracing through a complete scoring matrix
def get_optimal(matrix,seq1_len,seq2_len):

    #find indices of max value
    temp_max = 0
    i_max = 0
    j_max = 0
    
    for i in range(seq2_len + 1):
        for j in range(seq1_len + 1):
            if(matrix[i][j].score >= temp_max):
                temp_max = matrix[i][j].score
                i_max = i
                j_max = j

    print("\nSCORE:",matrix[i_max][j_max].score)

    #backtrace through entire path
    path = []
    path.append((i_max,j_max))
    cur_node = matrix[i_max][j_max]
    
    while(cur_node.prev != None):

        path.append((cur_node.i,cur_node.j))
        cur_node = cur_node.prev

    return path
    
#translates the path from get_optimal into the final aligned sequences
def translate_path(matrix,path,seq1,seq2):

    align1 = ""
    align2 = ""
    
    for i in range(len(path)-1,0,-1):

        if (i < len(path)-1) and (path[i+1][0] == path[i][0]):
            align2 += '-'
        else:
            align2 += seq2[path[i][0]-1]

        if(i < len(path)-1) and (path[i+1][1] == path[i][1]):
            align1 += '-'
        else:
            align1 += seq1[path[i][1]-1]

    print("\nFINAL ALIGNMENT:")
    print(align2)
    print(align1)

#for easily printing the score matrix. Currently only works with less rows than columns (x axis is longer sequence)
def print_matrix(matrix, seq1_len, seq2_len):

    for j in range(seq2_len+1):
        print("")
        for i in range(seq1_len+1):
            print(matrix[j][i].score, "\t",end="")

sequence1 = "1213434222"
sequence2 = "1343422421"

scores = init_matrix(len(sequence1),len(sequence2))
fill_matrix(scores,sequence1,sequence2)
print_matrix(scores,len(sequence1),len(sequence2))
path = get_optimal(scores,len(sequence1),len(sequence2))
translate_path(scores, path, sequence1, sequence2)
