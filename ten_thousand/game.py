from ten_thousand.game_logic import GameLogic


class Game:
    def __init__(self, roller=GameLogic.roll_dice):
        self.round = 0
        self.banked_score = 0
        self.unbanked_points = 0
        self.num_dice = 6
        self._roller = roller

    def start_game(self):
        print("Welcome to Ten Thousand")
        self._ask_to_play()

    def _ask_to_play(self):
        print("(y)es to play or (n)o to decline")
        user_input = self._multiple_choice_input('y', 'n')
        if (user_input == "y"):
            self._new_round()
        elif (user_input == "n"):
            self._quit()

    def _new_round(self):
        self.round += 1
        self.num_dice = 6
        print(f"Starting round {self.round}")
        self._roll_dices()

    def _roll_dices(self):
        dice_rolls = self._roller(self.num_dice)
        # TODO: check for zilch
        print(f"Rolling {self.num_dice} dice...")
        print(f"*** {' '.join(str(dice) for dice in dice_rolls)} ***")
        self._ask_dices_to_keep()

    def _ask_dices_to_keep(self):
        print("Enter dice to keep, or (q)uit:")
        user_input = input("> ")
        if (user_input == 'q'):
            return self._quit()

        dices = self._parse_dice_input(user_input)
        # TODO: validate input and dices
        self._keep_dices(dices)

    def _keep_dices(self, dices: tuple[int, ...]):
        self.num_dice -= len(dices)
        dice_score = GameLogic.calculate_score(dices)
        self.unbanked_points = dice_score
        print(f"You have {dice_score} unbanked points and {self.num_dice} dice remaining")
        self._ask_after_keep()

    def _ask_after_keep(self):
        print("(r)oll again, (b)ank your points or (q)uit:")
        user_input = self._multiple_choice_input('r', 'b', 'q')
        if (user_input == 'r'):
            self._roll_dices()
        elif (user_input == 'b'):
            self._bank_points()
        elif (user_input == 'q'):
            self._quit()

    def _bank_points(self):
        self.banked_score += self.unbanked_points
        print(f"You banked {self.unbanked_points} points in round {self.round}")
        print(f"Total score is {self.banked_score } points")
        self.unbanked_points = 0
        self._new_round()

    def _quit(self):
        if (self.round == 0):
            print("OK. Maybe another time")
            return quit()

        print(f"Thanks for playing. You earned {self.banked_score} points")
        quit()

    @staticmethod
    def _multiple_choice_input(*expected: str):
        user_input = input("> ")
        while (not user_input in expected):
            print("not valid")
            user_input = input("> ")
        return user_input

    @staticmethod
    def _parse_dice_input(dices_str: str):
        return tuple([int(dice_str) for dice_str in dices_str])


def play(roller=GameLogic.roll_dice):

    game = Game(roller)
    game.start_game()