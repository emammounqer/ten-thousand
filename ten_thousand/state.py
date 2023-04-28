from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ten_thousand.game_logic import GameLogic

if TYPE_CHECKING:
    from ten_thousand.game import Game


class State(ABC):
    def __init__(self, game: 'Game'):
        self.game = game

    @abstractmethod
    def start(self):
        pass


class StartState(State):
    def start(self):
        print("Welcome to Ten Thousand")
        self._ask_to_play()

    def _ask_to_play(self):
        print("(y)es to play or (n)o to decline")
        user_input = self.game._multiple_choice_input('y', 'n')
        if (user_input == "y"):
            self.game.set_state(NewRoundState(self.game))
        elif (user_input == "n"):
            self.game.set_state(QuitState(self.game))


class NewRoundState(State):
    def start(self):
        self.game.round += 1
        self.game.num_dice = 6
        print(f"Starting round {self.game.round}")
        self.game.set_state(RollState(self.game))


class RollState(State):
    def start(self):
        dice_rolls = self.game._roller(self.game.num_dice)
        # TODO: check for zilch
        print(f"Rolling {self.game.num_dice} dice...")
        print(f"*** {' '.join(str(dice) for dice in dice_rolls)} ***")
        self.game.set_state(KeepState(self.game))


class KeepState(State):
    def start(self):
        print("Enter dice to keep, or (q)uit:")
        user_input = input("> ")
        if (user_input == 'q'):
            return self.game.set_state(QuitState(self.game))

        dices = self.game._parse_dice_input(user_input)
        # TODO: validate input and dices
        self.keep_dices(dices)
        self.game.set_state(AfterKeepState(self.game))

    def keep_dices(self, dices: tuple[int, ...]):
        self.game.num_dice -= len(dices)
        dice_score = GameLogic.calculate_score(dices)
        self.game.unbanked_points = dice_score
        print(f"You have {dice_score} unbanked points and {self.game.num_dice} dice remaining")


class AfterKeepState(State):
    def start(self):
        print("(r)oll again, (b)ank your points or (q)uit:")
        user_input = self.game._multiple_choice_input('r', 'b', 'q')
        if (user_input == 'r'):
            return self.game.set_state(RollState(self.game))

        if (user_input == 'b'):
            return self.game.set_state(BankState(self.game))

        if (user_input == 'q'):
            return self.game.set_state(QuitState(self.game))


class BankState(State):
    def start(self):
        self.game.banked_score += self.game.unbanked_points
        print(f"You banked {self.game.unbanked_points} points in round {self.game.round}")
        print(f"Total score is {self.game.banked_score } points")
        self.game.unbanked_points = 0
        self.game.set_state(NewRoundState(self.game))


class QuitState(State):
    def start(self):
        if (self.game.round == 0):
            print("OK. Maybe another time")
            return quit()

        print(f"Thanks for playing. You earned {self.game.banked_score} points")
        quit()
