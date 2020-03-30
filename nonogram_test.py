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


def test_heart_print():
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

    assert str(nono) == heart
