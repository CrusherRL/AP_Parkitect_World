from typing import Any

from BaseClasses import Tutorial, ItemClassification, Entrance, CollectionRule
from rule_builder.rules import Rule
from worlds.AutoWorld import World, WebWorld

from .src.Options import ParkitectOptions, parkitect_option_groups
from .src.Items import get_items
from .src.Regions import Regions, ParkitectLocation
from .src.RegionsV2 import RegionsV2
from .src.LoggerHelper import LoggerHelper
from .src.Item import ParkitectItem, ItemHelper
from .src.Rules import Rules
from .src.RulesV2 import RulesV2
from .src.ParkitectGoals import ParkitectGoals

from .data.items import *
from .data.constants import AP_WORLD_VERSION, ITEM_NAME_TO_ID, LOCATION_NAME_TO_ID, THEME, FAIL, TASTE_OF_ADVENTURE_SCENARIOS, LOCATION_NAME_TO_ID_V2

class ParkitectWebWorld(WebWorld):
  theme = THEME

  setup_en = Tutorial(
    "Multiworld Setup Guide",
    "A guide to setting up the Parkitect randomizer on your computer.",
    "English",
    "setup_en.md",
    "setup/en",
    ["Crusher"]
  )

  tutorials = [setup_en]
  option_groups = parkitect_option_groups


