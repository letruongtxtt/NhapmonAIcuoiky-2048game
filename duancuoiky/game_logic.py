# =====================================================================
# FILE: game_logic.py
# =====================================================================
import random
import numpy as np
from config import GRID_SIZE

def slide_and_merge(row):
    """Trượt, gộp các ô và tính điểm số thu được từ lượt gộp đó"""
    non_zero = row[row != 0]
    new_row = []
    score_gained = 0  # Điểm ghi được của hàng này
    skip = False
    
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
            merged_val = non_zero[i] * 2
            new_row.append(merged_val)
            score_gained += merged_val  # Cộng điểm bằng giá trị ô sau gộp
            skip = True
        else:
            new_row.append(non_zero[i])
            
    new_row += [0] * (GRID_SIZE - len(new_row))
    return np.array(new_row), score_gained

def move_left(matrix):
    new_matrix = np.zeros_like(matrix)
    total_score = 0
    for i in range(GRID_SIZE):
        row, score = slide_and_merge(matrix[i, :])
        new_matrix[i, :] = row
        total_score += score
    return new_matrix, total_score

def move_right(matrix):
    new_matrix = np.zeros_like(matrix)
    total_score = 0
    for i in range(GRID_SIZE):
        row, score = slide_and_merge(matrix[i, ::-1])
        new_matrix[i, : ] = row[::-1]
        total_score += score
    return new_matrix, total_score

def move_up(matrix):
    flipped, score = move_left(matrix.T)
    return flipped.T, score

def move_down(matrix):
    flipped, score = move_right(matrix.T)
    return flipped.T, score

def get_move_result(matrix, direction):
    """Trả về ma trận mới và điểm số thưởng thêm"""
    if direction == 0: return move_up(matrix)
    if direction == 1: return move_right(matrix)
    if direction == 2: return move_down(matrix)
    if direction == 3: return move_left(matrix)
    return matrix, 0

def has_moves(matrix):
    for d in range(4):
        next_matrix, _ = get_move_result(matrix, d)
        if not np.array_equal(matrix, next_matrix):
            return True
    return False

def add_new_tile(matrix):
    empty_cells = list(zip(*np.where(matrix == 0)))
    if empty_cells:
        r, c = random.choice(empty_cells)
        matrix[r, c] = 4 if random.random() < 0.1 else 2
    return matrix