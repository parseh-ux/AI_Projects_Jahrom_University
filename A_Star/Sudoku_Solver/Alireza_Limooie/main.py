import csv
import numpy as np
import time
from heapq import heappush, heappop


start_time = time.perf_counter()


class SudokuTable:
    def __init__(self, st, g, h, f):
        self.st = st
        self.g = g
        self.h = h
        self.f = f


def copy(state, sg, sh):
    return SudokuTable(state.copy(), sg, sh, sg + sh)


def heuristic(sudoku):
    return np.count_nonzero(sudoku == 0)


def get_empty_cells(matrix):
    return [(i, j) for i in range(9) for j in range(9) if matrix[i][j] == 0]


def find_best(sudoku, indices):
    # Compute sets of possible values for each row, column, and subgrid
    rows = [set(range(1, 10)) - set(row) for row in sudoku]
    cols = [set(range(1, 10)) - set(col) for col in zip(*sudoku)]
    sub_grids = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = set()
            for k in range(3):
                for ll in range(3):
                    subgrid.add(sudoku[i + k][j + ll])
            sub_grids.append(set(range(1, 10)) - subgrid)

    best_cells = []
    for i, j in indices:
        # Compute the number of possible values for the current cell
        empty_cells = len(rows[i] & cols[j] & sub_grids[(i // 3) * 3 + j // 3])
        heappush(best_cells, (empty_cells, (i, j)))

    # Return the cell with the fewest possible values
    return heappop(best_cells)[1]


def possible_values(sudoku, ini, inj):
    possible_values_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # Compute possible values in row ini
    row_values = set(sudoku[ini, :])
    possible_values_set -= row_values

    # Compute possible values in column inj
    col_values = set(sudoku[:, inj])
    possible_values_set -= col_values

    # Compute possible values in subgrid containing cell (ini, inj)
    for sl in ss:
        if (ini, inj) in sl:
            for co in sl:
                element = sudoku[co[0]][co[1]]
                if element != 0 and element in possible_values_set:
                    possible_values_set = set(possible_values_set) - {element}

    return possible_values_set


def sudoku_solver(state):
    fringe = [state]
    pop_from_fringe = 0

    while True:
        if not fringe:
            print("lost!")
            return state.st

        # Sort the states in the fringe by their f value
        fringe.sort(key=lambda x: x.f, reverse=True)
        current_state = fringe.pop()
        pop_from_fringe += 1

        if not(np.count_nonzero(current_state.st == 0)):
            print("Found it!")
            return current_state.st

        # Find the cell with the fewest possible values
        i, j = find_best(current_state.st, get_empty_cells(current_state.st))
        # print(find_best(current_state.st, get_empty_cells(current_state.st)))

        # Try each possible value for the cell and add the resulting states to the fringe
        for k in possible_values(current_state.st, i, j):
            current_state.st[i][j] = k
            fringe.append(copy(current_state.st, current_state.g + 1, current_state.h - 1))


ss = (((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
      ((0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)),
      ((0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)),
      ((3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)),
      ((3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)),
      ((3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)),
      ((6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)),
      ((6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)),
      ((6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)))

# Read input matrix from file
with open('evil.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    input_matrix = [int(val) for row in reader for val in row]

# Reshape input matrix as a 9x9 numpy array
input_matrix = np.array(input_matrix).reshape((9, 9))

# Create initial state and write output to file
start_state = SudokuTable(input_matrix, 0, np.inf, np.inf)

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    start_state.h = heuristic(start_state.st)
    writer.writerows(sudoku_solver(start_state))

# Print execution time
print("--- %s seconds ---" % (time.perf_counter() - start_time))
