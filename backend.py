from typing import List
from multiprocessing import Process
import random
import zmq


class wordle(Process):
    # initialise wordle class
    def __init__(self, wordList: List[str] = [], maxtries: int = 6):
        context = zmq.Context()
        self.server = context.socket(zmq.PAIR)
        self.server.connect("tcp://localhost:5555")
        
        self.wordList = wordList
        self.maxtries = maxtries

    # Draw board based on user input
    def drawBoard(self, indexList: List[int] = []):
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

    # check if the word input is hit, present or miss compared to answer
    def checker(self, wordInput, answer) -> List[int]:
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
        if self.wordList == [] or self.maxtries == 0:
            return False

        # choose random answer from wordList
        answer = random.choice(self.wordList)

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

            # if guess is incorect then continue
            elif wordInput in self.wordList:
                self.server.send_string("continue")

            # check for hit, present or miss to compare user input and answer
            output = self.checker(wordInput, answer)

            # print the board based on hit, present or miss
            self.drawBoard(output)

        # exceed max tries
        self.server.send_string("failed")
