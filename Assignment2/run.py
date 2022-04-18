from Simplex import Simplex
from fractions import Fraction
objective = ('maximize','2x_1 + 5x_2')
constraints = ['1x_1 + 1x_2 <= 6', '1x_2 <= 3', '1x_1 + 2x_2 <= 9']
lp_system = Simplex(2, constraints, objective)
print(lp_system.solution)
#{'x_2': Fraction(6, 1), 'x_1': Fraction(2, 1)}
print(lp_system.optimize_val)