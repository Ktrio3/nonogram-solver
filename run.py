from nonogram import Nonogram
from solver import Solver

rows = [[1, 1], [5], [5], [3], [1]]
cols = [[2], [4], [4], [4], [2]]

nono = Nonogram(rows, cols)
s = Solver(nono, False)
s.solve()

print(nono)

rows = [[1, 2, 3], [3, 1], [4, 2], [1, 3], [1, 2, 3]]
cols = [[1, 3], [2], [3], [3, 1], [1], [1], [1, 2], [2, 2], [1, 2], [1]]

nono = Nonogram(rows, cols)
s = Solver(nono, False)
s.solve()

print(nono)
