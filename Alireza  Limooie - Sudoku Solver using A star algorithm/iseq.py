import csv
import numpy as np


def eq(im1, im2):
    for i in range(9):
        for j in range(9):
            if im1[i][j] != im2[i][j]:
                return False
    return True


with open('evil_answer.csv', 'r') as file:
    reader = csv.reader(file)
    input_matrix1 = [int(val) for row in reader for val in row]
input_matrix1 = np.array(input_matrix1).reshape((9, 9))


with open('output.csv', 'r') as file:
    reader = csv.reader(file)
    input_matrix2 = [int(val) for row in reader for val in row]
input_matrix2 = np.array(input_matrix2).reshape((9, 9))


print(eq(input_matrix1, input_matrix2))

