
def minor(m, i, j):
    # calculate the minor of the matrix (MM)
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
m1 = minor(matrix, 0, 1)
print(m1)
