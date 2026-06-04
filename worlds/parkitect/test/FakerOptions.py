from ..src.Options import Difficulty

class FakeOption:
    def __init__(self, value):
        self.value = value

class FakeParkitectOptions:
    difficulty = FakeOption(Difficulty.easy.value)
    goal_guests = FakeOption(0)
    goal_money = FakeOption(0)
    challenge_park_guests = FakeOption(1)
    challenge_employees = FakeOption(0)
    challenge_pay_money = FakeOption(0)
    challenge_enable_decoration = FakeOption(0)
    challenge_customers = FakeOption(1000)
    challenge_maximum_excitement = FakeOption(1000)
    challenge_maximum_intensity = FakeOption(1000)
    challenge_maximum_nausea = FakeOption(1000)
    challenge_maximum_satisfaction = FakeOption(1000)
    challenge_maximum_ride_revenue = FakeOption(1000)
    challenge_maximum_shop_revenue = FakeOption(1000)
