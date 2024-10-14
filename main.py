from server import wordleServer
from client import wordleClient
import threading
import sys

if __name__ == "__main__":
    # configuration
    wordList = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 2

    try:
        # server initialisation
        server = wordleServer(wordList=wordList, maxtries=maxtries)
        serverThread = threading.Thread(target=server.start)
        serverThread.start()

        # client initialisation
        client = wordleClient(wordList=wordList, maxtries=maxtries)
        client.start()

        # terminate thread
        serverThread.join()
        
    except KeyboardInterrupt as e:
        serverThread.join()
        sys.exit()
