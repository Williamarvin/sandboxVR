from typing import List
import random
import zmq
import sys


class wordleServer():
    """Wordle server class to manage the game logic and communication with clients."""

    def __init__(self, wordList: List[str] = [], maxtries: int = 6):
        """
        Initialize the Wordle server.

        Args:
            wordList (List[str]): List of valid words for the game.
            maxtries (int): Maximum number of tries allowed.
        """

        # server initialisation
        self.context = zmq.Context()
        self.server = self.context.socket(zmq.PAIR)
        self.server.bind("tcp://*:5555")

        self.wordList = wordList
        self.maxtries = maxtries

    def drawBoard(self, indexList: List[int] = []) -> List[str]:
        """
        Draw the game board based on hit, present, and miss status.

        Args:
            indexList (List[int]): List indicating the status of each letter (0, 1, 2).

        Returns:
            List[str]: Board representation.
        """
        board = []

        # HIT 0 = 0
        # Present 1 = ?
        # Miss 2 = _
        for index in indexList:
            # if hit
            if index == 0:
                board.append('0')
            # if present
            elif index == 1:
                board.append('?')
            # if miss
            elif index == 2:
                board.append('_')

        print(''.join(board))
        return board

    def countPoints(self, board: List[str]) -> int:
        """
        Calculate points for the current round.

        Args:
            board (List[str]): Board representation.

        Returns:
            int: Points for the round.
        """
        points = 0

        for i in board:
            if i == "0":
                points += 2
            elif i == "?":
                points += 1
            else:
                points += 0

        return points

    # check if the word input is hit, present or miss compared to answer
    def checker(self, wordInput: str, answer: str) -> List[int]:
        """
        Check the user's input against the answer to determine hit, present, or miss.

        Args:
            wordInput (str): User's word guess.
            answer (str): Correct answer word.

        Returns:
            List[int]: List indicating the status of each letter (0, 1, 2).
        """
        output = []
        # check if hit, present or miss
        for index in range(5):

            # if hit
            if wordInput[index] == answer[index]:
                output.append(0)

            # if present
            elif wordInput[index] in answer:
                output.append(1)

            # if miss
            else:
                output.append(2)

        return output

    # Start wordle game
    def start(self) -> bool:
        """
        Start the Wordle game session.

        Returns:
            bool: False if game cannot start, otherwise continues the game loop.
        """
        if self.wordList == [] or self.maxtries == 0:
            return False

        mode = self.server.recv_json()

        # choose random answer from wordList
        answer = random.choice(self.wordList)
        try:
            if "single" in mode:
                for i in range(self.maxtries):

                    # wait for client answer
                    wordInput = self.server.recv_string()

                    # if client answer not in word list
                    while wordInput not in self.wordList:
                        self.server.send_string("error")
                        wordInput = self.server.recv_string()

                    # if guess is correct then return success
                    if wordInput == answer:
                        self.server.send_string("success")
                        break

                    # if guess is more than the max tries return failed
                    elif i + 1 == self.maxtries:
                        self.server.send_string("failed")

                    # if guess is incorect then continue
                    else:
                        self.server.send_string("continue")

                    # check for hit, present or miss to compare user input and answer
                    output = self.checker(wordInput, answer)

                    # print the board based on hit, present or miss
                    self.drawBoard(output)

            elif "multi" in mode:
                playerNum = mode["multi"]
                playerData = {"player " + str(i): 0 for i in range(playerNum)}

                # The number of tries allowed
                for round in range(self.maxtries):
                    # Iterate each player playing at the round
                    for num in range(playerNum):
                        response = self.server.recv_json()
                        player = next(iter(response))
                        wordInput = next(iter(response.values()))

                        while wordInput not in self.wordList:
                            self.server.send_string("error")
                            response = self.server.recv_json()
                            wordInput = next(iter(response.values()))

                        # check for hit, present or miss to compare user input and answer
                        output = self.checker(wordInput, answer)

                        # print the board based on hit, present or miss
                        board = self.drawBoard(output)
                        point = self.countPoints(board=board)
                        player = "player " + str(player)

                        newPoint = playerData[player]
                        newPoint += point
                        playerData[player] = newPoint

                        # if guess is correct then return success
                        if wordInput == answer:
                            playerData[player] = 10
                            self.server.send_string("success")
                            break

                        # if guess is incorect after maxtries
                        elif round + 1 == self.maxtries and num + 1 == playerNum:
                            self.server.send_string("failed")
                            break

                        self.server.send_string(str(playerData[player]))

                    # Break the second loop
                    if wordInput == answer or round + 1 == self.maxtries:
                        break

                # send player data to client
                self.server.send_json(playerData)

        except KeyboardInterrupt as e:
            print("\nGame interrupted. Exiting gracefully.")
            self.server.destroy()
            self.context.term()
