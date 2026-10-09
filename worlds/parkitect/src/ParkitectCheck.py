from ..data.constants import START_ITEMS_PER_LOCATION
from .Statistics import Statistics
from .StatisticsV2 import StatisticsV2


class ParkitectCheck:
    def __init__(self, location_id: int):
        self.location_id = location_id
        self.item = None

        if location_id < START_ITEMS_PER_LOCATION:
            challenge_index = location_id
        else:
            challenge_index = location_id - START_ITEMS_PER_LOCATION

        self.challenge_index = challenge_index


    def set_item(self, item: Statistics|StatisticsV2) -> None:
        self.item = item


    def update_item_name(self, item_name: str) -> None:
        self.item.name = item_name


    def to_dict(self):
        return {
            "location_id": self.location_id,
            "item": self.item.to_dict(),
            "challenge_index": self.challenge_index,
        }


    def has_decoration(self) -> bool:
        return self.item.deco is not "" and len(self.item.deco) > 0


    def get_decoration_index(self) -> bool:
        return self.item.deco