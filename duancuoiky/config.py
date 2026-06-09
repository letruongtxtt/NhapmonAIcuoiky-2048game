import numpy as np

# Cấu hình kích thước lưới và cửa sổ
GRID_SIZE = 4
SIZE = 450
FONT = ("Verdana", 20, "bold")

# Màu sắc giao diện
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

CELL_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#3c3a32"
}

CELL_TEXT_COLORS = {
    2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
    32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
    512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#f9f6f2"
}

# Ma trận trọng số Heuristic (Snake Pattern) dồn ô lớn vào góc trên-trái
SCORE_MATRIX = np.array([
    [10000, 4000, 1000, 500],
    [200,   400,  600,  800],
    [150,   100,  50,   20],
    [0,     2,    5,    10]
])

SEARCH_DEPTH = 3

# Các chế độ AI
MODE_EXPECTIMAX = "Expectimax"
MODE_MINIMAX = "Minimax"
MODE_GREEDY = "Greedy Heuristic"