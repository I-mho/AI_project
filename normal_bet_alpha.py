# Name: normal_bet_alpha.py
import random
from roulette_alpha import Roulette

class NormalBetGame:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.win_probability = 0

    def bet(self, amount):
        if amount > self.user.coins:
            return "코인이 부족합니다. 다시 입력해주세요."
        
        # 당첨 확률 설정
        self.win_probability = random.randint(20, 80)
        roulette = Roulette(self.root, self.win_probability)
        result_index = roulette.spin()

        # 당첨 결과에 따라 금액 계산
        if result_index in [3, 4, 5]:  # 성공 영역
            multiplier = [1, 2, 3][result_index - 3]
            self.user.coins += amount * multiplier
            return f"축하합니다! {multiplier}배 당첨되었습니다. 현재 코인 잔액: {self.user.coins}"
        else:  # 실패 영역
            multiplier = [1, 2, 3][result_index]
            loss_amount = amount * multiplier
            if loss_amount > self.user.coins:
                self.user.coins = 0
            else:
                self.user.coins -= loss_amount
            return f"아쉽게도 {multiplier}배 손실입니다. 현재 코인 잔액: {self.user.coins}"
