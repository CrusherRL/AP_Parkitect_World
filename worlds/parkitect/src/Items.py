import copy

from ..data.constants import Scenario_Items
from ..data.items import *
from ..src.Item import ItemHelper

from .LoggerHelper import LoggerHelper

def filter_dlc_items(items, options):
  """Add all DLC items"""
  exclude_items = set()

  # taste_of_adventures
  if not options.dlc1.value:
    for dlc_items in DLC[DLC_TASTE_OF_ADVENTURES].values():
      exclude_items.update(dlc_items)
  
  # booms_and_blooms
  if not options.dlc2.value:
    for dlc_items in DLC[DLC_BOOMS_AND_BLOOMS].values():
      exclude_items.update(dlc_items)
  
  # dinos_and_dynasties
  if not options.dlc3.value:
    for dlc_items in DLC[DLC_DINOS_AND_DYNASTIES].values():
      exclude_items.update(dlc_items)

  # Remove Items from exclude list
  for item in exclude_items:
    while item in items:
      items.remove(item)

  return items

def filter_mod_items(items, options):
  """Filter Parkitect Mod items based on which mod toggles are enabled."""
  filtered_items = items[:]

  if not options.dragon_shop:
    filtered_items.remove(DRAGON_SHOP)
  if not options.taco_shop:
    filtered_items.remove(TACO_SHOP)
  if not options.pancake_shop:
    filtered_items.remove(PANCAKE_SHOP)

  if not options.revolution_attraction:
    filtered_items.remove(REVOLUTION)
  if not options.monster_attraction:
    filtered_items.remove(MONSTER)
  if not options.inverter_and_somersault_attraction:
    filtered_items.remove(INVERTER)
    filtered_items.remove(SOMERSAULT)
  if not options.circus_show_attraction:
    filtered_items.remove(CIRCUS_SHOW)
  if not options.jump_attraction:
    filtered_items.remove(JUMP)
  if not options.rockin_tug_attraction:
    filtered_items.remove(ROCKIN_TUG)
  if not options.fish_barrel_attraction:
    filtered_items.remove(FISH_IN_A_BARREL)
  if not options.hopper_attraction:
    filtered_items.remove(HOPPER)
  if not options.demon_drop_attraction:
    filtered_items.remove(DEMON_DROP)
  if not options.roto_shake_attraction:
    filtered_items.remove(ROTO_SHAKE)
  if not options.hexentanz_attraction:
    filtered_items.remove(HEXENTANZ)
  if not options.kraken_attack_attraction:
    filtered_items.remove(KRAKEN_ATTACK)
  if not options.power_swing_and_mega_swing_attraction:
    filtered_items.remove(POWER_SWING)
    filtered_items.remove(MEGA_SWING)

  if not options.corkscrew_coaster:
    filtered_items.remove(CORKSCREW_COASTER)
  if not options.inverted_launch_coaster:
    filtered_items.remove(INVERTED_LAUNCH_COASTER)
  if not options.quadruple_rail_coaster:
    filtered_items.remove(QUADRUPLE_RAIL_COASTER)
  if not options.retro_steel_coaster:
    filtered_items.remove(RETRO_STEEL_COASTER)

  return filtered_items

