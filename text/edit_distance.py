
__author__ = 'tg'

from util.arrays import format_2d_array
import sys



def min_lavenshtein_distance(s1, s2):
    '''
    Computes Minimum Lavenshtein Distance between two strings
    :param s1: string 1
    :param s2: string 2
    :return: minimum edit distance
    '''


    s1 = '#' + s1  # An empty space is added to make space for base case
    s2 = '#' + s2  # An empty space is added to make space for base case
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

    print format_2d_array(matrix, s1, s2)

    return matrix[n-1][m-1]

if __name__ == '__main__':
    s1 = 'intention'
    s2 = 'execution'
    min_edit_distance = min_lavenshtein_distance(s1, s2)
    print min_edit_distance