from solver import Solver
from nonogram import Nonogram


def test_overlap_simple():
    s = Solver()
    hints = [4]
    u = s.UNKNOWN
    f = s.FILLED
    row = [u, u, u, u, u]
    answer = [u, f, f, f, u]

    assert s.overlap(row, hints)[0] == answer


def test_overlap_complex():
    s = Solver()
    hints = [3, 2, 4]
    u = s.UNKNOWN
    f = s.FILLED
    row = [u] * 13
    answer = [u, u, f, u, u, u, u, u, u, f, f, u, u]

    assert s.overlap(row, hints)[0] == answer


def test_overlap_full():
    s = Solver()
    hints = [4]
    u = s.UNKNOWN
    f = s.FILLED
    row = [u, u, u, u]
    answer = [f, f, f, f]

    assert s.overlap(row, hints)[0] == answer


def test_overlap_exact():
    s = Solver()
    hints = [4, 2]
    u = s.UNKNOWN
    f = s.FILLED
    e = s.EMPTY
    row = [u] * 7
    answer = [f, f, f, f, u, f, f]

    assert s.overlap(row, hints)[0] == answer


def test_overlap_zero():
    s = Solver()
    hints = [0]
    u = s.UNKNOWN
    f = s.FILLED
    e = s.EMPTY
    row = [u, u, u, u, u]
    answer = [e, e, e, e, e]

    assert s.overlap(row, hints)[0] == answer


def test_overlap_none():
    s = Solver()
    hints = [4]
    u = s.UNKNOWN
    f = s.FILLED
    row = [u, u, u, u, u, u, u, u]
    answer = [u, u, u, u, u, u, u, u]

    assert s.overlap(row, hints)[0] == answer


def test_trim_simple():
    s = Solver()
    hints = [2, 4]
    u = s.UNKNOWN
    e = s.EMPTY
    f = s.FILLED
    row = [e, f, f, e, u, u, u, u]
    trimmed_row = [u, u, u, u]
    trimmed_hints = [4]

    assert s.trim(row, hints) == (trimmed_row, 4, trimmed_hints)


def test_trim_unfinished_right():
    s = Solver()
    hints = [3, 2]
    u = s.UNKNOWN
    e = s.EMPTY
    f = s.FILLED
    row = [f, f, f, e, u, f, f, e]
    trimmed_row = [u, f, f]
    trimmed_hints = [2]

    assert s.trim(row, hints) == (trimmed_row, 4, trimmed_hints)


def test_repair():
    s = Solver()
    hints = [2, 4]
    u = s.UNKNOWN
    e = s.EMPTY
    f = s.FILLED
    row = [e, f, f, e, u, u, u, u]
    answer = [e, f, f, e, f, f, f, f]

    (trimmed_row, start, _) = s.trim(row, hints)
    trimmed_row = [f] * 4

    assert s.repair(row, trimmed_row, start) == answer


def test_trim_finished_right():
    s = Solver()
    hints = [3, 1, 2]
    u = s.UNKNOWN
    e = s.EMPTY
    f = s.FILLED
    row = [f, f, f, e, u, e, f, f]
    trimmed_row = [u]
    trimmed_hints = [1]

    assert s.trim(row, hints) == (trimmed_row, 4, trimmed_hints)


def test_init_overlap():
    rows = [[1, 1], [5], [5], [3], [1]]
    cols = [[2], [4], [4], [4], [2]]

    nono = Nonogram(rows, cols)
    e = nono.EMPTY
    u = nono.UNKNOWN
    f = nono.FILLED
    answer = [[u, u, u, u, u], [f, f, f, f, f], [f, f, f, f, f], [u, f, f, f, u], [u, u, u, u, u]]

    s = Solver(nono)
    s.initial_overlaps()

    assert nono.board == answer
