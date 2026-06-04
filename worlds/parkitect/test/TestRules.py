import unittest
from unittest.mock import patch

from BaseClasses import MultiWorld
from worlds.parkitect.src.Item import ItemHelper
from worlds.parkitect.src.Options import Difficulty

from .. import ParkitectWorld

from ..src.Rules import Rules

from .FakerOptions import FakeParkitectOptions, FakeOption

from ..data.items import *
from ..data.constants import (
  CHALLENGE_PARK_GUESTS_RANGES,
  RULE_RIDE_STAT_EXEMPT_REVENUE_MAX,
  RULE_SHOP_STAT_EXEMPT_REVENUE_MAX,
  TIER_2_PROGRESS,
)

class TestRules(unittest.TestCase):
  def setUp(self):
    self.player = 1
    self.world = MultiWorld(1)
    self.parkitectWorld = ParkitectWorld(self.world, self.player)
    self.parkitectWorld.options = FakeParkitectOptions
    self.parkitectWorld.item_table = [CAR_RIDE] * 8
    self.rules = Rules(self.parkitectWorld)

  def assert_has_keys(self, obj, keys):
    for key in keys:
      self.assertIn(key, obj)

  def test_create_check(self):
    items = [
      # Rides
      {
        "item": CAR_RIDE,
        "category": TYPE_CALM_RIDES,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },
      {
        "item": ORBITER,
        "category": TYPE_THRILL_RIDES,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },
      {
        "item": TILT_COASTER,
        "category": TYPE_COASTER_RIDES,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },
      {
        "item": JUNIOR_COASTER,
        "category": TYPE_COASTER_RIDES,
        TYPE_STAT_EXEMPT: True, # Here with low stats!
        TYPE_NON_PROFIT: False,
      },
      {
        "item": MINI_MONORAIL,
        "category": TYPE_TRANSPORT_RIDES,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },
      {
        "item": LOG_FLUME,
        "category": TYPE_WATER_RIDES,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },

      # Shops
      {
        "item": SOUVENIR_SHOP,
        "category": TYPE_SHOPS,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
      },
      {
        "item": COTTON_CANDY_STALL,
        "category": TYPE_SHOPS,
        TYPE_STAT_EXEMPT: True, # Here with low stats!
        TYPE_NON_PROFIT: False,
      },
      {
        "item": TOILETS,
        "category": TYPE_SHOPS,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: True, # Here with non profits!
      },
    ]

    number = 0
    
    progresses = [
      0.01, # Tier 1
      0.08, # Tier 2
      0.24, # Tier 3
      0.52, # Tier 4
      0.91, # Tier 5
    ]

    prerequisites = [ROCKIN_TUG]

    for item in items:
      is_shop_category = item in TYPES[TYPE_SHOPS]
      is_ride_category = item in TYPES[TYPE_RIDES]

      # for Every Tier
      for index in range(0,4):
        itemHelper = ItemHelper(item["item"])
        check = self.rules._create_check(number, itemHelper, prerequisites, progresses[index])
        check_item = check['item']
        check_item_name = check_item['name']

        self.assert_has_keys(check, ["location_id", "item"])
        self.assertIsInstance(check["location_id"], int)
        self.assertIsInstance(check["item"], dict)

        self.assertEqual(check['location_id'], number)

        if is_shop_category or is_ride_category:
          self.assertEqual(check_item_name, item["category"])
        else:
          self.assertEqual(check_item_name, item["item"])

        self._evaluate_check_values(check_item, item)

        number += 1
      number += 1

  def _evaluate_check_values(self, check_item: dict[str, str|int], origin_item):
    itemHelper = ItemHelper(check_item["name"])

    if itemHelper.is_coaster():
      self.assert_has_keys(
        check_item,
        ["name", "amount", "excitement", "intensity", "nausea", "satisfaction", "revenue", "customers", "type"]
      )

    elif itemHelper.is_ride() or itemHelper.is_shop():
      self.assert_has_keys(
        check_item,
        ["name", "amount", "revenue", "customers", "type"]
      )

    if itemHelper.is_shop_category() or itemHelper.is_ride_category() or itemHelper.is_coaster_category():
      self.assert_has_keys(
        check_item,
        ["amount", "type"]
      )

      self.assertEqual(check_item["name"], "")
      self.assertIn(check_item["type"], TYPES[TYPE_SHOPS] + TYPES[TYPE_RIDES])

    elif itemHelper.is_trap():
      self.assert_has_keys(
        check_item,
        ["name", "amount", "type"]
      )
      self.assertNotIn("revenue", check_item)
      self.assertNotIn("customers", check_item)

    if origin_item[TYPE_STAT_EXEMPT]:
      max = RULE_RIDE_STAT_EXEMPT_REVENUE_MAX

      if itemHelper.is_shop() or itemHelper.is_shop_category():
        max = RULE_SHOP_STAT_EXEMPT_REVENUE_MAX

      if "revenue" in check_item:
        self.assertLessEqual(
          check_item["revenue"],
          max
        )

    if itemHelper.is_shop() and origin_item[TYPE_NON_PROFIT]:
      self.assertEqual(check_item.get("revenue", 0), 0)

  def test_challenge_park_guests_ranges(self):
    self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[0], [100, 300])
    self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[1], [200, 500])
    self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[2], [400, 800])
    self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[3], [600, 1000])

  def test_determine_park_guests_max_scales_with_progress(self):
    self.parkitectWorld.options.goal_guests = FakeOption(0)
    self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

    with patch.object(self.parkitectWorld.random, "uniform", return_value=200.0):
      early = self.rules.determine_park_guests_max(TIER_2_PROGRESS)
      late = self.rules.determine_park_guests_max(TIER_2_PROGRESS + 0.01)

    self.assertEqual(early, 50)
    self.assertEqual(late, 200)

  def test_determine_park_guests_max_minimum_is_one(self):
    self.parkitectWorld.options.goal_guests = FakeOption(0)
    self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

    with patch.object(self.parkitectWorld.random, "uniform", return_value=0.0):
      guests = self.rules.determine_park_guests_max(0.0)

    self.assertEqual(guests, 1)

  def test_determine_employee_max_scales_with_progress(self):
    self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

    with patch.object(self.parkitectWorld.random, "uniform", return_value=10.0):
      early = self.rules.determine_employee_max(EMPLOYEE_MECHANIC, TIER_2_PROGRESS)
      late = self.rules.determine_employee_max(EMPLOYEE_MECHANIC, TIER_2_PROGRESS + 0.01)

    self.assertEqual(early, 2)
    self.assertEqual(late, 10)

  def test_create_check_park_guests_challenge(self):
    item_helper = ItemHelper(CHALLENGE_PARK_GUESTS)
    with patch.object(self.rules, "determine_park_guests_max", return_value=250) as determine_guests:
      check = self.rules._create_check(5, item_helper, [ROCKIN_TUG], 0.5)

    determine_guests.assert_called_once_with(0.5)
    self.assertEqual(check["item"]["type"], "Guest")
    self.assertEqual(check["item"]["amount"], 250)

  def test_create_check_employees_challenge(self):
    item_helper = ItemHelper(CHALLENGE_EMPLOYEES)
    with (
      patch.object(self.parkitectWorld.random, "choice", return_value=EMPLOYEE_JANITOR),
      patch.object(self.rules, "determine_employee_max", return_value=4) as determine_employees,
    ):
      check = self.rules._create_check(5, item_helper, [ROCKIN_TUG], 0.5)

    determine_employees.assert_called_once_with(EMPLOYEE_JANITOR, 0.5)
    self.assertEqual(check["item"]["name"], EMPLOYEE_JANITOR)
    self.assertEqual(check["item"]["amount"], 4)


