from enum import IntEnum
from Options import Range, Choice, PerGameCommonOptions, OptionGroup, Toggle
from dataclasses import dataclass

# Helpers
class Scenario(IntEnum):
    lakeside_gardens = 0
    dusty_ridge_ranch = 1
    the_broken_atoll = 2
    magma_falls = 3
    maple_meadows = 100
    chanute_airfield = 101
    victoria_lake = 102
    western_roundup = 103
    coral_caldera = 104
    mystic_oasis = 105
    nova_labs = 106
    archipelago_adventures = 107
    adventure_island = 108
    batavia_cay = 109
    ice_shelf_islands = 110
    happyco_harbor = 111
    biscayne_beach = 112
    highway_hijinks = 113
    honey_hills = 114
    orchard_acres = 115
    coaster_canyon = 116
    hickory_hill = 117
    pagoda_valley = 118
    kaiserberg = 119
    sakura_gardens = 120
    silica_slopes = 121
    disaster_peaks = 122
    robopark = 123
    sheer_cliffs = 124
    zalgonia = 125
    happyco_bakery = 126
    yucatan_ridge = 200
    brimstone_peak = 201
    candyland = 202
    timber_creek = 203
    jungle_adventure = 204
    technopolis = 205
    dragon_valley = 206
    victoria_island = 207
    celeste_mountain = 208
    the_moon = 209

class Difficulty(IntEnum):
    easy = 0
    medium = 1
    hard = 2
    extreme = 3

class DLC(IntEnum):
    taste_of_adventures = 1
    booms_and_blooms = 2
    dinos_and_dynasties = 3

# Selectable options
class SelectedScenario(Choice):
    """
    Choose which scenario you'd like to play!

    Custom Campaign:
    0 - "Archipelago - Lakeside Gardens"
    1 - "Archipelago - Dusty Ridge Ranch,
    2 - "Archipelago - The Broken Atoll,
    3 - "Archipelago - Magma Falls"

    Main Campaign:
    100 - "Maple Meadows"
    101 - "Chanute Airfield"
    102 - "Victoria Lake"
    103 - "Western Roundup"
    104 - "Coral Caldera"
    105 - "Mystic Oasis"
    106 - "Nova Labs"
    107 - "Archipelago Adventures"
    108 - "Adventure Island"
    109 - "Batavia Cay"
    110 - "Ice-Shelf Islands"
    111 - "HappyCo Harbor"
    112 - "Biscayne Beach"
    113 - "Highway Hijinks"
    114 - "Honey Hills"
    115 - "Orchard Acres"
    116 - "Coaster Canyon"
    117 - "Hickory Hill"
    118 - "Pagoda Valley"
    119 - "Kaiserberg"
    120 - "Sakura Gardens"
    121 - "Silica Slopes"
    122 - "Disaster Peaks"
    123 - "Robopark"
    124 - "Sheer Cliffs"
    125 - "Zalgonia"
    126 - "HappyCo. Bakery"

    Taste of Adventure Campaign:
    200 - "Yucatán Ridge"
    201 - "Brimstone Peak"
    202 - "Candyland"
    203 - "Timber Creek"
    204 - "Jungle Adventure"
    205 - "Technopolis"
    206 - "Dragon Valley"
    207 - "Victoria Island"
    208 - "Celeste Mountain"
    209 - "The Moon"
    """
    display_name = "Scenario"
    option_lakeside_gardens = Scenario.lakeside_gardens.value
    option_dusty_ridge_ranch = Scenario.dusty_ridge_ranch.value
    option_the_broken_atoll = Scenario.the_broken_atoll.value
    option_magma_falls = Scenario.magma_falls.value
    option_maple_meadows = Scenario.maple_meadows.value
    option_chanute_airfield = Scenario.chanute_airfield.value
    option_victoria_lake = Scenario.victoria_lake.value
    option_western_roundup = Scenario.western_roundup.value
    option_coral_caldera = Scenario.coral_caldera.value
    option_mystic_oasis = Scenario.mystic_oasis.value
    option_nova_labs = Scenario.nova_labs.value
    option_archipelago_adventures = Scenario.archipelago_adventures.value
    option_adventure_island = Scenario.adventure_island.value
    option_batavia_cay = Scenario.batavia_cay.value
    option_ice_shelf_islands = Scenario.ice_shelf_islands.value
    option_happyco_harbor = Scenario.happyco_harbor.value
    option_biscayne_beach = Scenario.biscayne_beach.value
    option_highway_hijinks = Scenario.highway_hijinks.value
    option_honey_hills = Scenario.honey_hills.value
    option_orchard_acres = Scenario.orchard_acres.value
    option_coaster_canyon = Scenario.coaster_canyon.value
    option_hickory_hill = Scenario.hickory_hill.value
    option_pagoda_valley = Scenario.pagoda_valley.value
    option_kaiserberg = Scenario.kaiserberg.value
    option_sakura_gardens = Scenario.sakura_gardens.value
    option_silica_slopes = Scenario.silica_slopes.value
    option_disaster_peaks = Scenario.disaster_peaks.value
    option_robopark = Scenario.robopark.value
    option_sheer_cliffs = Scenario.sheer_cliffs.value
    option_zalgonia = Scenario.zalgonia.value
    option_happyco_bakery = Scenario.happyco_bakery.value
    option_yucatan_ridge = Scenario.yucatan_ridge.value
    option_brimstone_peak = Scenario.brimstone_peak.value
    option_candyland = Scenario.candyland.value
    option_timber_creek = Scenario.timber_creek.value
    option_jungle_adventure = Scenario.jungle_adventure.value
    option_technopolis = Scenario.technopolis.value
    option_dragon_valley = Scenario.dragon_valley.value
    option_victoria_island = Scenario.victoria_island.value
    option_celeste_mountain = Scenario.celeste_mountain.value
    option_the_moon = Scenario.the_moon.value

