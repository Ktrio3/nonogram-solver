import nonogram as n
import pytest

heart = '''+---+---+---+---+---+
| x |███| x |███| x |
+---+---+---+---+---+
|███|███|███|███|███|
+---+---+---+---+---+
|███|███|███|███|███|
+---+---+---+---+---+
| x |███|███|███| x |
+---+---+---+---+---+
| x | x |███| x | x |
+---+---+---+---+---+'''


def test_init():
    # Invalid row hints
    with pytest.raises(n.OutOfBoundsHints):
        n.Nonogram([[10]], [[1]])

    with pytest.raises(n.OutOfBoundsHints):
        n.Nonogram([[1]], [[10]])

    # Check board is created correctly
    rows = [[1], [1]]
    cols = [[1], [1]]
    answer = [[None, None], [None, None]]

    nono = n.Nonogram(rows, cols)
    assert answer == nono.board


def test_fill():
    rows = [[1], [1]]
    cols = [[1], [1]]

    nono = n.Nonogram(rows, cols)
    assert nono.board[0][1] is nono.UNKNOWN
    nono.fill(0, 1)
    assert nono.board[0][1] is nono.FILLED


def test_empty():
    rows = [[1], [1]]
    cols = [[1], [1]]

    nono = n.Nonogram(rows, cols)
    assert nono.board[0][1] is nono.UNKNOWN
    nono.empty(0, 1)
    assert nono.board[0][1] is nono.EMPTY


def test_clear():
    rows = [[1], [1]]
    cols = [[1], [1]]

    nono = n.Nonogram(rows, cols)
    nono.fill(0, 1)
    assert nono.board[0][1] is nono.FILLED
    nono.clear(0, 1)
    assert nono.board[0][1] is nono.UNKNOWN

    nono.empty(0, 1)
    assert nono.board[0][1] is nono.EMPTY
    nono.clear(0, 1)
    assert nono.board[0][1] is nono.UNKNOWN


def test_getrow():
    rows = [[1], [1], [1]]
    cols = [[1], [1], [1]]

    nono = n.Nonogram(rows, cols)

    u = nono.UNKNOWN
    f = nono.FILLED

    # -*-
    nono.fill(0, 1)
    # *-*
    nono.fill(1, 0)
    nono.fill(1, 2)
    # --*
    nono.fill(2, 2)

    assert nono.get_row(0) == [u, f, u]
    assert nono.get_row(1) == [f, u, f]
    assert nono.get_row(2) == [u, u, f]


def test_saverow():
    rows = [[1], [1], [1]]
    cols = [[1], [1], [1]]

    nono = n.Nonogram(rows, cols)

    u = nono.UNKNOWN
    f = nono.FILLED

    # -*-
    nono.save_row(0, [u, f, u])
    # *-*
    nono.save_row(1, [f, u, f])
    # --*
    nono.save_row(2, [u, u, f])

    assert nono.get_row(0) == [u, f, u]
    assert nono.get_row(1) == [f, u, f]
    assert nono.get_row(2) == [u, u, f]


def test_getcol():
    rows = [[1], [1], [1]]
    cols = [[1], [1], [1]]

    nono = n.Nonogram(rows, cols)

    u = nono.UNKNOWN
    f = nono.FILLED

    # -*-
    # *-*
    # --*
    nono.fill(0, 1)
    nono.fill(1, 0)
    nono.fill(1, 2)
    nono.fill(2, 2)

    assert nono.get_column(0) == [u, f, u]
    assert nono.get_column(1) == [f, u, u]
    assert nono.get_column(2) == [u, f, f]


def test_savecol():
    rows = [[1], [1], [1]]
    cols = [[1], [1], [1]]

    nono = n.Nonogram(rows, cols)

    u = nono.UNKNOWN
    f = nono.FILLED

    # -*-
    # *-*
    # --*
    nono.save_col(0, [u, f, u])
    nono.save_col(1, [f, u, u])
    nono.save_col(2, [u, f, f])

    assert nono.get_column(0) == [u, f, u]
    assert nono.get_column(1) == [f, u, u]
    assert nono.get_column(2) == [u, f, f]


def test_heart_print():
    rows = [[1, 1], [5], [5], [3], [1]]
    cols = [[2], [4], [4], [4], [2]]

    nono = n.Nonogram(rows, cols)
    e = nono.EMPTY
    f = nono.FILLED

    answer = [[e, f, e, f, e], [f, f, f, f, f], [f, f, f, f, f], [e, f, f, f, e], [e, e, f, e, e]]
    for i, r in enumerate(answer):
        nono.save_row(i, r)

    assert str(nono) == heart
