__author__ = 'tg'

def format_2d_array(arr, col_head, row_head):
    '''
    Formats a 2d array (list of lists) into a matrix like rows x columns representation
    :param arr:  The array to be formatted
    :param col_head:  the header for each column
    :param row_head: the header for each row
    :return: the string created by formatting the contents of array with headers
    '''
    res = '*'
    for i in col_head:  ## adding the header to columns
        res += '\t' + str(i)
    res += '\n'

    for row_idx in range(0, len(row_head)):
        res += row_head[row_idx] # row head
        for j in arr[row_idx]:
            res += '\t' + str(j)
        res += '\n'
    return res

if __name__ == '__main__':
    arr = [[i for i in range(4)] for j in range(5)]
    res = format_2d_array(arr, 'abcd', 'xyzf')
    print res


