"""
Sudoku Solver GUI.

A tkinter front end for SudokuSolver. Two ways to enter a puzzle:

  1. Browse for a puzzle text file (9 lines, 9 numbers each, 0 = empty), or
  2. Type the clues directly into the grid, leaving unknown cells empty.

Pressing "Solve" writes the puzzle to puzzle.txt, solves it, fills the grid
(solved digits shown in blue), and writes solution.txt and solution.png next
to it. Output location follows the loaded file, or the working directory for
manually entered puzzles.

Run:  python sudoku_gui.py
"""

import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

from sudoku_solver import SudokuSolver

BLOCK_BG = ('#ffffff', '#e8eef7')       # alternating 3x3 block backgrounds
CLUE_FG = 'black'
SOLVED_FG = '#1f5fbf'


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        root.title('Sudoku Solver')
        root.resizable(False, False)
        self.out_dir = os.getcwd()

        grid_frame = tk.Frame(root, bg='black', bd=2)
        grid_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        vcmd = (root.register(self._validate), '%P')
        self.cells = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                block = (i // 3 + j // 3) % 2
                e = tk.Entry(grid_frame, width=2, justify='center',
                             font=('Helvetica', 20),
                             bg=BLOCK_BG[block], fg=CLUE_FG,
                             relief='flat', highlightthickness=1,
                             highlightbackground='#999',
                             validate='key', validatecommand=vcmd)
                e.grid(row=i, column=j,
                       padx=(2 if j % 3 == 0 and j else 0, 0),
                       pady=(2 if i % 3 == 0 and i else 0, 0),
                       ipady=4)
                row_entries.append(e)
            self.cells.append(row_entries)

        tk.Button(root, text='Load puzzle…', command=self.load_file
                  ).grid(row=1, column=0, padx=6, pady=(0, 10), sticky='ew')
        tk.Button(root, text='Solve', command=self.solve,
                  font=('Helvetica', 11, 'bold')
                  ).grid(row=1, column=1, padx=6, pady=(0, 10), sticky='ew')
        tk.Button(root, text='Clear', command=self.clear
                  ).grid(row=1, column=2, padx=6, pady=(0, 10), sticky='ew')
        tk.Button(root, text='Quit', command=root.destroy
                  ).grid(row=1, column=3, padx=6, pady=(0, 10), sticky='ew')

        self.status = tk.Label(root, text='Enter clues or load a puzzle file.',
                               anchor='w')
        self.status.grid(row=2, column=0, columnspan=4, sticky='ew',
                         padx=10, pady=(0, 8))

    @staticmethod
    def _validate(proposed):
        return proposed == '' or (proposed.isdigit() and len(proposed) == 1
                                  and proposed != '0')

    # ------------------------------------------------------------------ grid io
    def read_grid(self):
        grid = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                v = self.cells[i][j].get().strip()
                grid[i, j] = int(v) if v else 0
        return grid

    def write_grid(self, board, given):
        for i in range(9):
            for j in range(9):
                e = self.cells[i][j]
                e.delete(0, tk.END)
                if board[i, j] != 0:
                    e.insert(0, str(board[i, j]))
                    e.config(fg=CLUE_FG if given[i, j] else SOLVED_FG)

    def clear(self):
        for row in self.cells:
            for e in row:
                e.delete(0, tk.END)
                e.config(fg=CLUE_FG)
        self.status.config(text='Cleared.')

    # ------------------------------------------------------------------ actions
    def load_file(self):
        path = filedialog.askopenfilename(
            title='Open puzzle file',
            filetypes=[('Text files', '*.txt'), ('All files', '*')])
        if not path:
            return
        solver = SudokuSolver()
        try:
            solver.load_sudoku(path)
        except (ValueError, FileNotFoundError) as err:
            messagebox.showerror('Load error', str(err))
            return
        self.out_dir = os.path.dirname(path)
        self.clear()
        self.write_grid(solver.board, solver.given)
        self.status.config(text=f'Loaded {os.path.basename(path)}.')

    def solve(self):
        solver = SudokuSolver()
        try:
            solver.load_from_array(self.read_grid())
        except ValueError as err:
            messagebox.showerror('Invalid puzzle', str(err))
            return

        puzzle_path = os.path.join(self.out_dir, 'puzzle.txt')
        solver.save_sudoku(puzzle_path)

        if not solver.solve():
            self.status.config(text='No solution exists for this puzzle.')
            messagebox.showinfo('Sudoku Solver', 'No solution exists.')
            return

        self.write_grid(solver.board, solver.given)
        sol_txt = os.path.join(self.out_dir, 'solution.txt')
        sol_png = os.path.join(self.out_dir, 'solution.png')
        solver.save_sudoku(sol_txt)
        try:
            solver.render(sol_png, 'Solution')
            self.status.config(
                text=f'Solved. Wrote puzzle.txt, solution.txt, solution.png.')
        except ImportError:
            self.status.config(
                text='Solved. Wrote puzzle.txt, solution.txt '
                     '(install matplotlib for PNG output).')


if __name__ == '__main__':
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
