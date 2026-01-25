from ..data.items import RIDES, SHOPS, TYPE_ALL, ALL_ITEMS
from ..data.locations import LOCATIONS

DEBUG = False

APWORLD_VERSION = "v1.3.0"
THEME = "stone"
BASE_ID = 3000000

Scenario_Items = {
  # "Lakeside Gardens"
  0: RIDES[TYPE_ALL] + SHOPS[TYPE_ALL],

  # "Dusty Ridge Ranch"
  1: RIDES[TYPE_ALL] + SHOPS[TYPE_ALL],

  # "The Broken Atoll"
  2: RIDES[TYPE_ALL] + SHOPS[TYPE_ALL],

  # "Magma Falls"
  3: RIDES[TYPE_ALL] + SHOPS[TYPE_ALL],
}

LOCATION_NAME_TO_ID = {name: id for id, name in enumerate(LOCATIONS, BASE_ID)}
ITEM_NAME_TO_ID = {name: id for id, name in enumerate(ALL_ITEMS, BASE_ID)}

RULE_TYPE_PARKITECT_ITEM = 'Parkitect_Item'
RULE_TYPE_CATEGORY = 'Category'

RULE_RIDE_STAT_EXEMPT_REVENUE_MIN = 0
RULE_RIDE_STAT_EXEMPT_REVENUE_MAX = 200

RULE_SHOP_STAT_EXEMPT_REVENUE_MIN = 200
RULE_SHOP_STAT_EXEMPT_REVENUE_MAX = 500

TIER_2_PROGRESS = 0.10
TIER_3_PROGRESS = 0.35
TIER_4_PROGRESS = 0.60
