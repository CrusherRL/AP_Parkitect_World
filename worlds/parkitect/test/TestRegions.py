import math
import unittest
from typing import Any

from BaseClasses import MultiWorld, CollectionRule, Entrance
from rule_builder.rules import Rule

from ..src.Regions import Regions, ParkitectLocation

from ..data.constants import LOCATION_NAME_TO_ID, START_ITEMS_PER_LOCATION, ITEMS_PER_LOCATION


class TestRegions(unittest.TestCase):
    def setUp(self):
        def set_rule(spot: ParkitectLocation | Entrance, rule: CollectionRule | Rule[Any]):
            return

        self.player = 1
        self.multiworld = MultiWorld(1)
        self.region = type("DummyRegion", (), {})()  # Simple object with locations
        self.regions = Regions(self.player, self.multiworld, LOCATION_NAME_TO_ID, set_rule)

        # Dummy IDs for all locations
        self.location_ids = {}
        for i in range(3 * 10):
            for c in range(1, 4):
                self.location_ids[f"Challenge_{c}_{i}"] = i * 3 + c


    def test_locations_sphere_one(self):
        locations = self.regions._locations_to_region(0, START_ITEMS_PER_LOCATION - 1, self.region)
        self.assertEqual(len(locations), START_ITEMS_PER_LOCATION)

        # Check names
        expected_names = [
            "Challenge_1_0", "Challenge_2_0", "Challenge_3_0",
            "Challenge_1_1", "Challenge_2_1", "Challenge_3_1",
            "Challenge_1_2", "Challenge_2_2", "Challenge_3_2",
            "Challenge_1_3", "Challenge_2_3", "Challenge_3_3",
        ]
        for loc, expected_name in zip(locations, expected_names):
            self.assertEqual(loc.name, expected_name)
            self.assertEqual(loc.player, self.player)
            self.assertIn(loc.address, self.regions.location_name_to_id.values())


    def test_locations_after_sphere_one(self):
        end = START_ITEMS_PER_LOCATION + (ITEMS_PER_LOCATION * 3)
        locations = self.regions._locations_to_region(START_ITEMS_PER_LOCATION, end - 1, self.region)
        self.assertEqual(len(locations), end - START_ITEMS_PER_LOCATION)

        # Check names
        expected_names = [
            "Challenge_1_4", "Challenge_2_4", "Challenge_3_4",
            "Challenge_1_5", "Challenge_2_5", "Challenge_3_5",
            "Challenge_1_6", "Challenge_2_6", "Challenge_3_6",
        ]
        for loc, expected_name in zip(locations, expected_names):
            self.assertEqual(loc.name, expected_name)
            self.assertEqual(loc.player, self.player)
            self.assertIn(loc.address, self.regions.location_name_to_id.values())


    def test_no_duplicate_locations(self):
        locations = self.regions._locations_to_region(0, 30, self.region)
        names = [loc.name for loc in locations]
        self.assertEqual(len(names), len(set(names)), "Duplicate location names found!")


    def test_regions_chain(self):
        item_length = 35
        self.regions.create(item_length)

        total_items = item_length - 1

        # Check Levels
        remaining_items_after_level_0 = total_items - START_ITEMS_PER_LOCATION
        total_levels = math.ceil(remaining_items_after_level_0 / 3)

        # + 1 for level_0
        num_levels: int = total_levels + 1

        expected_regions = ["Menu", "Challenges"]
        expected_regions += [f"Parkitect_Challenge_Level_{i}" for i in range(num_levels)]
        expected_regions += ["Victory"]

        # check Region/Level
        actual_region_names = [r.name for r in self.multiworld.regions]
        for name in expected_regions:
            self.assertIn(name, actual_region_names, f"Region {name} missing!")

        # check Locations
        all_locations = list(self.multiworld.get_locations(self.player))
        self.assertEqual(len(all_locations), item_length + 1, "Location count incorrect (+1 for Victory)")

        for index, location in enumerate(all_locations[:-1]):  # skip Victory
            location_name = self._expected_location_name(index)
            self.assertEqual(location.name, location_name, "Location name does not match")
            self.assertEqual(location.player, self.player, "Location player does not match")
            self.assertIn(location.address, self.regions.location_name_to_id.values())

        # check Victory
        victory = all_locations[-1]
        self.assertEqual(victory.name, "Victory")

        # check Chain
        region_menu = self.multiworld.get_region("Menu", self.player)
        region_challenges = self.multiworld.get_region("Challenges", self.player)
        self.assertIn(region_challenges, [e.connected_region for e in region_menu.exits])

        for i in range(num_levels):
            region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{i}", self.player)

            if i < num_levels - 1:
                next_region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{i + 1}", self.player)
            else:
                next_region = self.multiworld.get_region("Victory", self.player)

            self.assertIn(next_region, [e.connected_region for e in region.exits])


    def test_get_region_from_parkitect_location(self):
        expected: list[str] = []
        expected.extend(["Parkitect_Challenge_Level_0"] * START_ITEMS_PER_LOCATION)
        expected.extend(["Parkitect_Challenge_Level_1"] * ITEMS_PER_LOCATION)
        expected.extend(["Parkitect_Challenge_Level_2"] * ITEMS_PER_LOCATION)
        expected.extend(["Parkitect_Challenge_Level_3"] * ITEMS_PER_LOCATION)
        expected.extend(["Parkitect_Challenge_Level_4"] * ITEMS_PER_LOCATION)
        expected.append("Parkitect_Challenge_Level_5")

        for index, level in enumerate(expected):
            l = Regions.get_region_from_parkitect_location(index)
            self.assertEqual(l, level)


    @staticmethod
    def _expected_location_name(index: int):
        if index < 3:
            return f"Challenge_{index + 1}_0"

        challenge_map = {0: "Challenge_1", 1: "Challenge_2", 2: "Challenge_3"}
        challenge = challenge_map[index % 3]
        id_num = index // 3

        return f"{challenge}_{id_num}"
