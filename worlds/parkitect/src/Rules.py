from rule_builder.rules import Has, HasGroup, And
from ..src.Item import ItemHelper
from .Options import Difficulty
from .ParkitectCheck import ParkitectCheck
from .Statistics import Statistics
from .Regions import Regions

from ..data.items import *
from ..src.Items import get_extra_checks
from ..data.constants import ATTRACTION_DECO_RATING_INDEX, CHALLENGE_PARK_GUESTS_RANGES, CHALLENGE_EMPLOYEE_RANGES, \
    RULE_TYPE_PARKITECT_ITEM, RULE_TYPE_CATEGORY, RULE_STAT_EXEMPT_REVENUE_MAX, RULE_STAT_EXEMPT_PROFIT_MAX, TIER_2_PROGRESS, TIER_3_PROGRESS, \
    TIER_4_PROGRESS, TIER_5_PROGRESS, CHALLENGE_PAY_MONEY_RANGES, RULE_TYPE_DECORATION, CHANCE_MEDIUM, CHANCE_VERY_HIGH, \
    ROUND_DIGITS_NONE, ROUND_DIGITS, ATTRACTION_DECO_RATING_LOW, ITEMS_PER_LOCATION_LEGACY, START_ITEMS_PER_LOCATION_LEGACY
from .LoggerHelper import LoggerHelper

