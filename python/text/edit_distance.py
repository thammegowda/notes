__author__ = 'Thamme Gowda tgowdan@gmail.com'
__date__ = "September 20, 2015"

from util.arrays import format_2d_array
import sys
import numpy as np

def __backtrace_alignment(matrix, i, j, alignments):
    """
    recursively back traces alignment of strings from given position (i,j) using edit distance matrix
    :param matrix:  edit distance matrix
    :param i: row index
    :param j: column index
    :param alignments: a place to store alignments, this is a list
    :return: True if the trace from (i,j) to position (0,0) was possible; False otherwise
    """
    if i == 0 and j == 0:
        ## this path is right
        alignments.append((0,0))
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
        if move[2] <= min_prev and __backtrace_alignment(matrix, move[0], move[1], alignments):
            alignments.append((i, j))
            return True
    return False

def __pad_string(s, alignments, pad_char = '*'):
    '''
    Creates padded string by inserting pad_char to help alignments
    :param s:   The string to be padded
    :param alignments: the list of alignment positions retrieved from edit distance matrix
    :param pad_char: the character sequence to be used as padding
    :return: padded string
    '''
    n = len(alignments)
    """
    res = []
    for c in range(1, n): #skipping the first
        # Look ahead
        if alignments[c] != alignments[c - 1]:
            res.append(s[alignments[c]])
        else:
            res.append(pad_char)
    return res
    """
    # in one line
    return [ s[alignments[c]] if alignments[c] != alignments[c - 1] else pad_char for c in range(1, n)]

def align_strings(s1, s2, pad_char="*"):
    """
    Aligns two strings based on matching characters
    :param s1: first string
    :param s2: second string
    :param pad_char: the character to be used as padding to indicate insert/delete
    :return: a tuple of (aligned_strings, min_edit_dist, edit_distance_matrix)
    """
    matrix = lavenshtein_matrix(s1, s2)
    s1 = '\0' + s1
    s2 = '\0' + s2

    alignments = []

    # find the minimum path in the matrix
    # back trace by starting from the last cell
    __backtrace_alignment(matrix, len(s1) -1, len(s2)-1, alignments)
    assert alignments[0] == (0,0) # check
    alignments = np.array(alignments)
    res = []
    res.append(__pad_string(s1, alignments[:, 0], pad_char))
    res.append(__pad_string(s2, alignments[:, 1], pad_char))
    return (res, matrix[-1][-1], matrix)

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

    ## matrix = [[0 for i in range(m)] for i in range(n)]
    matrix = np.zeros(shape=(n,m), dtype=int)

    for i in range(n):
        for j in range(m):
            if i == 0:          # base case 1
                distance = j
            elif j == 0:        # base case 2
                distance = i
            else:              # general case
                distance = sys.maxint              # use this as reference to find minimum distance
                if matrix[i-1][j] + 1 < distance:  #horizontal move, insert s2 char
                    distance = matrix[i-1][j] + 1
                if matrix[i][j-1] + 1 < distance:   #vertical move, insert a char from s1
                    distance = matrix[i][j-1] + 1

                # diagonal move :
                # the distance increases if the characters are different (substitution weight = 2)
                # the distance remains same if characters are same (weight = 0)
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
    s1 = 'abbaba'#'intention'
    s2 = 'aabbcva'#'executions'
    #distance = min_edit_distance(s1, s2)
    #print distance
    alignment, min_dist, matrix = align_strings(s1, s2, pad_char="-")

    print format_2d_array(matrix, '\0' + s1, '\0' + s2)
    print alignment[0]
    print alignment[1]
    print "\nMin Edit Distance = %d " % min_dist


