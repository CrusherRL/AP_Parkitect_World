from BaseClasses import Item

from ..data.items import RESEARCH_TRAP, SHOPS, RIDES, STATISTICS, TRAPS, TYPE_ALL, TYPES, TYPE_SHOPS, TYPE_NON_PROFIT, TYPE_STAT_EXEMPT, TYPE_RIDES, TYPE_COASTER_RIDES, CHALLENGE_PARK_GUESTS, CHALLENGE_EMPLOYEES, CHALLENGE_PAY_MONEY, DECORATION_THEMES

class ParkitectItem(Item):
  game: str = "Parkitect"

class ItemHelper:
  def __init__(self, item: str) -> None:
    self.item = item

  def is_shop(self) -> bool:
    return self.item in SHOPS[TYPE_ALL]

  def is_shop_category(self) -> bool:
    return self.item == TYPE_SHOPS

  def is_shop_non_profit(self) -> bool:
    return self.item in SHOPS[TYPE_NON_PROFIT]

  def is_shop_stat_exempt(self) -> bool:
    return self.item in SHOPS[TYPE_STAT_EXEMPT]

  def is_ride(self) -> bool:
    return self.item in RIDES[TYPE_ALL]

  def is_ride_category(self) -> bool:
    return self.item in TYPES[TYPE_RIDES]

  def is_ride_stat_exempt(self) -> bool:
    return self.item in RIDES[TYPE_STAT_EXEMPT]

  def is_coaster(self) -> bool:
    return self.item in RIDES[TYPE_COASTER_RIDES]

  def is_coaster_category(self) -> bool:
    return self.item == TYPE_COASTER_RIDES

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
