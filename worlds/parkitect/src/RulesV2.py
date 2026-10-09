import math

from rule_builder.rules import Has, HasGroup, And
from ..src.Item import ItemHelper
from .Options import Difficulty
from .ParkitectCheck import ParkitectCheck
from .StatisticsV2 import StatisticsV2
from .RegionsV2 import RegionsV2

from ..data.items import *
from ..src.Items import get_extra_checks
from ..data.constants import ATTRACTION_DECO_RATING_INDEX, CHALLENGE_PARK_GUESTS_RANGES, CHALLENGE_EMPLOYEE_RANGES, \
  RULE_TYPE_PARKITECT_ITEM, RULE_TYPE_CATEGORY, TIER_2_PROGRESS, TIER_3_PROGRESS, \
  TIER_4_PROGRESS, TIER_5_PROGRESS, CHALLENGE_PAY_MONEY_RANGES, RULE_TYPE_DECORATION, CHANCE_MEDIUM, CHANCE_VERY_HIGH, \
  ATTRACTION_DECO_RATING_LOW, ITEMS_PER_LOCATION, START_ITEMS_PER_LOCATION
from .LoggerHelper import LoggerHelper


class RulesV2:
    def __init__(self, world):
        self.world = world
        self.extra_challenges = get_extra_checks(self.world)
        self.world.random.shuffle(self.extra_challenges)


    @staticmethod
    def _build_ruleset(rule_type, selected_item: str):
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

        region_name = RegionsV2.get_region_from_parkitect_location(location_number)
        region = self.world.multiworld.get_region(region_name, self.world.player)
        entrance = region.entrances[0]

        assert entrance is not None, f"Couldn't find regions entrance \"{region_name}\"->\"{entrance}\" for location_number {location_number}"

        self.world.set_rule(entrance, rules)

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


    def _get_ride_shop_modified_value(self, amount: int) -> int:
        if self.world.options.difficulty == Difficulty.extreme.value:
            return amount

        if self.world.options.difficulty == Difficulty.medium.value:
            return round(amount * .75)

        if self.world.options.difficulty == Difficulty.hard.value:
            return round(amount * .85)

        if self.world.options.difficulty == Difficulty.extreme.value:
            return round(amount * 1)

        return round(amount * .65)


    def _is_difficulty(self, difficulty: Difficulty) -> bool:
        return self.world.options.difficulty == difficulty.value


    def determine_pay_money(self, number: int) -> int:
        value = self.world.options.goal_money.value
        difficulty = self.world.options.difficulty.value
        maximum = CHALLENGE_PAY_MONEY_RANGES[difficulty][1]
        multiplier = 1
        if number < START_ITEMS_PER_LOCATION:
          multiplier /= 2

        # Unset Money Goal, so we take from ranges
        if value <= 0:
            return int(self.world.random.uniform(CHALLENGE_PAY_MONEY_RANGES[difficulty][0], maximum) * multiplier)

        minimum = value / 200 # .5%
        return int(self.world.random.uniform(minimum, maximum) * multiplier)


    def determine_park_guests(self, progress: float, location_id: int) -> int:
        multiplier = self._get_modifier()
        if location_id <= START_ITEMS_PER_LOCATION:
            multiplier /= 2
        elif progress > TIER_2_PROGRESS:
            multiplier = 1

        value = self.world.options.goal_guests.value
        difficulty = self.world.options.difficulty.value
        maximum = CHALLENGE_PARK_GUESTS_RANGES[difficulty][1]

        # Unset ParkGuest Goal, so we take from ranges
        if value <= 0:
            return int(self.world.random.uniform(CHALLENGE_PARK_GUESTS_RANGES[difficulty][0], maximum) * multiplier)

        minimum = max(50, value / 2)
        return int(self.world.random.uniform(minimum, maximum) * multiplier)


    def determine_employees(self, employee_type: str, progress: float, location_id: int = START_ITEMS_PER_LOCATION) -> int:
        multiplier = self._get_modifier()
        if location_id <= START_ITEMS_PER_LOCATION:
            multiplier /= 2
        elif progress > TIER_2_PROGRESS:
            multiplier = 1

        difficulty = self.world.options.difficulty.value
        ranges = CHALLENGE_EMPLOYEE_RANGES[employee_type][difficulty]
        return int(self.world.random.uniform(ranges[0], ranges[1]) * multiplier)


    def create_mask(self, at_least: int, maximum: int) -> list[int]:
        values = [True] * maximum
        indices = self.world.random.sample(range(maximum), at_least)

        for i in indices:
            values[i] = False

        return values


    def set(self) -> None:
        difficulty_modifier: float = self._get_modifier()
        item_table_length = len(self.world.item_table)

        used_requisites: list[str] = []
        unused_requisites: list[str] = []
        current_requisite: str = self.world.starter
        maximum_requisite: int = math.ceil(self.world.random.uniform(1, START_ITEMS_PER_LOCATION * difficulty_modifier))
        requisites_order = self.create_mask(maximum_requisite, START_ITEMS_PER_LOCATION)

        rules = []

        LoggerHelper.log(self.world.starter, "starter")

        for location_id, parkitect_item in enumerate(self.world.item_table):
            parkitect_item_helper = ItemHelper(parkitect_item)
            progress: float = location_id / item_table_length

            LoggerHelper.info("____________________________________________________________________________")
            LoggerHelper.log(unused_requisites, "unused_requisites")
            LoggerHelper.log(parkitect_item, "parkitect_item")
            LoggerHelper.log(requisites_order, "requisites_order")
            LoggerHelper.log(current_requisite, "current_requisite")

            is_requisite = requisites_order.pop()
            item_or_category = current_requisite

            # Chosen prerequisite
            if self.world.random.random() < difficulty_modifier:
                LoggerHelper.log(current_requisite, "Chosen Requisite")
                rules.append(self._build_ruleset(RULE_TYPE_PARKITECT_ITEM, item_or_category))

            # Is category
            else:
                should_be_generic_type = self.world.random.random() < CHANCE_MEDIUM
                item_or_category = ItemHelper.determine_item_category(current_requisite, should_be_generic_type)
                LoggerHelper.log(item_or_category, "Chosen Category")
                rules.append(self._build_ruleset(RULE_TYPE_CATEGORY, item_or_category))

            # ! is_requisite and extra challenges left means Extra Challenge, otherwise its always requisite
            item_helper = ItemHelper(item_or_category)
            if len(self.extra_challenges) > 0 and not is_requisite:
                item_helper = ItemHelper(self.extra_challenges.pop(0))

            parkitect_check: ParkitectCheck = self._create_check(location_id, item_helper, used_requisites, progress)
            LoggerHelper.log(parkitect_check.to_dict(), "parkitect_check")

            if parkitect_check.has_decoration():
                if ATTRACTION_DECO_RATING_INDEX[parkitect_check.get_decoration_index()] >= ATTRACTION_DECO_RATING_INDEX[
                    ATTRACTION_DECO_RATING_LOW]:
                    rules.append(self._build_ruleset(RULE_TYPE_DECORATION, ''))

            # Handle unlocked rides
            if parkitect_item_helper.is_shop() or parkitect_item_helper.is_ride():
                unused_requisites.append(parkitect_item_helper.item)

            self.world.challenges.setdefault(current_requisite, []).append(
                parkitect_check.to_dict()
            )

            # recreate requisites if order empty
            if len(requisites_order) <= 0:
                used_requisites.append(current_requisite)
                current_requisite = self.world.random.choice(unused_requisites)
                unused_requisites.remove(current_requisite)
                maximum_requisite = math.ceil(self.world.random.uniform(1, ITEMS_PER_LOCATION * difficulty_modifier))
                requisites_order = self.create_mask(maximum_requisite, ITEMS_PER_LOCATION)

                # Apply rules
                self._set_parkitect_rule(And(*rules), location_id - 1)
                rules.clear()


    def _create_check(self, location_id: int, item_helper: ItemHelper, used_requisites: list[str], progress: float) -> ParkitectCheck:
        statistics: StatisticsV2 = StatisticsV2(self.world, item_helper, used_requisites)

        # Pay Money -> {money}
        if item_helper.is_challenge_pay_money():
            money = self.determine_pay_money(location_id)
            statistics.amount = money


        # Park Guests -> {guests}
        elif item_helper.is_challenge_park_guests():
            guests = self.determine_park_guests(progress, location_id)
            statistics.amount = guests


        # Employees -> {employee}
        elif item_helper.is_challenge_employees():
            employee_type = self.world.random.choice(EMPLOYEES[TYPE_ALL])
            employees = self.determine_employees(employee_type, progress, location_id)
            statistics.name = employee_type
            statistics.amount = employees


        # Here begins stuff with Attraction / Shop and its categories
        # --- Tier 1: -> Level 0 ---
        elif location_id < START_ITEMS_PER_LOCATION:
            # max: 2
            maximum = 2

            if item_helper.is_coaster() or item_helper.is_coaster_type():
                maximum = 1

            statistics.set_amount(maximum)


        # --- Tier 2: -> 10% ---
        elif progress <= TIER_2_PROGRESS:
            # Shop -> max: 3
            # Shop Category Type -> max: 6
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 3

                if item_helper.is_shop_type():
                  maximum = 6

                statistics.set_amount(maximum)

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_revenue()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_profit()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_customers()

                statistics.decide_revenue_or_profit()

                # Both given? I only want 1
                if (statistics.revenue > 0 or statistics.profit > 0) and statistics.customers > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        statistics.customers = 0
                    else:
                        statistics.revenue = 0
                        statistics.profit = 0

            # Ride -> max: 2
            # Ride Category Type -> max: 4
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 2

                if item_helper.is_ride_type():
                    maximum = 4

                statistics.set_amount(maximum)

                if self.world.random.random() < CHANCE_VERY_HIGH:
                    statistics.roll_photos()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_revenue()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_profit()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_customers()

                statistics.decide_revenue_or_profit()

                # Both given? I only want 1
                if (statistics.revenue > 0 or statistics.profit > 0) and statistics.customers > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        statistics.customers = 0
                    else:
                        statistics.revenue = 0
                        statistics.profit = 0

                statistics.try_add_deco_rating()


        # --- Tier 3: -> 18% ---
        elif progress <= TIER_3_PROGRESS:
            # Shop -> max: 3
            # Shop Category Type -> max: 6
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 3

                if item_helper.is_shop_type():
                    maximum = 6

                statistics.set_amount(maximum)

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_revenue()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_profit()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_customers()

                if self._is_difficulty(Difficulty.extreme) and self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_vouchers()

                statistics.decide_revenue_or_profit()

                # Both given? I only want 1
                if (statistics.revenue > 0 or statistics.profit > 0) and statistics.customers > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        statistics.customers = 0
                    else:
                        statistics.revenue = 0
                        statistics.profit = 0

            # Ride -> max: 3
            # Ride Category Type -> max: 6
            # Coaster -> max: 2
            # Ride Coaster Category Type -> max: 2
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 3

                if item_helper.is_ride_type():
                    maximum = 6

                statistics.set_amount(maximum)

                if self.world.random.random() < CHANCE_VERY_HIGH:
                    statistics.roll_photos()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_revenue()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_profit()

                if self._is_difficulty(Difficulty.extreme) and self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_vouchers()

                if self.world.random.random() < CHANCE_MEDIUM:
                    statistics.roll_customers()

                statistics.decide_revenue_or_profit()

                # Both given? I only want 1
                if (statistics.revenue > 0 or statistics.profit > 0) and statistics.customers > 0:
                    if self.world.random.random() < CHANCE_MEDIUM:
                        statistics.customers = 0
                    else:
                        statistics.revenue = 0
                        statistics.profit = 0

                statistics.try_add_deco_rating()


        # --- Tier 4: -> 35% ---
        elif progress <= TIER_4_PROGRESS:
            maximum = 1

            # Shop -> max: 4
            # Shop Category Type -> max: 12
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 4

                if item_helper.is_shop_type():
                    maximum = self._get_ride_shop_modified_value(12)

            # Ride -> max: 3
            # Ride Category Type -> max: 7
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 3

                if item_helper.is_ride_type():
                    maximum = 7

            statistics.set_amount(maximum)
            statistics.roll()
            statistics.try_add_deco_rating()


        # --- Tier 5: -> 60% ---
        elif progress <= TIER_5_PROGRESS:
            maximum = 1

            # Shop -> max: 6
            # Shop Category -> max: 24
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 6

                if item_helper.is_shop_type():
                    maximum = self._get_ride_shop_modified_value(24)

            # Ride -> max: 4
            # Coaster -> max: 3
            # Ride Category Type -> max: 10
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 4

                if item_helper.is_coaster():
                    maximum = 3

                elif item_helper.is_ride_type():
                    maximum = self._get_ride_shop_modified_value(10)

            statistics.set_amount(maximum)
            statistics.roll()
            statistics.try_add_deco_rating()


        # --- Tier 6: +60% ---
        else:
            maximum = 1

            # Shops -> max: 6
            # Shop Category -> max: 30
            if item_helper.is_shop() or item_helper.is_shop_category():
                maximum = 6

                if item_helper.is_shop_type():
                    maximum = self._get_ride_shop_modified_value(20)

            # Ride -> max: 4
            # Coaster Ride -> max: 4
            # Ride Category -> max: 15
            elif item_helper.is_ride() or item_helper.is_ride_category():
                maximum = 4

                if item_helper.is_ride_type():
                    maximum = self._get_ride_shop_modified_value(15)

            statistics.set_amount(maximum)
            statistics.roll()
            statistics.try_add_deco_rating()

        parkitect_check = ParkitectCheck(location_id)
        parkitect_check.set_item(statistics)

        assert parkitect_check.location_id >= 0, f"Missing location_id for item: \"{item_helper.item}\""
        assert parkitect_check.item is not None, f"Parkitect Item unset: \"{item_helper.item}\""
        assert len(parkitect_check.item.to_dict()) > 0, f"No item set for a check. Item: \"{item_helper.item}\""

        return parkitect_check