def add_filter_items(items, options):
  for each in range(options.trap_player_money.value):
    items.append(PLAYER_MONEY_TRAP)

  for each in range(options.trap_attraction_breakdown.value):
    items.append(ATTRACTION_BREAKDOWN_TRAP)

  for each in range(options.trap_attraction_voucher.value):
    items.append(ATTRACTION_VOUCHER_TRAP)

  for each in range(options.trap_shops_ingredient.value):
    items.append(SHOP_INGREDIENTS_TRAP)

  for each in range(options.trap_shops_clean.value):
    items.append(SHOP_CLEANING_TRAP)

  for each in range(options.trap_shops_voucher.value):
    items.append(SHOP_VOUCHER_TRAP)

  for each in range(options.trap_employees_hiring.value):
    items.append(EMPLOYEE_HIRING_TRAP)

  for each in range(options.trap_employees_training.value):
    items.append(EMPLOYEE_TRAINING_TRAP)

  for each in range(options.trap_employees_tired.value):
    items.append(EMPLOYEE_TIREDNESS_TRAP)

  for each in range(options.trap_weather.value):
    items.append(WEATHER_RAINY_TRAP)
    items.append(WEATHER_STORMY_TRAP)
    items.append(WEATHER_CLOUDY_TRAP)
    items.append(WEATHER_SUNNY_TRAP)

  for each in range(options.trap_guests_spawn.value):
    items.append(GUEST_SPAWN_TRAP)

  for each in range(options.trap_guests_kill.value):
    items.append(GUEST_KILL_TRAP)

  for each in range(options.trap_guests_money.value):
    items.append(GUEST_MONEY_TRAP)

  for each in range(options.trap_guests_hunger.value):
    items.append(GUEST_HUNGER_TRAP)

  for each in range(options.trap_guests_thirst.value):
    items.append(GUEST_THIRST_TRAP)

  for each in range(options.trap_guests_bathroom.value):
    items.append(GUEST_BATHROOM_TRAP)

  for each in range(options.trap_guests_vomit.value):
    items.append(GUEST_VOMITING_TRAP)

  for each in range(options.trap_guests_happiness.value):
    items.append(GUEST_HAPPINESS_TRAP)

  for each in range(options.trap_guests_tiredness.value):
    items.append(GUEST_TIREDNESS_TRAP)

  for each in range(options.trap_guests_vandal.value):
    items.append(GUEST_VANDAL_TRAP)

  for each in range(options.trap_research.value):
    items.append(RESEARCH_TRAP)

  if options.progressive_speedups:
    for each in range(6):
      items.append(PROGRESSIVE_SPEED)

  # Utility Buildings
  if not options.utility_buildings:
    for utility_building in UTILITY_BUILDINGS[TYPE_ALL]:
      if utility_building in items:
        items.remove(utility_building)

  # Statistics
  if not options.statistics:
    for statistic in STATISTICS[TYPE_ALL]:
      if statistic in items:
        items.remove(statistic)

  # Decoration Themes
  if not options.decorations:
    for decoration_theme_tag in DECORATION_THEMES[TYPE_ALL]:
      if decoration_theme_tag in items:
        items.remove(decoration_theme_tag)

  for each in range(options.challenge_skips.value):
    items.append(CHALLENGE_SKIP)

  return items

def filter_from_options(scenario_items, options):
  """Filter items based on which DLCs are active."""

  items = filter_dlc_items(scenario_items, options)
  return filter_mod_items(items, options)

def find_starter(items, world):
  starter = world.random.choice(items)
  item_helper = ItemHelper(starter)

  if item_helper.is_coaster() or item_helper.is_ride() or item_helper.is_shop():
    return starter

  return find_starter(items, world)

def get_items(world):
  assert world.options.scenario.value in Scenario_Items, "Scenario not found"
  scenario_items = copy.deepcopy(Scenario_Items[world.options.scenario.value])
  items = filter_from_options(scenario_items, world.options)

  starter = find_starter(items, world)
  items.remove(starter)
  items = add_filter_items(items, world.options)

  assert len(items) > 0, "No Items found"
  assert starter not in items, "Starter is listed as usual item. That should never be the case!"

  LoggerHelper.log(starter, "starter")

  return items, starter

def get_extra_checks(world) -> list[str]:
  extra_checks: list[str] = []

  extra_checks.extend([CHALLENGE_PARK_GUESTS] * int(world.options.challenge_park_guests.value))
  extra_checks.extend([CHALLENGE_EMPLOYEES] * int(world.options.challenge_employees.value))
  extra_checks.extend([CHALLENGE_PAY_MONEY] * int(world.options.challenge_pay_money.value))

  return extra_checks