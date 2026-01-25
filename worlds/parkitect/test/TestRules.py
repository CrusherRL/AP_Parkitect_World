from cgi import print_form
import unittest

from BaseClasses import MultiWorld
from worlds.parkitect.src.Item import ItemHelper

from .. import ParkitectWorld

from ..src.Rules import Rules

from .FakerOptions import FakeParkitectOptions

from ..data.items import *
from ..data.constants import RULE_RIDE_STAT_EXEMPT_REVENUE_MAX, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX

class TestRules(unittest.TestCase):
  def setUp(self):
    self.player = 1
    self.world = MultiWorld(1)
    self.parkitectWorld = ParkitectWorld(self.world, self.player)
    self.parkitectWorld.options = FakeParkitectOptions
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
      # Traps
      {
        "item": SHOP_CLEANING_TRAP,
        "category": TYPE_TRAPS,
        TYPE_STAT_EXEMPT: False,
        TYPE_NON_PROFIT: False,
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


