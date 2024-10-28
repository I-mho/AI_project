# Name: roulette.py
import tkinter as tk
import math
import random
import time

# 룰렛 결과와 콘솔에 출력되는 결과는 일치
# 위 결과들과 normal_bet.py에서 결정되는 당첨 여부가 일치하지 않는 듯함

class Roulette:
    def __init__(self, root, win_probability):
        self.root = root
        self.items = ['실패 x1', '성공 x1', '실패 x2', '성공 x2', '실패 x3', '성공 x3']
        self.num_items = len(self.items)

        print(f'성공 확률 : {win_probability}')
        self.win_probability = win_probability
        self.lose_probability = 100 - win_probability

        # 비율 설정 (성공과 실패 항목의 순서 번갈아 배치)
        self.probabilities = [
            self.lose_probability * 0.5,   # 실패 x1 (3/6)
            self.win_probability * 0.5,    # 성공 x1 (3/6)
            self.lose_probability * (2/6), # 실패 x2 (2/6)
            self.win_probability * (2/6),  # 성공 x2 (2/6)
            self.lose_probability * (1/6), # 실패 x3 (1/6)
            self.win_probability * (1/6)   # 성공 x3 (1/6)
        ]

        # 각 항목의 각도 계산
        self.angles = [(p / 100) * 360 for p in self.probabilities]

        self.canvas_size = 400
        self.radius = self.canvas_size // 2 - 20
        self.angle = 0

        # 각 항목의 색상 (성공과 실패 색상을 번갈아 배치)
        # 실패 x1, 성공 x1, 실패 x2, 성공 x2, 실패 x3, 성공 x3 순서
        self.colors = ['red', 'cyan', 'lightcoral', 'lightblue', 'darkred', 'blue']

        # 팝업 창 설정
        self.child = tk.Toplevel(self.root)
        self.child.title("룰렛 창")
        txt = f'성공 확률 : {self.win_probability}%'
        child_label = tk.Label(self.child, text=txt)
        child_label.pack()

        # 캔버스 설정
        self.canvas = tk.Canvas(self.child, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

    # 룰렛 GUI 그리기
    def draw_roulette(self):
        self.canvas.delete("all")
        center = self.canvas_size // 2
        start_angle = self.angle

        for i, item in enumerate(self.items):
            color = self.colors[i]
            extent_angle = self.angles[i]

            if start_angle >= 360:
                start_angle = start_angle - 360

            self.canvas.create_arc(20, 20, self.canvas_size-20, self.canvas_size-20,
                                   start=start_angle, extent=extent_angle, fill=color, outline="black")
            
            text_angle = math.radians(start_angle + extent_angle / 2)
            text_x = center + self.radius * 0.7 * math.cos(text_angle)
            text_y = center - self.radius * 0.7 * math.sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=item, font=("Arial", 12))

            start_angle += extent_angle

        self.canvas.create_polygon([center-10, 10, center+10, 10, center, 30], fill="red")

    # 룰렛 시작 함수
    def spin(self):
        spin_speed = random.uniform(0.04, 0.06)
        total_spins = random.randint(6, 10) * 360
        deceleration_rate = 0.99

        rand_spin = random.randint(1, 10)
        spin_steps = int(total_spins / rand_spin) 

        for _ in range(spin_steps):
            self.angle = (self.angle - 5) % 360
            self.draw_roulette()
            self.root.update()
            time.sleep(spin_speed)
            spin_speed *= deceleration_rate

        result_index = self.calculate_result()
        result = self.items[result_index]

        print(f'결과: {result} ({result_index})')
        return result_index

    # 결과 계산
    def calculate_result(self):
        if self.angle >= 360:
            self.angle = self.angle - 360

        current_angle = (360 - self.angle) % 360
        cumulative_angle = 360 - 90

        for i, sector_angle in reversed(list(enumerate(self.angles))):
            cumulative_angle -= sector_angle
            if current_angle > cumulative_angle:
                self.root.after(5000, self.close_lable)
                return i

        return -1

    def close_lable(self):
        self.child.destroy()
