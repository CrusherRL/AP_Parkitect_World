from worlds.parkitect.src.Item import ItemHelper
from .Options import Difficulty
from .Statistics import Statistics
from .Regions import Regions

from worlds.generic.Rules import add_rule

from ..data.items import *
from ..src.Items import get_extra_checks
from ..data.constants import ATTRACTION_DECO_RATING_INDEX, CHALLENGE_PARK_GUESTS_RANGES, CHALLENGE_EMPLOYEE_RANGES, RULE_TYPE_PARKITECT_ITEM, RULE_TYPE_CATEGORY, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX, RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX, TIER_2_PROGRESS, TIER_3_PROGRESS, TIER_4_PROGRESS, TIER_5_PROGRESS, CHALLENGE_PAY_MONEY_RANGES, RULE_TYPE_DECORATION, CHANCE_MEDIUM, CHANCE_VERY_HIGH, ROUND_DIGITS_NONE, ROUND_DIGITS

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

  def _is_difficulty(self, difficulty: Difficulty) -> bool:
    return self.world.options.difficulty == difficulty.value

  @staticmethod
  def determine_item_category(item: str, should_be_generic_type: bool = False) -> str:
    if should_be_generic_type:
      if item in SHOPS[TYPE_ALL]:
        return TYPE_SHOPS
      return TYPE_RIDES

    if item in SHOPS[TYPE_SHOP_DRINKS]:
      return TYPE_SHOP_DRINKS

    if item in SHOPS[TYPE_SHOP_FOOD]:
      return TYPE_SHOP_FOOD

    if item in SHOPS[TYPE_SHOP_FACILITIES]:
      return TYPE_SHOP_FACILITIES

    if item in RIDES[TYPE_CALM_RIDES]:
      return TYPE_CALM_RIDES

    if item in RIDES[TYPE_THRILL_RIDES]:
      return TYPE_THRILL_RIDES

    if item in RIDES[TYPE_COASTER_RIDES]:
      return TYPE_COASTER_RIDES

    if item in RIDES[TYPE_TRANSPORT_RIDES]:
      return TYPE_TRANSPORT_RIDES

    if item in RIDES[TYPE_WATER_RIDES]:
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
        should_be_generic_type = self.world.random.random() < CHANCE_MEDIUM
        item = Rules.determine_item_category(self.world.random.choice(prerequisites), should_be_generic_type)
        LoggerHelper.log(item, "Chosen category")
        self._set_parkitect_rule(RULE_TYPE_CATEGORY, item, number)

      progress = number / item_table_length
      item_helper = self._find_challenge(item, number)
      check = self._create_check(number, item_helper, prerequisites, progress)
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

  def _create_check(self, number: int, item_helper: ItemHelper, prerequisites: list, progress: float) -> dict[str, str|int]:
    min = 1
    check = {
      "location_id": number,
      "item": None
    }

    # Pay Money -> {money}
    if item_helper.is_challenge_pay_money():
      money = self.determine_pay_money_max()
      check["item"] = Statistics(item_helper, money).to_dict()

    # Park Guests -> {guests}
    elif item_helper.is_challenge_park_guests():
      guests = self.determine_park_guests_max(progress)
      check["item"] = Statistics(item_helper, guests).to_dict()

    # Employees -> {employee}
    elif item_helper.is_challenge_employees():
      type = self.world.random.choice(EMPLOYEES[TYPE_ALL])
      employees = self.determine_employee_max(type, progress)
      check["item"] = Statistics(item_helper, employees).to_dict()
      check["item"]["name"] = type

    # Here begins stuff with Attraction / Shop and its categories

    # --- Tier 1: -> until first 3 items ---
    elif number <= 3:
      # max: 2
      max = 2

      if item_helper.is_coaster() or item_helper.is_coaster_type():
        max = 1

      check["item"] = Statistics(
        item_helper,
        self.world.random.randint(min, max),
      ).to_dict()

    # --- Tier 2: -> 10% ---
    elif progress <= TIER_2_PROGRESS:
      customers = 0

      # Shop -> max: 3
      # Shop Category Type -> max: 6
      if item_helper.is_shop() or item_helper.is_shop_category():
        max = 3
        shop_revenue = 0
        shop_profit = 0

        if item_helper.is_shop_type():
          max = 6

        # We can make shop_revenue or shop_profit if shop can make good money
        if not item_helper.is_shop_non_profit() and self.world.random.random() < CHANCE_MEDIUM:
          shop_revenue = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_shop_revenue.value
          ), ROUND_DIGITS)

          shop_profit = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_shop_profit.value
          ), ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          customers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_customers.value
          ), ROUND_DIGITS_NONE)

        if shop_revenue > 0 and shop_profit > 0:
          if self.world.random.random() < CHANCE_MEDIUM:
            shop_profit = 0
          else:
            shop_revenue = 0

        # Both given? i only want 1
        if (shop_revenue > 0 and shop_profit > 0) and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < CHANCE_MEDIUM:
            customers = 0
          else:
            shop_revenue = 0
            shop_profit = 0

        if item_helper.is_shop_stat_exempt() and shop_revenue > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
          shop_revenue = round(
            self.world.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX),
            ROUND_DIGITS)

        check["item"] = Statistics(
          item_helper,
          self.world.random.randint(min, max),
          revenue=shop_revenue,
          profit=shop_profit,
          customers=customers,
        ).to_dict()

      # Ride -> max: 2
      # Ride Category Type -> max: 4
      # Coaster + Type -> max: 1
      elif item_helper.is_ride() or item_helper.is_ride_category():
        max = 2
        ride_revenue = 0
        ride_profit = 0
        ride_photos = 0

        if item_helper.is_ride_type():
          max = 4

        elif item_helper.is_coaster() or item_helper.is_coaster_type():
          max = 1

          if self.world.random.random() < CHANCE_VERY_HIGH:
            ride_photos = round(self.world.random.uniform(
              0,
              self.world.options.challenge_maximum_photos.value
            ), ROUND_DIGITS_NONE)

        if self.world.random.random() < CHANCE_MEDIUM:
          ride_revenue = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_ride_revenue.value
          ), ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          ride_profit = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_ride_profit.value
          ), ROUND_DIGITS)

        if item_helper.is_ride_stat_exempt() and ride_revenue > RULE_RIDE_STAT_EXEMPT_REVENUE_MAX:
          ride_revenue = round(
            self.world.random.uniform(RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX),
            ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          customers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_customers.value
          ), ROUND_DIGITS_NONE)

        if ride_revenue > 0 and ride_profit > 0:
          if self.world.random.random() < CHANCE_MEDIUM:
            ride_profit = 0
          else:
            ride_revenue = 0

        # Both given? i only want 1
        if (ride_revenue > 0 or ride_profit > 0) and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < CHANCE_MEDIUM:
            customers = 0
          else:
            ride_profit = 0
            ride_revenue = 0

        check["item"] = Statistics(
          item_helper,
          self.world.random.randint(min, max),
          revenue=ride_revenue,
          profit=ride_profit,
          customers=customers,
          photos=ride_photos
        ).try_add_deco_rating(item_helper, self.world).to_dict()

    # --- Tier 2: -> 18% ---
    elif progress <= TIER_3_PROGRESS:
      customers = 0

      # Shop -> max: 3
      # Shop Category Type -> max: 6
      if item_helper.is_shop() or item_helper.is_shop_category():
        max = 3
        shop_revenue = 0
        shop_profit = 0
        shop_vouchers = 0

        if item_helper.is_shop_type():
          max = 6

        # We can make shop_revenue or shop_profit if shop can make good money
        if not item_helper.is_shop_non_profit() and self.world.random.random() < CHANCE_MEDIUM:
          shop_revenue = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_shop_revenue.value
          ), ROUND_DIGITS)

          shop_profit = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_shop_profit.value
          ), ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          customers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_customers.value
          ), ROUND_DIGITS_NONE)

        if self._is_difficulty(Difficulty.extreme) and (
                item_helper.is_drink_shop() or item_helper.is_food_shop()) and self.world.random.random() < CHANCE_MEDIUM:
          shop_vouchers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_shop_vouchers.value
          ), ROUND_DIGITS_NONE)

        if shop_revenue > 0 and shop_profit > 0:
          if self.world.random.random() < CHANCE_MEDIUM:
            shop_profit = 0
          else:
            shop_revenue = 0

        # Both given? i only want 1
        if (shop_revenue > 0 and shop_profit > 0) and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < CHANCE_MEDIUM:
            customers = 0
          else:
            shop_revenue = 0
            shop_profit = 0

        if item_helper.is_shop_stat_exempt() and shop_revenue > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
          shop_revenue = round(
            self.world.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX),
            ROUND_DIGITS)

        check["item"] = Statistics(
          item_helper,
          self.world.random.randint(min, max),
          revenue=shop_revenue,
          profit=shop_profit,
          customers=customers,
          vouchers=shop_vouchers
        ).to_dict()

      # Ride -> max: 3
      # Ride Category Type -> max: 6
      # Coaster -> max: 2
      # Ride Coaster Category Type -> max: 2
      elif item_helper.is_ride() or item_helper.is_ride_category():
        max = 3
        ride_revenue = 0
        ride_profit = 0
        ride_photos = 0
        ride_vouchers = 0

        if item_helper.is_ride_type():
          max = 6

        elif item_helper.is_coaster() or item_helper.is_coaster_type():
          max = 2

          if self.world.random.random() < CHANCE_VERY_HIGH:
            ride_photos = round(self.world.random.uniform(
              0,
              self.world.options.challenge_maximum_photos.value
            ), ROUND_DIGITS_NONE)

        if self.world.random.random() < CHANCE_MEDIUM:
          ride_revenue = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_ride_revenue.value
          ), ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          ride_profit = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_ride_profit.value
          ), ROUND_DIGITS)

        if self._is_difficulty(Difficulty.extreme) and self.world.random.random() < CHANCE_MEDIUM:
          ride_vouchers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_ride_vouchers.value
          ), ROUND_DIGITS_NONE)

        if item_helper.is_ride_stat_exempt() and ride_revenue > RULE_RIDE_STAT_EXEMPT_REVENUE_MAX:
          ride_revenue = round(
            self.world.random.uniform(RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX),
            ROUND_DIGITS)

        if self.world.random.random() < CHANCE_MEDIUM:
          customers = round(self.world.random.uniform(
            0,
            self.world.options.challenge_maximum_customers.value
          ), ROUND_DIGITS_NONE)

        if ride_revenue > 0 and ride_profit > 0:
          if self.world.random.random() < CHANCE_MEDIUM:
            ride_profit = 0
          else:
            ride_revenue = 0

        # Both given? i only want 1
        if (ride_revenue > 0 or ride_profit > 0) and customers > 0:
          # Coin flip to decide which one to keep
          if self.world.random.random() < CHANCE_MEDIUM:
            customers = 0
          else:
            ride_profit = 0
            ride_revenue = 0

        check["item"] = Statistics(
          item_helper,
          self.world.random.randint(min, max),
          revenue=ride_revenue,
          profit=ride_profit,
          customers=customers,
          vouchers=ride_vouchers,
          photos=ride_photos
        ).try_add_deco_rating(item_helper, self.world).to_dict()

    # --- Tier 3: -> 35% ---
    elif progress <= TIER_4_PROGRESS:
      # Shop -> max: 4
      # Shop Category Type -> max: 12
      if item_helper.is_shop() or item_helper.is_shop_category():
        max = 4

        if item_helper.is_shop_type():
          max = 12

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 3
      # Ride Category Type -> max: 7
      elif item_helper.is_ride() or item_helper.is_ride_category():
        max = 3

        if item_helper.is_ride_type():
          max = 7

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).try_add_deco_rating(item_helper, self.world).to_dict()

    # --- Tier 4: -> 60% ---
    elif progress <= TIER_5_PROGRESS:
      # Shop -> max: 6
      # Shop Category -> max: 24
      if item_helper.is_shop() or item_helper.is_shop_category():
        max = 6
    
        if item_helper.is_shop_type():
          max = 24

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 4
      # Coaster -> max: 3
      # Ride Category Type -> max: 10
      elif item_helper.is_ride() or item_helper.is_ride_category():
        max = 4
        
        if item_helper.is_coaster():
          max = 3

        elif item_helper.is_ride_type():
          max = 10

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).try_add_deco_rating(item_helper, self.world).to_dict()

    # --- Tier 5: +60% ---
    else:
      # Shops -> max: 6
      # Shop Category -> max: 30
      if item_helper.is_shop() or item_helper.is_shop_category():
        max = 6

        if item_helper.is_shop_type():
          max = 30

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).to_dict()

      # Ride -> max: 4
      # Coaster Ride -> max: 4
      # Ride Category -> max: 15
      elif item_helper.is_ride() or item_helper.is_ride_category():
        max = 4

        if item_helper.is_ride_type():
          max = 15

        check["item"] = Statistics.random_roll(
          item_helper,
          self.world.random.randint(min, max),
          self.world,
          prerequisites
        ).try_add_deco_rating(item_helper, self.world).to_dict()

    assert check["location_id"] >= 0, f"Missing location_id for item: \"{item_helper.item}\""
    assert len(check["item"]) > 0, f"No item set for a check. Item: \"{item_helper.item}\""

    return check