import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from worlds.parkitect.src.Item import ItemHelper
from worlds.parkitect.src.Options import Difficulty
from worlds.parkitect.src.Statistics import Statistics

from ..data.constants import (
  ATTRACTION_DECO_RATING,
  RULE_SHOP_STAT_EXEMPT_REVENUE_MAX,
  RULE_SHOP_STAT_EXEMPT_REVENUE_MIN,
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
  TYPE_TRAPS,
)

class FakeOption:
  def __init__(self, value):
    self.value = value

def make_world(**option_values):
  defaults = {
    "difficulty": Difficulty.easy.value,
    "challenge_enable_decoration": 0,
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
    "challenge_maximum_photos": 0,
    "challenge_maximum_ride_vouchers": 0,
    "challenge_maximum_shop_vouchers": 0,
  }
  defaults.update(option_values)

  return SimpleNamespace(
    options=SimpleNamespace(**{
      name: FakeOption(value)
      for name, value in defaults.items()
    }),
    random=MagicMock(),
  )

class TestStatistics(unittest.TestCase):
  def test_to_dict_for_coaster_includes_all_coaster_stats(self):
    stats = Statistics(
      ItemHelper(TILT_COASTER),
      amount=2,
      excitement=7.5,
      intensity=6.25,
      nausea=3.75,
      satisfaction=85.5,
      revenue=125.25,
      profit=33.5,
      customers=150,
      deco="High",
      photos=12,
      vouchers=4,
    )

    self.assertEqual(stats.to_dict(), {
      "name": TILT_COASTER,
      "amount": 2,
      "excitement": 7.5,
      "intensity": 6.25,
      "nausea": 3.75,
      "satisfaction": 85.5,
      "revenue": 125.25,
      "profit": 33.5,
      "customers": 150,
      "deco": "High",
      "photos": 12,
      "vouchers": 4,
      "type": TYPE_COASTER_RIDES,
    })

  def test_to_dict_for_ride_shop_and_trap_uses_type_specific_fields(self):
    ride = Statistics(ItemHelper(CAR_RIDE), amount=1, revenue=20, profit=5, customers=30, deco="Low", vouchers=2)
    shop = Statistics(ItemHelper(SOUVENIR_SHOP), amount=1, revenue=40, profit=10, customers=50, vouchers=3)
    trap = Statistics(ItemHelper(GUEST_SPAWN_TRAP), amount=4, revenue=100, customers=200)

    self.assertEqual(ride.to_dict(), {
      "name": CAR_RIDE,
      "amount": 1,
      "revenue": 20,
      "profit": 5,
      "customers": 30,
      "deco": "Low",
      "vouchers": 2,
      "type": TYPE_CALM_RIDES,
    })
    self.assertEqual(shop.to_dict(), {
      "name": SOUVENIR_SHOP,
      "amount": 1,
      "revenue": 40,
      "profit": 10,
      "customers": 50,
      "vouchers": 3,
      "type": TYPE_SHOP_FACILITIES,
    })
    self.assertEqual(trap.to_dict(), {
      "name": GUEST_SPAWN_TRAP,
      "amount": 4,
      "type": TYPE_TRAPS,
    })

  def test_to_dict_for_category_and_challenge_items(self):
    category = Statistics(ItemHelper(TYPE_SHOPS), amount=3, revenue=90, profit=15, customers=25)
    challenge = Statistics(ItemHelper(CHALLENGE_PARK_GUESTS), amount=250)

    self.assertEqual(category.to_dict(), {
      "name": "",
      "amount": 3,
      "revenue": 90,
      "profit": 15,
      "customers": 25,
      "vouchers": 0,
      "type": TYPE_SHOPS,
    })
    self.assertEqual(challenge.to_dict(), {
      "name": "",
      "amount": 250,
      "type": "Guest",
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
