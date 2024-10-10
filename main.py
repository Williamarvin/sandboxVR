from server import wordleServer
from client import wordleClient
import zmq
import threading

if __name__ == "__main__":
    # configuration
    wordList = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 6

    # server initialisation
    server = wordleServer(wordList=wordList, maxtries=maxtries)
    serverThread = threading.Thread(target=server.start)
    serverThread.start()
    
    # client initialisation
    client = wordleClient(wordList=wordList, maxtries=maxtries)
    clientThread = threading.Thread(target=client.start)
    clientThread.start()

    # terminate thread
    serverThread.join()
    clientThread.join()