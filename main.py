from typing import List
import random
import zmq


class wordle:
    # initialise wordle class
    def __init__(self, wordList: List[str] = [], maxtries: int = 6):
        self.wordList = wordList
        self.maxtries = maxtries

    # Draw board based on user input
    # HIT 0 = 0
    # Present 1 = ?
    # Miss 2 = _
    def drawBoard(self, indexList: List[int] = []):
        board = []

        for index in indexList:
            # Hit
            if index == 0:
                board.append('0')
            # Present
            elif index == 1:
                board.append('?')
            # MISS
            elif index == 2:
                board.append('_')

        print(''.join(board))
    
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
    def playWordle(self) -> bool:
        if self.wordList == []:
            return False

        # choose random answer from wordList
        answer = random.choice(self.wordList)

        for round in range(self.maxtries):

            wordInput = input("Please input a word to the wordle: ")

            while wordInput.lower() not in self.wordList:
                wordInput = input("Please enter a 5 letter word from the list")

            # if correct, then return true
            if wordInput == answer:
                return True

            # check for hit, present or miss to compare user input and answer
            output = self.checker(wordInput, answer)

            # print the board based on hit, present or miss
            self.drawBoard(output)

        # Failed so return false
        return False


if __name__ == "__main__":
    words = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 6

    wordleObj = wordle(wordList=words, maxtries=maxtries)
    success = wordleObj.playWordle()

    # check if success
    if success:
        print("wordle success")

    elif not success:
        print("Wordle failed")
