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
    def calculate_score(cls, dices_value: tuple[int, ...]):
        """
        calculate the score of the dices value

        Args:
            dices_value (tuple[int, ...]): the dices value

        Returns:
            int: the score of the dices value
        """
        # no dice
        if (len(dices_value) == 0):
            return 0

        dice_counter = Counter(dices_value)
        score: int = 0

        # straight dices
        if len(dice_counter) == 6:
            return 1500

        # three pairs
        if (len(dice_counter) == 3 and cls.all_eq_num(dice_counter.values(), 2)):
            return 1000

        # 3 or more of a kind
        dices = [dice for dice in dice_counter.items() if dice[1] >= 3]
        for dice_num, dice_rep in dices:
            if (dice_num == 1):
                score += 1000 * 2 ** (dice_rep - 3)
            else:
                score += dice_num * 100 * 2 ** (dice_rep - 3)

        # ones
        dice_one_rep = dice_counter.get(1)
        if (dice_one_rep is not None and dice_one_rep <= 2):
            score += dice_one_rep * 100

        # fives
        dice_five_rep = dice_counter.get(5)
        if (dice_five_rep is not None and dice_five_rep <= 2):
            score += dice_five_rep * 50

        return score

    @classmethod
    def roll_dice(cls, num_of_dices):
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
