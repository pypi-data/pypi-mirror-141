__version__ = '0.1.0'
import random
import numpy

class MockGame:
    def __init__(self):
        # Initialize
        self.other_team = None
        self.board_state = None

        # Private------------
        self.__player = None
        self.__total_random_board()

    def submit_move(self, x, y):
        if (self.board_state[x][y] == " "):
            self.board_state[x][y] = self.__player
        else:
            print("Unable to submit move!")

    def opposite_team(self, current_team):
        # return "O" if team passed as argument is "X" and return "X" if not
        return "O" if current_team == "X" else "X"

    def get_team(self):
        return self.other_team

    def get_board_state(self):
        return self.board_state

    def print_board(self):
        print("\n")
        print(" ".join(self.board_state[0]))
        print(" ".join(self.board_state[1]))
        print(" ".join(self.board_state[2]))
        print("\n")

    # Private---------------
    def __check_for_winner(self):
        # These two arrays represent the board's diagonal lines
        diagonal_check_1 = numpy.array([
            self.board_state[0, 0], self.board_state[1, 1], self.board_state[2,
                                                                             2]
        ])
        diagonal_check_2 = numpy.array([
            self.board_state[0, 2], self.board_state[1, 1], self.board_state[2,
                                                                             0]
        ])

        # These ifs check all four win conditions (row, column, diagonal 1, diagonal 2) for X, then O, returning a winner if there is one.
        if numpy.any(
            (numpy.all(self.board_state == "X", axis=1))) or numpy.any(
                (numpy.all(self.board_state == "X", axis=0))) or numpy.all(
                    diagonal_check_1 == "X") or numpy.all(
                        diagonal_check_2 == "X"):
            return "X"
        elif numpy.any(
            (numpy.all(self.board_state == "O", axis=1))) or numpy.any(
                (numpy.all(self.board_state == "O", axis=0))) or numpy.all(
                    diagonal_check_1 == "O") or numpy.all(
                        diagonal_check_2 == "O"):
            return "O"

        # If no winner can be found, check for a tie
        else:
            # If there are no blank spaces left, then the game will work towards a tiebreaker
            # Side note: not sure if checking all 3 states like this is max efficiency, I might have missed some magic numpy function that does exactly this but easier
            if " " not in self.board_state[0] and " " not in self.board_state[
                    1] and " " not in self.board_state[2]:
                return "TIE"
            # If there are still playable spaces, the game will continue
            else:
                return "NONE"

    def __total_random_board(self):
        teams = ["X", "O"]
        number_of_moves = 0

        self.board_state = numpy.array([[" ", " ", " "], [" ", " ", " "],
                                        [" ", " ", " "]])

        first_move_team = teams[random.randint(0, 1)]
        next_move_team = " "

        while number_of_moves < 6:
            if number_of_moves == 0:
                self.board_state[random.randint(0, 2)][random.randint(
                    0, 2)] = first_move_team
                next_move_team = self.opposite_team(first_move_team)
                number_of_moves = number_of_moves + 1
            elif number_of_moves < 5:
                self.board_state[random.randint(0, 2)][random.randint(
                    0, 2)] = next_move_team
                next_move_team = self.opposite_team(next_move_team)
                number_of_moves = number_of_moves + 1
            elif number_of_moves == 5:
                self.board_state[random.randint(0, 2)][random.randint(
                    0, 2)] = next_move_team
                next_move_team = self.opposite_team(next_move_team)
                number_of_moves = number_of_moves + 1
                if (self.__check_for_winner() != "NONE"):
                    self.board_state = numpy.array([[" ", " ", " "],
                                                    [" ", " ", " "],
                                                    [" ", " ", " "]])
                    first_move_team = teams[random.randint(0, 1)]
                    number_of_moves = 0

        self.other_team = teams[random.randint(0, 1)]
        self.__player = self.opposite_team(self.other_team)
