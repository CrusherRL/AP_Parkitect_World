import math

from BaseClasses import  Region, Location
from rule_builder.rules import HasGroup
from ..data.items import TYPE_RIDES, TYPE_SHOPS
from ..data.constants import DEBUG, ITEMS_PER_LOCATION, START_ITEMS_PER_LOCATION, REGION_NAME
from .LoggerHelper import LoggerHelper
from Utils import visualize_regions

class ParkitectLocation(Location):
  game = "Parkitect"


class RegionsV2:
  def __init__(self, world):
    self.world = world


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
    if location_number < START_ITEMS_PER_LOCATION:
      return f"{REGION_NAME} 1"

    additional_levels = int(START_ITEMS_PER_LOCATION / ITEMS_PER_LOCATION) - 1 # 1 because of index

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
    level = math.floor(location_number / ITEMS_PER_LOCATION)
    return f"{REGION_NAME} {level - additional_levels}"


  def _locations_to_region(self, start: int, end: int, chosen_region: Region) -> list[ParkitectLocation]:
    locations = []
    count = start

    while count <= end:
      if count < START_ITEMS_PER_LOCATION:
        location_name = f"Level 1 Challenge {count}"
        locations.append(ParkitectLocation(
          self.world.player,
          location_name,
          self.world.location_name_to_id_v2[location_name], chosen_region
        ))

      else:
        level = math.ceil((count - START_ITEMS_PER_LOCATION + ITEMS_PER_LOCATION) / ITEMS_PER_LOCATION)
        item_index = (count - START_ITEMS_PER_LOCATION - 1) % 5
        location_name = f"Level {level} Challenge {item_index + 1}"
        locations.append(ParkitectLocation(
          self.world.player,
          location_name,
          self.world.location_name_to_id_v2[location_name], chosen_region
        ))

      count += 1

    return locations


  def create(self, item_length: int) -> None:
    m = Region("Menu", self.world.player, self.world.multiworld)
    m.locations = []
    self.world.multiworld.regions.append(m)

    c = Region("Challenges", self.world.player, self.world.multiworld)
    c.locations = []
    self.world.multiworld.regions.append(c)

    # Connecting Menu with Challenges
    m.connect(c)

    # first Challenges we can submit easily
    # Also just a show how the flow should look alike
    level_1 = Region(f"{REGION_NAME} 1", self.world.player, self.world.multiworld)  # Levels of the unlock tree

    # So have a fixed issue for early items, we provide enough first challenges
    level_1.locations = [
      ParkitectLocation(self.world.player, f"Level 1 Challenge {item}", self.world.location_name_to_id_v2[f"Level 1 Challenge {item}"], level_1) for item in (range(1, START_ITEMS_PER_LOCATION + 1))
    ]
    self.world.multiworld.regions.append(level_1)

    # Connecting Challenges to first level
    c.connect(level_1)

    current_level = 2
    current_item_count = len(level_1.locations)

    while (current_item_count + ITEMS_PER_LOCATION) <= item_length:
      LoggerHelper.info(f"level {current_level} = {current_item_count}-{current_item_count + ITEMS_PER_LOCATION}")
      level = Region(f"{REGION_NAME} {current_level}", self.world.player, self.world.multiworld)
      level.locations = self._locations_to_region(current_item_count + 1, current_item_count + ITEMS_PER_LOCATION, level)
      self.world.multiworld.regions.append(level)

      # connect them
      if current_level != 2:
        previous_level = self.world.multiworld.get_region(f"{REGION_NAME} {current_level - 1}", self.world.player)
      else:
        previous_level = level_1

      previous_level.connect(level)

      current_item_count += ITEMS_PER_LOCATION
      current_level += 1

    LoggerHelper.info(f"ending: {current_level} - {current_item_count}")

    # fill rest of items, if there are any
    if current_item_count < item_length:
      LoggerHelper.info("setting extra end level")
      end_level = Region(f"{REGION_NAME} {current_level}", self.world.player, self.world.multiworld)
      end_level.locations = self._locations_to_region(current_item_count + 1, item_length, end_level)
      self.world.multiworld.regions.append(end_level)

      previous_level = self.world.multiworld.get_region(f"{REGION_NAME} {current_level - 1}", self.world.player)
      previous_level.connect(end_level)

      current_level += 1

    current_level -= 1

    all_locations = list[Location](self.world.multiworld.get_locations(self.world.player))
    location_count = len(all_locations)

    # Playthrough
    for level in range(1, current_level):
      region_name = f"{REGION_NAME} {level}"
      region = self.world.multiworld.get_region(region_name, self.world.player)

      if not region.entrances:
        continue

      self.world.set_rule(region.entrances[0], HasGroup(TYPE_RIDES) | HasGroup(TYPE_SHOPS))

    victory = Region("Victory", self.world.player, self.world.multiworld)
    victory.locations = [ParkitectLocation(self.world.player, "Victory", None, victory)]
    self.world.multiworld.regions.append(victory)

    final_region = self.world.multiworld.get_region(f"{REGION_NAME} {current_level}", self.world.player)
    final_region.connect(victory)

    LoggerHelper.log(all_locations, "all locations")

    if DEBUG:
      visualize_regions(m, './worlds/parkitect/generated/parkitect-regions-v2')

    LoggerHelper.log(item_length, "item_length")
    LoggerHelper.log(location_count, "location_count")

    assert location_count == item_length, "Fillable Locations and Items aren't equal"
