"""
Line Edit
Compare new and old versions of files to find out the differences in terms of deletion, insertion, alteration, and substitution of lines.
Author: Aditi Sharma
Date: 1/6/2023
"""

def lcs(s1, s2):
    """takes two strings as parameters and returns 
    the longest common subsequence,without using recursion"""
    s1 = " "+s1
    s2 = " "+s2
    rows = len(s1)
    cols = len(s2)
    cache = [[0 for i in range(cols)] for j in range(rows)]
    
    #making table
    for i in range(rows):
        for j in range(cols):
            if i == 0 or j == 0:
                cache[i][j] = 0
            elif s1[i] == s2[j]:
                cache[i][j] = cache[i-1][j-1] + 1
            else:
                cache[i][j] = max(cache[i][j-1], cache[i-1][j])
    
    #trace back
    longest_seq = ''
    row = rows-1
    col = cols-1
    while (row > 0 and col > 0):
        if s1[row] == s2[col]:
            longest_seq = s1[row] + longest_seq
            row -= 1
            col -= 1
        else:
            if cache[row-1][col] > cache[row][col-1]: #line will cause errors
                row -= 1
            else:
                col -= 1
    
    return longest_seq

def extra_ind(longest, s):
    """returns the indexes of characters not in lcs but in s""" 
    ind = []
    i = 0
    for c in s:
        if len(longest) != 0 and longest[0] == c:
            longest = longest[1:]
        else:
            ind.append(i)
        i += 1
    return ind

def change_s(ind, s):
    """returns changed string to include brackets around extra characters"""
    s_list = [x for x in s]
    for index in ind:
        s_list[index] = "[[" + s_list[index] + "]]"
    return "".join(s_list)
        
    

def process_s(s1, s2):
    """processes the strings all characters in both the left and right strings 
    that are not present in their longest common subsequence will be wrapped
    in double square brackets and return them"""
    longest = lcs(s1, s2)
    ind_s1 = extra_ind(longest, s1)
    ind_s2 = extra_ind(longest, s2)
    new_s1 = change_s(ind_s1, s1)
    new_s2 = change_s(ind_s2, s2)    
    return new_s1, new_s2


def minimum(cache, i, j):
    """deals with finding the operation and returns the operation"""
    operation = None
    if i == 0:
        operation = "I"
    elif j == 0:
        operation = "D"
    else:
        lst = [cache[i-1][j-1], cache[i-1][j], cache[i][j-1]]
        min_index = lst.index(min(lst))
        if min_index == 0:
            operation = "S"
        elif min_index == 1:
            operation = "D"
        else:
            operation = "I"
    return operation
        
    

def traceback(cache, lines1, lines2):
    """traces back through the cache to find which lines had insertion, deletion,
    substitution and copying. returns this information as list of tuples"""
    result = []
    i = len(lines1)-1
    j = len(lines2)-1
    while (i > 0 or j > 0):
        if lines1[i] == lines2[j]:
            result.append(("C", lines1[i], lines2[j]))
            i -= 1
            j -= 1
        else:
            operation = minimum(cache, i, j)
            if operation == "D":
                result.append((operation, lines1[i], ""))
                i -= 1
            elif operation == "I":
                result.append((operation, "", lines2[j]))
                j -= 1
            else:
                prev, current = process_s(lines1[i], lines2[j])
                result.append((operation, prev, current))
                i -= 1
                j -= 1
    return result
                
    
    
def make_cache(lines1, lines2):
    """goes through the edit-distance algorithm and returns the cache"""
    rows = len(lines1)
    cols = len(lines2)
    cache = [[0 for i in range(cols)] for j in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                cache[row][col] = 0
            elif row == 0:
                cache[row][col] = col
            elif col == 0:
                cache[row][col] = row
            elif lines1[row] == lines2[col]:
                cache[row][col] = cache[row-1][col-1]
            else:
                min_last = min(cache[row-1][col], cache[row][col-1], cache[row-1][col-1])
                cache[row][col] = min_last + 1
    return cache
    

def line_edits(s1, s2):
    """ take as parameters two strings representing the previous and current
    versions of the code file.The output from the function will be a list of
    3-element tuples (operation, left_line, right_line).Operation will have the
    value 'C', 'S', 'D' or 'I' for Copied, Substituted, Deleted and 
    Inserted, respectively. left_line will be the empty string for 'I' 
    operations and right_line will be empty for 'D' operations."""
    lines1 = [""] + s1.splitlines()
    lines2 = [""] + s2.splitlines() 
    cache = make_cache(lines1, lines2)
    result = traceback(cache, lines1, lines2)
    result.reverse()
    return result
   


def test():
    """Test cases for assignment"""
    s2 = "Line1\nLine2"
    s1 = ""
    table = line_edits(s1, s2)
    for row in table:
        print(row)
    print()
    #should get output: ('D', 'Line1', '')


    s1 = "Line1\nLine2\nLine3\nLine4\n"
    s2 = "Line1\nLine3\nLine4\nLine5\n"
    table = line_edits(s1, s2)
    for row in table:
        print(row)
    print()
    #should get output:
    """('D', 'Line1', '')↩
    ('S', 'Line3', 'Twaddle')↩
    ('C', 'Line5', 'Line5')"""

    print()

    s1 = "Line1\nLine2\nLine3\nLine4\nLine5\n"
    s2 = "Line3\nLine2\n"
    table = line_edits(s1, s2)
    for row in table:
        print(row)    
    print()
    #should get output:
    """('D', 'Line1', '')
    ('D', 'Line2', '')
    ('C', 'Line3', 'Line3')
    ('D', 'Line4', '')
    ('S', 'Line5', 'Line2')"""

test()
