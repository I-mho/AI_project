import tkinter as tk
import math
import random
import time

class Roulette:
    def __init__(self, root, win_probability):
        self.root = root
        self.items = ['실패', '성공']
        self.num_items = len(self.items)

        print(f'성공 확률 : {win_probability}')
        self.win_probability = win_probability
        self.lose_probability = 100 - win_probability

        self.probabilities = [self.lose_probability, self.win_probability]

        # 확률에 따라 섹터의 각도를 계산
        self.angles = [(p / 100) * 360 for p in self.probabilities]

        self.canvas_size = 400  # 캔버스 크기
        self.radius = self.canvas_size // 2 - 20  # 룰렛 반지름
        self.angle = 0  # 룰렛의 초기 각도

        # TODO: 성공, 실패 색상 정해주시면 감사하겠습니다...!
        self.colors = ['red', 'blue']

        # 추가 팝업 창 설정
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
        self.canvas.delete("all")  # 이전에 그린 것 지우기
        center = self.canvas_size // 2  # 캔버스의 중앙
            
        start_angle = self.angle  # 시작 각도

        # 각 항목별로 섹터를 그리기
        for i, item in enumerate(self.items):
            color = self.colors[i]  # 고정된 색상 사용
            extent_angle = self.angles[i]  # 확률에 따른 각도 사용
            
            if start_angle >= 360:
                start_angle = start_angle - 360

            self.canvas.create_arc(20, 20, self.canvas_size-20, self.canvas_size-20,
                                   start=start_angle, extent=extent_angle, fill=color, outline="black")
            
            # 텍스트는 항상 섹터의 중앙에 배치
            text_angle = math.radians(start_angle + extent_angle / 2)  # 각도 조정
            text_x = center + self.radius * 0.7 * math.cos(text_angle)
            text_y = center - self.radius * 0.7 * math.sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=item, font=("Arial", 12))

            start_angle += extent_angle

        # 화살표(12시 방향에 고정)
        self.canvas.create_polygon([center-10, 10, center+10, 10, center, 30], fill="red")

    # 룰렛 시작 함수
    def spin(self):
        # 무작위로 회전 횟수와 속도 설정
        spin_speed = random.uniform(0.04, 0.06)  # 룰렛 회전 속도(빠르게 시작)
        total_spins = random.randint(6, 10) * 360  # 룰렛이 몇 번 회전할지 무작위로 결정
        deceleration_rate = 0.99  # 회전 속도를 점점 줄이기 위한 감속 비율

        rand_spin = random.randint(1, 10)
        spin_steps = int(total_spins / rand_spin) 

        for _ in range(spin_steps):
            self.angle = (self.angle - 5) % 360  # 각도를 업데이트하여 오른쪽으로 회전시킴
            self.draw_roulette()
            self.root.update()
            time.sleep(spin_speed)

            spin_speed *= deceleration_rate

        # 결과 계산 (12시 방향에 있는 항목 찾기)
        result_index = self.calculate_result()
        result = self.items[result_index]

        # 성공 : 1  | 실패 : 0
        print(f'결과: {result} ({result_index})')

        return result_index

    # 결과 계산
    def calculate_result(self):
        if self.angle >= 360:
            self.angle = self.angle - 360

        current_angle = (360 - self.angle) % 360  # 현재 룰렛의 각도 (12시 방향 기준)
        cumulative_angle = 360 - 90 # 캔버스 시작이 9시 방향이므로 -90도 계산하여 12시 방향 기준으로 함

        # 각 섹터의 각도를 누적하여 현재 각도가 어느 섹터에 속하는지 계산
        for i, sector_angle in reversed(list(enumerate(self.angles))):
            cumulative_angle -= sector_angle
            if current_angle > cumulative_angle:
                self.root.after(5000, self.close_lable) # 룰렛 종료 시, 5초 뒤 창 종료
                return i  # 해당 섹터의 인덱스를 반환

        return -1  # 예외적인 경우

    def close_lable(self):
        self.child.destroy()