from typing import List
import random


def wordle(wordList: List[str] = [], maxtries: int = 6) -> bool:
    if wordList == []:
        return False

    answer = random.choice(wordList)

    for round in range(maxtries):

        wordInput = input("Please input a word to the wordle: ")
        if wordInput == answer:
            return True

        if wordInput.lower() in wordList:
            pass

    return False


if __name__ == "__main__":
    words = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 2

    success = wordle(wordList=words, maxtries=maxtries)

    if success:
        print("wordle success")

    elif not success:
        print("Wordle failed")
