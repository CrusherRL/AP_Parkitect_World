class FakeOption:
    def __init__(self, value):
        self.value = value

class FakeParkitectOptions:
    challenge_customers = FakeOption(1000)
    challenge_maximum_excitement = FakeOption(1000)
    challenge_maximum_intensity = FakeOption(1000)
    challenge_maximum_nausea = FakeOption(1000)
    challenge_maximum_satisfaction = FakeOption(1000)
    challenge_maximum_ride_revenue = FakeOption(1000)
    challenge_maximum_shop_revenue = FakeOption(1000)