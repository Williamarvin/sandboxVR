from backend import wordle
import zmq
import threading

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
