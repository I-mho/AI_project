import tkinter as tk
from normal_bet import NormalBetGame
import time
import sqlite3

class User:
    def __init__(self):
        self.coins = 10000
        self.last_bonus_time = time.time()
        self.username = ""

    def load_data(self):
        self.username = input("사용자의 이니셜을 입력하세요: ").strip()
        db_file = f"{self.username}_info.db"
        
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY,
                coins INTEGER,
                last_bonus_time REAL
            )
        """)
        self.conn.commit()
        
        self.cursor.execute("SELECT coins, last_bonus_time FROM user_info WHERE id = 1")
        result = self.cursor.fetchone()

        if result:
            self.coins, self.last_bonus_time = result
        else:
            self.save_data()

    def save_data(self):
        self.cursor.execute("DELETE FROM user_info WHERE id = 1")
        self.cursor.execute("INSERT INTO user_info (id, coins, last_bonus_time) VALUES (1, ?, ?)",
                            (self.coins, self.last_bonus_time))
        self.conn.commit()

    def add_bonus(self):
        current_time = time.time()
        if current_time - self.last_bonus_time >= 60:
            self.coins += 1000
            self.last_bonus_time = current_time
            self.save_data()
            return "1000 코인을 추가로 받았습니다."
        else:
            remaining_time = int(60 - (current_time - self.last_bonus_time))
            seconds = remaining_time % 60
            return f"{seconds}초 후에 다시 시도하세요."

    def close_connection(self):
        self.conn.close()

class BetApp:
    def __init__(self, root):
        self.user = User()
        self.user.load_data()
        self.game = NormalBetGame(root, self.user)
        
        self.root = root
        self.root.title("베팅 게임")
        self.root.geometry("500x300")
        
        self.coins_label = tk.Label(root, text=f"현재 코인 잔액: {self.user.coins}", font=("Arial", 14))
        self.coins_label.pack(pady=10)

        self.bet_entry = tk.Entry(root, font=("Arial", 12), width=20)
        self.bet_entry.pack(pady=5)

        self.bet_button = tk.Button(root, text="베팅하기", command=self.place_bet, font=("Arial", 12), width=15, height=2)
        self.bet_button.pack(pady=5)

        self.bonus_button = tk.Button(root, text="1000 코인 받기", command=self.claim_bonus, font=("Arial", 12), width=15, height=2)
        self.bonus_button.pack(pady=5)

        self.probability_label = tk.Label(root, text="당첨 확률: -%", font=("Arial", 12))
        self.probability_label.pack(pady=10)

        self.message_label = tk.Label(root, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)

        self.update_coins_label()

    def place_bet(self):
        try:
            amount = int(self.bet_entry.get())
        except ValueError:
            self.message_label.config(text="숫자를 입력하세요.")
            return

        if amount <= 0:
            self.message_label.config(text="올바른 금액을 입력하세요.")
            return
        
        result = self.game.bet(amount)
        self.user.save_data()
        self.probability_label.config(text=f"당첨 확률: {self.game.win_probability}%")
        self.message_label.config(text=result)
        self.update_coins_label()
        self.bet_entry.delete(0, tk.END)

    def claim_bonus(self):
        bonus_message = self.user.add_bonus()
        self.message_label.config(text=bonus_message)
        self.update_coins_label()

    def update_coins_label(self):
        self.coins_label.config(text=f"현재 코인 잔액: {self.user.coins}")

    def on_close(self):
        self.user.close_connection()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BetApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
