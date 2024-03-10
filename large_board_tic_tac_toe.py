import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import random


class RandomBoardTicTacToe:
    def __init__(self, size=(600, 600)):

        self.size = self.width, self.height = size
        self.BLACK = '#000000'
        self.WHITE = '#FFFFFF'
        self.GREEN = '#00FF00'
        self.RED = '#FF0000'
        self.GRID_SIZE = 4
        self.OFFSET = 5
        self.CIRCLE_COLOR = '#8C92AC'
        self.CROSS_COLOR = '#8C92AC'
        self.WIDTH = self.size[0] / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1] / self.GRID_SIZE - self.OFFSET
        self.MARGIN = 5
        self.mode = None  # Initialize mode as None
        self.root = tk.Tk()

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self.root, width=self.size[0], height=self.size[1])
        self.canvas.pack()

        self.game_reset()

    def draw_game(self):
        self.canvas.delete("all")
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x0 = (self.MARGIN + self.WIDTH) * col + self.MARGIN
                y0 = (self.MARGIN + self.HEIGHT) * row + self.MARGIN + 100  # Adjusted for the menu on top
                x1 = x0 + self.WIDTH
                y1 = y0 + self.HEIGHT
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.WHITE)

    def draw_menu(self):
        player_name = simpledialog.askstring("Player Name", "Enter your name:")
        ai_mode = simpledialog.askinteger("AI Mode", "Select AI Mode (1 for Minimax, 2 for Negamax):", minvalue=1,
                                          maxvalue=2)
        self.set_ai_mode(ai_mode)
        self.start_game()

    def set_ai_mode(self, value):
        if value == 1:
            self.mode = 'minimax'
        elif value == 2:
            self.mode = 'negamax'

    def start_game(self):
        self.game_reset()

    def draw_circle(self, x, y):
        cx = (self.MARGIN + self.WIDTH) * y + self.MARGIN + self.WIDTH / 2
        cy = (self.MARGIN + self.HEIGHT) * x + self.MARGIN + self.HEIGHT / 2 + 100  # Adjusted for the menu on top
        radius = min(self.WIDTH, self.HEIGHT) / 2 - 10
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline=self.CIRCLE_COLOR)

    def draw_cross(self, x, y):
        x0 = (self.MARGIN + self.WIDTH) * y + self.MARGIN + 10
        y0 = (self.MARGIN + self.HEIGHT) * x + self.MARGIN + 10 + 100  # Adjusted for the menu on top
        x1 = (self.MARGIN + self.WIDTH) * (y + 1) - self.MARGIN - 10
        y1 = (self.MARGIN + self.HEIGHT) * (x + 1) - self.MARGIN - 10 + 100
        self.canvas.create_line(x0, y0, x1, y1, fill=self.CROSS_COLOR, width=5)
        self.canvas.create_line(x1, y0, x0, y1, fill=self.CROSS_COLOR, width=5)

    def is_game_over(self):
        return self.game_state.is_terminal()

    def move(self, event):
        if not self.is_game_over():
            col = int(event.x // (self.WIDTH + self.MARGIN))
            row = int(event.y // (self.HEIGHT + self.MARGIN)) - 2  # Adjusted for the menu on top
            if self.game_state.board_state[row][col] == 0:
                self.game_state.board_state[row][col] = 1
                self.draw_cross(row, col)

                if self.is_game_over():
                    winner = "Player" if self.game_state.winner == 1 else "AI"
                    messagebox.showinfo("Game Over", f"Winner: {winner}\nScores: {self.game_state.get_scores(True)}")
                else:
                    self.play_ai()

    def play_ai(self):
        self.root.after(1000, self.ai_move)

    def ai_move(self):
        if not self.is_game_over():
            terminal = self.game_state.is_terminal()

            if self.mode == "minimax":
                value, best_move = minimax(self.game_state, 2, not self.game_state.turn_O)
            else:
                value, best_move = negamax(self.game_state, 2, 1 if not self.game_state.turn_O else -1)

            self.move_ai(best_move)

            if not terminal:
                self.root.after(1000, self.change_turn)

    def move_ai(self, move):
        if not self.is_game_over():
            self.game_state = self.game_state.get_next_state(move)
            self.draw_circle(move[0], move[1])

    def change_turn(self):
        self.draw_game()

    def game_reset(self):
        self.draw_game()
        self.mode = None  # Reset mode to None
        self.game_state = GameStatus(np.zeros((self.GRID_SIZE, self.GRID_SIZE)), random.choice([True, False]))

    def play_game(self):
        self.draw_menu()
        self.root.bind("<Button-1>", self.move)
        self.root.mainloop()


tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()