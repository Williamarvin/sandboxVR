import zmq


class wordleClient:

    def __init__(self, wordList, maxtries):
        context = zmq.Context()
        self.client = context.socket(zmq.PAIR)
        self.client.connect("tcp://localhost:5555")

        self.wordList = wordList
        self.maxtries = maxtries

    def printScore(self, playerData):
        # Sort the dictionary by values in descending order
        sorted_scores = sorted(playerData.items(),
                               key=lambda item: item[1],
                               reverse=True)

        # Print the scores
        for player, points in sorted_scores:
            print(f"Player {player}: {points} points")

    def start(self):

        mode = input(
            "Input single for single player and multi for multi player: ")
        playerNum = 2

        if mode == "single":
            self.client.send_json({"single": 1})
        else:
            self.client.send_json({"mutiple", playerNum})

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
            print("win within", str(self.maxtries),
                  "tries and get more points then your opponent")
            print("When playing, don't show your screen to the others")
            print("If your score ends up the same, then its a tie")

            counter = 0

            while counter >= 0:
                if counter >= 1000 * playerNum:
                    counter == 0

                player = counter % playerNum
                wordInput = input("player", player,
                                  "Please input a word to the wordle: ")

                self.client.send_json({player: wordInput})
                response = self.client.recv()

                # if response from server is success, win the game
                if response == "success":
                    print("wordle success")
                    break

                # elif response from server is failed, lose the game
                elif response == "failed":
                    print("wordle fails")
                    break

                # else response from server something else, continue
                elif response == "error":
                    continue

                else:
                    print("player", player, "current score is: ", response)
                    counter += 1

            playerData = self.client.recv_json()
            self.printScore(playerData)
