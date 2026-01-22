from asyncio.windows_events import NULL
from BaseClasses import Item
from ..data.constants import Scenario_Items
from ..data.items import *
import copy

from .LoggerHelper import LoggerHelper

class ParkitectItem(Item):
    game: str = "Parkitect"

def filter_dlc_items(items, options):
  """Add all DLC items"""
  exclude_items = set()

  # taste_of_adventures
  if not options.dlc1.value:
    for dlc_items in DLC[DLC_TASTE_OF_ADVENTURES].values():
      exclude_items.update(dlc_items)
  
  # booms_and_blooms
  if not options.dlc2.value:
    for dlc_items in DLC[DLC_TASTE_OF_ADVENTURES].values():
      exclude_items.update(dlc_items)
  
  # dinos_and_dynasties
  if not options.dlc3.value:
    for dlc_items in DLC[DLC_TASTE_OF_ADVENTURES].values():
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
    filtered_items = [i for i in filtered_items if i != DRAGON_SHOP]
  if not options.taco_shop:
    filtered_items = [i for i in filtered_items if i != TACO_SHOP]
  if not options.pancake_shop:
    filtered_items = [i for i in filtered_items if i != PANCAKE_SHOP]

  if not options.revolution_attraction:
    filtered_items = [i for i in filtered_items if i != REVOLUTION]
  if not options.monster_attraction:
    filtered_items = [i for i in filtered_items if i != MONSTER]
  if not options.inverter_and_somersault_attraction:
    filtered_items = [i for i in filtered_items if i not in [INVERTER, SOMERSAULT]]
  if not options.circus_show_attraction:
    filtered_items = [i for i in filtered_items if i != CIRCUS_SHOW]
  if not options.jump_attraction:
    filtered_items = [i for i in filtered_items if i != JUMP]
  if not options.rockin_tug_attraction:
    filtered_items = [i for i in filtered_items if i != ROCKIN_TUG]
  if not options.fish_barrel_attraction:
    filtered_items = [i for i in filtered_items if i != FISH_IN_A_BARREL]
  if not options.hopper_attraction:
    filtered_items = [i for i in filtered_items if i != HOPPER]
  if not options.demon_drop_attraction:
    filtered_items = [i for i in filtered_items if i != DEMON_DROP]
  if not options.roto_shake_attraction:
    filtered_items = [i for i in filtered_items if i != ROTO_SHAKE]
  if not options.hexentanz_attraction:
    filtered_items = [i for i in filtered_items if i != HEXENTANZ]
  if not options.kraken_attack_attraction:
    filtered_items = [i for i in filtered_items if i != KRAKEN_ATTACK]
  if not options.power_swing_and_mega_swing_attraction:
    filtered_items = [i for i in filtered_items if i not in [POWER_SWING, MEGA_SWING]]

  if not options.corkscrew_coaster:
    filtered_items = [i for i in filtered_items if i != CORKSCREW_COASTER]
  if not options.inverted_launch_coaster:
    filtered_items = [i for i in filtered_items if i != INVERTED_LAUNCH_COASTER]
  if not options.quadruple_rail_coaster:
    filtered_items = [i for i in filtered_items if i != QUADRUPLE_RAIL_COASTER]
  if not options.retro_steel_coaster:
    filtered_items = [i for i in filtered_items if i != RETRO_STEEL_COASTER]

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

  for each in range(options.challenge_skips.value):
    items.append(SKIP)

  if (options.progressive_speedups.value == 1):
    for each in range(6):
      items.append(PROGRESSIVE_SPEED)

  return items

def filter_from_options(scenario_items, options):
  """Filter items based on which DLCs are active."""

  items = filter_dlc_items(scenario_items, options)
  return filter_mod_items(items, options)

def set_items(world):
  assert world.options.scenario.value in Scenario_Items, "Scenario not found"
  scenario_items = copy.deepcopy(Scenario_Items[world.options.scenario.value])
  items = filter_from_options(scenario_items, world.options)

  #starter = world.random.choice(items)
  starter = items[0]
  items.remove(starter)

  items = add_filter_items(items, world.options)

  assert len(items) > 0, "No Items found"
  assert starter not in items, "Starter is listed as usual item. That should never be the case!"

  LoggerHelper.log(items, "items")
  LoggerHelper.log(starter, "starter")

  return items, starter