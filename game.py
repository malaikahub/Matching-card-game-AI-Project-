import tkinter as tk
from tkinter import messagebox
import random
import time

# ---------------------------
# Memory Card Matching Game
# Developed by: Malaika Arooj
# Features: Timer, Move Counter, Restart Button, Dynamic Grid
# ---------------------------

class MemoryGame:
    def __init__(self, root, grid_size=4, move_limit=20):
        self.root = root
        self.root.title("🧠 Memory Card Matching Game")
        self.root.config(bg="#2c3e50")

        # Game variables
        self.grid_size = grid_size
        self.move_limit = move_limit
        self.moves = 0
        self.start_time = None
        self.timer_running = False
        self.first_card = None
        self.second_card = None
        self.buttons = []
        self.card_values = []
        self.revealed = [[False]*grid_size for _ in range(grid_size)]

        # Top bar (Move counter + Timer + Restart)
        self.top_frame = tk.Frame(root, bg="#2c3e50")
        self.top_frame.pack(pady=10)

        self.move_label = tk.Label(self.top_frame, text="Moves: 0", font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.move_label.grid(row=0, column=0, padx=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 14, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.timer_label.grid(row=0, column=1, padx=10)

        self.restart_btn = tk.Button(self.top_frame, text="🔄 Restart", font=("Arial", 12, "bold"), command=self.restart_game,
                                     bg="#16a085", fg="white", relief="raised", padx=10)
        self.restart_btn.grid(row=0, column=2, padx=10)

        # Game board
        self.board_frame = tk.Frame(root, bg="#34495e", padx=15, pady=15)
        self.board_frame.pack()

        self.create_cards()
        self.update_timer()

    # ---------------------------
    # Create Cards
    # ---------------------------
    def create_cards(self):
        symbols = list(range(1, (self.grid_size**2)//2 + 1)) * 2
        random.shuffle(symbols)
        self.card_values = [symbols[i:i+self.grid_size] for i in range(0, len(symbols), self.grid_size)]

        for r in range(self.grid_size):
            row_buttons = []
            for c in range(self.grid_size):
                btn = tk.Button(self.board_frame, text="❓", width=6, height=3,
                                font=("Arial", 18, "bold"), bg="#1abc9c", fg="#2c3e50",
                                command=lambda r=r, c=c: self.flip_card(r, c))
                btn.grid(row=r, column=c, padx=8, pady=8)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    # ---------------------------
    # Flip Card Logic
    # ---------------------------
    def flip_card(self, r, c):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        if self.revealed[r][c] or (self.first_card and self.second_card):
            return

        self.buttons[r][c].config(text=str(self.card_values[r][c]), bg="#f1c40f")
        if not self.first_card:
            self.first_card = (r, c)
        else:
            self.second_card = (r, c)
            self.root.after(700, self.check_match)
            self.moves += 1
            self.move_label.config(text=f"Moves: {self.moves}")

    # ---------------------------
    # Match Checking
    # ---------------------------
    def check_match(self):
        r1, c1 = self.first_card
        r2, c2 = self.second_card

        if self.card_values[r1][c1] == self.card_values[r2][c2]:
            self.revealed[r1][c1] = self.revealed[r2][c2] = True
            self.buttons[r1][c1].config(bg="#2ecc71", state="disabled")
            self.buttons[r2][c2].config(bg="#2ecc71", state="disabled")
        else:
            self.buttons[r1][c1].config(text="❓", bg="#1abc9c")
            self.buttons[r2][c2].config(text="❓", bg="#1abc9c")

        self.first_card = self.second_card = None
        self.check_game_over()

    # ---------------------------
    # Game Over / Win Condition
    # ---------------------------
    def check_game_over(self):
        if all(all(row) for row in self.revealed):
            self.timer_running = False
            total_time = int(time.time() - self.start_time)
            messagebox.showinfo("🎉 Congratulations!",
                                f"You matched all cards in {self.moves} moves and {total_time} seconds!")
        elif self.moves >= self.move_limit:
            self.timer_running = False
            messagebox.showwarning("⏰ Game Over", "You reached the move limit! Try again.")

    # ---------------------------
    # Timer Update
    # ---------------------------
    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    # ---------------------------
    # Restart Game
    # ---------------------------
    def restart_game(self):
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 0s")
        self.start_time = None
        self.timer_running = False
        self.first_card = self.second_card = None
        self.buttons = []
        self.revealed = [[False]*self.grid_size for _ in range(self.grid_size)]

        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.create_cards()


# ---------------------------
# Main Program
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root, grid_size=4, move_limit=20)
    root.mainloop()
