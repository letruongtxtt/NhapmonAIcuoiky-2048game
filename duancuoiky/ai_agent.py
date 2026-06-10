import numpy as np
import math
import game_logic
from config import SCORE_MATRIX, SEARCH_DEPTH, MODE_EXPECTIMAX, MODE_MINIMAX, MODE_GREEDY

def evaluate_board(matrix):
    """Hàm lượng giá Heuristic đa tiêu chí"""
    if not game_logic.has_moves(matrix):
        return -float('inf')
    
    weight_score = np.sum(matrix * SCORE_MATRIX)
    empty_cells = len(list(zip(*np.where(matrix == 0))))
    empty_score = empty_cells * 1000
    
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if matrix[i, j] != 0:
                val = math.log2(matrix[i, j])
                if i + 1 < 4 and matrix[i+1, j] != 0:
                    smoothness -= abs(val - math.log2(matrix[i+1, j]))
                if j + 1 < 4 and matrix[i, j+1] != 0:
                    smoothness -= abs(val - math.log2(matrix[i, j+1]))

    return weight_score + empty_score + (smoothness * 200)

# --- THUẬT TOÁN 1: EXPECTIMAX ---
def expectimax(matrix, depth, is_ai_turn):
    if depth == 0 or (not is_ai_turn and not game_logic.has_moves(matrix)):
        return evaluate_board(matrix)

    if is_ai_turn:
        max_val = -float('inf')
        for d in range(4):
            next_matrix, _ = game_logic.get_move_result(matrix, d) # Thêm , _ tại đây
            if not np.array_equal(matrix, next_matrix):
                val = expectimax(next_matrix, depth - 1, False)
                max_val = max(max_val, val)
        return max_val
    else:
        empty_cells = list(zip(*np.where(matrix == 0)))
        if not empty_cells:
            return evaluate_board(matrix)
        total_val = 0
        cells_to_check = empty_cells[:4]
        for (r, c) in cells_to_check:
            m2 = matrix.copy()
            m2[r, c] = 2
            total_val += 0.9 * expectimax(m2, depth - 1, True)
            m4 = matrix.copy()
            m4[r, c] = 4
            total_val += 0.1 * expectimax(m4, depth - 1, True)
        return total_val / len(cells_to_check)

# --- THUẬT TOÁN 2: MINIMAX TRUYỀN THỐNG ---
def minimax(matrix, depth, is_ai_turn):
    if depth == 0 or (not is_ai_turn and not game_logic.has_moves(matrix)):
        return evaluate_board(matrix)

    if is_ai_turn:
        max_val = -float('inf')
        for d in range(4):
            next_matrix, _ = game_logic.get_move_result(matrix, d) # Thêm , _ tại đây
            if not np.array_equal(matrix, next_matrix):
                val = minimax(next_matrix, depth - 1, False)
                max_val = max(max_val, val)
        return max_val
    else:
        # TẦNG MIN: Giả định máy tính cố tình chọn ô trống và sinh số 2/4 tệ nhất cho người chơi
        min_val = float('inf')
        empty_cells = list(zip(*np.where(matrix == 0)))
        if not empty_cells:
            return evaluate_board(matrix)
        
        cells_to_check = empty_cells[:4]
        for (r, c) in cells_to_check:
            # Máy thả số 2
            m2 = matrix.copy()
            m2[r, c] = 2
            val2 = minimax(m2, depth - 1, True)
            
            # Máy thả số 4
            m4 = matrix.copy()
            m4[r, c] = 4
            val4 = minimax(m4, depth - 1, True)
            
            min_val = min(min_val, val2, val4)
        return min_val

# --- HÀM ĐIỀU PHỐI LẤY BƯỚC ĐI TỐI ƯU ---
def get_best_move(matrix, mode):
    best_score = -float('inf')
    best_move = -1
    
    if mode == MODE_GREEDY:
        for d in range(4):
            next_matrix, _ = game_logic.get_move_result(matrix, d) # Thêm , _ tại đây
            if not np.array_equal(matrix, next_matrix):
                score = evaluate_board(next_matrix)
                if score > best_score:
                    best_score = score
                    best_move = d
        return best_move

    for d in range(4):
        next_matrix, _ = game_logic.get_move_result(matrix, d) # Thêm , _ tại đây
        if not np.array_equal(matrix, next_matrix):
            if mode == MODE_EXPECTIMAX:
                score = expectimax(next_matrix, SEARCH_DEPTH - 1, False)
            elif mode == MODE_MINIMAX:
                score = minimax(next_matrix, SEARCH_DEPTH - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = d
    return best_move