class GuaranteedUnlockedStarter(Choice):
    """
    Starter Attraction/Shop is guaranteed unlocked from the beginning.
    """
    display_name = "Guaranteed unlocked Starter"
    option_no = 0
    option_yes = 1
    default = 1

class SelectedDifficulty(Choice):
    """
    Choose a difficulty for the randomization. This will make Checks harder to complete.
    """
    display_name = "Difficulty"
    option_easy = Difficulty.easy.value
    option_medium = Difficulty.medium.value
    option_hard = Difficulty.hard.value
    option_extreme = Difficulty.extreme.value
    default = Difficulty.medium.value

# DLC's
class SelectedDLC1(Choice):
    """
    Taste of Adventures DLC
    """
    display_name = "Taste of Adventures"
    option_no = 0
    option_yes = 1
    default = 0

class SelectedDLC2(Choice):
    """
    Booms and Blooms DLC
    """
    display_name = "Booms and Blooms"
    option_no = 0
    option_yes = 1
    default = 0

class SelectedDLC3(Choice):
    """
    Dinos and Dynasties DLC
    """
    display_name = "Dinos and Dynasties"
    option_no = 0
    option_yes = 1
    default = 0

# Extra Items
class UtilityBuildings(Toggle):
    """
    Adding all 4 Utility Buildings to the pool.
    """
    default = False

class Decorations(Toggle):
    """
    Adding all 11 Decoration Themes to the pool.
    (9 Items if not having DLC \"Dinos and Dynasties DLC\")
    """
    default = False

class Statistics(Toggle):
    """
    Adding all 32 Statistics to the pool.
    """
    default = False

# Goals
class GoalGuests(Range): # GuestsInParkGoal
    """
    Choose how many guests are required to win the scenario
    """
    display_name = "Guest Goal"
    range_start = 200
    range_end = 2500
    default = 1000

class GoalMoney(Range): # MoneyGoal
    """
    Choose how much money is required to win the scenario
    """
    display_name = "Money Goal"
    range_start = 50000
    range_end = 500000
    default = 100000

class GoalCoasters(Range): # CoastersGoal
    """
    Choose how many coasters are required to win the scenario
    """
    display_name = "Roller Coaster Goal"
    range_start = 0
    range_end = 12
    default = 4

