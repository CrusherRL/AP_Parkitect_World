import unittest

from BaseClasses import ItemClassification, MultiWorld

from ..data.items import *
from ..data.constants import ITEM_NAME_TO_ID

from .. import ParkitectWorld

class TestItems(unittest.TestCase):
  def setUp(self):
    self.player = 1
    self.world = MultiWorld(1)
    self.parkitectWorld = ParkitectWorld(self.world, self.player)

  def _add_items_to_pool(self, starter: str, items: list):
    self.parkitectWorld.starter = starter
    self.parkitectWorld.item_table = items

    for i in self.parkitectWorld.item_table:
      self.assertIsNotNone(i)

    with self.assertRaises(AttributeError) as context:
      self.parkitectWorld.create_items()

    # Exception because starter couldn't be pushed
    self.assertIn("'MultiWorld' object has no attribute 'state'", str(context.exception))

    self.assertEqual(len(self.parkitectWorld.multiworld.itempool), len(items))
    self.assertNotIn(starter, self.parkitectWorld.multiworld.precollected_items)

  def test_item_classifications(self):
    progression_items = RIDES[TYPE_ALL] + SHOPS[TYPE_ALL]
    trap_items = TRAPS[TYPE_ALL]

    for item in progression_items:
      i = self.parkitectWorld.create_item(item)
      self.assertEqual(i.name, item)
      self.assertEqual(i.classification, ItemClassification.progression)
      self.assertEqual(i.code, ITEM_NAME_TO_ID[item])
      self.assertEqual(i.player, self.player)

    for item in trap_items:
      i = self.parkitectWorld.create_item(item)
      self.assertEqual(i.name, item)
      self.assertEqual(i.classification, ItemClassification.trap)
      self.assertEqual(i.code, ITEM_NAME_TO_ID[item])
      self.assertEqual(i.player, self.player)

  def test_add_items_to_pool__traps(self):
    self._add_items_to_pool(ENTERPRISE, TRAPS[TYPE_ALL])

  def test_add_items_to_pool__rides(self):
    self._add_items_to_pool(DRAGON_SHOP, RIDES[TYPE_ALL])

  def test_add_items_to_pool__shops(self):
    self._add_items_to_pool(GUEST_SPAWN_TRAP, SHOPS[TYPE_ALL])

