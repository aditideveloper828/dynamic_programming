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

s1 = "Look at me, I can fly!"
s2 = "Look at that, it's a fly"
print(lcs(s1, s2))

s1 = "abcdefghijklmnopqrstuvwxyz"
s2 = "ABCDEFGHIJKLMNOPQRSTUVWXYS"
print(lcs(s1, s2))

s1 = "balderdash!"
s2 = "balderdash!"
print(lcs(s1, s2))


s1 = "*abbcccddddeeeeeffffgghhijjkkkllllmmmmm*"
s2 = "abcdefghijklmnopqrst"
lcs_string = lcs(s1, s2)
print(lcs_string)
