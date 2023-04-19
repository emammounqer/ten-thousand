from ten_thousand.game_logic import GameLogic


class Game:
    def __init__(self, roller=GameLogic.roll_dice):
        self.banked_score = 0
        self.unbanked_points = 0
        self.round = 0
        self.num_dice = 6
        self.roller = roller

    def start_game(self):
        print("Welcome to Ten Thousand")
        print("(y)es to play or (n)o to decline")
        self._take_input()

    def _new_round(self):
        self.round += 1
        self.num_dice = 6

        print(f"Starting round {self.round}")
        print(f"Rolling {self.num_dice} dice...")

        self._roll_dice()

    def _bank_points(self):
        self.banked_score += self.unbanked_points
        print(f"You banked {self.unbanked_points} points in round {self.round}")
        print(f"Total score is {self.banked_score } points")
        self.unbanked_points = 0
        self._new_round()

    def _roll_dice(self):
        dice_rolls = self.roller(self.num_dice)
        print(f"*** {' '.join(str(dice) for dice in dice_rolls)} ***")
        print("Enter dice to keep, or (q)uit:")

        self._take_input('dices', 'q')

    def _keep_the_dices(self, dices_input: str):
        dices = self._parse_dice_input(dices_input)
        self.num_dice -= len(dices)
        dice_score = GameLogic.calculate_score(dices)
        self.unbanked_points = dice_score
        print(f"You have {dice_score} unbanked points and {self.num_dice} dice remaining")
        print("(r)oll again, (b)ank your points or (q)uit:")

        self._take_input('r', 'b', 'q')

    def _take_input(self, *expected: str):
        user_input = input("> ")
        # TODO: if expected input is int should not check y or n or q
        if (user_input == "y"):
            return self._new_round()

        if (user_input == "n" and self.round == 0):
            print("OK. Maybe another time")
            return quit()

        if (user_input == 'q'):
            print(f"Thanks for playing. You earned {self.banked_score} points")
            return quit()

        if (user_input == 'b'):
            self._bank_points()

        if ('dices' in expected):
            self._keep_the_dices(user_input)

    @staticmethod
    def _parse_dice_input(dices_str: str):
        return tuple([int(dice_str) for dice_str in dices_str])


def play(roller=GameLogic.roll_dice):

    game = Game(roller)
    game.start_game()
