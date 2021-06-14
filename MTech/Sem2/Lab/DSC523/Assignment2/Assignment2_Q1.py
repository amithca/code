def minor_matrix(m, i, j):
    # calculate the minor of the matrix (MM)
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]
mtx_A = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
m1 = minor_matrix(mtx_A, 0, 1)
print(f'Matrix minor is:{m1}')
