from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

from .src.Options import ParkitectOptions, parkitect_option_groups
from .src.Items import set_items
from .src.Regions import Regions
from .src.LoggerHelper import LoggerHelper

from .data.items import *
from .data.constants import BASE_ID
from .data.locations import LOCATIONS

class ParkitectWebWorld(WebWorld):
  theme = "partyTime"

  setup_en = Tutorial(
    "Multiworld Setup Guide",
    "A guide to setting up the Parkitect randomizer on your computer.",
    "English",
    "setup_en.md",
    "setup/en",
    ["Crusher"]
  )

  tutorials = [setup_en]
  option_groups = parkitect_option_groups

class ParkitectWorld(World):
  """
  Parkitect is a modern take on classic theme park tycoon games where you build and manage the theme parks of your dreams!
  Construct your own coasters, design efficiently operating parks that fully immerse your guests in their theming and play through the campaign.
  """

  game = "Parkitect"
  web = ParkitectWebWorld()
  options_dataclass = ParkitectOptions
  options = ParkitectOptions
  location_name_to_id = {name: id for id, name in enumerate(LOCATIONS, BASE_ID)}
  item_name_to_id = {name: id for id, name in enumerate(ALL_ITEMS, BASE_ID)}
  item_name_groups = {
    TYPE_CALM_RIDES: RIDES[TYPE_CALM_RIDES],
    TYPE_THRILL_RIDES: RIDES[TYPE_THRILL_RIDES],
    TYPE_COASTER_RIDES: RIDES[TYPE_COASTER_RIDES],
    TYPE_WATER_RIDES: RIDES[TYPE_WATER_RIDES],
    TYPE_TRANSPORT_RIDES: RIDES[TYPE_TRANSPORT_RIDES],
    TYPE_RIDES: RIDES['all'],
    TYPE_SHOPS: RIDES['all'],
  }

  def __init__(self, multiworld, player: int):
    super().__init__(multiworld, player)
    self.starter = None
    self.item_table = []
    self.challenges = [] # Parkitect Challenge Window

  def generate_early(self) -> None:
    self.item_table, self.starter = set_items(self)

  def create_regions(self) -> None:
    Regions(self.player, self.multiworld, self.location_name_to_id).create((len(self.item_table)))
    LoggerHelper.log("Currently done")