
__author__ = 'tg'

from util.arrays import format_2d_array
import sys


def __find_alignment(matrix, i, j, alignments):

    if i == 0 and j == 0:
        ## this path is right
        return True

    possible_moves = []

    min_prev =  matrix[i][j]               # this will be updated with minimum of three moves
    # TODO: simplify this decision tree
    if i > 0 and j > 0:     # Diagonal Move is possible
        possible_moves.append((i-1, j-1, matrix[i-1][j-1]))
        if matrix[i-1][j-1] <= min_prev:
            min_prev = matrix[i-1][j-1]
    if i > 0 :               # Horizontal is possible
        possible_moves.append((i-1, j, matrix[i-1][j]))
        if matrix[i-1][j] <= min_prev:
            min_prev = matrix[i-1][j]
    if j > 0 :               # Vertical is possible
        possible_moves.append((i, j-1, matrix[i][j-1]))
        if matrix[i][j-1] <= min_prev:
            min_prev = matrix[i][j-1]

    for move in possible_moves:
        if move[2] <= min_prev and __find_alignment(matrix, move[0], move[1], alignments):
            alignments.append((move[0], move[1]))
            return True
    return False

def align_strings(s1, s2):

    matrix = lavenshtein_matrix(s1, s2)
    print format_2d_array(matrix, '#' + s1, '#' + s2)

    # find the minimum path in the matrix
    # start from last cell

    i, j = len(s1), len(s2)
    alignments = []
    __find_alignment(matrix, i, j, alignments)

    n = len(alignments)
    res = ''
    for c in range(n):
        # Look ahead
        res += s1[alignments[c][0]] if c == n-1 or c < n - 1 and alignments[c][0] != alignments[c + 1][0] else '*'
    res += '\n'
    for c in range(n):
        res += s2[alignments[c][1]] if c == n-1 or c < n - 1 and alignments[c][1] != alignments[c + 1][1] else '*'
    print res



def lavenshtein_matrix(s1, s2):
    '''
    Computes Minimum Lavenshtein Distance matrixtwo strings. This implementation
    uses dynamic programming approach.
    :param s1: string 1
    :param s2: string 2
    :return: minimum edit distance matrix.
     The cell present in the last row and last last column contains the min edit distance
    '''

    s1 = ' ' + s1  #  making space for base case
    s2 = ' ' + s2  #  making space for base case
    n = len(s1)
    m = len(s2)

    # declaring an empty array
    matrix = [[0 for i in range(m)] for i in range(n)]

    for i in range(n):
        for j in range(m):
            if i == 0:          # base case 1
                distance = j
            elif j == 0:        # base case 2
                distance = i
            else:              # general case
                distance = sys.maxint  # use this as reference to find minimum distance
                if matrix[i-1][j] + 1 < distance:  #horizontal move, insert s2 char
                    distance = matrix[i-1][j] + 1
                if matrix[i][j-1] + 1 < distance:   #vertical move, insert a char from s1
                    distance = matrix[i][j-1] + 1

                # diagonal move :
                # the distance increases if the characters are different (substitution)
                # the distance remains same if characters are same
                diagonal_dist = matrix[i-1][j-1]  + (0 if s1[i] == s2[j] else 2)
                if diagonal_dist < distance:
                    distance = diagonal_dist
            matrix[i][j] = distance
    return matrix

def min_edit_distance(s1, s2):
    '''
    Computes Minimum edit distance for the two strings
    :param s1: first string
    :param s2: second string
    :return: minimum edit distance (lavenshtein value)
    '''
    matrix = lavenshtein_matrix(s1, s2)
    print format_2d_array(matrix, '#' + s1, '#' + s2)
    return matrix[-1][-1] # the last cell has the value for two complete strings

if __name__ == '__main__':
    s1 = 'intention'
    s2 = 'execution'
    #FIXME: nxm when n != m
    #distance = min_edit_distance(s1, s2)
    #print distance
    align_strings(s1, s2)
