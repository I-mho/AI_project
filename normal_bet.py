import random
from roulette import Roulette

class NormalBetGame:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.win_probability = 0

    def bet(self, amount):
        if amount > self.user.coins:
            return "코인이 부족합니다. 다시 입력해주세요."
        
        # 당첨 확률 설정 및 표시
        self.win_probability = random.randint(20, 80)
        roulette = Roulette(self.root, self.win_probability)
        is_winner = roulette.spin() # 리턴값(0 : 실패, 1 : 성공)

        if is_winner:
            self.user.coins += amount
            return f"축하합니다! 당첨되었습니다. 당첨 확률: {self.win_probability}% 현재 코인 잔액: {self.user.coins}"
        else:
            self.user.coins -= amount
            return f"아쉽게도 당첨되지 않았습니다. 당첨 확률: {self.win_probability}% 현재 코인 잔액: {self.user.coins}"
