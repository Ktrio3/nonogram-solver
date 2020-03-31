from nonogram import Nonogram
from typing import List


class Solver:
    UNKNOWN = None
    EMPTY = 0
    FILLED = 1

    def __init__(self, n: Nonogram = None, show_steps: bool = False):
        if n is not None:
            self.set_nonogram(n)
        else:
            self.nono = None
        self.show_steps = show_steps

    def set_nonogram(self, n: Nonogram):
            self.nono = n
            self.num_rows = n.num_rows
            self.num_cols = n.num_cols

            self.solved_rows = [False] * self.num_rows
            self.solved_cols = [False] * self.num_cols

    def repair(self, row, trimmed, start):
        for i in range(len(trimmed)):
            row[start + i] = trimmed[i]
        return row

    def solve(self):
        self.initial_overlaps()
        if self.show_steps:
            print("Calculating overlap")
            print(self.nono)
        self.check_all_completes()
        if self.show_steps:
            print("Checking for completed rows and columns")
            print(self.nono)

        updated = True

        while (False in self.solved_rows or False in self.solved_cols) and updated:
            updated = False
            for i in range(self.num_rows):
                if self.solved_rows[i]:
                    continue
                row = self.nono.get_row(i)
                row, completed, update = self.check_complete(row, self.nono.rows[i])
                if completed:
                    updated = True
                    self.solved_rows[i] = True
                    self.nono.save_row(i, row)
                    if self.show_steps and update:
                        print("Completing row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, start, hints = self.trim(row, self.nono.rows[i])
                trimmed, update = self.check_edges(trimmed, hints)
                if update:
                    updated = True
                    row = self.repair(row, trimmed, start)
                    self.nono.save_row(i, row)
                    if self.show_steps:
                        print("Filled edges of row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.complete_max(trimmed, hints)
                if update:
                    updated = True
                    row = self.repair(row, trimmed, start)
                    self.nono.save_row(i, row)
                    if self.show_steps:
                        print("Completed the largest hint in row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.first_gaps(trimmed, hints)
                if update:
                    updated = True
                    row = self.repair(row, trimmed, start)
                    self.nono.save_row(i, row)
                    if self.show_steps:
                        print("Removed small gaps at the start of row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.last_gaps(trimmed, hints)
                if update:
                    updated = True
                    row = self.repair(row, trimmed, start)
                    self.nono.save_row(i, row)
                    if self.show_steps:
                        print("Removed small gaps at the end of row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.remove_smalls(trimmed, hints)
                if update:
                    updated = True
                    row = self.repair(row, trimmed, start)
                    self.nono.save_row(i, row)
                    if self.show_steps:
                        print("Removed too small gaps from row {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.overlap(trimmed, hints)
                if update:
                    updated = True
                    self.nono.save_row(i, self.repair(row, trimmed, start))
                    if self.show_steps:
                        print("Updating row {0}".format(i))
                        print(self.nono)
            for i in range(self.num_cols):
                if self.solved_cols[i]:
                    continue
                col = self.nono.get_column(i)
                col, completed, update = self.check_complete(col, self.nono.columns[i])
                if completed:
                    updated = True
                    self.solved_cols[i] = True
                    self.nono.save_col(i, col)
                    if self.show_steps and update:
                        print("Completing column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, start, hints = self.trim(col, self.nono.columns[i])
                trimmed, update = self.check_edges(trimmed, hints)
                if update:
                    updated = True
                    col = self.repair(col, trimmed, start)
                    self.nono.save_col(i, col)
                    if self.show_steps:
                        print("Filled edges of column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.first_gaps(trimmed, hints)
                if update:
                    updated = True
                    col = self.repair(col, trimmed, start)
                    self.nono.save_col(i, col)
                    if self.show_steps:
                        print("Removed small gaps at the start of column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.last_gaps(trimmed, hints)
                if update:
                    updated = True
                    col = self.repair(col, trimmed, start)
                    self.nono.save_col(i, col)
                    if self.show_steps:
                        print("Removed small gaps at the end of column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.complete_max(trimmed, hints)
                if update:
                    updated = True
                    col = self.repair(col, trimmed, start)
                    self.nono.save_col(i, col)
                    if self.show_steps:
                        print("Completed the largest hint in column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.remove_smalls(trimmed, hints)
                if update:
                    updated = True
                    col = self.repair(col, trimmed, start)
                    self.nono.save_col(i, col)
                    if self.show_steps:
                        print("Removed too small gaps from column {0}".format(i))
                        print(self.nono)
                    continue
                trimmed, update = self.overlap(trimmed, hints)
                if update:
                    updated = True
                    self.nono.save_col(i, self.repair(col, trimmed, start))
                    if self.show_steps:
                        print("Updating column {0}".format(i))
                        print(self.nono)
        if not updated:
            # TODO: Raise exception about incomplete
            print("Puzzle unsolved")

    def first_gaps(self, row, hints):
        i = 0
        updated = False
        while i < len(row):
            if row[i] == self.UNKNOWN:
                size = 0
                while i + size < len(row) and row[i + size] == self.UNKNOWN:
                    size += 1
                if i + size < len(row) and size < hints[0] and row[i + size] == self.EMPTY:
                    # Hole too small. Close it
                    x = 0
                    while x < size:
                        row[i + x] = self.EMPTY
                        x += 1
                    updated = True
                i += size
            elif row[i] == self.FILLED:
                break
            else:
                i += 1
        return row, updated

    def last_gaps(self, row, hints):
        row.reverse()
        hints.reverse()
        row, updated = self.first_gaps(row, hints)
        row.reverse()
        hints.reverse()
        return row, updated

    def complete_max(self, row, hints):
        updated = False
        big = max(hints)

        i = 0
        while i < len(row):
            if row[i] == self.FILLED:
                j = 0
                while row[i + j] == self.FILLED:
                    j += 1
                if j == big and (row[i + j] != self.EMPTY or row[i - 1] != self.EMPTY):
                    row[i + j] = self.EMPTY
                    row[i - 1] = self.EMPTY
                    updated = True
                i += j
            else:
                i += 1

        return row, updated

    def check_edges(self, row, hints):
        updated = False
        if row[0] is self.FILLED:
            for i in range(hints[0]):
                row[i] = self.FILLED
            if hints[0] < len(row):
                row[hints[0]] = self.EMPTY
            updated = True

        if row[-1] is self.FILLED:
            for i in range(hints[-1]):
                row[len(row) - 1 - i] = self.FILLED
            if hints[-1] < len(row):
                row[len(row) - 1 - hints[-1]] = self.EMPTY
            updated = True

        return row, updated

    def remove_smalls(self, row, hints):
        small = min(hints)
        update = False
        i = 0
        while i < len(row):
            if row[i] == self.UNKNOWN and (i == 0 or row[i - 1] == self.EMPTY):
                j = 0
                while i + j < len(row) and row[i + j] == self.UNKNOWN:
                    j += 1
                if j < small and (i + j == len(row) or row[i + j] == self.EMPTY):
                    # Smallest hint cannot fit here, so this gap is impossible
                    for x in range(j):
                        row[i + x] = self.EMPTY
                        update = True
                i += j
            else:
                i += 1
        return row, update

    def trim(self, row, hints):
        """Trims a row by returning only unsolved sections and hints"""
        i = 0
        hint_start = 0

        # Trim left
        while i < len(row):
            if row[i] == self.EMPTY:
                i += 1
            if row[i] == self.FILLED:
                length = hints[hint_start]
                # Note that we do not count the first hint as fulfilled unless it
                # has an empty after it. That should be fixed later
                if all(map(lambda x: x == self.FILLED, row[i:i + length])) and (i + length == len(row) or row[i + length] == self.EMPTY):
                    # Hint completed
                    hint_start += 1
                    i += length
                    continue
                else:
                    break  # Not the full first hint
            if row[i] == self.UNKNOWN:
                break
        if i == len(row):
            # TODO: Raise exception
            print("trim called on completed row")
            exit(-1)

        j = len(row) - 1
        hint_end = len(hints) - 1
        while j > -1 and j > i:
            if row[j] == self.EMPTY:
                j -= 1
            if row[j] == self.FILLED:
                length = hints[hint_end]
                # Note that we do not count the first hint as fulfilled unless it
                # has an empty after it. That should be fixed later
                if all(map(lambda x: x == self.FILLED, row[j - length + 1:j + 1])) and row[j - length] == self.EMPTY:
                    # Hint completed
                    hint_end -= 1
                    j -= length
                else:
                    break  # Not the full first hint
            if row[j] == self.UNKNOWN:
                break

        if j == -1:
            # TODO: Raise exception
            print("trim called on completed row")
            exit(-1)

        return row[i:j + 1], i, hints[hint_start:hint_end + 1]

    def check_all_completes(self):
        for i in range(self.num_rows):
            row = self.nono.get_row(i)
            (row, solved, _) = self.check_complete(row, self.nono.rows[i])
            self.solved_rows[i] = solved
            if solved:
                self.nono.save_row(i, row)
        for i in range(self.num_cols):
            col = self.nono.get_column(i)
            (col, solved, _) = self.check_complete(col, self.nono.columns[i])
            self.solved_cols[i] = solved
            if solved:
                self.nono.save_col(i, col)

    def check_complete(self, row: List[int], hints: List[int]):
        """Check if a row is complete. If so, fills in blanks with empties"""
        total_filled = sum(filter(None, row))
        total_needed = sum(hints)
        completed = False
        updated = False

        if total_filled > total_needed:
            # TODO: Raise exception
            print("Reached invalid state")
            exit(-1)

        if total_filled == total_needed:
            completed = True
            for i in range(len(row)):
                if row[i] == self.UNKNOWN:
                    row[i] = self.EMPTY
                    updated = True

        return row, completed, updated

    def initial_overlaps(self):
        for i in range(self.num_rows):
            row = self.nono.get_row(i)
            (row, update) = self.overlap(row, self.nono.rows[i])

            if update:
                self.nono.save_row(i, row)
        for i in range(self.num_cols):
            col = self.nono.get_column(i)
            (col, update) = self.overlap(col, self.nono.columns[i])
            if update:
                self.nono.save_col(i, col)

    def overlap(self, row, hints):
        total_filled = sum(hints) + (len(hints) - 1)
        length = len(row)
        uncertainty = length - total_filled
        updated = False

        if total_filled is 0:
            # Make the whole row empty
            row = [self.EMPTY for i in range(length)]
            return row, True

        current = 0
        for h in hints:
            fill = h - uncertainty
            if fill <= 0:
                current += h + 1  # Just skip ahead, no knowledge gained here
                continue
            current += uncertainty  # Skip uncertain boxes
            for _ in range(fill):
                if row[current] != self.FILLED:
                    updated = True
                row[current] = self.FILLED
                current += 1
            current += 1  # Move to first possible box for next hint

        return row, updated
