import random
from collections import Counter
from typing import Iterable


class GameLogic:
    """
    This class is responsible for ten thousand game logic.

    methods:
        calculate_score(dices_value: tuple[int, ...]) -> int :
            calculate the score of the dices value

        roll_dice(num_of_dices: int) -> tuple[int, ...] :
            roll the dices and return the dices value
    """

    @classmethod
    def get_dices_info(cls, dices_value: Iterable[int]) -> tuple[int, list[int]]:
        """
            get info for the dices (score, dice_that_used)
        """
        score: int = 0
        scored_dice: list[int] = []

        dice_counter = Counter(dices_value)

        # no dice
        if (len(dice_counter) == 0):
            return (score, scored_dice)

        # straight dices
        if len(dice_counter) == 6:
            score = 1500
            scored_dice = list(dices_value)
            return (score, scored_dice)

        # three pairs
        if (len(dice_counter) == 3 and cls.all_eq_num(dice_counter.values(), 2)):
            score = 1000
            scored_dice = list(dices_value)
            return (score, scored_dice)

        # 3 or more of a kind
        dices = [dice for dice in dice_counter.items() if dice[1] >= 3]
        for dice_num, dice_rep in dices:
            if (dice_num == 1):
                score += 1000 * 2 ** (dice_rep - 3)
            else:
                score += dice_num * 100 * 2 ** (dice_rep - 3)
            scored_dice += [dice_num] * dice_rep

        # ones
        dice_one_rep = dice_counter.get(1)
        if (dice_one_rep is not None and dice_one_rep <= 2):
            score += dice_one_rep * 100
            scored_dice += [1] * dice_one_rep

        # fives
        dice_five_rep = dice_counter.get(5)
        if (dice_five_rep is not None and dice_five_rep <= 2):
            score += dice_five_rep * 50
            scored_dice += [5] * dice_five_rep

        return (score, scored_dice)

    @classmethod
    def calculate_score(cls, dices_value: tuple[int, ...]) -> int:
        """
        calculate the score of the dices value

        Args:
            dices_value (tuple[int, ...]): the dices value

        Returns:
            int: the score of the dices value
        """
        score = cls.get_dices_info(dices_value)[0]
        return score

    @classmethod
    def get_scorers(cls, dices_value: Iterable[int]) -> tuple[int, ...]:
        """
        get the dices that used to calculate the score

        Args:
            dices_value (tuple[int, ...]): the dices value

        Returns:
            tuple[int, ...]: the dices that used to calculate the score
        """
        scored_dice = cls.get_dices_info(dices_value)[1]
        return tuple(scored_dice)

    @classmethod
    def validate_keepers(cls, roll: tuple[int, ...], keeper: tuple[int, ...]) -> bool:
        """
        check if the keeper is valid

        Args:
            roll (tuple[int, ...]): the roll value
            keeper (tuple[int, ...]): the keeper value

        Returns:
            bool: True if the keeper is valid, False otherwise
        """
        roll_counter = Counter(roll)
        keeper_counter = Counter(keeper)

        extra_dice = keeper_counter - roll_counter
        if (len(extra_dice) != 0):
            return False

        return True

    @classmethod
    def roll_dice(cls, num_of_dices: int) -> tuple[int, ...]:
        '''
        Simulate the rolling of multiple dice and return the results as a tuple.

        Args:
        - num_of_dices: An integer representing the number of dice to roll.

        Returns:
        - A tuple of integers representing the results of the dice rolls.
        Each integer is between 1 and 6, inclusive, and corresponds to the
        outcome of one die roll.
        '''
        return tuple(random.randint(1, 6) for _ in range(num_of_dices))

    @staticmethod
    def all_eq_num(nums: Iterable[int], value: int) -> bool:
        bool_list = [num == value for num in nums]
        return all(bool_list)
