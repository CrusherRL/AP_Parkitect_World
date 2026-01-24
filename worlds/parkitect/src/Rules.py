from worlds.parkitect.src.Item import ItemHelper
from .Options import Difficulty
from .Statistics import Statistics
from .Regions import Regions

from worlds.generic.Rules import add_rule
from ..data.items import *

from ..data.constants import RULE_TYPE_PARKITECT_ITEM, RULE_TYPE_CATEGORY, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX, RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX, TIER_2_PROGRESS, TIER_3_PROGRESS, TIER_4_PROGRESS

from .LoggerHelper import LoggerHelper

class Rules:
  def __init__(self, world):
    self.world = world

  def _set_parkitect_rule(self, rule_type, selected_item, location_number) -> None:
    LoggerHelper.log(location_number, "_set_parkitect_rule")
    region_name = Regions.get_previous_region_from_parkitect_location(location_number)
    assert region_name is not None and region_name != '', "Couldn't find Regionname for _set_parkitect_rule"
    
    LoggerHelper.log(region_name, "region_name")
    entrance = self.world.multiworld.get_region(region_name, self.world.player).entrances[0]
    assert entrance is not None and entrance != '', f"Couldn't find entrance from Region \"{region_name}\""

    #LoggerHelper.info(f"-> set_parkitect_rule rule_type: {rule_type}")
    #LoggerHelper.info(f"-> set_parkitect_rule selected_item: {selected_item}")
    #LoggerHelper.info(f"-> set_parkitect_rule location_number: {location_number}")
    #LoggerHelper.info(f"-> set_parkitect_rule region_name: {region_name}")
    #LoggerHelper.info(f"Entrance {entrance.name} existing rule: {entrance.access_rule}")

    if rule_type == RULE_TYPE_PARKITECT_ITEM:
      #add_rule(entrance, lambda state: state.has(selected_item, self.world.player))
      return

    if rule_type == RULE_TYPE_CATEGORY:
      #add_rule(entrance, lambda state: state.has_group(selected_item, self.world.player))
      return

    assert rule_type in (
      RULE_TYPE_PARKITECT_ITEM,
      RULE_TYPE_CATEGORY,
    ), "Rule type unknown!"

  def _get_modifier(self) -> float:
    if self.world.options.difficulty == Difficulty.medium.value:
      return .45

    if self.world.options.difficulty == Difficulty.hard.value:
      return .65

    if self.world.options.difficulty == Difficulty.extreme.value:
      return .85

    return .25

  @staticmethod
  def determine_item_category(item: str) -> str:
    if (item in SHOPS[TYPE_ALL]):
      return TYPE_SHOPS

    if (item in RIDES[TYPE_CALM_RIDES]):
      return TYPE_CALM_RIDES

    if (item in RIDES[TYPE_THRILL_RIDES]):
      return TYPE_THRILL_RIDES

    if (item in RIDES[TYPE_COASTER_RIDES]):
      return TYPE_COASTER_RIDES

    if (item in RIDES[TYPE_TRANSPORT_RIDES]):
      return TYPE_TRANSPORT_RIDES

    if (item in RIDES[TYPE_WATER_RIDES]):
      return TYPE_WATER_RIDES

    raise AssertionError(f"No Item Category found for item \"{item}\"")

  def set(self) -> None:
    difficulty_modifier = self._get_modifier()

    prerequisites = [self.world.starter]
    queued_prerequisites = []
    item_table_length = len(self.world.item_table)

    LoggerHelper.log(self.world.starter, "starter")

    for number, parkitect_item in enumerate(self.world.item_table):
      check = {
        "location_id": number,
        "item": None
      }

      LoggerHelper.log(prerequisites, "prerequisites")

      # Chosen prerequisite
      if self.world.random.random() < difficulty_modifier:
        item = self.world.random.choice(prerequisites)
        LoggerHelper.log(item, "Chosen prerequisite")

        self._set_parkitect_rule(RULE_TYPE_PARKITECT_ITEM, item, number)

      # Is category
      else:
        item = Rules.determine_item_category(self.world.random.choice(prerequisites))
        LoggerHelper.log(item, "Chosen category")
        self._set_parkitect_rule(RULE_TYPE_CATEGORY, item, number)

      progress = number / item_table_length
      itemHelper = ItemHelper(item)
      check = self._create_check(number, itemHelper, prerequisites, progress)
      LoggerHelper.log(check, "check")
      self.world.challenges.append(check)

      # Handle unlocked rides
      if parkitect_item in SHOPS[TYPE_ALL] or parkitect_item in RIDES[TYPE_ALL]:
        queued_prerequisites.append(parkitect_item)

      # Every fourth
      if number == 2 or number % 5 == 0:
        for prereq in queued_prerequisites:
          prerequisites.append(prereq)
        queued_prerequisites.clear()

  def _create_check(self, number: int, itemHelper: ItemHelper, prerequisites: list, progress: float) -> dict[str, str|int]:
    min = 1
    check = {
      "location_id": number,
      "item": None
    }

    # Set Statistics for item

    # Trap -> 1
    if itemHelper.is_trap():
      check["item"] = Statistics(itemHelper, 1).to_dict()

    # --- Tier 1: -> until first 3 items ---
    elif number <= 3:
      # max: 2
      max = 2

      if itemHelper.is_coaster():
        max = 1

      check["item"] = Statistics(
        itemHelper,
        self.world.random.randint(min, max),
      ).to_dict()

    # --- Tier 2: -> 10% ---
    elif progress <= TIER_2_PROGRESS: 
      customers = 0
      
      # Shop -> max: 3
      # Shop Category -> max: 6
      if itemHelper.is_shop() or itemHelper.is_shop_category():
        max = 3
        shop_revenue = 0

        if itemHelper.is_shop_category():
          max = 6

        # We can make shop_revenue if shop can make good money
        if not itemHelper.is_shop_non_profit() and self.world.random.random() < .5:
          shop_revenue = round(self.world.random.uniform(
            0, 
            self.world.options.challenge_maximum_shop_revenue.value
          ))

        if self.world.random.random() < .5:
          customers = round(self.world.random.uniform(
            0, 
            self.world.options.challenge_customers.value
          ))

        # Both given? i only want 1
        if shop_revenue > 0 and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < 0.5:
            customers = 0

          else:
            shop_revenue = 0

        if itemHelper.is_shop_stat_exempt() and shop_revenue > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
          shop_revenue = round(self.world.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX))

        check["item"] = Statistics(
          itemHelper,
          self.world.random.randint(min, max),
          revenue=shop_revenue,
          customers=customers
        ).to_dict()

      # Ride -> max: 3
      # Coaster -> max: 2
      # Ride Category -> max: 5
      elif itemHelper.is_ride() or itemHelper.is_ride_category():
        max = 3
        ride_revenue = 0

        if itemHelper.is_ride_category():
          max = 5

        elif itemHelper.is_coaster():
          max = 2

        if self.world.random.random() < .5:
          ride_revenue = round(self.world.random.uniform(
            0, 
            self.world.options.challenge_maximum_ride_revenue.value
          ))

        if itemHelper.is_ride_stat_exempt() and ride_revenue > RULE_RIDE_STAT_EXEMPT_REVENUE_MAX:
          ride_revenue = round(self.world.random.uniform(RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX))

        if self.world.random.random() < .5:
          customers = round(self.world.random.uniform(
            0, 
            self.world.options.challenge_customers.value
          ))

        # Both given? i only want 1
        if ride_revenue > 0 and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < 0.5:
            customers = 0

          else:
            ride_revenue = 0


        check["item"] = Statistics(
            itemHelper,
            self.world.random.randint(min, max),
            revenue=ride_revenue,
            customers=customers
        ).to_dict()

    # --- Tier 3: -> 35% ---
    elif progress <= TIER_3_PROGRESS:
      # Shop -> max: 4
      # Shop Category -> max: 12
      if itemHelper.is_shop() or itemHelper.is_shop_category():
        max = 4

        if itemHelper.is_shop_category():
          max = 12

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 4
      # Coaster -> max: 3
      # Ride Category -> max: 8
      elif itemHelper.is_ride() or itemHelper.is_ride_category():
        max = 4

        if itemHelper.is_ride_category():
          max = 8
        
        elif itemHelper.is_coaster():
          max = 3

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

    # --- Tier 4: -> 60% ---
    elif progress <= TIER_4_PROGRESS:
      # Shop -> max: 6
      # Shop Category -> max: 24
      if itemHelper.is_shop() or itemHelper.is_shop_category():
        max = 6
    
        if itemHelper.is_shop_category():
          max = 24

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 5
      # Coaster -> max: 3
      # Ride Category -> max: 10
      elif itemHelper.is_ride() or itemHelper.is_ride_category():
        max = 5
        
        if itemHelper.is_coaster():
          max = 3

        elif itemHelper.is_ride_category():
          max = 10

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

    # --- Tier 5: +60% ---
    else:
      # Shops -> max: 6
      # Shop Category -> max: 30
      if itemHelper.is_shop() or itemHelper.is_shop_category():
        max = 6

        if itemHelper.is_shop_category():
          max = 30

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 5
      # Coaster Ride -> max: 4
      # Ride Category -> max: 12
      elif itemHelper.is_ride() or itemHelper.is_ride_category():
        max = 5

        if itemHelper.is_coaster():
          max = 4
    
        elif itemHelper.is_ride_category():
          max = 12

        check["item"] = Statistics.random_roll(
          itemHelper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

    assert check["location_id"] >= 0, f"Missing location_id for item: \"{itemHelper.item}\""
    assert len(check["item"]) > 0, f"No item set for a check. Item: \"{itemHelper.item}\""

    return check