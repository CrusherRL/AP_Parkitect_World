import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from worlds.parkitect.src.Item import ItemHelper
from worlds.parkitect.src.Options import Difficulty
from worlds.parkitect.src.Statistics import Statistics

from ..data.constants import (
    ATTRACTION_DECO_RATING_HIGH,
    RULE_SHOP_STAT_EXEMPT_REVENUE_MAX,
    RULE_SHOP_STAT_EXEMPT_REVENUE_MIN,
    ATTRACTION_DECO_RATING_LOW,
    ATTRACTION_DECO_RATING_MEDIUM,
    ATTRACTION_DECO_RATING_VERY_LOW,
    ATTRACTION_DECO_RATING_AMAZING,
    ATTRACTION_DECO_RATING_BAD,
    ATTRACTION_DECO_RATING
)
from ..data.items import (
    CAR_RIDE,
    CHALLENGE_PARK_GUESTS,
    COTTON_CANDY_STALL,
    GUEST_SPAWN_TRAP,
    SOUVENIR_SHOP,
    TILT_COASTER,
    TYPE_CALM_RIDES,
    TYPE_COASTER_RIDES,
    TYPE_SHOP_FACILITIES,
    TYPE_SHOP_FOOD,
    TYPE_SHOPS,
    TYPE_TRAPS, ORBITER, PADDLEBOATS, ELEVATOR, TYPE_THRILL_RIDES, TYPE_TRANSPORT_RIDES, TYPE_WATER_RIDES,
    HOT_DRINKS_STALL, TYPE_SHOP_DRINKS, HOT_DOG_STALL, CASH_MACHINE, STATISTICS_BUILDER_LABEL_GUEST,
    CHALLENGE_EMPLOYEES,
    STATISTICS_BUILDER_LABEL_EMPLOYEE, STATISTICS_BUILDER_LABEL_MONEY, CHALLENGE_PAY_MONEY,
)


class FakeOption:
    def __init__(self, value):
        self.value = value


def make_world(**option_values):
    defaults = {
        "difficulty": Difficulty.easy.value,
        "challenge_maximum_customers": 0,
        "challenge_maximum_excitement": 0,
        "challenge_maximum_intensity": 0,
        "challenge_maximum_nausea": 0,
        "challenge_maximum_satisfaction": 0,
        "challenge_maximum_coaster_revenue": 0,
        "challenge_maximum_ride_revenue": 0,
        "challenge_maximum_shop_revenue": 0,
        "challenge_maximum_ride_profit": 0,
        "challenge_maximum_shop_profit": 0,
        "challenge_enable_decoration": 0,
        "challenge_maximum_photos": 0,
        "challenge_maximum_ride_vouchers": 0,
        "challenge_maximum_shop_vouchers": 0,
    }
    defaults.update(option_values)

    options = {}
    for name, value in defaults.items():
        options[name] = FakeOption(value)

    return SimpleNamespace(
        options=SimpleNamespace(**options),
        random=MagicMock(),
    )


