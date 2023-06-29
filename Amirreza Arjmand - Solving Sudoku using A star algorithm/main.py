import sys
import os
import time
from heapq import heappop, heappush

class SudokuNode:
    '''
    Representation of each state of the Sudoku game.
    '''

    def __init__(self, state, g=0, h=None):
        self.state = state
        self.g = g
        self.heuristic = h

    @property
    def h(self):
        '''
        Heuristic function which counts the number
        of empty cells in a given state and caches it
        for faster lookups later.
        '''
        if self.heuristic is None:
            self.heuristic = self.flatten().count(0)

        return self.heuristic

    @property
    def f(self):
        '''
        Returns the summation of h and g and caches it 
        for faster lookups later.
        '''
        return self.g + self.h

    def flatten(self):
        return [i for r in self.state for i in r]

    def row(self, i):
        return self.state[i]

    def column(self, j):
        return [r[j] for r in self.state]

    def box(self, k):
        '''
        Returns a box from a specific state.
        The boxes are numbered in the following manner.
        ┏━━━┳━━━┳━━━┓
        ┃ 0 ┃ 1 ┃ 2 ┃
        ┣━━━╋━━━╋━━━┫
        ┃ 3 ┃ 4 ┃ 5 ┃
        ┣━━━╋━━━╋━━━┫
        ┃ 6 ┃ 7 ┃ 8 ┃
        ┗━━━┻━━━┻━━━┛
        '''
        cl, cu = (k % 3) * 3, (k % 3) * 3 + 3
        rl, ru = (k // 3) * 3, (k // 3) * 3 + 3

        return [self.state[i][cl:cu] for i in range(rl, ru)]

    def flattened_box(self, k):
        return [i for r in self.box(k) for i in r]
    
    def empty_cells(self):
        res = []
        for i in range(9):
            for j in range(9):
                if self.state[i][j] == 0:
                    res.append((i, j))

        return res

    def copy(self):
        return SudokuNode([r[:] for r in self.state], self.g, self.h)

    def __repr__(self):
        res = ""
        for r in self.state:
            res += str(r) + '\n'

        return res

    def __str__(self):
        '''
        Prints out a specific state in a nice format.
        '''
        output = ""
        output += f"┏{7 * '━'}┳{7 * '━'}┳{7 * '━'}┓\n"
        for i in range(9):
            if i == 3 or i == 6:
                output += f"┣{7 * '━'}╋{7 * '━'}╋{7 * '━'}┫\n"

            output += "┃ "
            for j in range(9):
                if j == 3 or j == 6:
                    output += "┃ "
                if self.state[i][j] == 0:
                    output += "  "
                else:
                    output += f"{self.state[i][j]} "

            output += "┃\n"

        output += f"┗{7 * '━'}┻{7 * '━'}┻{7 * '━'}┛\n"

        return output


class Frontier:
    '''
    Frontier/Fringe list for the A* algorithm.
    '''

    def __init__(self):
        self.frontier = []

    def empty(self):
        return len(self.frontier) == 0

    def add(self, x):
        self.frontier.append(x)

    def remove(self):
        self.frontier.sort(key=lambda x: x.f, reverse=True)
        return self.frontier.pop()

    def len(self):
        return len(self.frontier)

    def __str__(self):
        return str(self.frontier)


class SolveSudoku:
    '''
    Solve a Sudoku game from a given file.
    '''

    def __init__(self, fpath):
        self.sud = []
        with open(fpath) as f:
            for l in f:
                self.sud.append(list(map(int, l.split())))

        self.sud = SudokuNode(self.sud)

    def goal_test(self):
        '''
        Goal test:
        If there are no empty cells in the board then we have solved the game.
        '''
        return not 0 in self.sud.flatten()

    def find_next_empty(self):
        '''
        Find the next empty cell in an unsolved board of Sudoku.
        The strategy is to find the cell that we think can has the minimum
        number of possible values.
        Return None if there aren't any empty cells left.
        '''
        rows = []
        columns = []
        boxes = []

        for i in range(9):
            rows.append(set(range(10)) - set(self.sud.row(i)))
            columns.append(set(range(10)) - set(self.sud.column(i))) 
            boxes.append(set(range(10)) - set(self.sud.flattened_box(i)))

        q = []
        for i, j in self.sud.empty_cells():
            possible_values = len(rows[i] & columns[j] & boxes[(i // 3) * 3 + j // 3])
            heappush(q, (possible_values, (i, j)))

        if q:
            return heappop(q)[1]
        

    def valid_move(self, cell, n):
        '''
        Check whether a move can cause any conflict in an uncompleted Sudoku game.
        '''
        i, j = cell

        if n in self.sud.row(i):
            return False
        if n in self.sud.column(j):
            return False
        if n in self.sud.flattened_box((i // 3) * 3 + j // 3):
            return False

        return True

    def solve(self):
        '''
        Solve sudoku game using A* algorithm.
        Explore possible moves until you reach the answer.
        Return False if there are no answerers and True otherwise.
        '''
        frontier = Frontier()
        frontier.add(self.sud)

        while True:
            if frontier.empty():
                return False

            self.sud = frontier.remove()
            next_empty = self.find_next_empty()

            # Goal test.
            if next_empty is None:
                return True
            
            for i in range(1, 10):
                # Fill the next empty cell only with eligible values, the values that
                # do not cause any conflict in the game.
                if self.valid_move(next_empty, i):
                    node = self.sud.copy()

                    node.state[next_empty[0]][next_empty[1]] = i
                    node.g += 1
                    node.heuristic -= 1

                    frontier.add(node)

    def print(self, fpath=None):
        '''
        Print the Sudoku game either to the terminal or a file.
        '''
        if fpath is not None:
            with open(fpath, "w", encoding="utf-8") as f:
                print(self.sud, file=f)
        else:
            print(self.sud)

if len(sys.argv) != 2:
    sys.exit("specify the puzzle name as the first command line argument.")

puzzle_name = sys.argv[1]

s = SolveSudoku(puzzle_name)
print("initial state: ")
s.print()

start = time.perf_counter()
if s.solve():
    print("solution: ")
    s.print()
    s.print(f"{os.path.splitext(sys.argv[1])[0]}.out")
else:
    print("no solution")

finish = time.perf_counter()

print(f"took {finish - start:.7f} seconds.")
