from worlds.parkitect.data.constants import RULE_SHOP_STAT_EXEMPT_REVENUE_MAX, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX
from worlds.parkitect.src.Item import ItemHelper
from .. import LoggerHelper
from ..data.items import *
from ..data.constants import ATTRACTION_DECO_RATING_CHANCES, ATTRACTION_DECO_RATING, CHANCE_VERY_LOW, CHANCE_LOW, CHANCE_MEDIUM, CHANCE_HIGH, CHANCE_VERY_HIGH, CHANCE_EXTREME, ROUND_DIGITS, ROUND_DIGITS_NONE

# Helper Class to have a structure for randomization
class Statistics:
  def __init__(
    self,
    name: ItemHelper,
    amount: int = 0,
    excitement: float = 0,
    intensity: float = 0,
    nausea: float = 0,
    satisfaction: float = 0,
    revenue: float = 0,
    profit: float = 0,
    customers: int = 0,
    deco: str = "",
    photos: int = 0,
    vouchers: int = 0,
  ):
    item_helper = name
    self.name = item_helper.item
    self.amount = int(amount)
    self.excitement = excitement
    self.intensity = intensity
    self.nausea = nausea
    self.satisfaction = satisfaction
    self.revenue = revenue
    self.profit = profit
    self.customers = int(customers)
    self.deco = deco
    self.photos = int(photos)
    self.vouchers = int(vouchers)

    # its a category
    if not item_helper.is_shop() and not item_helper.is_ride() and not item_helper.is_trap():
      self.type = item_helper.item
      self.name = ""

    else:
      # Shop
      if item_helper.is_shop():
        self.type = TYPE_SHOPS

      if item_helper.is_drink_shop():
        self.type = TYPE_SHOP_DRINKS

      if item_helper.is_food_shop():
        self.type = TYPE_SHOP_FOOD

      if item_helper.is_facility_shop():
        self.type = TYPE_SHOP_FACILITIES

      # Ride
      if item_helper.is_ride():
        self.type = TYPE_RIDES

      if item_helper.is_calm_ride():
        self.type = TYPE_CALM_RIDES

      if item_helper.is_thrill_ride():
        self.type = TYPE_THRILL_RIDES

      if item_helper.is_coaster():
        self.type = TYPE_COASTER_RIDES

      if item_helper.is_transport_ride():
        self.type = TYPE_TRANSPORT_RIDES

      if item_helper.is_water_ride():
        self.type = TYPE_WATER_RIDES

      if item_helper.is_trap():
        self.type = TYPE_TRAPS

    assert self.type != None, f"No Type found for namend item \"{self.name}\""

  def to_dict(self):
    if self.type == TYPE_COASTER_RIDES:
      return {
        "name": self.name,
        "amount": self.amount,
        "excitement": self.excitement,
        "intensity": self.intensity,
        "nausea": self.nausea,
        "satisfaction": self.satisfaction,
        "revenue": self.revenue,
        "profit": self.profit,
        "customers": self.customers,
        "deco": self.deco,
        "photos": self.photos,
        "vouchers": self.vouchers,
        "type": self.type,
      }

    if self.type == TYPE_RIDES or self.type in TYPES[TYPE_RIDES]:
      return {
        "name": self.name,
        "amount": self.amount,
        "revenue": self.revenue,
        "profit": self.profit,
        "customers": self.customers,
        "deco": self.deco,
        "vouchers": self.vouchers,
        "type": self.type,
      }

    if self.type == TYPE_SHOPS or self.type in TYPES[TYPE_SHOPS]:
      return {
        "name": self.name,
        "amount": self.amount,
        "revenue": self.revenue,
        "profit": self.profit,
        "customers": self.customers,
        "vouchers": self.vouchers,
        "type": self.type,
      }

    if self.type == TYPE_TRAPS:
      return {
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      }

    if self.type == CHALLENGE_PARK_GUESTS or self.type == CHALLENGE_EMPLOYEES or self.type == CHALLENGE_PAY_MONEY:
      type = "Guest"
      if self.type == CHALLENGE_EMPLOYEES:
        type = "Employee"
      if self.type == CHALLENGE_PAY_MONEY:
        type = "Money"

      return {
        "name": self.name.replace(str(self.amount), "X"),
        "amount": self.amount,
        "type": type,
      }

    LoggerHelper.log({
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      }, "Statistics -> to_dict")

  @staticmethod
  def random_roll(item_helper: ItemHelper, amount: int, world, prerequisites = [], force = False):
    """
    Creates and returns a new Statistics object with randomly generated values.
    """
    option_total_customers = 0
    option_excitement = 0
    option_intensity = 0
    option_nausea = 0 
    option_satisfaction = 0 
    option_revenue = 0
    option_profit = 0
    option_photos = 0
    option_vouchers = 0

    max_customers = world.options.challenge_maximum_customers.value
    max_excitement = world.options.challenge_maximum_excitement.value
    max_intensity = world.options.challenge_maximum_intensity.value
    max_nausea = world.options.challenge_maximum_nausea.value
    max_satisfaction = world.options.challenge_maximum_satisfaction.value
    max_coaster_revenue = world.options.challenge_maximum_coaster_revenue.value
    max_ride_revenue = world.options.challenge_maximum_ride_revenue.value
    max_shop_revenue = world.options.challenge_maximum_shop_revenue.value
    max_ride_profit = world.options.challenge_maximum_ride_profit.value
    max_shop_profit = world.options.challenge_maximum_shop_profit.value
    max_photos = world.options.challenge_maximum_photos.value
    challenge_maximum_ride_vouchers = world.options.challenge_maximum_ride_vouchers.value
    challenge_maximum_shop_vouchers = world.options.challenge_maximum_shop_vouchers.value

    is_coaster = item_helper.is_coaster()

    # If it's a coaster, set all coaster values
    if is_coaster:
      if max_excitement > 0 and world.random.random() < CHANCE_VERY_HIGH:
        option_excitement = round(world.random.uniform(0, max_excitement), ROUND_DIGITS)

      if max_intensity > 0 and world.random.random() < CHANCE_VERY_HIGH:
        option_intensity = round(world.random.uniform(0, max_intensity), ROUND_DIGITS)

      if max_nausea > 0 and world.random.random() < CHANCE_MEDIUM:
        option_nausea = round(world.random.uniform(0, max_nausea), ROUND_DIGITS)

      if max_satisfaction > 0 and world.random.random() < CHANCE_MEDIUM:
        option_satisfaction = round(world.random.uniform(0, max_satisfaction), ROUND_DIGITS)

      if max_coaster_revenue > 0 and world.random.random() < CHANCE_HIGH:
        option_revenue = round(world.random.uniform(0, max_coaster_revenue), ROUND_DIGITS) / amount

    if is_coaster or item_helper.is_coaster_type():
      if max_photos > 0 and world.random.random() < CHANCE_LOW:
        option_photos = round(world.random.uniform(0, max_photos), ROUND_DIGITS)

      # Helps less good stat Coaster to reach it easier
      if item_helper.is_ride_stat_exempt() or any(item in RIDES[TYPE_STAT_EXEMPT] for item in prerequisites):
        if max_excitement >= 15:
          option_excitement = round(min(15, option_excitement * 0.33), ROUND_DIGITS)
        if max_intensity >= 15:
          option_intensity = round(min(15, option_intensity * 0.33), ROUND_DIGITS)
          option_nausea = 0
          option_satisfaction = round(option_satisfaction * .5, ROUND_DIGITS)

    # if it's a ride (also coasters!)
    if item_helper.is_ride() or item_helper.is_ride_category() or item_helper.is_ride_type():
      if (not item_helper.is_coaster() and item_helper.is_coaster_type()) and max_ride_revenue > 0 and world.random.random() < CHANCE_HIGH:
        option_revenue = round(world.random.uniform(0, max_ride_revenue), ROUND_DIGITS)

      if max_ride_profit > 0 and world.random.random() < CHANCE_HIGH:
        option_profit = round(world.random.uniform(0, max_ride_profit), ROUND_DIGITS)

      if challenge_maximum_ride_vouchers > 0 and world.random.random() < CHANCE_MEDIUM:
        option_vouchers = round(world.random.uniform(0, challenge_maximum_ride_vouchers), ROUND_DIGITS_NONE)

    # if it's a shop or shop type add a revenue
    elif (
      (item_helper.is_shop() and not item_helper.is_shop_non_profit() and not item_helper.is_facility_shop())
      or (item_helper.is_shop_category() and any (item not in SHOPS[TYPE_NON_PROFIT] for item in prerequisites))
    ):
      if max_shop_revenue > 0 and world.random.random() < CHANCE_VERY_HIGH:
        option_revenue = round(world.random.uniform(0, max_shop_revenue), ROUND_DIGITS)

      if max_shop_profit > 0 and world.random.random() < CHANCE_VERY_HIGH:
        option_profit = round(world.random.uniform(0, max_shop_profit), ROUND_DIGITS)

      if challenge_maximum_shop_vouchers > 0 and world.random.random() < CHANCE_MEDIUM:
        option_vouchers = round(world.random.uniform(0, challenge_maximum_shop_vouchers), ROUND_DIGITS_NONE)

      if item_helper.is_shop_stat_exempt() and option_revenue > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
        option_revenue = round(world.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX), ROUND_DIGITS)

      if item_helper.is_shop_stat_exempt() and option_profit > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
        option_profit = round(world.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX), ROUND_DIGITS)

    if item_helper.is_ride():
      option_revenue /= amount

    if item_helper.is_shop_type() or item_helper.is_ride_type():
      option_revenue *= amount
      option_profit *= amount
      option_photos *= amount
      option_vouchers *= amount

      # Only one, since the text is pretty long
      if option_revenue > 0 and option_profit > 0:
        if world.random.random() < CHANCE_MEDIUM:
          option_profit = 0
        else:
          option_revenue = 0

      if max_photos > 0 and option_photos == 0 and world.random.random() < CHANCE_LOW:
        option_photos = round(world.random.uniform(0, max_photos), ROUND_DIGITS)

    if not item_helper.is_trap():
      if world.random.random() < CHANCE_HIGH:
        option_total_customers = round(world.random.uniform(0, max_customers), ROUND_DIGITS_NONE)

      no_stats = option_excitement == 0 and option_intensity == 0 and option_nausea == 0 and option_revenue == 0 and option_total_customers == 0

      if no_stats and (world.random.random() < CHANCE_EXTREME or force):
        option_total_customers = round(world.random.uniform(0, max_customers), ROUND_DIGITS_NONE)

      if item_helper.is_ride_stat_exempt() and option_revenue > RULE_RIDE_STAT_EXEMPT_REVENUE_MAX:
        option_revenue = round(world.random.uniform(RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX), ROUND_DIGITS)

    # Create and return a new Statistics object
    return Statistics(
      name = item_helper,
      amount = amount,
      excitement = option_excitement,
      intensity = option_intensity,
      nausea = option_nausea,
      satisfaction = option_satisfaction,
      revenue = option_revenue,
      profit = option_profit,
      customers = option_total_customers,
      deco = "",
      photos = option_photos,
      vouchers = option_vouchers,
    )
  
  def try_add_deco_rating(self, item_helper: ItemHelper, world):
    enabled_deco = world.options.challenge_enable_decoration.value

    if not enabled_deco or not item_helper.is_coaster():
      return self

    if world.random.random() > CHANCE_VERY_LOW:
      return self

    if self.amount > 3:
      self.amount = 3

    self.deco = self.get_rating(world.options.difficulty.value, world)
    return self

  def get_rating(self, difficulty: int, world):
    chances = ATTRACTION_DECO_RATING_CHANCES[difficulty]

    index = world.random.choices(
        population=list(chances.keys()),
        weights=list(chances.values()),
        k=1,
    )[0]
    return ATTRACTION_DECO_RATING[index];