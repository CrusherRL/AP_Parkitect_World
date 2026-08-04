from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .src.Options import ParkitectOptions, parkitect_option_groups
from .src.Items import get_items
from .src.Regions import Regions
from .src.LoggerHelper import LoggerHelper
from .src.Item import ParkitectItem, ItemHelper
from .src.Rules import Rules

from .data.items import *
from .data.constants import AP_WORLD_VERSION, ITEM_NAME_TO_ID, LOCATION_NAME_TO_ID, THEME, FAIL, TASTE_OF_ADVENTURE_SCENARIOS, EARLY_ITEM_RANGE

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
    self.challenges = [] # Parkitect Challenge Window

  def validate_scenario_dlc(self) -> None:
    if self.options.scenario.value in TASTE_OF_ADVENTURE_SCENARIOS:
      assert self.options.dlc1.value, f"Parkitect scenario \"{self.options.scenario.value}\" requires DLC \"{self.options.dlc1.display_name}\" to be set to yes."

  def reshuffle_items(self, items: list[str]) -> list[str]:
    early_items = self.get_early_items(items)
    early_items_verifier = early_items.copy()

    if len(early_items) == 0:
      return items

    # Remove all early items first
    for item in early_items:
      if item in items:
        items.remove(item)

    # Pick positions in the first 30 slots
    positions = self.random.sample(range(EARLY_ITEM_RANGE), len(early_items))

    # Insert them into their final positions
    for index, item in sorted(zip(positions, early_items)):
      items.insert(index, item)

    self.verify_early_items(early_items_verifier)
    return items

  def verify_early_items(self, items):
    for item in items:
        if items.index(item) >= EARLY_ITEM_RANGE:
          raise Exception(f"{item} was not early: {items.index(item)}")

  def get_early_items(self, items: list[str]) -> list[str]:
    item_helper = ItemHelper(self.starter)
    early_items = []

    if self.options.early_toilets.value and item_helper.item != TOILETS:
      early_items.append(TOILETS)

    if self.options.early_cash_machine.value and item_helper.item != CASH_MACHINE:
      early_items.append(CASH_MACHINE)

    if self.options.early_first_aid_room.value and item_helper.item != FIRST_AID_ROOM:
      early_items.append(FIRST_AID_ROOM)

    if self.options.utility_buildings.value and self.options.early_staff_room.value and item_helper.item != UTILITY_BUILDING_STAFF_ROOM:
      early_items.append(UTILITY_BUILDING_STAFF_ROOM)

    if self.options.utility_buildings.value and self.options.early_training_room.value and item_helper.item != UTILITY_BUILDING_TRAINING_ROOM:
      early_items.append(UTILITY_BUILDING_TRAINING_ROOM)

    if self.options.early_edible_shop.value and not (
      item_helper.is_food_shop() or item_helper.is_drink_shop()
    ):
      while True:
        candidate = ItemHelper(
          self.random.choice(items)
        )
        if candidate.is_food_shop() or candidate.is_drink_shop():
          early_items.append(candidate.item)
          break

    if self.options.early_ride.value and not item_helper.is_ride():
      while True:
        candidate = ItemHelper(
          self.random.choice(items)
        )
        if candidate.is_ride():
          early_items.append(candidate.item)
          break

    if self.options.early_decoration and self.options.decorations and not item_helper.is_decoration_themes():
      while True:
        candidate = ItemHelper(
          self.random.choice(items)
        )
        if candidate.is_decoration_themes():
          early_items.append(candidate.item)
          break

    return early_items

  def generate_early(self) -> None:
    self.validate_scenario_dlc()
    item_table, self.starter = get_items(self)
    item_table_length = len(item_table)
    self.random.shuffle(item_table)
    self.item_table = self.reshuffle_items(item_table)

    assert item_table_length == len(self.item_table), (
      f"Custom shuffling mistake! {item_table_length} != {len(self.item_table)}"
    )
    LoggerHelper.log(len(self.item_table), "Total Items")

  def create_regions(self) -> None:
    Regions(self.player, self.multiworld, self.location_name_to_id).create((len(self.item_table)))
    LoggerHelper.log("Created Regions and their locations + connections")
        
  def create_items(self) -> None:
    for item in self.item_table:
      self.multiworld.itempool.append(self.create_item(item))

    assert len(self.multiworld.itempool) > 0, "No Items found in Itempool"
    LoggerHelper.log("Created Items and added to pool")
  
    # Adds the starting ride to precollected items
    self.multiworld.push_precollected(self.create_item(self.starter))

    assert len(self.multiworld.precollected_items[self.player]) == 1, f"Starter item \"{self.starter}\" was not added to precollected_items"
    LoggerHelper.log("Added starter as precollect")

  def create_item(self, item: str) -> ParkitectItem:
    # A classification must be set, otherwise its an error
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
    Rules(self).set()
    LoggerHelper.log("Set Rules")

  def fill_slot_data(self):
    goal_guests = self.options.goal_guests.value
    goal_money = self.options.goal_money.value
    goal_coasters = self.options.goal_coasters.value
    goal_coaster_excitement = self.options.goal_coaster_excitement.value
    goal_coaster_intensity = self.options.goal_coaster_intensity.value
    goal_ride_profit = self.options.goal_ride_profit.value
    goal_park_tickets = self.options.goal_park_tickets.value
    goal_shops = self.options.goal_shops.value
    goal_shop_profit = self.options.goal_shop_profit.value

    seed = "_".join([
      str(self.options.scenario.value),
      self.multiworld.player_name[self.player],
      str(self.multiworld.seed_name)
    ])

    goals = {
      "park_tickets": {
        "enabled": goal_park_tickets > 0,
        "value": goal_park_tickets,
      },
      "guests": {
        "enabled": goal_guests > 0,
        "value": goal_guests,
      },
      "money": {
        "enabled": goal_money > 0,
        "value": goal_money,
      },
      "coaster_rides": {
        "enabled": goal_coasters > 0,
        "value": goal_coasters,
        "values": {
          "excitement": goal_coaster_excitement,
          "intensity": goal_coaster_intensity,
        },
      },
      "ride_profit": {
        "enabled": goal_ride_profit > 0,
        "value": goal_ride_profit,
      },
      "shop_profit": {
        "enabled": goal_shop_profit > 0,
        "value": goal_shop_profit,
      },
      "shops": {
        "enabled": goal_shops > 0,
        "value": goal_shops,
      },
    }
    slot_data = self.options.as_dict(
      "scenario",
    )
    slot_data["goals"] = goals
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
    
    slot_data["seed"] = seed
    slot_data["version"] = AP_WORLD_VERSION
    slot_data["challenges"] = self.challenges

    LoggerHelper.log(self.item_table, "Item Pool")
    LoggerHelper.log(dict(slot_data), "Slot data")

    if FAIL == True:
      if len(goal_shops) > 0:
        LoggerHelper.force_info(self.starter)
        return True

    return slot_data
