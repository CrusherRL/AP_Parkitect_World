from .Options import ParkitectOptions

class ParkitectGoals:
    def __init__(self, options: ParkitectOptions):
        self.park_tickets = options.goal_park_tickets.value
        self.guests = options.goal_guests.value
        self.money = options.goal_money.value
        self.coaster_rides = options.goal_coasters.value
        self.ride_profit = options.goal_ride_profit.value
        self.shop_profit = options.goal_shop_profit.value
        self.shops = options.goal_shops.value

        self.coaster_excitement = options.goal_coaster_excitement.value
        self.coaster_intensity = options.goal_coaster_intensity.value


    def to_dict(self):
        return {
            "park_tickets": {
                "enabled": self.park_tickets > 0,
                "value": self.park_tickets,
            },
            "guests": {
                "enabled": self.guests > 0,
                "value": self.guests,
            },
            "money": {
                "enabled": self.money > 0,
                "value": self.money,
            },
            "coaster_rides": {
                "enabled": self.coaster_rides > 0,
                "value": self.coaster_rides,
                "values": {
                    "excitement": self.coaster_excitement,
                    "intensity": self.coaster_intensity,
                },
            },
            "ride_profit": {
                "enabled": self.ride_profit > 0,
                "value": self.ride_profit,
            },
            "shop_profit": {
                "enabled": self.shop_profit > 0,
                "value": self.shop_profit,
            },
            "shops": {
                "enabled": self.shops > 0,
                "value": self.shops,
            },
        }