class ParkitectWorld(World):
  """
  Parkitect is a modern take on classic theme park tycoon games where you build and manage the theme parks of your dreams!
  Construct your own coasters, design efficiently operating parks that fully immerse your guests in their theming and play through the campaign.
  """

  game = "Parkitect"
  web = ParkitectWebWorld()
  options_dataclass = ParkitectOptions
  options: ParkitectOptions

  location_name_to_id = LOCATION_NAME_TO_ID
  location_name_to_id_v2 = LOCATION_NAME_TO_ID_V2
  item_name_to_id = ITEM_NAME_TO_ID
  item_name_groups = {
    TYPE_RIDES: RIDES[TYPE_ALL],
    TYPE_CALM_RIDES: RIDES[TYPE_CALM_RIDES],
    TYPE_THRILL_RIDES: RIDES[TYPE_THRILL_RIDES],
    TYPE_COASTER_RIDES: RIDES[TYPE_COASTER_RIDES],
    TYPE_WATER_RIDES: RIDES[TYPE_WATER_RIDES],
    TYPE_TRANSPORT_RIDES: RIDES[TYPE_TRANSPORT_RIDES],
    TYPE_SHOPS: SHOPS[TYPE_ALL],
    TYPE_SHOP_DRINKS: SHOPS[TYPE_SHOP_DRINKS],
    TYPE_SHOP_FOOD: SHOPS[TYPE_SHOP_FOOD],
    TYPE_SHOP_FACILITIES: SHOPS[TYPE_SHOP_FACILITIES],
    TYPE_DECORATIONS: DECORATION_THEMES[TYPE_ALL],
  }

  def __init__(self, multiworld, player: int):
    super().__init__(multiworld, player)
    self.starter = None
    self.item_table = []
    self.challenges: dict[str, str] = {} # Parkitect Challenge Window


  def validate_scenario_dlc(self) -> None:
    if self.options.scenario.value in TASTE_OF_ADVENTURE_SCENARIOS:
      assert self.options.dlc1.value, f"Parkitect scenario \"{self.options.scenario.value}\" requires DLC \"{self.options.dlc1.display_name}\" to be set to yes."


  def handle_early_items(self):
    item_helper = ItemHelper(self.starter)

    if self.options.early_toilets.value and item_helper.item != TOILETS:
      self.multiworld.early_items[self.player][TOILETS] = 1

    if self.options.early_cash_machine.value and item_helper.item != CASH_MACHINE:
      self.multiworld.early_items[self.player][CASH_MACHINE] = 1

    if self.options.early_first_aid_room.value and item_helper.item != FIRST_AID_ROOM:
      self.multiworld.early_items[self.player][FIRST_AID_ROOM] = 1

    if self.options.utility_buildings.value:
      if self.options.early_staff_room.value and item_helper.item != UTILITY_BUILDING_STAFF_ROOM:
        self.multiworld.early_items[self.player][UTILITY_BUILDING_STAFF_ROOM] = 1

      if self.options.early_staff_room.value and item_helper.item != UTILITY_BUILDING_TRAINING_ROOM:
        self.multiworld.early_items[self.player][UTILITY_BUILDING_TRAINING_ROOM] = 1

    if self.options.early_edible_shop.value and not (
      item_helper.is_food_shop() or item_helper.is_drink_shop()
    ):
      while True:
        candidate = ItemHelper(
          self.random.choice(self.item_table)
        )
        if candidate.is_food_shop() or candidate.is_drink_shop():
          self.multiworld.early_items[self.player][candidate.item] = 1
          break

    if self.options.early_attraction.value and not item_helper.is_ride():
      while True:
        candidate = ItemHelper(
          self.random.choice(self.item_table)
        )
        if candidate.is_ride():
          self.multiworld.early_items[self.player][candidate.item] = 1
          break

    if self.options.early_decoration.value and self.options.decorations and not item_helper.is_decoration_themes():
      while True:
        candidate = ItemHelper(
          self.random.choice(self.item_table)
        )
        if candidate.is_decoration_themes():
          self.multiworld.early_items[self.player][candidate.item] = 1
          break


  def generate_early(self) -> None:
    self.validate_scenario_dlc()
    item_table, self.starter = get_items(self)
    self.random.shuffle(item_table)
    self.item_table = item_table
    self.handle_early_items()

    LoggerHelper.log(len(self.item_table), "Total Items")


  def create_regions(self) -> None:
    if self.options.randomizer_v2.value:
      RegionsV2(self).create((len(self.item_table)))
    else:
      Regions(self.player, self.multiworld, self.location_name_to_id, self._set_rule).create((len(self.item_table)))

    LoggerHelper.log("Created Regions and their locations")


  def create_items(self) -> None:
    for item in self.item_table:
      self.multiworld.itempool.append(self.create_item(item))

    assert len(self.multiworld.itempool) > 0, "No Items found in Itempool"
    LoggerHelper.log("Created Items and added to pool")
  
    # Adds the starting ride to precollected items
    parkitect_item_starter = self.create_item(self.starter)
    self.multiworld.push_precollected(parkitect_item_starter)

    assert parkitect_item_starter in self.multiworld.precollected_items[self.player], "Starter not found in precollected items"
    LoggerHelper.log("Added starter as precollect")


  def create_item(self, item: str) -> ParkitectItem:
    # A classification must be set, otherwise it's an error
    classification = ItemClassification.useful

    if item in RIDES[TYPE_ALL] or item in SHOPS[TYPE_ALL] or item in UTILITY_BUILDINGS[TYPE_ALL] or item == DECORATION_THEME_GENERIC:
      classification = ItemClassification.progression

    elif item in TRAPS[TYPE_ALL]:
      classification = ItemClassification.trap

    elif item in STATISTICS[TYPE_ALL]:
      classification = ItemClassification.filler

    assert item in self.item_name_to_id, f"Item \"{item}\" is not found in \"item_name_to_id\""

    return ParkitectItem(item, classification, self.item_name_to_id[item], self.player)


  def generate_basic(self) -> None:
    # place "Victory" at the end of the unlock tree and set collection as win condition
    self.multiworld.get_location("Victory", self.player).place_locked_item(
      ParkitectItem("Victory", ItemClassification.progression, None, self.player)
    )
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


  def set_rules(self) -> None:
    if self.options.randomizer_v2.value:
      RulesV2(self).set()
    else:
      Rules(self, self._set_rule).set()

    LoggerHelper.log("Set Rules")


  def fill_slot_data(self):
    seed = "_".join([
      str(self.options.scenario.value),
      self.multiworld.player_name[self.player],
      str(self.multiworld.seed_name)
    ])

    parkitect_goals = ParkitectGoals(self.options)

    slot_data = self.options.as_dict(
      "scenario",
    )
    slot_data["goals"] = parkitect_goals.to_dict()
    slot_data["rules"] = self.options.as_dict(
      "difficulty",
      "guests_money_flux",
      "progressive_speedups",
      "utility_buildings",
      "decorations",
      "statistics",
      "trap_link",
      "release_mode",
    )
    
    slot_data["randomizer_v2"] = self.options.randomizer_v2.value
    slot_data["seed"] = seed
    slot_data["version"] = AP_WORLD_VERSION
    slot_data["challenges"] = self.challenges

    LoggerHelper.log(self.item_table, "Item Pool")
    LoggerHelper.log(dict(slot_data), "Slot data")

    if FAIL == True:
      if len(parkitect_goals.shops) > 0:
        LoggerHelper.force_info(self.starter)
        return True

    return slot_data
