from server import wordleServer
from client import wordleClient
import zmq
import threading

if __name__ == "__main__":
    # configuration
    words = ["hello", "world", "fresh", "crazy", "quite", "fancy"]
    maxtries = 6

    # server initialisation
    server = wordleServer(wordList=words, maxtries=maxtries)
    serverThread = threading.Thread(target=server.start)
    serverThread.start()
    
    # client initialisation
    context = zmq.Context()
    client = context.socket(zmq.PAIR)
    client.connect("tcp://localhost:5555")


    while True:
        if words == [] or maxtries == 0:
            print("max tries 0 or words list have no words")
            break
        
        # send input to server
        wordInput = input("Please input a word to the wordle: ")
        client.send_string(wordInput)
        response = client.recv_string()

        # if response from server is success, win the game
        if response == "success":
            print("wordle success")
            break

        # elif response from server is failed, lose the game
        elif response == "failed":
            print("wordle fails")
            break

        # else response from server something else, continue
        else:
            continue
        
    # terminate thread
    serverThread.join()
