from ..data.items import EMPLOYEE_MECHANIC, ALL_ITEMS, EMPLOYEE_JANITOR, EMPLOYEE_SECURITY, EMPLOYEE_ENTERTAINER, \
    EMPLOYEE_HANDYMAN
from ..data.locations import LOCATIONS

from .scenarios import lakeside_gardens, dusty_ridge_ranch, the_broken_atoll, magma_falls, yucatan_ridge, \
    brimstone_peak, candyland, timber_creek, jungle_adventure, technopolis, dragon_valley, victoria_island, \
    celeste_mountain, the_moon, maple_meadows, chanute_airfield, victoria_lake, western_roundup, coral_caldera, mystic_oasis, nova_labs, archipelago_adventures, adventure_island, batavia_cay, \
    ice_shelf_islands, happyco_harbor, biscayne_beach, highway_hijinks, honey_hills, orchard_acres, hickory_hill, \
    pagoda_valley, kaiserberg, sakura_gardens, silica_slopes, disaster_peaks, zalgonia, happyco_bakery, sheer_cliffs, \
    coaster_canyon, robopark

DEBUG = False
FAIL = False

AP_WORLD_VERSION = "v1.5.0"
THEME = "stone"
BASE_ID = 3000000

Scenario_Items = {
    # Custom Campaign
    0: lakeside_gardens.park,
    1: dusty_ridge_ranch.park,
    2: the_broken_atoll.park,
    3: magma_falls.park,

    # Main Campaign
    100: maple_meadows.park,
    101: chanute_airfield.park,
    102: victoria_lake.park,
    103: western_roundup.park,
    104: coral_caldera.park,
    105: mystic_oasis.park,
    106: nova_labs.park,
    107: archipelago_adventures.park,
    108: adventure_island.park,
    109: batavia_cay.park,
    110: ice_shelf_islands.park,
    111: happyco_harbor.park,
    112: biscayne_beach.park,
    113: highway_hijinks.park,
    114: honey_hills.park,
    115: orchard_acres.park,
    116: coaster_canyon.park,
    117: hickory_hill.park,
    118: pagoda_valley.park,
    119: kaiserberg.park,
    120: sakura_gardens.park,
    121: silica_slopes.park,
    122: disaster_peaks.park,
    123: robopark.park,
    124: sheer_cliffs.park,
    125: zalgonia.park,
    126: happyco_bakery.park,

    # Taste of Adventure Campaign
    200: yucatan_ridge.park,
    201: brimstone_peak.park,
    202: candyland.park,
    203: timber_creek.park,
    204: jungle_adventure.park,
    205: technopolis.park,
    206: dragon_valley.park,
    207: victoria_island.park,
    208: celeste_mountain.park,
    209: the_moon.park,
}

Scenario_Items_Starters = {
    # Main Campaign
    100: maple_meadows.starters,
    101: chanute_airfield.starters,
    102: victoria_lake.starters,
    103: western_roundup.starters,
    104: coral_caldera.starters,
    105: mystic_oasis.starters,
    106: nova_labs.starters,
    107: archipelago_adventures.starters,
    108: adventure_island.starters,
    109: batavia_cay.starters,
    110: ice_shelf_islands.starters,
    111: happyco_harbor.starters,
    112: biscayne_beach.starters,
    113: highway_hijinks.starters,
    114: honey_hills.starters,
    115: orchard_acres.starters,
    116: coaster_canyon.starters,
    117: hickory_hill.starters,
    118: pagoda_valley.starters,
    119: kaiserberg.starters,
    120: sakura_gardens.starters,
    121: silica_slopes.starters,
    122: disaster_peaks.starters,
    123: robopark.starters,
    124: sheer_cliffs.starters,
    125: zalgonia.starters,
    126: happyco_bakery.starters,

    # Taste of Adventure Campaign
    200: yucatan_ridge.starters,
    201: brimstone_peak.starters,
    202: candyland.starters,
    203: timber_creek.starters,
    204: jungle_adventure.starters,
    205: technopolis.starters,
    206: dragon_valley.starters,
    207: victoria_island.starters,
    208: celeste_mountain.starters,
    209: the_moon.starters,
}

TASTE_OF_ADVENTURE_SCENARIOS = set(range(200, 210))

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
    0: {  # Easy Difficulty
        0: 20,  # Bad
        1: 35,  # Very Low
        2: 30,  # Low
        3: 9,  # Medium
        4: 5,  # High
        5: 1,  # Amazing
    },
    1: {  # Medium Difficulty
        0: 10,  # Bad
        1: 20,  # Very Low
        2: 35,  # Low
        3: 28,  # Medium
        4: 5,  # High
        5: 2,  # Amazing
    },
    2: {  # Hard Difficulty
        0: 2,  # Bad
        1: 5,  # Very Low
        2: 10,  # Low
        3: 25,  # Medium
        4: 33,  # High
        5: 25,  # Amazing
    },
    3: {  # Extreme Difficulty
        0: 1,  # Bad
        1: 1,  # Very Low
        2: 1,  # Low
        3: 20,  # Medium
        4: 45,  # High
        5: 32,  # Amazing
    },
}

CHALLENGE_PAY_MONEY_RANGES = {
    0: [250, 500],  # Easy Difficulty
    1: [500, 1000],  # Medium Difficulty
    2: [1000, 2500],  # Hard Difficulty
    3: [1500, 4000],  # Extreme Difficulty
}

CHALLENGE_PARK_GUESTS_RANGES = {
    0: [100, 300],  # Easy Difficulty
    1: [200, 500],  # Medium Difficulty
    2: [400, 800],  # Hard Difficulty
    3: [600, 1000],  # Extreme Difficulty
}

CHALLENGE_EMPLOYEE_RANGES = {
    EMPLOYEE_MECHANIC: {
        0: [1, 4],  # Easy Difficulty
        1: [3, 8],  # Medium Difficulty
        2: [6, 10],  # Hard Difficulty
        3: [10, 20],  # Extreme Difficulty
    },
    EMPLOYEE_JANITOR: {
        0: [1, 4],  # Easy Difficulty
        1: [3, 8],  # Medium Difficulty
        2: [6, 10],  # Hard Difficulty
        3: [10, 20],  # Extreme Difficulty
    },
    EMPLOYEE_SECURITY: {
        0: [1, 4],  # Easy Difficulty
        1: [3, 8],  # Medium Difficulty
        2: [6, 10],  # Hard Difficulty
        3: [10, 20],  # Extreme Difficulty
    },
    EMPLOYEE_ENTERTAINER: {
        0: [1, 4],  # Easy Difficulty
        1: [4, 12],  # Medium Difficulty
        2: [6, 20],  # Hard Difficulty
        3: [12, 32],  # Extreme Difficulty
    },
    EMPLOYEE_HANDYMAN: {
        0: [1, 4],  # Easy Difficulty
        1: [3, 8],  # Medium Difficulty
        2: [6, 10],  # Hard Difficulty
        3: [10, 20],  # Extreme Difficulty
    },
}
