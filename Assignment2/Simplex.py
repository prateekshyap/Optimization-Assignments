s = " obj: x1 +   2 x2 +  3 x3  +  x4"
txt = s.strip().split()
print(txt)
# Subject To
#  c1: - x1 + x2 + x3 + 10 x4 <= 20
#  c2: x1 - 3 x2 + x3 <= 30
#  c3: x2 - 3.5 x4 = 0
# Bounds
#  0 <= x1 <= 40
#  2 <= x4 <= 3
# General
#  x4
# End