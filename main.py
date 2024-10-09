from typing import List
import random


# HIT 0 = 0
# Present 1 = ?
# Miss 2 = _
def drawBoard(indexList: List[int] = []):
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


def wordle(wordList: List[str] = [], maxtries: int = 6) -> bool:
    if wordList == []:
        return False

    # choose random answer from wordList
    answer = random.choice(wordList)

    for round in range(maxtries):

        wordInput = input("Please input a word to the wordle: ")

        # if correct, then return true
        if wordInput == answer:
            return True

        # if word input is in the list
        if wordInput.lower() in wordList:
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

            # print the board based on hit, present or miss
            drawBoard(output)

    # Failed so return false
    return False


if __name__ == "__main__":
    words = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 6

    success = wordle(wordList=words, maxtries=maxtries)

    # check if success
    if success:
        print("wordle success")

    elif not success:
        print("Wordle failed")
