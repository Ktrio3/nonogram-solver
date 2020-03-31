from typing import List


class OutOfBoundsHints(Exception):
    def __init___(self, *args):
        Exception.__init__(self, "The hints for {0} {1} sum out of bounds ({2}/{3})".format(args))


class Nonogram:
    """Represents a nonogram game board"""
    UNKNOWN = None
    EMPTY = 0
    FILLED = 1

    def __str__(self):
        """Return the board as a string."""
        s = ""
        for row in self.board:
            s += "+---" * self.len_row + "+\n"
            for x in row:
                s += "|"
                if x is self.FILLED:
                    s += "███"
                elif x is self.EMPTY:
                    s += " x "
                else:
                    s += "   "
            s += "|\n"
        s += "+---" * self.len_row + "+"
        return s

    def verify(self):
        for i in range(self.num_rows):
            row = self.get_row(i)
            hints = self.rows[i]

            if not self.verify_row(row, hints):
                return False

        for i in range(self.num_cols):
            row = self.get_column(i)
            hints = self.columns[i]

            if not self.verify_row(row, hints):
                return False
        return True

    def verify_row(self, row, hints):
        current_hint = 0
        i = 0
        while i < len(row):
            if row[i] == self.EMPTY:
                i += 1
            elif row[i] == self.FILLED:
                if current_hint == len(hints):
                    return False  # Should have already been done
                j = 0
                while i + j < len(row) and row[i + j] == self.FILLED:
                    j += 1
                if i + j < len(row) and row[i + j] == self.UNKNOWN:
                    return False
                if j == hints[current_hint]:
                    current_hint += 1
                else:
                    return False
                i += j
            else:
                return False
        if current_hint != len(hints):
            return False
        return True

    def __init__(s, rows: List[List[int]],
                 columns: List[List[int]], debug: bool = False):
        """Initialize a gameboard from a list of row hints and col hints"""
        s.rows = rows
        s.columns = columns

        s.debug = debug

        s.num_rows = len(rows)
        s.num_cols = len(columns)

        # Length of columns is the length of a row and vice versa
        s.len_row = len(columns)
        s.len_col = len(rows)

        if s.debug:
            print("Creating {0}x{1} board".format(s.len_row, s.len_col))

        # Check that rows and columns are valid
        for n, row in enumerate(s.rows):
            if sum(row) > s.len_row:
                raise OutOfBoundsHints("row", n, sum(row), s.len_row)
        for n, col in enumerate(s.columns):
            if sum(col) > s.len_col:
                raise OutOfBoundsHints("column", n, sum(col), s.len_col)

        # Init board
        s.board = [[s.UNKNOWN] * s.num_cols for _ in range(s.num_rows)]

    def fill(self, x, y):
        """Marks coordinate (x,y) as filled"""
        if self.debug:
            print("Marked ({0}, {1}) as filled".format(x, y))
        self.board[x][y] = self.FILLED

    def clear(self, x, y):
        """Marks coordinate (x,y) as unknown"""
        if self.debug:
            print("Marked ({0}, {1}) as unknown".format(x, y))
        self.board[x][y] = self.UNKNOWN

    def empty(self, x, y):
        """Marks coordinate (x,y) as empty"""
        if self.debug:
            print("Marked ({0}, {1}) as empty".format(x, y))
        self.board[x][y] = self.EMPTY

    def get_row(self, index):
        """Gets the i-th row from the board"""
        return self.board[index]  # Simple, since we store in rows

    def get_column(self, index):
        """Gets the i-th column from the board"""
        # Unlike row, need to create a new list and get values
        ret = []
        for row in self.board:
            ret.append(row[index])
        return ret

    def save_row(self, index, row):
        """Saves a row to the board"""
        self.board[index] = row  # Again, simple

    def save_col(self, index, col):
        """Saves a row to the board"""
        # Unlike row, need to store into appropriate locations
        for n, row in enumerate(self.board):
            row[index] = col[n]
