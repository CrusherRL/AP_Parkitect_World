from .Statistics import Statistics

class ParkitectCheck:
    def __init__(self, location_id: int):
        self.location_id = location_id
        self.item = None

    def set_item(self, item: Statistics) -> None:
        self.item = item

    def update_item_name(self, item_name: str) -> None:
        self.item.name = item_name

    def to_dict(self):
        return {
            "location_id": self.location_id,
            "item": self.item.to_dict(),
        }

    def has_decoration(self) -> bool:
        return self.item.deco is not "" and len(self.item.deco) > 0

    def get_decoration_index(self) -> bool:
        return self.item.deco