from typing import List
import random
import zmq


class wordleServer():
    # initialise wordle class
    def __init__(self, wordList: List[str] = [], maxtries: int = 6):
        # server initialisation
        context = zmq.Context()
        self.server = context.socket(zmq.PAIR)
        self.server.bind("tcp://*:5555")

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
        return board
    
    def countPoints(self, board) -> int:
        points = 0

        for i in board:
            if i == "0":
                points += 2
            elif i == "?":
                points += 1
            else:
                points += 0

        return points

    def printScore(self, scores):
        # Sort the dictionary by values in descending order
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        # Print the scores
        for player, points in sorted_scores:
            print(f"Player {player}: {points} points")


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
        
        mode = self.server.recv_json()

        # choose random answer from wordList
        answer = random.choice(self.wordList)

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

                # if guess is incorect then continue
                elif i + 1 == self.maxtries:
                    self.server.send_string("failed")

                else:
                    self.server.send_string("continue")

                # check for hit, present or miss to compare user input and answer
                output = self.checker(wordInput, answer)

                # print the board based on hit, present or miss
                self.drawBoard(output)
            
        elif mode == "mutiple":
            playerNum = mode["mutiple"]
            playerData = {}

            for round in range(self.maxtries):  
                for num in range(playerNum):
                    wordInput = self.server.recv_json()

                    while wordInput not in self.wordList:
                        self.server.send_string("error")
                        wordInput = self.server.recv_string()

                    # if guess is correct then return success
                    if wordInput == answer:
                        self.server.send_string("success")
                        break

                    # if guess is incorect then continue
                    elif i + 1 == self.maxtries:
                        self.server.send_string("failed")

                    else:
                        self.server.send_string("continue")

                    # check for hit, present or miss to compare user input and answer
                    output = self.checker(wordInput, answer)

                    # print the board based on hit, present or miss
                    board = self.drawBoard(output)
                    point = self.countPoints(board=board)
                    

                    if wordInput.keys() in playerData:
                        playerData[wordInput.keys()] = point
                    else:
                        playerData[wordInput.key()] += point
            
            self.printScore(playerData)

        # exceed max tries
        self.server.send_string("failed")
