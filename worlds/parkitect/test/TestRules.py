import unittest
from typing import Any
from unittest.mock import patch

from BaseClasses import MultiWorld, Entrance, CollectionRule
from rule_builder.rules import Rule
from worlds.cv64.data.patches import multiworld_item_name_loader
from ..src.ParkitectCheck import ParkitectCheck
from .. import ParkitectLocation
from ..src.Item import ItemHelper
from ..src.Options import Difficulty

from .. import ParkitectWorld

from ..src.Rules import Rules

from .FakerOptions import FakeParkitectOptions, FakeOption

from ..data.items import *
from ..data.constants import (
    CHALLENGE_PARK_GUESTS_RANGES,
    TIER_2_PROGRESS, START_ITEMS_PER_LOCATION, CHALLENGE_PAY_MONEY_RANGES,
)


class TestRules(unittest.TestCase):
    def setUp(self):
        def set_rule(spot: ParkitectLocation | Entrance, rule: CollectionRule | Rule[Any]):
            return

        self.player = 1
        self.world = MultiWorld(1)
        self.parkitectWorld = ParkitectWorld(self.world, self.player)
        self.parkitectWorld.options = FakeParkitectOptions
        self.parkitectWorld.item_table = [CAR_RIDE] * 8
        self.rules = Rules(self.parkitectWorld, set_rule)


    def test_create_checks(self):
        items = [
            SHOP_INGREDIENTS_TRAP,
            ATTRACTION_BREAKDOWN_TRAP,
            PLAYER_MONEY_TRAP,
            CAROUSEL,
            INVERTED_DARK_RIDE,
            STANDUP_COASTER,
            MINI_MONORAIL,
            BUMPER_BOATS,
            BUBBLE_TEA_STALL,
            HOT_DOG_STALL,
            CASH_MACHINE,
        ]

        number = 0
        item_table_length = len(items)
        prerequisites = [GRAVITRON]

        for item in items:
            item_helper = ItemHelper(item)
            parkitect_check = self.rules._create_check(number, item_helper, prerequisites, number // item_table_length)

            self.assertEqual(item, parkitect_check.item.name)
            self.assertEqual(number, parkitect_check.location_id)

            number += 1


    def test_challenge_park_guests_ranges(self):
        self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[0], [100, 500])
        self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[1], [200, 1000])
        self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[2], [400, 1150])
        self.assertEqual(CHALLENGE_PARK_GUESTS_RANGES[3], [600, 1300])


    def test_determine_park_guests_max_scales_with_progress(self):
        self.parkitectWorld.options.goal_guests = FakeOption(1000)
        self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

        with patch.object(self.parkitectWorld.random, "uniform", return_value=200.0):
            very_early = self.rules.determine_park_guests_max(TIER_2_PROGRESS, START_ITEMS_PER_LOCATION - 1)
            early = self.rules.determine_park_guests_max(TIER_2_PROGRESS)
            late = self.rules.determine_park_guests_max(TIER_2_PROGRESS + 0.01)

        self.assertEqual(very_early, 25)
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
            very_early = self.rules.determine_employee_max(EMPLOYEE_MECHANIC, TIER_2_PROGRESS, START_ITEMS_PER_LOCATION - 1)
            early = self.rules.determine_employee_max(EMPLOYEE_MECHANIC, TIER_2_PROGRESS)
            late = self.rules.determine_employee_max(EMPLOYEE_MECHANIC, TIER_2_PROGRESS + 0.01)

        self.assertEqual(very_early, 1)
        self.assertEqual(early, 2)
        self.assertEqual(late, 10)


    def test_determine_employee_max_minimum_is_one(self):
        self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

        with patch.object(self.parkitectWorld.random, "uniform", return_value=0.0):
            employee = self.rules.determine_employee_max(EMPLOYEE_SECURITY, 0.0)

        self.assertEqual(employee, 1)


    def test_determine_pay_money_max_scales_with_progress(self):
        self.parkitectWorld.options.goal_money = FakeOption(1000)
        self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)

        with patch.object(self.parkitectWorld.random, "uniform", return_value=300.0):
            very_early = self.rules.determine_pay_money_max(START_ITEMS_PER_LOCATION - 1)
            late = self.rules.determine_pay_money_max(100)

        self.assertEqual(very_early, 150)
        self.assertEqual(late, 300)


    def test_determine_pay_money_max_minimum_is_one(self):
        self.parkitectWorld.options.difficulty = FakeOption(Difficulty.easy.value)
        money = self.rules.determine_pay_money_max(100)

        self.assertGreater(money, CHALLENGE_PAY_MONEY_RANGES[Difficulty.easy.value][0])


    def test_create_check_park_guests_challenge(self):
        item_helper = ItemHelper(CHALLENGE_PARK_GUESTS)
        with patch.object(self.rules, "determine_park_guests_max", return_value=250) as determine_guests:
            parkitect_check: ParkitectCheck = self.rules._create_check(5, item_helper, [ROCKIN_TUG], 0.5)

        determine_guests.assert_called_once_with(0.5, 5)
        self.assertEqual(parkitect_check.item.name, "")
        self.assertEqual(parkitect_check.item.amount, 250)
        self.assertEqual(parkitect_check.item.type, CHALLENGE_PARK_GUESTS)

        check = parkitect_check.to_dict()
        self.assertEqual(check["item"]["name"], "")
        self.assertEqual(check["item"]["amount"], 250)
        self.assertEqual(check["item"]["type"], STATISTICS_BUILDER_LABEL_GUEST)


    def test_create_check_employees_challenge(self):
        item_helper = ItemHelper(CHALLENGE_EMPLOYEES)
        with (
            patch.object(self.parkitectWorld.random, "choice", return_value=EMPLOYEE_JANITOR),
            patch.object(self.rules, "determine_employee_max", return_value=4) as determine_employees,
        ):
            parkitect_check: ParkitectCheck = self.rules._create_check(5, item_helper, [ROCKIN_TUG], 0.5)

        determine_employees.assert_called_once_with(EMPLOYEE_JANITOR, 0.5, 5)
        self.assertEqual(parkitect_check.item.name, EMPLOYEE_JANITOR)
        self.assertEqual(parkitect_check.item.amount, 4)
        self.assertEqual(parkitect_check.item.type, CHALLENGE_EMPLOYEES)

        check = parkitect_check.to_dict()
        self.assertEqual(check["item"]["name"], EMPLOYEE_JANITOR)
        self.assertEqual(check["item"]["amount"], 4)
        self.assertEqual(check["item"]["type"], STATISTICS_BUILDER_LABEL_EMPLOYEE)


    def test_create_check_pay_money_challenge(self):
        item_helper = ItemHelper(CHALLENGE_PAY_MONEY)
        with patch.object(self.rules, "determine_pay_money_max", return_value=660) as determine_pay_money:
            parkitect_check: ParkitectCheck = self.rules._create_check(1, item_helper, [ROCKIN_TUG], 0.5)

        determine_pay_money.assert_called_once_with(1)
        self.assertEqual(parkitect_check.item.name, "")
        self.assertEqual(parkitect_check.item.amount, 660)
        self.assertEqual(parkitect_check.item.type, CHALLENGE_PAY_MONEY)

        check = parkitect_check.to_dict()
        self.assertEqual(check["item"]["name"], "")
        self.assertEqual(check["item"]["amount"], 660)
        self.assertEqual(check["item"]["type"], STATISTICS_BUILDER_LABEL_MONEY)
