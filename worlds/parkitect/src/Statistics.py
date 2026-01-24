from worlds.parkitect.data.constants import RULE_SHOP_STAT_EXEMPT_REVENUE_MAX, RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX
from worlds.parkitect.src import LoggerHelper
from worlds.parkitect.src.Item import ItemHelper
from ..data.items import *

# Helper Class to have a structure for randomization
class Statistics:
  def __init__(
    self,
    name: ItemHelper,
    amount = 0,
    excitement = 0,
    intensity = 0,
    nausea = 0,
    satisfaction = 0,
    revenue = 0,
    customers = 0,
  ):
    itemHelper = name
    self.name = itemHelper.item
    self.amount = amount
    self.excitement = excitement
    self.intensity = intensity
    self.nausea = nausea
    self.satisfaction = satisfaction
    self.revenue = revenue
    self.customers = customers

    # its a category
    if not itemHelper.is_shop() and not itemHelper.is_ride() and not itemHelper.is_coaster() and not itemHelper.is_trap():
      self.type = itemHelper.item
      self.name = ""

    else:
      if itemHelper.is_shop():
        self.type = TYPE_SHOPS
        
      elif itemHelper.is_coaster():
        self.type = TYPE_COASTER_RIDES
        
      elif itemHelper.is_ride():
        self.type = TYPE_RIDES
        
      elif itemHelper.is_trap():
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
        "customers": self.customers,
        "type": self.type,
      }

    if self.type == TYPE_SHOPS or self.type == TYPE_RIDES or self.type in TYPES[TYPE_SHOPS] or self.type in TYPES[TYPE_RIDES]:
      return {
        "name": self.name,
        "amount": self.amount,
        "revenue": self.revenue,
        "customers": self.customers,
        "type": self.type,
      }

    if self.type == TYPE_TRAPS:
      return {
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      }

    LoggerHelper.log({
        "name": self.name,
        "amount": self.amount,
        "type": self.type,
      }, "Statistics -> to_dict")

  @staticmethod
  def random_roll(itemHelper: ItemHelper, amount: int, rule, prerequisites = [], force = False):
    """
    Creates and returns a new Statistics object with randomly generated values.
    """
    option_excitement = 0
    option_intensity = 0
    option_nausea = 0 
    option_satisfaction = 0 
    option_revenue = 0
    option_total_customers = 0

    max_excitement = rule.options.challenge_maximum_excitement.value
    max_intensity = rule.options.challenge_maximum_intensity.value
    max_nausea = rule.options.challenge_maximum_nausea.value
    max_satisfaction = rule.options.challenge_maximum_satisfaction.value
    max_ride_revenue = rule.options.challenge_maximum_ride_revenue.value
    max_shop_revenue = rule.options.challenge_maximum_shop_revenue.value
    max_customers = rule.options.challenge_customers.value
    
    # If its a coaster, set all coaster values
    if itemHelper.is_coaster() or itemHelper.is_coaster_category():
      if rule.random.random() < .5 and max_excitement > 0:
        option_excitement = 0 if max_excitement <= 0 else round(rule.random.uniform(0, max_excitement))

      if rule.random.random() < .5 and max_intensity > 0:
        option_intensity = 0 if max_intensity <= 0 else round(rule.random.uniform(0, max_intensity))

      if rule.random.random() < .5 and max_nausea > 0:
        option_nausea = 0 if max_nausea <= 0 else round(rule.random.uniform(0, max_nausea))

      if rule.random.random() < .5 and max_satisfaction > 0:
        option_satisfaction = 0 if max_satisfaction <= 0 else round(rule.random.uniform(0, max_satisfaction))

      # Helps less good stat Coaster to reach it easier
      if itemHelper.is_ride_stat_exempt() or any(item in RIDES[TYPE_STAT_EXEMPT] for item in prerequisites):
        if max_excitement >= 15:
          option_excitement = min(15, option_excitement * 0.33)
        if max_intensity >= 15:
          option_intensity = min(15, option_intensity * 0.33)
      
          option_nausea = 0
          option_satisfaction = option_satisfaction * .5

    # if its a ride (also coasters!) add a revenue
    if itemHelper.is_ride() or itemHelper.is_ride_category():
      if rule.random.random() < .5:
        option_revenue = round(rule.random.uniform(0, max_ride_revenue))

    elif (itemHelper.is_shop() and not itemHelper.is_shop_non_profit()) or (itemHelper.is_shop_category() and any (item not in SHOPS[TYPE_NON_PROFIT] for item in prerequisites)):
      if rule.random.random() < .5:
        option_revenue = round(rule.random.uniform(0, max_shop_revenue))

      if itemHelper.is_shop_stat_exempt() and option_revenue > RULE_SHOP_STAT_EXEMPT_REVENUE_MAX:
        option_revenue = round(rule.random.uniform(RULE_SHOP_STAT_EXEMPT_REVENUE_MIN, RULE_SHOP_STAT_EXEMPT_REVENUE_MAX))

    if not itemHelper.is_trap():
      if rule.random.random() < .5:
        option_total_customers = round(rule.random.uniform(0, max_customers))

      no_stats = option_excitement == 0 and option_intensity == 0 and option_nausea == 0 and option_revenue == 0 and option_total_customers == 0

      if no_stats and (rule.random.random() < .85 or force):
        option_total_customers = round(rule.random.uniform(0, max_customers))

      if itemHelper.is_ride_stat_exempt() and option_revenue > RULE_RIDE_STAT_EXEMPT_REVENUE_MAX:
        option_revenue = round(rule.random.uniform(RULE_RIDE_STAT_EXEMPT_REVENUE_MIN, RULE_RIDE_STAT_EXEMPT_REVENUE_MAX))

    # Create and return a new Statistics object
    return Statistics(
      name = itemHelper,
      amount = amount,
      excitement = option_excitement,
      intensity = option_intensity,
      nausea = option_nausea,
      satisfaction = option_satisfaction,
      revenue = option_revenue,
      customers = option_total_customers,
    )
  