import unittest

from BaseClasses import MultiWorld

from ..src.Regions import Regions

from ..data.constants import LOCATION_NAME_TO_ID

class TestRegions(unittest.TestCase):
  def setUp(self):
    self.player = 1
    self.multiworld = MultiWorld(1)
    self.region = type("DummyRegion", (), {})() # Simple object with locations
    self.regions = Regions(self.player, self.multiworld, LOCATION_NAME_TO_ID)

    # Dummy IDs for all locations
    self.location_ids = {}
    for i in range(10):
      for c in range(1, 4):
        self.location_ids[f"Challenge_{c}_{i}"] = i*3 + c

  def _expected_location_name(self, index: int):
    if index < 3:
        return f"Challenge_{index + 1}_0"

    challenge_map = {0: "Challenge_1", 1: "Challenge_2", 2: "Challenge_3"}
    challenge = challenge_map[index % 3]
    id_num = index // 3

    return f"{challenge}_{id_num}"

  def test_first_three_locations(self):
    locations = self.regions._locations_to_region(0, 2, self.region)
    
    # Check count
    self.assertEqual(len(locations), 3)
    
    # Check names
    expected_names = ["Challenge_1_0", "Challenge_2_0", "Challenge_3_0"]
    for loc, expected_name in zip(locations, expected_names):
      self.assertEqual(loc.name, expected_name)
      self.assertEqual(loc.player, self.player)
      self.assertIn(loc.address, self.regions.location_name_to_id.values())

  def test_later_level_locations(self):
    # example location 3 - 8
    locations = self.regions._locations_to_region(3, 8, self.region)
    self.assertEqual(len(locations), 6)
    
    # Check names
    expected_names = [
      "Challenge_1_1", "Challenge_2_1", "Challenge_3_1",
      "Challenge_1_2", "Challenge_2_2", "Challenge_3_2"
    ]
    for loc, expected_name in zip(locations, expected_names):
      self.assertEqual(loc.name, expected_name)
      self.assertEqual(loc.player, self.player)
      self.assertIn(loc.address, self.regions.location_name_to_id.values())

  def test_no_duplicate_locations(self):
    locations = self.regions._locations_to_region(0, 8, self.region)
    names = [loc.name for loc in locations]
    self.assertEqual(len(names), len(set(names)), "Duplicate location names found!")

  def test_regions_chain(self):
      item_length = 12
      self.regions.create(item_length)

      # 1️⃣ Prüfe die Region-Namen
      num_levels = ((item_length - 1) // 3) + 1
      expected_regions = ["Menu", "Challenges"]
      expected_regions += [f"Parkitect_Challenge_Level_{i}" for i in range(num_levels)]
      expected_regions += ["Victory"]

      actual_region_names = [r.name for r in self.multiworld.regions]
      for name in expected_regions:
        self.assertIn(name, actual_region_names, f"Region {name} fehlt!")

      # 2️⃣ Prüfe Locations
      all_locations = list(self.multiworld.get_locations(self.player))
      self.assertEqual(len(all_locations), item_length + 1, "Location count stimmt nicht (+1 für Victory)")

      seen_names = set()

      for idx, loc in enumerate(all_locations[:-1]):  # Victory auslassen
        expected_name = self._expected_location_name(idx)
        self.assertEqual(loc.name, expected_name)
        self.assertEqual(loc.player, self.player)
        self.assertIn(loc.address, self.regions.location_name_to_id.values())
        seen_names.add(loc.name)

      # Victory prüfen
      victory = all_locations[-1]
      self.assertEqual(victory.name, "Victory")

      # 3️⃣ Prüfe die Verbindungen
      menu_region = self.multiworld.get_region("Menu", self.player)
      challenges_region = self.multiworld.get_region("Challenges", self.player)
      self.assertIn(challenges_region, [e.connected_region for e in menu_region.exits])

      for i in range(num_levels):
        region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{i}", self.player)

        if i < num_levels - 1:
          next_region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{i+1}", self.player)
        else:
          next_region = self.multiworld.get_region("Victory", self.player)

        self.assertIn(next_region, [e.connected_region for e in region.exits])

  def test_get_previous_region_from_parkitect_location(self):
    expected = [
      "Parkitect_Challenge_Level_0",
      "Parkitect_Challenge_Level_0",
      "Parkitect_Challenge_Level_0",
      "Parkitect_Challenge_Level_1",
      "Parkitect_Challenge_Level_1",
      "Parkitect_Challenge_Level_1",
      "Parkitect_Challenge_Level_2",
      "Parkitect_Challenge_Level_2",
      "Parkitect_Challenge_Level_2",
      "Parkitect_Challenge_Level_3",
      "Parkitect_Challenge_Level_3",
      "Parkitect_Challenge_Level_3",
      "Parkitect_Challenge_Level_4",
      "Parkitect_Challenge_Level_4",
      "Parkitect_Challenge_Level_4",
      "Parkitect_Challenge_Level_5",
    ]

    for index, level in enumerate(expected):
      l = Regions.get_previous_region_from_parkitect_location(index)
      self.assertEqual(l, level)