class Rules:
    def __init__(self, world, _set_rule):
        self.world = world
        self._set_rule = _set_rule
        self.extra_challenges = get_extra_checks(self.world)
        self.world.random.shuffle(self.extra_challenges)


    @staticmethod
    def _build_ruleset(rule_type, selected_item: str, location_number: int):
        LoggerHelper.log(location_number, "_build_ruleset:location_number")

        if rule_type == RULE_TYPE_PARKITECT_ITEM:
            return Has(selected_item)

        if rule_type == RULE_TYPE_CATEGORY:
            return HasGroup(selected_item)

        if rule_type == RULE_TYPE_DECORATION:
            return HasGroup(TYPE_DECORATIONS)

        assert rule_type in (
            RULE_TYPE_PARKITECT_ITEM,
            RULE_TYPE_CATEGORY,
            RULE_TYPE_DECORATION,
        ), "Rule type unknown!"

        return None


    def _set_parkitect_rule(self, rules, location_number: int) -> None:
        LoggerHelper.log(location_number, "_set_parkitect_rule:location_number")
        LoggerHelper.log(rules, "_set_parkitect_rule:rules")

        region_name = Regions.get_region_from_parkitect_location(location_number)
        region = self.world.multiworld.get_region(region_name, self.world.player)
        entrance = region.entrances[0]

        assert entrance is not None, f"Couldn't find regions entrance \"{region_name}\"->\"{entrance}\" for location_number {location_number}"

        self._set_rule(entrance, rules)

        LoggerHelper.log(
            region.name,
            "REGION"
        )

        for entrance in region.entrances:
            LoggerHelper.log(
                entrance.access_rule,
                f"ENTRANCE RULE: {entrance.name}"
            )


    def _get_modifier(self) -> float:
        if self.world.options.difficulty == Difficulty.medium.value:
            return .45

        if self.world.options.difficulty == Difficulty.hard.value:
            return .65

        if self.world.options.difficulty == Difficulty.extreme.value:
            return .85

        return .25


    def _is_difficulty(self, difficulty: Difficulty) -> bool:
        return self.world.options.difficulty == difficulty.value


    @staticmethod
    def determine_item_category(item: str, should_be_generic_type: bool = False) -> str:
        if should_be_generic_type:
            if item in SHOPS[TYPE_ALL]:
                return TYPE_SHOPS
            return TYPE_RIDES

        if item in SHOPS[TYPE_SHOP_DRINKS]:
            return TYPE_SHOP_DRINKS

        if item in SHOPS[TYPE_SHOP_FOOD]:
            return TYPE_SHOP_FOOD

        if item in SHOPS[TYPE_SHOP_FACILITIES]:
            return TYPE_SHOP_FACILITIES

        if item in RIDES[TYPE_CALM_RIDES]:
            return TYPE_CALM_RIDES

        if item in RIDES[TYPE_THRILL_RIDES]:
            return TYPE_THRILL_RIDES

        if item in RIDES[TYPE_COASTER_RIDES]:
            return TYPE_COASTER_RIDES

        if item in RIDES[TYPE_TRANSPORT_RIDES]:
            return TYPE_TRANSPORT_RIDES

        if item in RIDES[TYPE_WATER_RIDES]:
            return TYPE_WATER_RIDES

        raise AssertionError(f"No Item Category found for item \"{item}\"")


    def determine_pay_money(self, number: int) -> int:
        value = self.world.options.goal_money.value
        difficulty = self.world.options.difficulty.value

        # Something between the ranges
        if value <= 0:
            ranges = CHALLENGE_PAY_MONEY_RANGES[difficulty]
            return int(self.world.random.uniform(ranges[0], ranges[1]))

        maximum = CHALLENGE_PAY_MONEY_RANGES[difficulty][1]
        multiplier = 1
        if number < START_ITEMS_PER_LOCATION_LEGACY:
            multiplier /= 2

        min = value / 200  # .5%
        return int(self.world.random.uniform(min, maximum) * multiplier)


    def determine_park_guests(self, progress: float, number: int = START_ITEMS_PER_LOCATION_LEGACY) -> int:
        multiplier = self._get_modifier()
        if number < START_ITEMS_PER_LOCATION_LEGACY:
            multiplier /= 2
        elif progress > TIER_2_PROGRESS:
            multiplier = 1

        value = self.world.options.goal_guests.value
        difficulty = self.world.options.difficulty.value

        # Something between the ranges
        if value <= 0:
            ranges = CHALLENGE_PARK_GUESTS_RANGES[difficulty]
            result = int(self.world.random.uniform(ranges[0], ranges[1]) * multiplier)
            return result if result > 0 else 1

        maximum = CHALLENGE_PARK_GUESTS_RANGES[difficulty][1]
        min = max(100, value / 2)  # 50%

        result = int(self.world.random.uniform(min, maximum) * multiplier)
        return result if result > 0 else 1


    def determine_employees(self, employee_type: str, progress: float, number: int = START_ITEMS_PER_LOCATION_LEGACY) -> int:
        multiplier = self._get_modifier()
        if number < START_ITEMS_PER_LOCATION_LEGACY:
            multiplier /= 2
        elif progress > TIER_2_PROGRESS:
            multiplier = 1

        difficulty = self.world.options.difficulty.value
        ranges = CHALLENGE_EMPLOYEE_RANGES[employee_type][difficulty]
        result = int(self.world.random.uniform(ranges[0], ranges[1]) * multiplier)

        return result if result > 0 else 1


    def set(self) -> None:
        difficulty_modifier: float = self._get_modifier()

        prerequisites = [self.world.starter]
        queued_prerequisites = []
        rules = []
        item_table_length = len(self.world.item_table)

        LoggerHelper.log(self.world.starter, "starter")

        for number, parkitect_item in enumerate(self.world.item_table):
            LoggerHelper.info("____________________________________________________________________________")
            LoggerHelper.log(prerequisites, "prerequisites")
            LoggerHelper.log(parkitect_item, "parkitect_item")
            parkitect_item_helper = ItemHelper(parkitect_item)

            # Chosen prerequisite
            if self.world.random.random() < difficulty_modifier:
                item = self.world.random.choice(prerequisites)
                LoggerHelper.log(item, "Chosen prerequisite")
                rules.append(self._build_ruleset(RULE_TYPE_PARKITECT_ITEM, item, number))

            # Is category
            else:
                should_be_generic_type = self.world.random.random() < CHANCE_MEDIUM
                item = Rules.determine_item_category(self.world.random.choice(prerequisites), should_be_generic_type)
                LoggerHelper.log(item, "Chosen category")
                rules.append(self._build_ruleset(RULE_TYPE_CATEGORY, item, number))

            progress: float = number / item_table_length
            item_helper = self._find_challenge(item, number)
            parkitect_check = self._create_check(number, item_helper, prerequisites, progress)
            LoggerHelper.log(parkitect_check.to_dict(), "parkitect_check")
            self.world.challenges.append(parkitect_check.to_dict())

            if parkitect_check.has_decoration():
                if ATTRACTION_DECO_RATING_INDEX[parkitect_check.get_decoration_index()] >= ATTRACTION_DECO_RATING_INDEX[
                    ATTRACTION_DECO_RATING_LOW]:
                    rules.append(self._build_ruleset(RULE_TYPE_DECORATION, '', number))

            # Handle unlocked rides
            if parkitect_item_helper.is_shop() or parkitect_item_helper.is_ride():
                queued_prerequisites.append(parkitect_item_helper.item)

            # Must be 11 or at least 12 and be dividable through 4 without rest
            # 11, 12, 16, 20, 24, 28, ...
            if (number + 1) == START_ITEMS_PER_LOCATION_LEGACY or (number >= START_ITEMS_PER_LOCATION_LEGACY and number % 4 == 0):
                for prereq in queued_prerequisites:
                    prerequisites.append(prereq)
                queued_prerequisites.clear()

            # apply rules
            if (number + 1) >= START_ITEMS_PER_LOCATION_LEGACY and (number + 1) % ITEMS_PER_LOCATION_LEGACY == 0:
                self._set_parkitect_rule(And(*rules), number)
                rules.clear()


    def _find_challenge(self, item: str, number: int) -> ItemHelper:
        if len(self.extra_challenges) > 0:
            chance = CHANCE_MEDIUM if number < START_ITEMS_PER_LOCATION_LEGACY else .2
            coin = self.world.random.random()  # 0.0 -> 1.0

            if coin < chance:
                item = self.extra_challenges.pop()
                LoggerHelper.log(item, "Extra Challenge")

        return ItemHelper(item)


    def _create_check(self, number: int, item_helper: ItemHelper, prerequisites: list, progress: float) -> ParkitectCheck:
        parkitect_check = ParkitectCheck(number)
        minimum = 1

        # Pay Money -> {money}
        if item_helper.is_challenge_pay_money():
            money = self.determine_pay_money(number)
            parkitect_check.set_item(Statistics(item_helper, money))


        # Park Guests -> {guests}
        elif item_helper.is_challenge_park_guests():
            guests = self.determine_park_guests(progress, number)
            parkitect_check.set_item(Statistics(item_helper, guests))


        # Employees -> {employee}
        elif item_helper.is_challenge_employees():
            employee_type = self.world.random.choice(EMPLOYEES[TYPE_ALL])
            employees = self.determine_employees(employee_type, progress, number)
            parkitect_check.set_item(Statistics(item_helper, employees))
            parkitect_check.update_item_name(employee_type)

        # Here begins stuff with Attraction / Shop and its categories

        # --- Tier 1: -> Level 0 ---
        elif number < START_ITEMS_PER_LOCATION_LEGACY:
            # max: 2
            maximum = 2

            if item_helper.is_coaster() or item_helper.is_coaster_type():
                maximum = 1

            parkitect_check.set_item(Statistics(
                item_helper,
                self.world.random.randint(minimum, maximum),
            ))


        # --- Tier 2: -> 10% ---
        elif progress <= TIER_2_PROGRESS:
            customers = 0

            # Shop -> max: 3
            # Shop Category Type -> max: 6
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 3
                shop_revenue = 0
                shop_profit = 0

                if item_helper.is_shop_type():
                    maximum = 6

                # We can make shop_revenue or shop_profit if shop can make good money
                if not item_helper.is_shop_non_profit() and not item_helper.is_facility_type():
                    if self.world.random.random() < CHANCE_MEDIUM:
                        shop_revenue = round(self.world.random.uniform(
                            0,
                            self.world.options.challenge_maximum_shop_revenue.value
                        ), ROUND_DIGITS)

                    if self.world.random.random() < CHANCE_MEDIUM:
                        shop_profit = round(self.world.random.uniform(
                            0,
                            self.world.options.challenge_maximum_shop_profit.value
                        ), ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    customers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_customers.value
                    ), ROUND_DIGITS_NONE)

                if shop_revenue > 0 and shop_profit > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        shop_profit = 0
                    else:
                        shop_revenue = 0

                # Both given? I only want 1
                if (shop_revenue > 0 or shop_profit > 0) and customers > 0:
                    # Coin flip to decide which one to keep
                    if self.world.random.random() < CHANCE_MEDIUM:
                        customers = 0
                    else:
                        shop_revenue = 0
                        shop_profit = 0

                if item_helper.is_shop_stat_exempt() and shop_revenue > RULE_STAT_EXEMPT_REVENUE_MAX:
                    shop_revenue = round(
                        self.world.random.uniform(0, RULE_STAT_EXEMPT_REVENUE_MAX),
                        ROUND_DIGITS)

                parkitect_check.set_item(Statistics(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    revenue=shop_revenue,
                    profit=shop_profit,
                    customers=customers,
                ))

            # Ride -> max: 2
            # Ride Category Type -> max: 4
            # Coaster + Type -> max: 1
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 2
                ride_revenue = 0
                ride_profit = 0
                ride_photos = 0

                if item_helper.is_ride_type():
                    maximum = 4

                elif item_helper.is_coaster() or item_helper.is_coaster_type():
                    maximum = 1

                    if self.world.random.random() < CHANCE_VERY_HIGH:
                        ride_photos = round(self.world.random.uniform(
                            0,
                            self.world.options.challenge_maximum_photos.value
                        ), ROUND_DIGITS_NONE)

                if self.world.random.random() < CHANCE_MEDIUM:
                    ride_revenue = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_ride_revenue.value
                    ), ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    ride_profit = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_ride_profit.value
                    ), ROUND_DIGITS)

                if item_helper.is_ride_stat_exempt() and ride_revenue > RULE_STAT_EXEMPT_REVENUE_MAX:
                    ride_revenue = round(
                        self.world.random.uniform(0, RULE_STAT_EXEMPT_REVENUE_MAX),
                        ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    customers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_customers.value
                    ), ROUND_DIGITS_NONE)

                if ride_revenue > 0 and ride_profit > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        ride_profit = 0
                    else:
                        ride_revenue = 0

                # Both given? i only want 1
                if (ride_revenue > 0 or ride_profit > 0) and customers > 0:
                    # Coin flip to decide which one to keep
                    if self.world.random.random() < CHANCE_MEDIUM:
                        customers = 0
                    else:
                        ride_profit = 0
                        ride_revenue = 0

                parkitect_check.set_item(Statistics(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    revenue=ride_revenue,
                    profit=ride_profit,
                    customers=customers,
                    photos=ride_photos
                ).try_add_deco_rating(item_helper, self.world))


        # --- Tier 3: -> 18% ---
        elif progress <= TIER_3_PROGRESS:
            customers = 0

            # Shop -> max: 3
            # Shop Category Type -> max: 6
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 3
                shop_revenue = 0
                shop_profit = 0
                shop_vouchers = 0

                if item_helper.is_shop_type():
                    maximum = 6

                # We can make shop_revenue or shop_profit if shop can make good money
                if not item_helper.is_shop_non_profit() and not item_helper.is_facility_type() and self.world.random.random() < CHANCE_MEDIUM:
                    shop_revenue = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_shop_revenue.value
                    ), ROUND_DIGITS)

                    shop_profit = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_shop_profit.value
                    ), ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    customers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_customers.value
                    ), ROUND_DIGITS_NONE)

                if self._is_difficulty(Difficulty.extreme) and (
                        item_helper.is_drink_shop() or item_helper.is_food_shop()
                ) and self.world.random.random() < CHANCE_MEDIUM:
                    shop_vouchers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_shop_vouchers.value
                    ), ROUND_DIGITS_NONE)

                if shop_revenue > 0 and shop_profit > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        shop_profit = 0
                    else:
                        shop_revenue = 0

                # Both given? i only want 1
                if (shop_revenue > 0 and shop_profit > 0) and customers > 0:
                    # Coin flip to decide which one to keep
                    if self.world.random.random() < CHANCE_MEDIUM:
                        customers = 0
                    else:
                        shop_revenue = 0
                        shop_profit = 0

                if item_helper.is_shop_stat_exempt() and shop_revenue > RULE_STAT_EXEMPT_REVENUE_MAX:
                    shop_revenue = round(
                        self.world.random.uniform(0, RULE_STAT_EXEMPT_REVENUE_MAX),
                        ROUND_DIGITS)

                parkitect_check.set_item(Statistics(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    revenue=shop_revenue,
                    profit=shop_profit,
                    customers=customers,
                    vouchers=shop_vouchers
                ))

            # Ride -> max: 3
            # Ride Category Type -> max: 6
            # Coaster -> max: 2
            # Ride Coaster Category Type -> max: 2
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 3
                ride_revenue = 0
                ride_profit = 0
                ride_photos = 0
                ride_vouchers = 0

                if item_helper.is_ride_type():
                    maximum = 6

                elif item_helper.is_coaster() or item_helper.is_coaster_type():
                    maximum = 2

                    if self.world.random.random() < CHANCE_VERY_HIGH:
                        ride_photos = round(self.world.random.uniform(
                            0,
                            self.world.options.challenge_maximum_photos.value
                        ), ROUND_DIGITS_NONE)

                if self.world.random.random() < CHANCE_MEDIUM:
                    ride_revenue = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_ride_revenue.value
                    ), ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    ride_profit = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_ride_profit.value
                    ), ROUND_DIGITS)

                if self._is_difficulty(Difficulty.extreme) and self.world.random.random() < CHANCE_MEDIUM:
                    ride_vouchers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_ride_vouchers.value
                    ), ROUND_DIGITS_NONE)

                if item_helper.is_ride_stat_exempt() and ride_revenue > RULE_STAT_EXEMPT_REVENUE_MAX:
                    ride_revenue = round(
                        self.world.random.uniform(0, RULE_STAT_EXEMPT_REVENUE_MAX),
                        ROUND_DIGITS)

                if item_helper.is_ride_stat_exempt() and ride_profit > RULE_STAT_EXEMPT_PROFIT_MAX:
                    ride_profit = round(
                        self.world.random.uniform(0, RULE_STAT_EXEMPT_PROFIT_MAX),
                        ROUND_DIGITS)

                if self.world.random.random() < CHANCE_MEDIUM:
                    customers = round(self.world.random.uniform(
                        0,
                        self.world.options.challenge_maximum_customers.value
                    ), ROUND_DIGITS_NONE)

                if ride_revenue > 0 and ride_profit > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        ride_profit = 0
                    else:
                        ride_revenue = 0

                # Both given? i only want 1
                if (ride_revenue > 0 or ride_profit > 0) and customers > 0:
                    # Coin flip to decide which one to keep
                    if self.world.random.random() < CHANCE_MEDIUM:
                        customers = 0
                    else:
                        ride_profit = 0
                        ride_revenue = 0

                parkitect_check.set_item(Statistics(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    revenue=ride_revenue,
                    profit=ride_profit,
                    customers=customers,
                    vouchers=ride_vouchers,
                    photos=ride_photos
                ).try_add_deco_rating(item_helper, self.world))


        # --- Tier 4: -> 35% ---
        elif progress <= TIER_4_PROGRESS:
            # Shop -> max: 4
            # Shop Category Type -> max: 12
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 4

                if item_helper.is_shop_type():
                    maximum = 12

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ))

            # Ride -> max: 3
            # Ride Category Type -> max: 7
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 3

                if item_helper.is_ride_type():
                    maximum = 7

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ).try_add_deco_rating(item_helper, self.world))


        # --- Tier 5: -> 60% ---
        elif progress <= TIER_5_PROGRESS:
            # Shop -> max: 6
            # Shop Category -> max: 24
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 6

                if item_helper.is_shop_type():
                    maximum = 24

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ))

            # Ride -> max: 4
            # Coaster -> max: 3
            # Ride Category Type -> max: 10
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 4

                if item_helper.is_coaster():
                    maximum = 3

                elif item_helper.is_ride_type():
                    maximum = 10

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ).try_add_deco_rating(item_helper, self.world))


        # --- Tier 6: +60% ---
        else:
            # Shops -> max: 6
            # Shop Category -> max: 30
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 6

                if item_helper.is_shop_type():
                    maximum = 30

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ))

            # Ride -> max: 4
            # Coaster Ride -> max: 4
            # Ride Category -> max: 15
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 4

                if item_helper.is_ride_type():
                    maximum = 15

                parkitect_check.set_item(Statistics.random_roll(
                    item_helper,
                    self.world.random.randint(minimum, maximum),
                    self.world,
                    prerequisites
                ).try_add_deco_rating(item_helper, self.world))

        assert parkitect_check.location_id >= 0, f"Missing location_id for item: \"{item_helper.item}\""
        assert parkitect_check.item is not None, f"Parkitect Item unset: \"{item_helper.item}\""
        assert len(parkitect_check.item.to_dict()) > 0, f"No item set for a check. Item: \"{item_helper.item}\""

        return parkitect_check
