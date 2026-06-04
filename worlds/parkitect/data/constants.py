from ..data.items import EMPLOYEE_MECHANIC, ALL_ITEMS, EMPLOYEE_JANITOR, EMPLOYEE_SECURITY, EMPLOYEE_ENTERTAINER, EMPLOYEE_HANDYMAN
from ..data.locations import LOCATIONS

from .scenarios import lakeside_gardens, dusty_ridge_ranch, the_broken_atoll, magma_falls

DEBUG = False
FAIL = False

APWORLD_VERSION = "v1.4.0"
THEME = "stone"
BASE_ID = 3000000

Scenario_Items = {
  0: lakeside_gardens.park,
  1: dusty_ridge_ranch.park,
  2: the_broken_atoll.park,
  3: magma_falls.park,
}

LOCATION_NAME_TO_ID = {name: id for id, name in enumerate(LOCATIONS, BASE_ID)}
ITEM_NAME_TO_ID = {name: id for id, name in enumerate(ALL_ITEMS, BASE_ID)}

RULE_TYPE_PARKITECT_ITEM = 'Parkitect_Item'
RULE_TYPE_CATEGORY = 'Category'
RULE_TYPE_DECORATION = 'Decoration'

RULE_RIDE_STAT_EXEMPT_REVENUE_MIN = 0
RULE_RIDE_STAT_EXEMPT_REVENUE_MAX = 200

RULE_SHOP_STAT_EXEMPT_REVENUE_MIN = 200
RULE_SHOP_STAT_EXEMPT_REVENUE_MAX = 500

TIER_2_PROGRESS = 0.10
TIER_3_PROGRESS = 0.35
TIER_4_PROGRESS = 0.60

ATTRACTION_DECO_RATING = {
  0: "Bad",
  1: "Very Low",
  2: "Low",
  3: "Medium",
  4: "High",
  5: "Amazing",
}

ATTRACTION_DECO_RATING_INDEX = {rating: index for index, rating in ATTRACTION_DECO_RATING.items()}

ATTRACTION_DECO_RATING_CHANCES = {
    0: { # Easy Difficulty
        0: 20,  # Bad
        1: 35,  # Very Low
        2: 30,  # Low
        3: 9,   # Medium
        4: 5,   # High
        5: 1,   # Amazing
    },
    1: { # Medium Difficulty
        0: 10,  # Bad
        1: 20,  # Very Low
        2: 35,  # Low
        3: 28,  # Medium
        4: 5,   # High
        5: 2,   # Amazing
    },
    2: { # Hard Difficulty
        0: 2,   # Bad
        1: 5,   # Very Low
        2: 10,  # Low
        3: 25,  # Medium
        4: 33,  # High
        5: 25,  # Amazing
    },
    3: { # Extreme Difficulty
        0: 1,   # Bad
        1: 1,   # Very Low
        2: 1,   # Low
        3: 20,  # Medium
        4: 45,  # High
        5: 32,  # Amazing
    },
}

CHALLENGE_PAY_MONEY_RANGES = {
    0: [250, 500], # Easy Difficulty
    1: [500, 1000], # Medium Difficulty
    2: [1000, 2500], # Hard Difficulty
    3: [1500, 4000], # Extreme Difficulty
}

CHALLENGE_PARK_GUESTS_RANGES = {
    0: [100, 300], # Easy Difficulty
    1: [200, 500], # Medium Difficulty
    2: [400, 800], # Hard Difficulty
    3: [600, 1000], # Extreme Difficulty
}

CHALLENGE_EMPLOYEE_RANGES = {
    EMPLOYEE_MECHANIC: {    
        0: [1, 4], # Easy Difficulty
        1: [3, 8], # Medium Difficulty
        2: [6, 10], # Hard Difficulty
        3: [10, 20], # Extreme Difficulty
    },
    EMPLOYEE_JANITOR: {    
        0: [1, 4], # Easy Difficulty
        1: [3, 8], # Medium Difficulty
        2: [6, 10], # Hard Difficulty
        3: [10, 20], # Extreme Difficulty
    },
    EMPLOYEE_SECURITY: {    
        0: [1, 4], # Easy Difficulty
        1: [3, 8], # Medium Difficulty
        2: [6, 10], # Hard Difficulty
        3: [10, 20], # Extreme Difficulty
    },
    EMPLOYEE_ENTERTAINER: {    
        0: [1, 4], # Easy Difficulty
        1: [4, 12], # Medium Difficulty
        2: [6, 20], # Hard Difficulty
        3: [12, 32], # Extreme Difficulty
    },
    EMPLOYEE_HANDYMAN: {    
        0: [1, 4], # Easy Difficulty
        1: [3, 8], # Medium Difficulty
        2: [6, 10], # Hard Difficulty
        3: [10, 20], # Extreme Difficulty
    },
}
