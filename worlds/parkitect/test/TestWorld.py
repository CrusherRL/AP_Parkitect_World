import unittest
from unittest.mock import MagicMock

from BaseClasses import MultiWorld

from .. import ParkitectWorld
from ..data.constants import AP_WORLD_VERSION
from ..data.items import CAR_RIDE


class TestWorld(unittest.TestCase):
  def setUp(self):
    self.player = 1
    self.multiworld = MultiWorld(1)
    self.multiworld.player_name = {self.player: "Tester"}
    self.multiworld.seed_name = 12345
    self.parkitect_world = ParkitectWorld(self.multiworld, self.player)
    self.parkitect_world.challenges = [{"location_id": 0, "item": {"name": CAR_RIDE, "amount": 1}}]

  def test_fill_slot_data_includes_trap_link_and_version(self):
    options = MagicMock()
    options.as_dict.side_effect = lambda *keys: {key: key for key in keys}
    options.goal_guests = MagicMock(value=0)
    options.goal_money = MagicMock(value=0)
    options.goal_coasters = MagicMock(value=0)
    options.goal_coaster_excitement = MagicMock(value=0)
    options.goal_coaster_intensity = MagicMock(value=0)
    options.goal_ride_profit = MagicMock(value=0)
    options.goal_park_tickets = MagicMock(value=0)
    options.goal_shops = MagicMock(value=0)
    options.goal_shop_profit = MagicMock(value=0)
    options.scenario = MagicMock(value=0)
    self.parkitect_world.options = options

    slot_data = self.parkitect_world.fill_slot_data()

    self.assertIn("trap_link", slot_data["rules"])
    self.assertEqual(slot_data["version"], AP_WORLD_VERSION)
    self.assertEqual(slot_data["challenges"], self.parkitect_world.challenges)
    self.assertIn("Tester", slot_data["seed"])
