from server import wordleServer
from client import wordleClient
import threading
import sys

if __name__ == "__main__":
    # configuration
    wordList = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 6

    try:
        # server initialisation
        server = wordleServer(wordList=wordList, maxtries=maxtries)
        serverThread = threading.Thread(target=server.start)
        serverThread.start()

        # client initialisation
        client = wordleClient(wordList=wordList, maxtries=maxtries)
        client.start()

        # clientThread = threading.Thread(target=client.start)
        # clientThread.start()

        # terminate thread
        serverThread.join()
        # clientThread.join()
    except KeyboardInterrupt as e:
        sys.exit()
