from ten_thousand.state import QuitState, StartState, State
from ten_thousand.game_logic import GameLogic


class Game:
    def __init__(self, roller=GameLogic.roll_dice):
        self.round = 0
        self.banked_score = 0
        self.unbanked_points = 0
        self.num_dice = 6
        self._roller = roller
        self._current_state: State

    def set_state(self, state: State):
        self._current_state = state

    def start_game(self):
        self.set_state(StartState(self))
        while self._current_state is not type(QuitState):
            self._current_state.start()

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