class GoalCoasterExcitement(Range):
    """
    Select the minimum excitement 😀 for a coaster to count towards your objective. 0 will disable a minimum excitement rating.
    """
    display_name = "Excitement Rating"
    range_start = 0
    range_end = 80
    default = 50

class GoalCoasterIntensity(Range):
    """
    Select the minimum intensity 😬 for a coaster to count towards your objective. 0 will disable a minimum intensity rating.
    """
    display_name = "Intensity Rating"
    default = 50
    range_start = 0
    range_end = 80

class GoalRideProfit(Range): # RideProfitGoal
    """
    Choose how much profit you need from all rides to win the scenario
    """
    display_name = "Ride Profit Goal"
    default = 1500
    range_start = 0
    range_end = 10000

class GoalParkTickets(Range): # ParkTicketsGoal
    """
    Choose how many park tickets has to be sold to win the scenario
    """
    display_name = "Park Tickets Goal"
    default = 0
    range_start = 0
    range_end = 20000

class GoalShops(Range): # ShopsCountGoal
    """
    Choose how many shops are required to win the scenario
    """
    display_name = "Shops Goal"
    default = 30
    range_start = 0
    range_end = 100

class GoalShopProfit(Range): # ShopProfitGoal
    """
    Choose how much profit you need from shops to win the scenario
    """
    display_name = "Shop Profit Goal"
    default = 500
    range_start = 0
    range_end = 3000

