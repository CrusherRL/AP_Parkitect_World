from BaseClasses import Item

from ..data.items import SHOPS, RIDES, STATISTICS, TRAPS, TYPE_ALL, TYPES, TYPE_SHOPS, TYPE_NON_PROFIT, TYPE_STAT_EXEMPT, TYPE_RIDES, TYPE_COASTER_RIDES, CHALLENGE_PARK_GUESTS, CHALLENGE_EMPLOYEES, CHALLENGE_PAY_MONEY, DECORATION_THEMES, TYPE_SHOP_DRINKS, TYPE_SHOP_FOOD, TYPE_SHOP_FACILITIES, TYPE_CALM_RIDES, TYPE_THRILL_RIDES, TYPE_TRANSPORT_RIDES, TYPE_WATER_RIDES

class ParkitectItem(Item):
  game: str = "Parkitect"

class ItemHelper:
  def __init__(self, item: str) -> None:
    self.item = item

  def is_shop(self) -> bool:
    return self.item in SHOPS[TYPE_ALL]

  def is_drink_shop(self) -> bool:
    return self.item in SHOPS[TYPE_SHOP_DRINKS]

  def is_food_shop(self) -> bool:
    return self.item in SHOPS[TYPE_SHOP_FOOD]

  def is_facility_shop(self) -> bool:
    return self.item in SHOPS[TYPE_SHOP_FACILITIES]

  def is_shop_category(self) -> bool:
    return self.item in TYPES[TYPE_SHOPS]

  def is_shop_type(self) -> bool:
    return self.item == TYPE_SHOPS

  def is_shop_non_profit(self) -> bool:
    return self.item in SHOPS[TYPE_NON_PROFIT]

  def is_shop_stat_exempt(self) -> bool:
    return self.item in SHOPS[TYPE_STAT_EXEMPT]

  def is_ride(self) -> bool:
    return self.item in RIDES[TYPE_ALL]

  def is_ride_type(self) -> bool:
    return self.item == TYPE_RIDES

  def is_ride_category(self) -> bool:
    return self.item in TYPES[TYPE_RIDES]

  def is_ride_stat_exempt(self) -> bool:
    return self.item in RIDES[TYPE_STAT_EXEMPT]

  def is_calm_ride(self) -> bool:
    return self.item in RIDES[TYPE_CALM_RIDES]

  def is_calm_ride_type(self) -> bool:
    return self.item == TYPE_CALM_RIDES

  def is_thrill_ride(self) -> bool:
    return self.item in RIDES[TYPE_THRILL_RIDES]

  def is_thrill_ride_type(self) -> bool:
    return self.item == TYPE_THRILL_RIDES

  def is_coaster(self) -> bool:
    return self.item in RIDES[TYPE_COASTER_RIDES]

  def is_coaster_type(self) -> bool:
    return self.item == TYPE_COASTER_RIDES

  def is_transport_ride(self) -> bool:
    return self.item in RIDES[TYPE_TRANSPORT_RIDES]

  def is_transport_ride_type(self) -> bool:
    return self.item == TYPE_TRANSPORT_RIDES

  def is_water_ride(self) -> bool:
    return self.item in RIDES[TYPE_WATER_RIDES]

  def is_water_ride_type(self) -> bool:
    return self.item == TYPE_WATER_RIDES

  def is_trap(self) -> bool:
    return self.item in TRAPS[TYPE_ALL]

  def is_challenge_park_guests(self) -> bool:
    return self.item == CHALLENGE_PARK_GUESTS
  
  def is_challenge_employees(self) -> bool:
    return self.item == CHALLENGE_EMPLOYEES

  def is_challenge_pay_money(self) -> bool:
    return self.item == CHALLENGE_PAY_MONEY

  def is_decoration_themes(self) -> bool:
    return self.item in DECORATION_THEMES[TYPE_ALL]

  def is_statistic(self) -> bool:
    return self.item in STATISTICS[TYPE_ALL]
