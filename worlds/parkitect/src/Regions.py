import math
from typing import Dict

from BaseClasses import MultiWorld, Region, Location
from worlds.generic.Rules import add_rule
from worlds.parkitect.data.items import TYPE_RIDES, TYPE_SHOPS

from ..data.constants import DEBUG
from .LoggerHelper import LoggerHelper

from Utils import visualize_regions

class ParkitectLocation(Location):
  game = "Parkitect"

class Regions:
  def __init__(self, player: int, multiworld: "MultiWorld", location_name_to_id: Dict[str, int]):
    self.player = player
    self.multiworld = multiworld
    self.location_name_to_id = location_name_to_id

  @staticmethod
  def get_region_from_parkitect_location(location_number: int):
    if location_number <= 2:
      return "Parkitect_Challenge_Level_0"

    if location_number <= 5:
      return "Parkitect_Challenge_Level_1"

    # level 3 -> 5 items / 3 rows
    # 6-5 = 1; 1/3 = 0.33; 0.33+1 = 1.33; -> ceil = 2
    # 7-5 = 2; 2/3 = 0.66; 0.66+1 = 1.66; -> ceil = 2
    # 8-5 = 3; 3/3 = 1; 1+1 = 2; -> ceil = 2
    # 9-5 = 4; 4/3 = 1.33; 0.33+1 = 2.33; -> ceil = 3
    id = math.ceil((location_number - 5) / 3) + 1
    return f"Parkitect_Challenge_Level_{id}"
    
  def _locations_to_region(self, location, ending_location, chosen_region):
    locations = []

    while location <= ending_location:
      if location < 3:
        locationName = f"Challenge_{location + 1}_0"
        locations.append(ParkitectLocation(
          self.player,
          locationName,
          self.location_name_to_id[locationName], chosen_region
        ))

      else:
        challenge_map = {
          0: "Challenge_1",
          1: "Challenge_2",
          2: "Challenge_3",
        }
        challenge = challenge_map[location % 3]
        id = math.floor(location / 3)
        locationName = f"{challenge}_{id}"

        locations.append(ParkitectLocation(
          self.player,
          locationName,
          self.location_name_to_id[locationName],
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
    level_0.locations = [
      ParkitectLocation(self.player, "Challenge_1_0", self.location_name_to_id["Challenge_1_0"], level_0),
      ParkitectLocation(self.player, "Challenge_2_0", self.location_name_to_id["Challenge_2_0"], level_0),
      ParkitectLocation(self.player, "Challenge_3_0", self.location_name_to_id["Challenge_3_0"], level_0),
    ]
    self.multiworld.regions.append(level_0)

    # Connecting Challenges to first level
    c.connect(level_0)

    current_level = 1
    item = 3

    while (item + 3) <= item_length:
      LoggerHelper.info(f"{current_level} - {item}")
      level = Region(f"Parkitect_Challenge_Level_{current_level}", self.player, self.multiworld)
      level.locations = self._locations_to_region(item, item + 2, level)
      self.multiworld.regions.append(level)

      # connect them
      if (current_level != 1):
        previous_level = self.multiworld.get_region(f"Parkitect_Challenge_Level_{current_level - 1}", self.player)
      else:
        previous_level = level_0

      previous_level.connect(level)

      item += 3
      current_level += 1

    LoggerHelper.info(f"ending: {current_level} - {item}")
    current_level -= 1

    # fill rest of items, if there are any
    if item < item_length:
      LoggerHelper.info("setting extra end level")
      end_level = Region(f"Parkitect_Challenge_Level_{current_level + 1}", self.player, self.multiworld)
      end_level.locations = self._locations_to_region(item, item_length - 1, end_level)
      self.multiworld.regions.append(end_level)

      previous_level = self.multiworld.get_region(f"Parkitect_Challenge_Level_{current_level}", self.player)
      previous_level.connect(end_level)

      current_level += 1

    all_locations = list[Location](self.multiworld.get_locations(self.player))
    location_count = len(all_locations)

    # Playthrough
    for level_index in range(1, current_level):
      region_name = f"Parkitect_Challenge_Level_{level_index}"
      region = self.multiworld.get_region(region_name, self.player)
      
      if not region.entrances:
        continue
        
      region_entrance = region.entrances[0]
      num_shops = 0
      num_rides = 0
      
      # Determine required ride and/or shop count based on level
      if level_index == 1:
        num_rides = 1
        num_shops = 1

      elif level_index == 2:
        num_rides = 3
        num_shops = 2

      elif level_index == 3:
        num_rides = 4
        num_shops = 3

      elif level_index == 4:
        num_rides = 5
        num_shops = 4

      elif level_index == 5:
        num_rides = 7
        num_shops = 5

      elif level_index == 6:
        num_rides = 9
        num_shops = 7

      elif level_index == 7:
        num_rides = 12
        num_shops = 9

      elif level_index == 8:
        num_rides = 13
        num_shops = 11
      
      add_rule(region_entrance, lambda state, count=num_rides: state.has_group(TYPE_RIDES, self.player, count))
      add_rule(region_entrance, lambda state, count=num_shops: state.has_group(TYPE_SHOPS, self.player, count), "or" if level_index == 1 else "and")

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
