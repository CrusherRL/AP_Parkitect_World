import math
from typing import Dict

from BaseClasses import MultiWorld, Region, Location
from worlds.generic.Rules import add_rule

from ..data.constants import BASE_ID
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
  def get_previous_region_from_parkitect_location(location_number: int):
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
        locationName = f"Challenge_{location}_0"
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

  def create(self, item_length) -> None:
    m = Region("Menu", self.player, self.multiworld)
    m.locations = []
    self.multiworld.regions.append(m)

    c = Region("Challenges", self.player, self.multiworld)
    c.locations = []
    self.multiworld.regions.append(c)

    # first Challenges we can submit easily
    # Also just a show how the flow should look alike
    level_0 = Region("Parkitect_Challenge_Level_0", self.player, self.multiworld)  # Levels of the unlock tree
    level_0.locations = [
      ParkitectLocation(self.player, "Challenge_1_0", self.location_name_to_id["Challenge_1_0"], level_0),
      ParkitectLocation(self.player, "Challenge_2_0", self.location_name_to_id["Challenge_2_0"], level_0),
      ParkitectLocation(self.player, "Challenge_3_0", self.location_name_to_id["Challenge_3_0"], level_0),
    ]
    self.multiworld.regions.append(level_0)

    current_level = 1
    item = 3

    while (item + 2) < item_length:
      level = Region("Parkitect_Challenge_Level_" + str(current_level), self.player, self.multiworld)
      level.locations = self._locations_to_region(item, item + 2, level)
      self.multiworld.regions.append(level)
      item += 3
      current_level += 1

    # fill rest of items, if there are any
    if item != item_length:
      end_level = Region("Parkitect_Challenge_Level_" + str(current_level), self.player, self.multiworld)
      end_level.locations = self._locations_to_region(item, (item_length - 1), end_level)
      self.multiworld.regions.append(end_level)
      current_level += 1

    current_level -= 1
   
    victory = Region("Victory", self.player, self.multiworld)
    victory.locations = [ParkitectLocation(self.player, "Victory", None, victory)]
    self.multiworld.regions.append(victory)

    m.connect(c)
    c.connect(self.multiworld.get_region("Parkitect_Challenge_Level_0", self.player))

    count = 0
    while count < current_level:
      region = self.multiworld.get_region(f"Parkitect_Challenge_Level_{count}", self.player)
      region_entrance = region.connect(self.multiworld.get_region(f"Parkitect_Challenge_Level_{count + 1}", self.player))
      num_rides = 0
      num_shops = 0

      if count == 0:
        pass

      elif count == 1:  # 5 total items, we want 1 ride and 1 shop
        num_rides = 1
        num_shops = 1

      elif count == 2:  # 8 total items, we want 3 rides and 2 shops
        num_rides = 3
        num_shops = 2

      elif count == 4 or count == 5:  # 14 total items, we want 3 rides and 3 shops
        num_rides = 3
        num_shops = 3

      elif count == 6:  # 20 total items, we want 5 rides and 4 shops
        num_rides = 5
        num_shops = 4

      elif count == 7:  # 23 total items, we want 6 rides and 5 shops
        num_rides = 6
        num_shops = 5

      add_rule(region_entrance, lambda state, num=num_rides: state.has_group("Rides", self.player, num))
      add_rule(region_entrance, lambda state, num=num_shops: state.has_group("Shops", self.player, num))
      count += 1

    final_region = self.multiworld.get_region("Parkitect_Challenge_Level_" + str(current_level), self.player)
    final_region.connect(victory)

    all_locations = list(self.multiworld.get_locations(self.player))
    location_count = len(all_locations) - 1

    LoggerHelper.log(all_locations, "all locations")
    # They must be equal
    assert location_count == item_length, "Fillable Locations and Items aren't equal"

    visualize_regions(m, 'parkitect-regions')
