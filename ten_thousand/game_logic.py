import random

class GameLogic:

    def __init__(self):
        pass

    @classmethod
    def calculate_score(cls, dice_values):
        pass

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
    
    
    

