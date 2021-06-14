import pulp as p

Lp_prob = p.LpProblem('Problem', p.LpMinimize)
# Create problem Variables
x = p.LpVariable("x", lowBound=0)  # Create a variable x >= 0
y = p.LpVariable("y", lowBound=0)  # Create a variable y >= 0
Lp_prob += 50 * x + 18 * y
Lp_prob += 2 * x + y <= 100
Lp_prob += x + y <= 80
# Lp_prob += x >= 0
# Lp_prob += y >= 0
# Display the problem
print(Lp_prob)
status = Lp_prob.solve()  # Solver
# print(p.LpStatus[status])  # The solution status
# Printing the final solution
# print(p.value(x), p.value(y), p.value(Lp_prob.objective))