# Challenge
class ChallengeMaximumExcitement(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum excitement, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Excitement"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeMaximumIntensity(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum intensity, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Intensity"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeMaximumNausea(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum nausea, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Nausea"
    range_start = 0
    range_end = 70
    default = 0

class ChallengeMaximumSatisfaction(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum satisfaction, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Satisfaction"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeCustomers(Range):
    """
    If a challenge determines you need a ride or shop with a maximum amount of customers, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Customers"
    range_start = 0
    range_end = 1000
    default = 0

class ChallengeMaximumRideRevenue(Range):
    """
    If a challenge determines you need a rollercoaster with a total revenue, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Total Ride Revenue"
    range_start = 0
    range_end = 5000
    default = 0

class ChallengeMaximumShopRevenue(Range):
    """
    If a challenge determines you need a shop with a total revenue, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Total Shop Revenue"
    range_start = 0
    range_end = 2500
    default = 0

class ChallengeDecorationRating(Toggle):
    """
    Determines if a challenge need an Attraction with a specific Decoration rating.
    Diffictuly depending on the value.
    """

class ChallengeParkGuests(Range):
    f"""
    Adding Challenge with \"Have X amount of Guests in your Park\""
    """
    display_name = "Challenge: X Park Guest"
    range_start = 0
    range_end = 25
    default = 15

class ChallengeEmployees(Range):
    """
    Adding Challenge with \"Have X amount of Employees\""
    Difficulty depends on the Experience Level an Employee must have
    """
    display_name = "Challenge: X Employees"
    range_start = 0
    range_end = 25
    default = 10

class ChallengePayMoney(Range):
    """
    Adding Challenge with \"Pay X amount of Money\""
    Depending on the Difficulty and if \"goal_money\" is set
    """
    display_name = "Challenge: Pay X Money"
    range_start = 0
    range_end = 30
    default = 20

class ChallengeSkips(Range):
    """
    by default, every game start with 5 skips to, well, skip a challenge. This will add additional skips to be found in the item pool.
    """
    display_name = "Skips"
    range_start = 0
    range_end = 30
    default = 10

# Traps
# Traps - Player
class TrapPlayerMoney(Range):
    """
    When found, little Money is added to your Bank Account! Adding traps will increase the total number of items in the world.
    """
    display_name = "Player Money Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Attraction
class TrapAttractionBreakdown(Range):
    """
    When found, instantly break specific amount of Attraction/s! Adding traps will increase the total number of items in the world.
    """
    display_name = "Attraction Breakdown Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapAttractionVoucher(Range):
    """
    When found, certain Guests will receive an Attraction Voucher in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Attraction Voucher Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Shop
class TrapShopsIngredient(Range):
    """
    When found, ProductShops ingredients needs to be restocked! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Ingredients Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapShopsClean(Range):
    """
    When found, Shops needs to be cleaned! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Cleaning Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapShopsVoucher(Range):
    """
    When found, some Guests will receive a Shop Voucher in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Voucher Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Employee
class TrapEmployeesHiring(Range):
    """
    When found, instantly Hire randomly picked Employees in your park! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be hired!
    """
    display_name = "Employee Hiring Trap"
    range_start = 0
    range_end = 20
    default = 10

class TrapEmployeesTraining(Range):
    """
    When found, instantly send randomly picked Employees to the training room! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be training!
    """
    display_name = "Employee Training Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapEmployeesTired(Range):
    """
    When found, instantly raise Employes tiredness! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be tired!
    """
    display_name = "Employee Tiredness Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Weather
class TrapWeather(Range):
    """
    When found, Rainy, Cloudy, Sunny or Stormy Weather is comming over! Adding traps will increase the total number of items in the world.
    """
    display_name = "Weather Trap"
    range_start = 0
    range_end = 30
    default = 10

# Traps - Guests
class TrapGuestsSpawn(Range):
    """
    When found, a wave of certain Guests appears in your Scenario! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Spawn Trap"
    range_start = 0
    range_end = 30
    default = 10

class TrapGuestsKill(Range):
    """
    When found, certain Guests will disappears in your Scenario! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Kill Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsMoney(Range):
    """
    When found, certain Guests will receive or lose their Money in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Money Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsMoneyFlux(Choice):
    """
    (If Guest Money Trap is enabled!)
    Decides if the Guest receive or/and lose money.
    """
    display_name = "Guest Money Flux"
    default = 2
    option_adding = 0
    option_removing = 1
    option_mixed = 2

class TrapGuestsHunger(Range):
    """
    When found, Guests will be hungry! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Hunger Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsThirst(Range):
    """
    When found, Guests will be thirsty! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Thirst Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsBathroom(Range):
    """
    When found, alot of Guests will be running to the next toilet! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Bathroom Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsVomit(Range):
    """
    When found, Too many Guests will try to find the next First-Aid room or Trashcan! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Vomiting Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsHappiness(Range):
    """
    When found, certain Guests will just be happy! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Happiness Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsTiredness(Range):
    """
    When found, certain Guests will just be tired! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Tiredness Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsVandal(Range):
    """
    When found, certain Guests become a Vandal! Adding traps will increase the total number of items in the world.
    The difficulty decides how many Guests vandalising your Park!
    """
    display_name = "Guest Vandal Trap"
    range_start = 0
    range_end = 30
    default = 10

# Traps - Research
class TrapResearchTrap(Range):
    """
    When found, certain Decoration (Path Attachments included) Theme, Attraction/s or Shop/s have to be researched again.
    """
    display_name = "Research Trap"
    range_start = 0
    range_end = 35
    default = 20

# TrapLink
class EnableTrapLink(Toggle):
    """
    When a player found a Trap, it will spread to everyone that has TrapLink enabled!
    """
    display_name = "Trap Link"
    default = False

# Speedups
class SelectedProgressiveSpeedups(Toggle):
    """
    If included, the ability to use the speedups at the window will be restricted behind an item. 6 items total will be added, each progressively unlocking a faster speed.
    Game Speedups (0x, 1x, 2x, 3x) are always usable.
    """
    display_name = "Progressive Speedups"
    default = False

# Parkitect Mods
class ParkitectModsInfo(Toggle):
    """
    Enable or disable individual Parkitect mods below.
    Steam Collection: https://steamcommunity.com/sharedfiles/filedetails/?id=3647109901

    You can ignore this setting. It is always on.
    """
    display_name = "ℹ Parkitect Mods"
    default = True

class DragonShop(Toggle):
    """Dragon Shop (Recommended)"""

class TacoShop(Toggle):
    """Taco Shop (Recommended)"""

class PancakeShop(Toggle):
    """Pancake Shop (Recommended)"""

class RevolutionAttraction(Toggle):
    """Revolution"""

class MonsterAttraction(Toggle):
    """Monster"""

class FishBarrelAttraction(Toggle):
    """Fish In A Barrel"""

class InverterAndSomersaultAttraction(Toggle):
    """Inverter & Somersault"""

class CircusShowAttraction(Toggle):
    """Circus Show (Recommended)"""

class JumpAttraction(Toggle):
    """Jump²"""

class RockinTugAttraction(Toggle):
    """Rockin' Tug (Recommended)"""

class HopperAttraction(Toggle):
    """Hopper (Recommended)"""

class DemonDropAttraction(Toggle):
    """Demon Drop"""

class RotoShakeAttraction(Toggle):
    """RotoShake"""

class HexentanzAttraction(Toggle):
    """Hexentanz"""

class PowerSwingAndMegaSwingAttraction(Toggle):
    """Power Swing & Mega Swing"""

class KrakenAttackAttraction(Toggle):
    """Kraken Attack (Recommended)"""

class CorkscrewCoaster(Toggle):
    """Corkscrew Coaster (Recommended)"""

class InvertedLaunchCoaster(Toggle):
    """Inverted Launch Coaster"""

class QuadrupleRailCoaster(Toggle):
    """Quadruple Rail Coaster (Recommended)"""

class RetroSteelCoaster(Toggle):
    """Retro Steel Coaster (Recommended)"""

parkitect_option_groups = [
    OptionGroup("Scenario Options", [
        SelectedScenario,
    GuaranteedUnlockedStarter,
        SelectedDifficulty
    ]),
    OptionGroup("DLC Options", [
        SelectedDLC1,
        SelectedDLC2,
        SelectedDLC3
    ]),
    OptionGroup("Extra items", [
        UtilityBuildings,
        Decorations,
        Statistics
    ]),
    OptionGroup("Goal Options", [
        GoalGuests,
        GoalMoney,
        GoalCoasters,
        GoalCoasterExcitement,
        GoalCoasterIntensity,
        GoalRideProfit,
        GoalParkTickets,
        GoalShops,
        GoalShopProfit
    ]),
    OptionGroup("Challenges/Checks", [
        ChallengeCustomers,
        ChallengeMaximumExcitement,
        ChallengeMaximumIntensity,
        ChallengeMaximumNausea,
        ChallengeMaximumSatisfaction,
        ChallengeMaximumRideRevenue,
        ChallengeMaximumShopRevenue,
        ChallengeDecorationRating,
        ChallengeParkGuests,
        ChallengeEmployees,
        ChallengePayMoney,
        ChallengeSkips,
    ]),
    OptionGroup("Traps", [
        TrapPlayerMoney,
        TrapAttractionBreakdown,
        TrapAttractionVoucher,
        TrapShopsIngredient,
        TrapShopsClean,
        TrapShopsVoucher,
        TrapEmployeesHiring,
        TrapEmployeesTraining,
        TrapEmployeesTired,
        TrapWeather,
        TrapGuestsSpawn,
        TrapGuestsKill,
        TrapGuestsMoney,
        TrapGuestsHunger,
        TrapGuestsThirst,
        TrapGuestsBathroom,
        TrapGuestsVomit,
        TrapGuestsHappiness,
        TrapGuestsTiredness,
        TrapGuestsVandal,
        TrapResearchTrap,
        EnableTrapLink
    ]),
    OptionGroup("Rules", [
        TrapGuestsMoneyFlux,
        SelectedProgressiveSpeedups
    ]),
    OptionGroup("Parkitect Mods", [
        ParkitectModsInfo,
        DragonShop,
        TacoShop,
        PancakeShop,
        RevolutionAttraction,
        MonsterAttraction,
        InverterAndSomersaultAttraction,
        CircusShowAttraction,
        JumpAttraction,
        RockinTugAttraction,
        FishBarrelAttraction,
        HopperAttraction,
        DemonDropAttraction,
        RotoShakeAttraction,
        HexentanzAttraction,
        PowerSwingAndMegaSwingAttraction,
        KrakenAttackAttraction,
        CorkscrewCoaster,
        InvertedLaunchCoaster,
        QuadrupleRailCoaster,
        RetroSteelCoaster,
    ]),
]

@dataclass
class ParkitectOptions(PerGameCommonOptions):
    difficulty: SelectedDifficulty
    guaranteed_unlocked_starter: GuaranteedUnlockedStarter
    scenario: SelectedScenario
    dlc1: SelectedDLC1
    dlc2: SelectedDLC2
    dlc3: SelectedDLC3

    # Extra Items
    utility_buildings: UtilityBuildings
    decorations: Decorations
    statistics: Statistics
    
    # Goals
    goal_guests: GoalGuests
    goal_money: GoalMoney
    goal_coasters: GoalCoasters
    goal_coaster_excitement: GoalCoasterExcitement
    goal_coaster_intensity: GoalCoasterIntensity
    goal_ride_profit: GoalRideProfit
    goal_park_tickets: GoalParkTickets
    goal_shops: GoalShops
    goal_shop_profit: GoalShopProfit

    # Challenges / Checks
    challenge_customers: ChallengeCustomers
    challenge_maximum_excitement: ChallengeMaximumExcitement
    challenge_maximum_intensity: ChallengeMaximumIntensity
    challenge_maximum_nausea: ChallengeMaximumNausea
    challenge_maximum_satisfaction: ChallengeMaximumSatisfaction
    challenge_maximum_ride_revenue: ChallengeMaximumRideRevenue
    challenge_maximum_shop_revenue: ChallengeMaximumShopRevenue
    challenge_enable_decoration: ChallengeDecorationRating
    challenge_park_guests: ChallengeParkGuests
    challenge_employees: ChallengeEmployees
    challenge_pay_money: ChallengePayMoney
    challenge_skips: ChallengeSkips

    # Traps
    trap_player_money: TrapPlayerMoney
    trap_attraction_breakdown: TrapAttractionBreakdown
    trap_attraction_voucher: TrapAttractionVoucher
    trap_shops_ingredient: TrapShopsIngredient
    trap_shops_clean: TrapShopsClean
    trap_shops_voucher: TrapShopsVoucher
    trap_employees_hiring: TrapEmployeesHiring
    trap_employees_training: TrapEmployeesTraining
    trap_employees_tired: TrapEmployeesTired
    trap_weather: TrapWeather
    trap_guests_spawn: TrapGuestsSpawn
    trap_guests_kill: TrapGuestsKill
    trap_guests_money: TrapGuestsMoney
    trap_guests_hunger: TrapGuestsHunger
    trap_guests_thirst: TrapGuestsThirst
    trap_guests_bathroom: TrapGuestsBathroom
    trap_guests_vomit: TrapGuestsVomit
    trap_guests_happiness: TrapGuestsHappiness
    trap_guests_tiredness: TrapGuestsTiredness
    trap_guests_vandal: TrapGuestsVandal
    trap_research: TrapResearchTrap
    trap_link: EnableTrapLink

    # Parkitect Mod rules.
    guests_money_flux: TrapGuestsMoneyFlux
    progressive_speedups: SelectedProgressiveSpeedups

    # Parkitect Mods
    parkitect_mods: ParkitectModsInfo
    dragon_shop: DragonShop
    taco_shop:  TacoShop
    pancake_shop : PancakeShop
    revolution_attraction : RevolutionAttraction
    monster_attraction : MonsterAttraction
    inverter_and_somersault_attraction : InverterAndSomersaultAttraction
    circus_show_attraction : CircusShowAttraction
    jump_attraction : JumpAttraction
    rockin_tug_attraction : RockinTugAttraction
    fish_barrel_attraction : FishBarrelAttraction
    hopper_attraction : HopperAttraction
    demon_drop_attraction : DemonDropAttraction
    roto_shake_attraction : RotoShakeAttraction
    hexentanz_attraction : HexentanzAttraction
    power_swing_and_mega_swing_attraction : PowerSwingAndMegaSwingAttraction
    kraken_attack_attraction : KrakenAttackAttraction
    corkscrew_coaster : CorkscrewCoaster
    inverted_launch_coaster : InvertedLaunchCoaster
    quadruple_rail_coaster : QuadrupleRailCoaster
    retro_steel_coaster : RetroSteelCoaster
