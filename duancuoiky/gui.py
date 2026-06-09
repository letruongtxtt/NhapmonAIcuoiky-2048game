# =====================================================================
# FILE: gui.py (Phiên bản tích hợp tính năng Auto-Reset & Chuyển thuật toán)
# =====================================================================
import tkinter as tk
from tkinter import ttk
import numpy as np
import game_logic
import ai_agent
from config import (GRID_SIZE, SIZE, BACKGROUND_COLOR_GAME, 
                    BACKGROUND_COLOR_CELL_EMPTY, CELL_COLORS, CELL_TEXT_COLORS,
                    MODE_EXPECTIMAX, MODE_MINIMAX, MODE_GREEDY)

class Game2048GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, bg="#faf8ef")
        self.grid(pady=10, padx=10)
        self.master.title('2048 AI Dashboard - Đồ Án Tốt Nghiệp')
        self.master.configure(bg="#faf8ef")
        
        self.matrix = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.ai_running = False
        self.game_state = "PLAYING" # Các trạng thái: PLAYING, WON, LOST, STUCK
        self.grid_cells = []
        
        self.current_score = 0
        self.best_score = 0

        self.create_header()
        self.init_grid()
        self.create_controls()
        
        self.start_game()
        self.update_grid_cells()

    def create_header(self):
        header_frame = tk.Frame(self, bg="#faf8ef")
        header_frame.grid(row=0, column=0, columnspan=GRID_SIZE, sticky="ew", pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="2048", font=("Verdana", 38, "bold"), fg="#776e65", bg="#faf8ef")
        title_label.pack(side="left", anchor="w")
        
        subtitle_label = tk.Label(header_frame, text="  AI Solver", font=("Verdana", 14, "italic", "bold"), fg="#bbada0", bg="#faf8ef")
        subtitle_label.pack(side="left", anchor="s", pady=(0, 8))

        score_container = tk.Frame(header_frame, bg="#faf8ef")
        score_container.pack(side="right", anchor="e")

        self.score_frame = tk.Frame(score_container, bg="#bbada0", bd=0, padx=15, pady=5)
        self.score_frame.pack(side="left", padx=5)
        tk.Label(self.score_frame, text="SCORE", font=("Verdana", 9, "bold"), fg="#eee4da", bg="#bbada0").pack()
        self.score_label = tk.Label(self.score_frame, text="0", font=("Verdana", 16, "bold"), fg="white", bg="#bbada0")
        self.score_label.pack()

        self.best_frame = tk.Frame(score_container, bg="#bbada0", bd=0, padx=15, pady=5)
        self.best_frame.pack(side="left", padx=5)
        tk.Label(self.best_frame, text="BEST", font=("Verdana", 9, "bold"), fg="#eee4da", bg="#bbada0").pack()
        self.best_lbl = tk.Label(self.best_frame, text="0", font=("Verdana", 16, "bold"), fg="white", bg="#bbada0")
        self.best_lbl.pack()

    def init_grid(self):
        background = tk.Frame(self, bg=BACKGROUND_COLOR_GAME, bd=0, padx=6, pady=6)
        background.grid(row=1, column=0, columnspan=GRID_SIZE, rowspan=GRID_SIZE, pady=5)
        
        for i in range(GRID_SIZE):
            grid_row = []
            for j in range(GRID_SIZE):
                cell = tk.Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_SIZE - 10, height=SIZE/GRID_SIZE - 10)
                cell.grid(row=i, column=j, padx=6, pady=6)
                cell.grid_propagate(False)
                
                cell_number = tk.Label(
                    master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, 
                    justify=tk.CENTER, font=("Verdana", 22, "bold"), width=5, height=2
                )
                cell_number.pack(expand=True, fill="both")
                grid_row.append(cell_number)
            self.grid_cells.append(grid_row)

    def create_controls(self):
        control_frame = tk.Frame(self, bg="#faf8ef")
        control_frame.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, sticky="ew", pady=(15, 0))

        tk.Label(control_frame, text="Thuật toán:", font=("Verdana", 11, "bold"), fg="#776e65", bg="#faf8ef").pack(side="left", padx=(5, 10))

        self.algo_mode = tk.StringVar(value=MODE_EXPECTIMAX)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background="#bbada0", font=("Verdana", 10))
        
        self.algo_dropdown = ttk.Combobox(
            control_frame, textvariable=self.algo_mode, 
            values=[MODE_EXPECTIMAX, MODE_MINIMAX, MODE_GREEDY], 
            state="readonly", width=28
        )
        self.algo_dropdown.pack(side="left", ipady=4)

        self.ai_button = tk.Button(
            control_frame, text="KÍCH HOẠT", 
            font=("Verdana", 11, "bold"), bg="#8f7a66", fg="white",
            activebackground="#9f8b77", activeforeground="white",
            bd=0, padx=15, pady=6, cursor="hand2", command=self.handle_button_click
        )
        self.ai_button.pack(side="right", padx=5)

    def start_game(self):
        self.matrix = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.matrix = game_logic.add_new_tile(self.matrix)
        self.matrix = game_logic.add_new_tile(self.matrix)
        self.current_score = 0
        self.game_state = "PLAYING"

    def update_grid_cells(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = self.matrix[i, j]
                if val == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    cell_bg = CELL_COLORS.get(val, "#3c3a32")
                    cell_fg = CELL_TEXT_COLORS.get(val, "#f9f6f2")
                    self.grid_cells[i][j].configure(text=str(val), bg=cell_bg, fg=cell_fg)
        
        self.score_label.configure(text=str(self.current_score))
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.best_lbl.configure(text=str(self.best_score))
            
        self.update_idletasks()

    def handle_button_click(self):
        """Hàm điều phối sự kiện nút bấm: Kiểm tra nếu đang kết thúc thì Reset game"""
        if self.game_state in ["WON", "LOST", "STUCK"]:
            # Reset toàn bộ bàn cờ về trạng thái ban đầu để chơi lại
            self.start_game()
            self.update_grid_cells()
            self.ai_button.config(text="KÍCH HOẠT", bg="#8f7a66")
            self.algo_dropdown.config(state="readonly")
            return

        # Nếu đang chơi bình thường thì chuyển đổi Start/Pause
        self.toggle_ai()

    def toggle_ai(self):
        self.ai_running = not self.ai_running
        if self.ai_running:
            self.ai_button.config(text="TẠM DỪNG", bg="#f44336")
            self.algo_dropdown.config(state="disabled")
            self.run_ai_loop()
        else:
            self.ai_button.config(text="KÍCH HOẠT", bg="#8f7a66")
            self.algo_dropdown.config(state="readonly")

    def run_ai_loop(self):
        if not self.ai_running or self.game_state != "PLAYING":
            return
            
        current_mode = self.algo_mode.get()
        best_move = ai_agent.get_best_move(self.matrix, current_mode)
        
        if best_move != -1:
            next_matrix, score_gained = game_logic.get_move_result(self.matrix, best_move)
            self.matrix = next_matrix
            self.current_score += score_gained
            
            self.matrix = game_logic.add_new_tile(self.matrix)
            self.update_grid_cells()
            
            # 1. TÌNH HUỐNG CHIẾN THẮNG (Đạt ô 2048)
            if 2048 in self.matrix:
                self.game_state = "WON"
                self.ai_button.config(text="WIN! CHƠI LẠI", bg="#2ca444") # Đổi sang nút chơi lại màu xanh lá
                self.algo_dropdown.config(state="readonly") # Mở khóa để đổi thuật toán lượt sau
                self.ai_running = False
                return

            # 2. TÌNH HUỐNG THUA CUỘC (Hết nước đi)
            if not game_logic.has_moves(self.matrix):
                self.game_state = "LOST"
                self.ai_button.config(text="THUA! CHƠI LẠI", bg="#4a4a4a") # Nút chơi lại màu xám tối
                self.algo_dropdown.config(state="readonly")
                self.ai_running = False
                return
                
            delay = 15 if current_mode == MODE_GREEDY else 35
            self.after(delay, self.run_ai_loop) 
        else:
            # 3. TÌNH HUỐNG BỊ KẸT THẾ CỜ (Không tìm thấy hướng tối ưu)
            self.game_state = "STUCK"
            self.ai_button.config(text="KẸT! CHƠI LẠI", bg="#ff9800") # Nút chơi lại màu cam
            self.algo_dropdown.config(state="readonly")
            self.ai_running = False