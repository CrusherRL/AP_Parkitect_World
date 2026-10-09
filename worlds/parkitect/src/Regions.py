import math

from typing import Dict
from BaseClasses import MultiWorld, Region, Location
from ..data.constants import DEBUG, ITEMS_PER_LOCATION_LEGACY, START_ITEMS_PER_LOCATION_LEGACY
from .LoggerHelper import LoggerHelper
from Utils import visualize_regions

class ParkitectLocation(Location):
  game = "Parkitect"


class Regions:
  def __init__(self, player: int, multiworld: "MultiWorld", location_name_to_id: Dict[str, int], _set_rule):
    self.player = player
    self.multiworld = multiworld
    self.location_name_to_id = location_name_to_id
    self._set_rule = _set_rule


  @staticmethod
  def get_location_name_from_index(location_number: int) -> str:
    if location_number < 3:
      return f"Challenge_{location_number + 1}_0"

    challenge_map = {
      0: "Challenge_1",
      1: "Challenge_2",
      2: "Challenge_3",
    }
    challenge = challenge_map[location_number % 3]
    id_num = location_number // 3
    return f"{challenge}_{id_num}"


  @staticmethod
  def get_region_from_parkitect_location(location_number: int) -> str:
    if location_number < START_ITEMS_PER_LOCATION_LEGACY:
      return "Parkitect_Challenge_Level_0"

    additional_levels = int(START_ITEMS_PER_LOCATION_LEGACY / ITEMS_PER_LOCATION_LEGACY) - 1 # 1 because of index

    # level = -> (items - 1) / rows
    # level 1 -> 3 / 3
    # 3/3 = 1; -> floor = 1
    # 4/3 = 1.33; -> floor = 1
    # 5/3 = 1.66; -> floor = 1

    # level = -> (items - 1) / rows
    # level 2 -> 6 / 3
    # 6/3 = 2; -> floor = 2
    # 7/3 = 2.33; -> floor = 2
    # 8/3 = 2.66; -> floor = 2
    level = math.floor(location_number / ITEMS_PER_LOCATION_LEGACY)
    return f"Parkitect_Challenge_Level_{level - additional_levels}"


  def _locations_to_region(self, location, ending_location, chosen_region):
    locations = []

    while location <= ending_location:
      if location < 3:
        location_name = f"Challenge_{location + 1}_0"
        locations.append(ParkitectLocation(
          self.player,
          location_name,
          self.location_name_to_id[location_name], chosen_region
        ))

      else:
        challenge_map = {
          0: "Challenge_1",
          1: "Challenge_2",
          2: "Challenge_3",
        }
        challenge = challenge_map[location % 3]
        challenge_id = math.floor(location / 3)
        location_name = f"{challenge}_{challenge_id}"

        locations.append(ParkitectLocation(
          self.player,
          location_name,
          self.location_name_to_id[location_name],
          chosen_region
        ))

      location += 1
    return locations


  def create(self, item_length: int) -> None:
    m = Region("Menu", self.player, self.multiworld)
    m.locations = []
    self.multiworld.regions.append(m)

    c = Region("Challenges", self.player, self.multiworld)
    c.locations = []
    self.multiworld.regions.append(c)

    # Connecting Menu with Challenges
    m.connect(c)

    # first Challenges we can submit easily
    # Also just a show how the flow should look alike
    level_0 = Region("Parkitect_Challenge_Level_0", self.player, self.multiworld)  # Levels of the unlock tree

    # So have a fixed issue for early items, we provide enough first challenges
    level_0.locations = [
      ParkitectLocation(self.player, "Challenge_1_0", self.location_name_to_id["Challenge_1_0"], level_0),
      ParkitectLocation(self.player, "Challenge_2_0", self.location_name_to_id["Challenge_2_0"], level_0),
      ParkitectLocation(self.player, "Challenge_3_0", self.location_name_to_id["Challenge_3_0"], level_0),
      ParkitectLocation(self.player, "Challenge_1_1", self.location_name_to_id["Challenge_1_1"], level_0),
      ParkitectLocation(self.player, "Challenge_2_1", self.location_name_to_id["Challenge_2_1"], level_0),
      ParkitectLocation(self.player, "Challenge_3_1", self.location_name_to_id["Challenge_3_1"], level_0),
      ParkitectLocation(self.player, "Challenge_1_2", self.location_name_to_id["Challenge_1_2"], level_0),
      ParkitectLocation(self.player, "Challenge_2_2", self.location_name_to_id["Challenge_2_2"], level_0),
      ParkitectLocation(self.player, "Challenge_3_2", self.location_name_to_id["Challenge_3_2"], level_0),
      ParkitectLocation(self.player, "Challenge_1_3", self.location_name_to_id["Challenge_1_3"], level_0),
      ParkitectLocation(self.player, "Challenge_2_3", self.location_name_to_id["Challenge_2_3"], level_0),
      ParkitectLocation(self.player, "Challenge_3_3", self.location_name_to_id["Challenge_3_3"], level_0),
    ]
    self.multiworld.regions.append(level_0)

    # Connecting Challenges to first level
    c.connect(level_0)

    current_level = 1
    current_item_count = len(level_0.locations)

    while (current_item_count + ITEMS_PER_LOCATION_LEGACY) <= item_length:
      LoggerHelper.info(f"{current_level} - {current_item_count}")
      level = Region(f"Parkitect_Challenge_Level_{current_level}", self.player, self.multiworld)
      level.locations = self._locations_to_region(current_item_count, current_item_count + ITEMS_PER_LOCATION_LEGACY - 1, level)
      self.multiworld.regions.append(level)

      # connect them
      if current_level != 1:
        previous_level = self.multiworld.get_region(f"Parkitect_Challenge_Level_{current_level - 1}", self.player)
      else:
        previous_level = level_0

      previous_level.connect(level)

      current_item_count += ITEMS_PER_LOCATION_LEGACY
      current_level += 1

    LoggerHelper.info(f"ending: {current_level} - {current_item_count}")
    current_level -= 1

    # fill rest of items, if there are any
    if current_item_count < item_length:
      LoggerHelper.info("setting extra end level")
      end_level = Region(f"Parkitect_Challenge_Level_{current_level + 1}", self.player, self.multiworld)
      end_level.locations = self._locations_to_region(current_item_count, item_length - 1, end_level)
      self.multiworld.regions.append(end_level)

      previous_level = self.multiworld.get_region(f"Parkitect_Challenge_Level_{current_level}", self.player)
      previous_level.connect(end_level)

      current_level += 1

    all_locations = list[Location](self.multiworld.get_locations(self.player))
    location_count = len(all_locations)

    victory = Region("Victory", self.player, self.multiworld)
    victory.locations = [ParkitectLocation(self.player, "Victory", None, victory)]
    self.multiworld.regions.append(victory)

    final_region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{current_level}", self.player)
    final_region.connect(victory)

    LoggerHelper.log(all_locations, "all locations")

    if DEBUG:
      visualize_regions(m, './worlds/parkitect/generated/parkitect-regions')

    LoggerHelper.log(item_length, "item_length")
    LoggerHelper.log(location_count, "location_count")

    assert location_count == item_length, "Fillable Locations and Items aren't equal"
