# Solving Sudoku using A* Algorithm

## General explanation

This implementation uses the A* algorithm to solve a given 9 x 9 Sudoku puzzle. It takes in an initial state from a file, and returns the solution to both stdout and a text file.

The input file is specified as a command line argument after the name of the program e.g. `python main.py evil.txt`. Within it, a 9 x 9 grid is stored, representing the Sudoku game. Each digit in the file is depicts a cell in the puzzle and the digits are separated by a whitespace character. Zeros signify an empty cell in the puzzle.

The output is a text file with the same name as the input file, except for the extension which is `.out`. The output is also printed to the stdout. The job of this program is to fill in the zeros with an appropriate digit, or in other words, solve the puzzle.

As for the details of the A* algorithm, each configuration of the board is considered as state in the search graph, and a transition is filling in an empty cell (i, j) with a specific value k. Then there is a frontier/fringe queue which always returns the Sudoku state that it thinks is closest to the answer (the one that has the smallest f = g + h). g is incremented every time that a transition is made (an empty cell is filled), and the heuristic is the number of the empty cells that are left in a specific state.

We can proclaim that the heuristic is admissable, since we have to make at least n moves to fill n empty cells making h <= h*.

Unlike the rudimentary A* algorithm, here the fringe is only filled with possible states i.e. states that do not cause any conflicts. This makes the search tree much more sparse and the algorithm faster significantly. We could have used the simpler algorithm in which every single cell is filled with digits 1 through 9, and all of the intermediate states are added to the fringe. Then there are states in the fringe in which there can be more than one instance of the same digit in a row, a column, or a 3 x 3 box. Then for every state that we dequeue from the fringe, we ought to check for the number of conflicts to be 0, but in this approach we don't need to check for the conflicts since no state with a conflict is added to the fringe at the first place.

## Optimization techniques used in this implementation

* Only the nodes that do not cause any conflicts are expanded, as specified above.
* Using the above approach, the goal test becomes a very efficient function; Wether or not there are any zeros left in the puzzle.
* When picking the next empty cell to fill, this algorithms picks the cell that has the minimum possible values based on the digits in its row, column, and box.
* Some of the data such as the heuristic of each state is cached for faster lookups.
