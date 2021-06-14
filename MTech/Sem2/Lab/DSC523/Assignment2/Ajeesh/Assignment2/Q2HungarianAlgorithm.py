import sys


def permute(a, results):
    if len(a) == 1:
        results.insert(len(results), a)
    else:
        for i in range(0, len(a)):
            element = a[i]
            a_copy = [a[j] for j in range(0, len(a)) if j != i]
            subresults = []
            permute(a_copy, subresults)
            for subresult in subresults:
                result = [element] + subresult
                results.insert(len(results), result)


results = []
matrix = [[1500, 4000, 4500],
          [2000, 6000, 3500],
          [2000, 4000, 2500]]

permute(range(len(matrix)), results)  # [0, 1, 2] for a 3x3 matrix
minval = sys.maxsize

for indexes in results:
    cost = 0
    for row, col in enumerate(indexes):
        cost += matrix[row][col]
    minval = min(cost, minval)

print("The optimal cost is", minval)
