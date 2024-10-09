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
            # check if hit, present or miss
            pass

    # Failed so return false
    return False


if __name__ == "__main__":
    words = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 2

    success = wordle(wordList=words, maxtries=maxtries)

    # check if success
    if success:
        print("wordle success")

    elif not success:
        print("Wordle failed")
