from worlds.parkitect.src.Item import ItemHelper
from .Options import Difficulty
from .Statistics import Statistics
from .Regions import Regions

from worlds.generic.Rules import add_rule

from ..data.items import *
from ..src.Items import get_extra_checks
from ..data.constants import ATTRACTION_DECO_RATING_INDEX, CHALLENGE_PARK_GUESTS_RANGES, CHALLENGE_EMPLOYEE_RANGES, RULE_TYPE_PARKITECT_ITEM, RULE_TYPE_CATEGORY, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX, RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX, TIER_2_PROGRESS, TIER_3_PROGRESS, TIER_4_PROGRESS, CHALLENGE_PAY_MONEY_RANGES, RULE_TYPE_DECORATION

from .LoggerHelper import LoggerHelper

class Rules:
  def __init__(self, world):
    self.world = world
    self.extra_challenges = get_extra_checks(self.world)
    self.world.random.shuffle(self.extra_challenges)
    self.guaranteed_extra_challenge = (
      round(len(world.item_table) / len(self.extra_challenges))
      if self.extra_challenges else 0
    )

  def _set_parkitect_rule(self, rule_type, selected_item, location_number) -> None:
    LoggerHelper.log(location_number, "_set_parkitect_rule")
    
    region_name = Regions.get_region_from_parkitect_location(location_number)
    location = self.world.multiworld.get_region(region_name, self.world.player).entrances[0]
    
    assert location is not None, f"Couldn't find region \"{region_name}\" for location_number {location_number}"

    if rule_type == RULE_TYPE_PARKITECT_ITEM:
      add_rule(location, lambda state, item=selected_item: state.has(item, self.world.player))
      return

    if rule_type == RULE_TYPE_CATEGORY:
      add_rule(location, lambda state, category=selected_item: state.has_group(category, self.world.player))
      return

    if rule_type == RULE_TYPE_DECORATION:
      add_rule(location, lambda state: state.has_group(TYPE_DECORATIONS, self.world.player))
      return

    assert rule_type in (
      RULE_TYPE_PARKITECT_ITEM,
      RULE_TYPE_CATEGORY,
      RULE_TYPE_DECORATION,
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

  def determine_pay_money_max(self) -> int:
    value = self.world.options.goal_money.value
    difficulty = self.world.options.difficulty.value
    maximum = CHALLENGE_PAY_MONEY_RANGES[difficulty][1]

    # Something between the ranges
    if value <= 0:
      ranges = CHALLENGE_PAY_MONEY_RANGES[difficulty]
      return int(self.world.random.uniform(ranges[0], ranges[1]))

    min = value / 200 # .5%
    return int(self.world.random.uniform(min, maximum))

  def determine_park_guests_max(self, progress: float) -> int:
    multiplier = 1 if progress > TIER_2_PROGRESS else self._get_modifier()
    value = self.world.options.goal_guests.value
    difficulty = self.world.options.difficulty.value
    maximum = CHALLENGE_PARK_GUESTS_RANGES[difficulty][1]

    # Something between the ranges
    if value <= 0:
      ranges = CHALLENGE_PARK_GUESTS_RANGES[difficulty]
      result = int(self.world.random.uniform(ranges[0], ranges[1]) * multiplier)
      return result if result > 0 else 1

    min = max(100, value / 2) # 50%

    result = int(self.world.random.uniform(min, maximum) * multiplier)
    return result if result > 0 else 1

  def determine_employee_max(self, type: str, progress: float) -> int:
    multiplier = 1 if progress > TIER_2_PROGRESS else self._get_modifier()
    difficulty = self.world.options.difficulty.value
    ranges = CHALLENGE_EMPLOYEE_RANGES[type][difficulty]
    result = int(self.world.random.uniform(ranges[0], ranges[1]) * multiplier)

    return result if result > 0 else 1

  def set(self) -> None:
    difficulty_modifier: float = self._get_modifier()

    prerequisites = [self.world.starter]
    queued_prerequisites = []
    item_table_length = len(self.world.item_table)

    LoggerHelper.log(self.world.starter, "starter")

    for number, parkitect_item in enumerate(self.world.item_table):
      #LoggerHelper.log(prerequisites, "prerequisites")
      LoggerHelper.log(parkitect_item, "parkitect_item")
      parkitect_item_helper = ItemHelper(parkitect_item)

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
      itemHelper = self._find_challenge(item, number)
      check = self._create_check(number, itemHelper, prerequisites, progress)
      LoggerHelper.log(check, "check")
      self.world.challenges.append(check)

      if "deco" in check["item"] and len(check["item"]["deco"]) > 0:
        if ATTRACTION_DECO_RATING_INDEX[check["item"]["deco"]] >= ATTRACTION_DECO_RATING_INDEX["Low"]:
          self._set_parkitect_rule(RULE_TYPE_DECORATION, None, number)
      # Handle unlocked rides
      if parkitect_item_helper.is_shop() or parkitect_item_helper.is_ride():
        queued_prerequisites.append(parkitect_item_helper.item)

      # Every fourth
      if number > 0 and (number == 2 or number % 4 == 0):
        for prereq in queued_prerequisites:
          prerequisites.append(prereq)
        queued_prerequisites.clear()

  def _find_challenge(self, item: str, number: int) -> ItemHelper:
    if len(self.extra_challenges) <= 0:
      return ItemHelper(item)
 
    coin = self.world.random.random() # 0.0 -> 1.0
    guaranteed = (
      self.guaranteed_extra_challenge > 0
      and number % self.guaranteed_extra_challenge == 0
    )

    if guaranteed or coin < .15: # 15% Chance
      item = self.extra_challenges.pop()
      LoggerHelper.log(item, "Extra Challenge")
      return ItemHelper(item)

    return ItemHelper(item)

  def _create_check(self, number: int, itemHelper: ItemHelper, prerequisites: list, progress: float) -> dict[str, str|int]:
    min = 1
    check = {
      "location_id": number,
      "item": None
    }

    # Pay Money -> {money}
    if itemHelper.is_challenge_pay_money():
      money = self.determine_pay_money_max()
      check["item"] = Statistics(itemHelper, money).to_dict()

    # Park Guests -> {guests}
    elif itemHelper.is_challenge_park_guests():
      guests = self.determine_park_guests_max(progress)
      check["item"] = Statistics(itemHelper, guests).to_dict()

    # Employees -> {employee}
    elif itemHelper.is_challenge_employees():
      type = self.world.random.choice(EMPLOYEES[TYPE_ALL])
      employees = self.determine_employee_max(type, progress)
      check["item"] = Statistics(itemHelper, employees).to_dict()
      check["item"]["name"] = type

    # Here begins stuff with Attraction / Shop and its categories

    # --- Tier 1: -> until first 3 items ---
    elif number <= 3:
      # max: 2
      max = 2

      if itemHelper.is_coaster() or itemHelper.is_coaster_category():
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
      # Ride Category -> max: 5
      # Coaster -> max: 2
      # Ride Category -> max: 2
      elif itemHelper.is_ride() or itemHelper.is_ride_category():
        max = 3
        ride_revenue = 0

        if itemHelper.is_ride_category():
          max = 5

        elif itemHelper.is_coaster() or itemHelper.is_coaster_category():
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
        ).try_add_deco_rating(itemHelper, self.world).to_dict()

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
        ).try_add_deco_rating(itemHelper, self.world).to_dict()

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
        ).try_add_deco_rating(itemHelper, self.world).to_dict()

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
        ).try_add_deco_rating(itemHelper, self.world).to_dict()

    assert check["location_id"] >= 0, f"Missing location_id for item: \"{itemHelper.item}\""
    assert len(check["item"]) > 0, f"No item set for a check. Item: \"{itemHelper.item}\""

    return check