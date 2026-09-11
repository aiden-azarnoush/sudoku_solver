'''
Author: Aiden Azarnoush
Dedicated to my mother, my true love, Simin Nematpour
School: Sharif University of Technology
Note:
Originally written in Pascal in 2010
Converted to Python in 2024
'''

import numpy as np
import os


class SudokuSolver:
    def __init__(self):
        # Initialize the Sudoku board, sets for available numbers, and list of empty cells
        self.board = np.zeros((9, 9), dtype=int)
        self.given = np.zeros((9, 9), dtype=bool)   # which cells were clues
        self.rows = [set(range(1, 10)) for _ in range(9)]
        self.cols = [set(range(1, 10)) for _ in range(9)]
        self.blocks = [set(range(1, 10)) for _ in range(9)]
        self.empty_cells = []

    def get_block_index(self, row, col):
        # Calculate the block index based on the row and column
        return (row // 3) * 3 + (col // 3)

    def load_from_array(self, grid):
        """Initialize from a 9x9 array-like of ints (0 = empty).

        Raises ValueError if the clues themselves conflict.
        """
        self.__init__()
        grid = np.asarray(grid, dtype=int)
        if grid.shape != (9, 9):
            raise ValueError("Grid must be 9x9.")
        for i in range(9):
            for j in range(9):
                num = grid[i, j]
                if not 0 <= num <= 9:
                    raise ValueError(f"Cell ({i+1},{j+1}) must be 0-9, got {num}.")
                if num != 0:
                    if not self.is_valid(i, j, num):
                        raise ValueError(
                            f"Conflicting clue {num} at row {i+1}, column {j+1}.")
                    self.place_number(i, j, num)
                    self.given[i, j] = True
                else:
                    self.empty_cells.append((i, j))

    def load_sudoku(self, filename):
        # Load the Sudoku puzzle from a file (0 = empty cell).
        # Absolute paths are used as-is; bare names resolve next to this script.
        if os.path.isabs(filename) or os.path.exists(filename):
            full_path = filename
        else:
            full_path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"No such file or directory: '{full_path}'")

        with open(full_path, 'r') as file:
            lines = [ln for ln in (l.strip() for l in file) if ln]
        if len(lines) != 9:
            raise ValueError("Input file must contain exactly 9 lines.")
        grid = []
        for i, ln in enumerate(lines):
            parts = ln.split()
            if len(parts) == 1 and len(parts[0]) == 9:
                parts = list(parts[0])          # also accept 530070000 style
            if len(parts) != 9:
                raise ValueError(f"Line {i + 1} must contain exactly 9 integers.")
            grid.append([int(p) for p in parts])
        self.load_from_array(grid)

    def is_valid(self, row, col, num):
        # Check if placing a number is valid by checking the row, column, and block sets
        block_idx = self.get_block_index(row, col)
        return (num in self.rows[row] and num in self.cols[col]
                and num in self.blocks[block_idx])

    def place_number(self, row, col, num):
        # Place a number on the board and update the row, column, and block sets
        self.board[row][col] = num
        self.rows[row].remove(num)
        self.cols[col].remove(num)
        self.blocks[self.get_block_index(row, col)].remove(num)

    def remove_number(self, row, col, num):
        # Remove a number from the board and update the row, column, and block sets
        self.board[row][col] = 0
        self.rows[row].add(num)
        self.cols[col].add(num)
        self.blocks[self.get_block_index(row, col)].add(num)

    def solve(self):
        # Backtracking solver for the Sudoku puzzle
        if not self.empty_cells:
            return True
        row, col = self.empty_cells.pop()
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.place_number(row, col, num)
                if self.solve():
                    return True
                self.remove_number(row, col, num)
        self.empty_cells.append((row, col))
        return False

    # ------------------------------------------------------------------ output
    def save_sudoku(self, filename):
        """Write the current board to a text file in the standard format."""
        with open(filename, 'w') as f:
            for i in range(9):
                f.write(' '.join(str(self.board[i][j]) for j in range(9)) + '\n')

    def print_sudoku(self):
        for i in range(9):
            print(' '.join(str(self.board[i][j]) for j in range(9)))

    def render(self, filename, title=None):
        """Render the board as a PNG. Clues are black, solved digits blue."""
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(5, 5))
        for k in range(10):
            lw = 2.2 if k % 3 == 0 else 0.7
            ax.plot([k, k], [0, 9], 'k', lw=lw)
            ax.plot([0, 9], [k, k], 'k', lw=lw)
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                if num != 0:
                    ax.text(j + 0.5, 8.5 - i, str(num),
                            ha='center', va='center', fontsize=16,
                            color='black' if self.given[i, j] else 'tab:blue',
                            fontweight='bold' if self.given[i, j] else 'normal')
        ax.set_xlim(-0.05, 9.05)
        ax.set_ylim(-0.05, 9.05)
        ax.set_aspect('equal')
        ax.axis('off')
        if title:
            ax.set_title(title, fontsize=13)
        fig.tight_layout()
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close(fig)


if __name__ == '__main__':
    import sys
    puzzle = sys.argv[1] if len(sys.argv) > 1 else 'sudoku.txt'
    solver = SudokuSolver()
    solver.load_sudoku(puzzle)
    if solver.solve():
        solver.print_sudoku()
        solver.save_sudoku('solution.txt')
        solver.render('solution.png', 'Solution')
        print("\nWrote solution.txt and solution.png")
    else:
        print("No solution exists")
