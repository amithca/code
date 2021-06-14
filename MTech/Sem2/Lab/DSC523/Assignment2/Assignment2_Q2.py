import sys
mtx_A = [[1500, 4000, 4500],
          [2000, 6000, 3500],
          [2000, 4000, 2500]]
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

permute(range(len(mtx_A)), results)
minval = sys.maxsize
for i in results:
    cost = 0
    for r, c in enumerate(i):
        cost += mtx_A[r][c]
    minval = min(cost, minval)

print(f'The optimal cost is {minval}')