class TestStatistics(unittest.TestCase):
    def test_to_dict_for_calm_rides_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(CAR_RIDE),
            amount=1,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_HIGH,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": CAR_RIDE,
            "amount": 1,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_HIGH,
            "vouchers": 4,
            "type": TYPE_CALM_RIDES,
        })


    def test_to_dict_for_thrill_rides_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(ORBITER),
            amount=2,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_HIGH,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": ORBITER,
            "amount": 2,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_HIGH,
            "vouchers": 4,
            "type": TYPE_THRILL_RIDES,
        })


    def test_to_dict_for_coaster_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TILT_COASTER),
            amount=3,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_HIGH,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": TILT_COASTER,
            "amount": 3,
            "excitement": 7.5,
            "intensity": 6.25,
            "nausea": 3.75,
            "satisfaction": 85.5,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_HIGH,
            "photos": 12,
            "vouchers": 4,
            "type": TYPE_COASTER_RIDES,
        })


    def test_to_dict_for_transport_rides_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(ELEVATOR),
            amount=4,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_LOW,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": ELEVATOR,
            "amount": 4,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_LOW,
            "vouchers": 4,
            "type": TYPE_TRANSPORT_RIDES,
        })


    def test_to_dict_for_water_rides_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(PADDLEBOATS),
            amount=5,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_LOW,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": PADDLEBOATS,
            "amount": 5,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_LOW,
            "vouchers": 4,
            "type": TYPE_WATER_RIDES,
        })


    def test_to_dict_for_drink_stall_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(HOT_DRINKS_STALL),
            amount=6,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_VERY_LOW,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": HOT_DRINKS_STALL,
            "amount": 6,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "vouchers": 4,
            "type": TYPE_SHOP_DRINKS,
        })


    def test_to_dict_for_food_stall_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(HOT_DOG_STALL),
            amount=7,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": HOT_DOG_STALL,
            "amount": 7,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "vouchers": 4,
            "type": TYPE_SHOP_FOOD,
        })


    def test_to_dict_for_facility_stall_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(CASH_MACHINE),
            amount=8,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": CASH_MACHINE,
            "amount": 8,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "vouchers": 4,
            "type": TYPE_SHOP_FACILITIES,
        })


    def test_to_dict_for_trap_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(GUEST_SPAWN_TRAP),
            amount=9,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": GUEST_SPAWN_TRAP,
            "amount": 9,
            "type": TYPE_TRAPS,
        })


    def test_to_dict_for_category_shop_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_SHOPS),
            amount=10,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 10,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "vouchers": 4,
            "type": TYPE_SHOPS,
        })


    def test_to_dict_for_category_calm_ride_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_CALM_RIDES),
            amount=11,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 11,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_AMAZING,
            "vouchers": 4,
            "type": TYPE_CALM_RIDES,
        })


    def test_to_dict_for_category_thrill_ride_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_THRILL_RIDES),
            amount=12,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_HIGH,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 12,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_HIGH,
            "vouchers": 4,
            "type": TYPE_THRILL_RIDES,
        })


    def test_to_dict_for_category_coaster_ride_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_COASTER_RIDES),
            amount=13,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_MEDIUM,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 13,
            "excitement": 7.5,
            "intensity": 6.25,
            "nausea": 3.75,
            "satisfaction": 85.5,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_MEDIUM,
            "photos": 12,
            "vouchers": 4,
            "type": TYPE_COASTER_RIDES,
        })


    def test_to_dict_for_category_transport_ride_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_TRANSPORT_RIDES),
            amount=14,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_LOW,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 14,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_LOW,
            "vouchers": 4,
            "type": TYPE_TRANSPORT_RIDES,
        })


    def test_to_dict_for_category_water_ride_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(TYPE_CALM_RIDES),
            amount=15,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_BAD,
            photos=12,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 15,
            "revenue": 125.25,
            "profit": 33.5,
            "customers": 150,
            "deco": ATTRACTION_DECO_RATING_BAD,
            "vouchers": 4,
            "type": TYPE_CALM_RIDES,
        })


    def test_to_dict_for_challenge_guest_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(CHALLENGE_PARK_GUESTS),
            amount=16,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=16,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 16,
            "type": STATISTICS_BUILDER_LABEL_GUEST,
        })


    def test_to_dict_for_challenge_employee_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(CHALLENGE_EMPLOYEES),
            amount=17,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_AMAZING,
            photos=16,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 17,
            "type": STATISTICS_BUILDER_LABEL_EMPLOYEE,
        })


    def test_to_dict_for_challenge_money_includes_all_stats(self):
        stats = Statistics(
            ItemHelper(CHALLENGE_PAY_MONEY),
            amount=18,
            excitement=7.5,
            intensity=6.25,
            nausea=3.75,
            satisfaction=85.5,
            revenue=125.25,
            profit=33.5,
            customers=150,
            deco=ATTRACTION_DECO_RATING_LOW,
            photos=16,
            vouchers=4,
        )

        self.assertEqual(stats.to_dict(), {
            "name": "",
            "amount": 18,
            "type": STATISTICS_BUILDER_LABEL_MONEY,
        })


    def test_random_roll_force_adds_customers_when_no_other_stats_roll(self):
        world = make_world(challenge_maximum_customers=1000)
        world.random.random.side_effect = [1.0, 1.0]
        world.random.uniform.return_value = 321.7

        stats = Statistics.random_roll(ItemHelper(CAR_RIDE), amount=1, world=world, force=True)

        self.assertEqual(stats.customers, 322)
        self.assertEqual(stats.revenue, 0)


    def test_random_roll_caps_stat_exempt_shop_revenue_and_profit(self):
        world = make_world(
            challenge_maximum_customers=1000,
            challenge_maximum_shop_revenue=1000,
            challenge_maximum_shop_profit=1000,
        )
        world.random.random.side_effect = [0.0, 0.0, 1.0]
        world.random.uniform.side_effect = [
            RULE_SHOP_STAT_EXEMPT_REVENUE_MAX + 100,
            RULE_SHOP_STAT_EXEMPT_REVENUE_MAX + 200,
            RULE_SHOP_STAT_EXEMPT_REVENUE_MIN + 50,
            RULE_SHOP_STAT_EXEMPT_REVENUE_MIN + 75,
        ]

        stats = Statistics.random_roll(ItemHelper(COTTON_CANDY_STALL), amount=1, world=world)

        self.assertEqual(stats.type, TYPE_SHOP_FOOD)
        self.assertEqual(stats.revenue, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN + 50)
        self.assertEqual(stats.profit, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN + 75)


    def test_try_add_deco_rating_ignores_disabled_and_non_coaster_items(self):
        world = make_world(challenge_enable_decoration=0)
        stats = Statistics(ItemHelper(TILT_COASTER), amount=5)

        self.assertIs(stats.try_add_deco_rating(ItemHelper(TILT_COASTER), world), stats)
        self.assertEqual(stats.amount, 5)
        self.assertEqual(stats.deco, "")

        enabled_world = make_world(challenge_enable_decoration=1)
        enabled_world.random.random.return_value = 0.0
        shop_stats = Statistics(ItemHelper(SOUVENIR_SHOP), amount=5)

        self.assertIs(shop_stats.try_add_deco_rating(ItemHelper(SOUVENIR_SHOP), enabled_world), shop_stats)
        self.assertEqual(shop_stats.deco, "")


    def test_try_add_deco_rating_caps_amount_and_uses_weighted_rating(self):
        world = make_world(challenge_enable_decoration=1, difficulty=Difficulty.easy.value)
        world.random.random.return_value = 0.0
        world.random.choices.return_value = [5]
        stats = Statistics(ItemHelper(TILT_COASTER), amount=5)

        stats.try_add_deco_rating(ItemHelper(TILT_COASTER), world)

        self.assertEqual(stats.amount, 3)
        self.assertEqual(stats.deco, ATTRACTION_DECO_RATING[5])
        world.random.choices.assert_called_once()


if __name__ == "__main__":
    unittest.main()
