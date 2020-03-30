import nonogram as n

rows = [[1, 1], [5], [5], [3], [1]]
cols = [[2], [4], [4], [4], [2]]

nono = n.Nonogram(rows, cols)
e = nono.EMPTY
f = nono.FILLED

answer = [[e, f, e, f, e], [f, f, f, f, f], [f, f, f, f, f], [e, f, f, f, e], [e, e, f, e, e]]
for i, r in enumerate(answer):
    nono.save_row(i, r)

print(nono)
