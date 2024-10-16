import random

class NormalBetGame:
    def __init__(self, user):
        self.user = user
        self.win_probability = 0

    def bet(self, amount):
        if amount > self.user.coins:
            return "코인이 부족합니다. 다시 입력해주세요."
        
        # 당첨 확률 설정 및 표시
        self.win_probability = random.randint(20, 80)
        is_winner = random.random() < (self.win_probability / 100)

        if is_winner:
            self.user.coins += amount
            return f"축하합니다! 당첨되었습니다. 당첨 확률: {self.win_probability}% 현재 코인 잔액: {self.user.coins}"
        else:
            self.user.coins -= amount
            return f"아쉽게도 당첨되지 않았습니다. 당첨 확률: {self.win_probability}% 현재 코인 잔액: {self.user.coins}"
