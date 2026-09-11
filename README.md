# Sudoku Solver

**[Open the solver in your browser →](https://aiden-azarnoush.github.io/sudoku_solver/)**

Enter the clues, press **Solve**. Backtracking with constraint propagation,
running entirely in your browser — nothing to install, nothing sent to a
server. A Python version (command line and desktop GUI) lives in
[`python/`](python/) for anyone who wants to run or study the code locally.

Originally written in Pascal in 2010 at Sharif University of Technology,
converted to Python in 2024, and to a web app in 2026.

<p align="center">
<img src="figures/solving.gif" width="340" alt="Solver filling in the grid">
</p>

## Using the web app

1. Press **Edit**. Click a cell — it turns yellow — then enter its digit
   with the keypad on the left or your keyboard. Arrow keys move around,
   Backspace clears a cell. Press **Done** when the clues are in.
2. Press **Solve**. The solution fills in **green**; your clues stay black.

> [!TIP]
> **Load example** puts in a classic puzzle so you can try it in two clicks.
> **Clear grid** starts over.

> [!NOTE]
> The solver tells you, on the right, when a puzzle cannot be solved and
> why: clues that repeat a digit in a row, column, or box are highlighted
> in red; fewer than 17 clues (or any set of clues that admits more than
> one solution) is reported as "not enough information"; and a
> conflict-free set of clues with no valid completion is reported as
> unsolvable.

## Run it locally (Python)

```bash
cd python
python sudoku_solver.py sudoku.txt      # command line: prints and saves the solution
python sudoku_gui.py                    # desktop GUI: type or load a puzzle, solve, save PNG
```

The text format is nine rows of nine digits, `0` for empty cells (the
compact `530070000` form is also accepted). See `python/sudoku.txt`.

> [!WARNING]
> The desktop GUI uses `tkinter`, which ships with the standard Python
> installers on macOS and Windows; on some Linux distributions it is a
> separate package (`sudo apt install python3-tk`).

## How it works

**Constraint propagation.** Three families of sets track which digits
remain available in each row, column, and 3×3 box, so checking whether a
digit can go in a cell is three set lookups rather than a scan of the
board.

**Backtracking.** The solver picks the empty cell with the fewest
candidates (most-constrained first, which prunes the search dramatically),
tries each candidate, recurses, and undoes the placement if the branch
dies. Placements and removals keep the three set families exactly in sync,
so the state after a backtrack is identical to the state before the
attempt.

**Uniqueness.** The web version counts solutions up to two. That is how it
distinguishes a well-posed puzzle from one with too few clues without
enumerating every completion.

Solving the classic example takes 1,959 place/backtrack steps to settle
its 51 empty cells; the animation above replays the placements that
survive.

## Files

```
index.html          the web app (GitHub Pages serves this)
python/
  sudoku_solver.py  solver class + command-line interface
  sudoku_gui.py     tkinter GUI
  sudoku.txt        example puzzle
figures/            images used in this README
```

## License

MIT — see [LICENSE](LICENSE).

---

*Dedicated to my beloved mother, Simin Nematpour.*
