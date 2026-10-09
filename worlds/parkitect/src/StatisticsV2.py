from ..src.Item import ItemHelper
from .LoggerHelper import LoggerHelper
from ..data.items import *
from ..data.constants import ATTRACTION_DECO_RATING_CHANCES, ATTRACTION_DECO_RATING, CHANCE_VERY_LOW, CHANCE_LOW, \
    CHANCE_MEDIUM, CHANCE_HIGH, CHANCE_VERY_HIGH, CHANCE_EXTREME, ROUND_DIGITS, ROUND_DIGITS_NONE, CHALLENGE_NAME, \
    CHALLENGE_AMOUNT, CHALLENGE_EXCITEMENT, CHALLENGE_INTENSITY, CHALLENGE_NAUSEA, CHALLENGE_SATISFACTION, \
    CHALLENGE_REVENUE, CHALLENGE_PROFIT, CHALLENGE_CUSTOMERS, CHALLENGE_DECO, CHALLENGE_PHOTOS, CHALLENGE_VOUCHERS, \
    CHALLENGE_TYPE, RULE_STAT_EXEMPT_PROFIT_MAX, RULE_STAT_EXEMPT_EXCITEMENT_MIN, \
    RULE_STAT_EXEMPT_EXCITEMENT_MAX_PERCENTAGE, RULE_STAT_EXEMPT_INTENSITY_MIN, \
    RULE_STAT_EXEMPT_INTENSITY_MAX_PERCENTAGE, RULE_STAT_EXEMPT_SATISFACTION_MAX_PERCENTAGE, \
    RULE_STAT_EXEMPT_REVENUE_MAX


