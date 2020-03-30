import nonogram as n

rows = [[1, 1], [5], [5], [3], [1]]
cols = [[2], [4], [4], [4], [2]]

nono = n.Nonogram(rows, cols)
nono.empty(0, 0)
nono.fill(0, 1)
nono.empty(0, 2)
nono.fill(0, 3)
nono.empty(0, 4)

for i in range(5):
    nono.fill(1, i)
    nono.fill(2, i)
nono.empty(3, 0)
nono.fill(3, 1)
nono.fill(3, 2)
nono.fill(3, 3)
nono.empty(3, 4)
nono.empty(4, 0)
nono.empty(4, 1)
nono.fill(4, 2)
nono.empty(4, 3)
nono.empty(4, 4)

print(nono)
