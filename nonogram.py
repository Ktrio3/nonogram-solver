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

    def __init__(s, rows: List[List[int]],
                 columns: List[List[int]], debug: bool = False):
        """Initialize a gameboard from a list of row hints and col hints"""
        s.rows = rows
        s.columns = columns

        s.debug = debug

        # Number of columns is the length of a row and vice versa
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
        s.board = [[s.UNKNOWN] * s.len_col for _ in range(s.len_row)]

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