# Helper Class to have a structure for randomization
class StatisticsV2:
    name: str
    amount: int
    excitement: float= 0
    intensity: float = 0
    nausea: float = 0
    satisfaction: float = 0
    revenue: int = 0
    profit: int = 0
    customers: int = 0
    deco: str = ""
    photos: int = 0
    vouchers: int = 0
    type: str | None = None
    world = None
    item_helper = ItemHelper

    def __init__(self, world, item_helper: ItemHelper, used_requisites: list[str] = []):
        self.world = world
        self.item_helper = item_helper
        self.name = item_helper.item
        self.used_requisites = used_requisites

        # it's a category
        if not item_helper.is_shop() and not item_helper.is_ride() and not item_helper.is_trap():
            self.type = item_helper.item
            self.name = ""

        else:
            # Shop
            if item_helper.is_shop():
                self.type = TYPE_SHOPS

            if item_helper.is_drink_shop():
                self.type = TYPE_SHOP_DRINKS

            if item_helper.is_food_shop():
                self.type = TYPE_SHOP_FOOD

            if item_helper.is_facility_shop():
                self.type = TYPE_SHOP_FACILITIES

            # Ride
            if item_helper.is_ride():
                self.type = TYPE_RIDES

            if item_helper.is_calm_ride():
                self.type = TYPE_CALM_RIDES

            if item_helper.is_thrill_ride():
                self.type = TYPE_THRILL_RIDES

            if item_helper.is_coaster():
                self.type = TYPE_COASTER_RIDES

            if item_helper.is_transport_ride():
                self.type = TYPE_TRANSPORT_RIDES

            if item_helper.is_water_ride():
                self.type = TYPE_WATER_RIDES

            if item_helper.is_trap():
                self.type = TYPE_TRAPS

        assert self.type != None, f"No Type found for named item \"{self.name}\""


    def to_dict(self):
        if self.type == TYPE_COASTER_RIDES:
            return {
                CHALLENGE_NAME: self.name,
                CHALLENGE_AMOUNT: self.amount,
                CHALLENGE_EXCITEMENT: self.excitement,
                CHALLENGE_INTENSITY: self.intensity,
                CHALLENGE_NAUSEA: self.nausea,
                CHALLENGE_SATISFACTION: self.satisfaction,
                CHALLENGE_REVENUE: self.revenue,
                CHALLENGE_PROFIT: self.profit,
                CHALLENGE_CUSTOMERS: self.customers,
                CHALLENGE_DECO: self.deco,
                CHALLENGE_PHOTOS: self.photos,
                CHALLENGE_VOUCHERS: self.vouchers,
                CHALLENGE_TYPE: self.type,
            }

        if self.type == TYPE_RIDES or self.type in TYPES[TYPE_RIDES]:
            return {
                CHALLENGE_NAME: self.name,
                CHALLENGE_AMOUNT: self.amount,
                CHALLENGE_REVENUE: self.revenue,
                CHALLENGE_PROFIT: self.profit,
                CHALLENGE_CUSTOMERS: self.customers,
                CHALLENGE_DECO: self.deco,
                CHALLENGE_VOUCHERS: self.vouchers,
                CHALLENGE_TYPE: self.type,
            }

        if self.type == TYPE_SHOPS or self.type in TYPES[TYPE_SHOPS]:
            return {
                CHALLENGE_NAME: self.name,
                CHALLENGE_AMOUNT: self.amount,
                CHALLENGE_REVENUE: self.revenue,
                CHALLENGE_PROFIT: self.profit,
                CHALLENGE_CUSTOMERS: self.customers,
                CHALLENGE_VOUCHERS: self.vouchers,
                CHALLENGE_TYPE: self.type,
            }

        if self.type == TYPE_TRAPS:
            return {
                CHALLENGE_NAME: self.name,
                CHALLENGE_AMOUNT: self.amount,
                CHALLENGE_TYPE: self.type,
            }

        if self.type == CHALLENGE_PARK_GUESTS or self.type == CHALLENGE_EMPLOYEES or self.type == CHALLENGE_PAY_MONEY:
            challenge_type = STATISTICS_BUILDER_LABEL_GUEST
            if self.type == CHALLENGE_EMPLOYEES:
                challenge_type = STATISTICS_BUILDER_LABEL_EMPLOYEE
            if self.type == CHALLENGE_PAY_MONEY:
                challenge_type = STATISTICS_BUILDER_LABEL_MONEY

            return {
                CHALLENGE_NAME: self.name.replace(str(self.amount), "X"),
                CHALLENGE_AMOUNT: self.amount,
                CHALLENGE_TYPE: challenge_type,
            }

        LoggerHelper.log({
            CHALLENGE_NAME: self.name,
            CHALLENGE_AMOUNT: self.amount,
            CHALLENGE_TYPE: self.type,
        }, "Statistics -> to_dict")


    def roll(self):
        # All Rides and Category
        if self.item_helper.is_ride() or self.item_helper.is_ride_category() or self.item_helper.is_ride_type():
            if self.world.random.random() < CHANCE_HIGH:
                self.roll_revenue()

            if self.world.random.random() < CHANCE_HIGH:
                self.roll_profit()

            if self.world.random.random() < CHANCE_LOW:
                self.roll_vouchers()

        # Coaster and Coaster Type
        # Note: Coaster Type will only have photos
        if self.item_helper.is_coaster() or self.item_helper.is_coaster_type():
            if self.world.random.random() < CHANCE_MEDIUM:
                self.roll_nausea()

            if self.world.random.random() < CHANCE_MEDIUM:
                self.roll_satisfaction()

            if self.world.random.random() < CHANCE_VERY_HIGH:
                self.roll_excitement()

            if self.world.random.random() < CHANCE_HIGH:
                self.roll_intensity()

            if self.world.random.random() < CHANCE_LOW:
                self.roll_photos()

        # Shops and Category
        if self.item_helper.is_shop() or self.item_helper.is_shop_type() or self.item_helper.is_shop_category():
            if self.world.random.random() < CHANCE_VERY_HIGH:
                self.roll_revenue()

            if self.world.random.random() < CHANCE_VERY_HIGH:
                self.roll_profit()

            if self.world.random.random() < CHANCE_LOW:
                self.roll_vouchers()

        # Only Profit OR Revenue possible
        if self.revenue > 0 and self.profit > 0:
            if self.world.random.random() < CHANCE_MEDIUM:
                self.profit = 0
            else:
                self.revenue = 0

        if not self.item_helper.is_trap():
            if self.world.random.random() < CHANCE_HIGH:
                self.roll_customers()

            if self.has_no_stats_set() and self.world.random.random() < CHANCE_EXTREME:
                self.roll_customers()


    def set_amount(self, maximum: int):
        self.amount = self.world.random.randint(1, maximum)


    def try_add_deco_rating(self):
        if not self.world.options.challenge_enable_decoration.value or not self.item_helper.is_coaster():
            return self

        if self.world.random.random() < CHANCE_VERY_LOW:
            return self

        if self.amount > 3:
            self.amount = 3

        self.deco = self.get_deco_rating(self.world.options.difficulty.value)
        return self


    def get_deco_rating(self, difficulty: int):
        chances = ATTRACTION_DECO_RATING_CHANCES[difficulty]

        index = self.world.random.choices(
            population=list(chances.keys()),
            weights=list(chances.values()),
            k=1,
        )[0]
        return ATTRACTION_DECO_RATING[index]


    def _has_valid_shop(self):
        return ((self.item_helper.is_shop() and not self.item_helper.is_facility_shop())
              or (self.item_helper.is_shop_type() and not self.item_helper.is_facility_type()))

    def has_used_shop_requisites_outside_non_profit(self):
        return any(item not in SHOPS[TYPE_NON_PROFIT] for item in self.used_requisites)


    def has_no_stats_set(self):
        return self.excitement == 0 and self.intensity == 0 and self.nausea == 0 and self.revenue == 0 and self.customers == 0


    def decide_revenue_or_profit(self):
        if not (self.revenue > 0 and self.profit > 0):
            return

        if self.world.random.random() < CHANCE_MEDIUM:
            self.profit = 0
        else:
            self.revenue = 0


    def roll_customers(self):
        maximum = 0
        if not self.item_helper.is_trap():
            maximum = self.world.options.challenge_maximum_customers.value

        self.customers = int(round(self.world.random.uniform(0, maximum), ROUND_DIGITS_NONE))


    def roll_excitement(self):
        if not self.item_helper.is_coaster():
            return

        self.excitement = round(self.world.random.uniform(0, self.world.options.challenge_maximum_excitement.value), ROUND_DIGITS)

        if self.item_helper.is_ride_stat_exempt() and self.excitement >= RULE_STAT_EXEMPT_EXCITEMENT_MIN:
            self.excitement = round(min(RULE_STAT_EXEMPT_EXCITEMENT_MIN,self.excitement * RULE_STAT_EXEMPT_EXCITEMENT_MAX_PERCENTAGE),ROUND_DIGITS)


    def roll_intensity(self):
        if not self.item_helper.is_coaster():
            return

        self.intensity = round(self.world.random.uniform(0, self.world.options.challenge_maximum_excitement.value), ROUND_DIGITS)

        if self.item_helper.is_ride_stat_exempt() and self.intensity >= RULE_STAT_EXEMPT_INTENSITY_MIN:
            self.intensity = round(min(RULE_STAT_EXEMPT_INTENSITY_MIN, self.intensity * RULE_STAT_EXEMPT_INTENSITY_MAX_PERCENTAGE),ROUND_DIGITS)
            self.nausea = 0
            self.satisfaction = round(self.satisfaction * RULE_STAT_EXEMPT_SATISFACTION_MAX_PERCENTAGE, ROUND_DIGITS)


    def roll_nausea(self):
        if not self.item_helper.is_coaster():
            return

        self.nausea = round(self.world.random.uniform(0, self.world.options.challenge_maximum_nausea.value), ROUND_DIGITS)

        if self.item_helper.is_ride_stat_exempt() and self.intensity >= RULE_STAT_EXEMPT_INTENSITY_MIN:
            self.nausea = 0


    def roll_satisfaction(self):
        if not self.item_helper.is_coaster():
            return

        self.satisfaction = round(self.world.random.uniform(0, self.world.options.challenge_maximum_satisfaction.value), ROUND_DIGITS)

        if self.item_helper.is_ride_stat_exempt() and self.intensity >= RULE_STAT_EXEMPT_INTENSITY_MIN:
            self.satisfaction = round(self.satisfaction * RULE_STAT_EXEMPT_SATISFACTION_MAX_PERCENTAGE, ROUND_DIGITS)


    def roll_revenue(self):
        maximum = 0

        # Rides
        if self.item_helper.is_ride() or self.item_helper.is_ride_type():
            maximum = self.world.options.challenge_maximum_ride_revenue.value

            if self.item_helper.is_coaster() or self.item_helper.is_coaster_type():
                maximum = self.world.options.challenge_maximum_coaster_revenue.value

            if self.item_helper.is_ride_stat_exempt():
                maximum = RULE_STAT_EXEMPT_REVENUE_MAX

        # Shops
        elif self._has_valid_shop():
            if self.item_helper.is_shop_non_profit() and not (self.has_used_shop_requisites_outside_non_profit()):
                return

            maximum = self.world.options.challenge_maximum_shop_revenue.value

            if self.item_helper.is_shop_stat_exempt():
                maximum = RULE_STAT_EXEMPT_REVENUE_MAX

        if self.item_helper.is_ride_type() or self.item_helper.is_shop_type():
            self.revenue = int(round(self.world.random.uniform(0, maximum) * self.amount, ROUND_DIGITS_NONE))
        else:
            self.revenue = int(round(self.world.random.uniform(0, maximum) / self.amount, ROUND_DIGITS_NONE))


    def roll_profit(self):
        maximum = 0

        # Rides
        if self.item_helper.is_ride() or self.item_helper.is_ride_type():
            maximum = self.world.options.challenge_maximum_ride_profit.value

            if self.item_helper.is_ride_stat_exempt():
                maximum = RULE_STAT_EXEMPT_REVENUE_MAX

        # Shops
        elif self._has_valid_shop():
            if self.item_helper.is_shop_non_profit() and not (self.has_used_shop_requisites_outside_non_profit()):
                return

            maximum = self.world.options.challenge_maximum_shop_profit.value

            if self.item_helper.is_shop_stat_exempt():
                maximum = RULE_STAT_EXEMPT_PROFIT_MAX


        if self.item_helper.is_ride_type() or self.item_helper.is_shop_type():
            self.profit = int(round(self.world.random.uniform(0, maximum) * self.amount, ROUND_DIGITS_NONE))
        else:
            self.profit = int(round(self.world.random.uniform(0, maximum) / self.amount, ROUND_DIGITS_NONE))


    def roll_photos(self):
        if not self.item_helper.is_coaster() or not self.item_helper.is_coaster_type():
            return

        self.photos = int(round(self.world.random.uniform(0, self.world.options.challenge_maximum_photos.value) * self.amount, ROUND_DIGITS_NONE))


    def roll_vouchers(self):
        maximum = 0

        # Rides
        if self.item_helper.is_ride() or self.item_helper.is_ride_type():
            maximum = self.world.options.challenge_maximum_ride_vouchers.value

        # Shops
        elif self._has_valid_shop():
            if self.item_helper.is_shop_non_profit() and not (self.has_used_shop_requisites_outside_non_profit()):
                return

            maximum = self.world.options.challenge_maximum_shop_revenue.value

        self.vouchers = int(round(self.world.random.uniform(0, maximum) * self.amount, ROUND_DIGITS_NONE))