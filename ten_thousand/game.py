from ten_thousand.game_logic import GameLogic


class Game:
    def __init__(self, roller=GameLogic.roll_dice, num_rounds=20):
        self.round = 0
        self.num_rounds = num_rounds
        self.banked_score = 0
        self.unbanked_points = 0
        self.num_dice = 6
        self.curr_round_kept_dices: list[tuple] = []
        self._roller = roller
        self._next = None
        self._last_roll: tuple[int, ...] = ()

    def play(self):
        print("Welcome to Ten Thousand")
        self._ask_to_play()
        while self._next:
            self._next()

    def _ask_to_play(self):
        print("(y)es to play or (n)o to decline")
        user_input = self._multiple_choice_input('y', 'n')
        if (user_input == "y"):
            self._next = self._new_round
        elif (user_input == "n"):
            self._next = self._quit

    def _new_round(self):
        if (self.round >= self.num_rounds):
            self._next = self._quit
            return
        self.round += 1
        self.num_dice = 6
        self.unbanked_points = 0
        self.curr_round_kept_dices = []
        print(f"Starting round {self.round}")
        self._next = self._roll_dices

    def _roll_dices(self):
        print(f"Rolling {self.num_dice} dice...")
        self._last_roll = self._roller(self.num_dice)
        if (self._is_zilch()):
            self._next = self._zilch
        else:
            self._next = self._ask_dices_to_keep

    def _ask_dices_to_keep(self):
        print(f"*** {' '.join(str(dice) for dice in self._last_roll)} ***")
        print("Enter dice to keep, or (q)uit:")
        user_input = self._keep_dices_input()
        if (user_input == 'q'):
            self._next = self._quit
            return
        elif (user_input == None):
            print("Cheater!!! Or possibly made a typo...")
            self._next = self._ask_dices_to_keep
            return

        dices = self._parse_dice_input(user_input)
        self._keep_dices(dices)
        if (self.num_dice == 0):
            self._next = self._bank_points
        else:
            self._next = self._ask_after_keep

    def _keep_dices(self, dices: tuple[int, ...]):
        self.num_dice -= len(dices)
        self.curr_round_kept_dices.append(dices)
        if (self._check_hot_dice()):
            self.num_dice = 6
        dice_score = GameLogic.calculate_score(dices)
        self.unbanked_points += dice_score
        print(f"You have {self.unbanked_points} unbanked points and {self.num_dice} dice remaining")

    def _check_hot_dice(self):
        if (self.num_dice != 0):
            return False

        for dices in self.curr_round_kept_dices:
            scorer = GameLogic.get_scorers(dices)
            if len(dices) != len(scorer):
                return False

        return True

    def _ask_after_keep(self):
        print("(r)oll again, (b)ank your points or (q)uit:")
        user_input = self._multiple_choice_input('r', 'b', 'q')
        if (user_input == 'r'):
            self._next = self._roll_dices
        elif (user_input == 'b'):
            self._next = self._bank_points
        elif (user_input == 'q'):
            self._next = self._quit

    def _bank_points(self):
        self.banked_score += self.unbanked_points
        print(f"You banked {self.unbanked_points} points in round {self.round}")
        print(f"Total score is {self.banked_score } points")
        self._next = self._new_round

    def _quit(self):
        if (self.round == 0):
            print("OK. Maybe another time")
            return quit()

        print(f"Thanks for playing. You earned {self.banked_score} points")
        quit()

    def _is_zilch(self):
        return (GameLogic.calculate_score(self._last_roll) == 0)

    def _zilch(self):
        print(f"*** {' '.join(str(dice) for dice in self._last_roll)} ***")
        print("****************************************")
        print("**        Zilch!!! Round over         **")
        print("****************************************")
        print(f"You banked 0 points in round {self.round}")
        print(f"Total score is {self.banked_score} points")

        self._next = self._new_round

    def _keep_dices_input(self):
        user_input = input("> ")
        while (not self._is_valid_dice_input(user_input)):
            if (user_input == 'q'):
                return user_input
            return None
        return user_input

    def _is_valid_dice_input(self, user_input: str):
        if (not user_input.isdigit()):
            return False
        dices = self._parse_dice_input(user_input)
        return GameLogic.validate_keepers(self._last_roll, dices)

    @staticmethod
    def _multiple_choice_input(*expected: str):
        user_input = input("> ")
        while (not user_input in expected):
            print("Cheater!!! Or possibly made a typo...")
            user_input = input("> ")
        return user_input

    @staticmethod
    def _parse_dice_input(dices_str: str):
        return tuple([int(dice_str) for dice_str in dices_str])


def play(roller=GameLogic.roll_dice, num_rounds=20):

    game = Game(roller, num_rounds)
    game.play()
