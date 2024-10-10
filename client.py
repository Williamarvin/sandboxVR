import zmq


class wordleClient:

    def __init__(self, wordList, maxtries):
        context = zmq.Context()
        self.client = context.socket(zmq.PAIR)
        self.client.connect("tcp://localhost:5555")

        self.wordList = wordList
        self.maxtries = maxtries

    def start(self):

        mode = input(
            "Input single for single player and multi for multi player: ")

        if mode == "single":
            print("win within", str(self.maxtries), "tries")

            while True:
                if self.wordList == [] or self.maxtries == 0:
                    print("Max tries 0 or words list have no words")
                    break

                # send input to server
                wordInput = input("Please input a word to the wordle: ")
                self.client.send_string(wordInput)
                response = self.client.recv_string()

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

        elif mode == "multi":
            # multi player
            print("win within" + self.maxtries +
                  "tries and get more points then your opponent")
            print("When playing, don't show your screen to the others")
            print("If your score ends up the same, then its a tie")
