from typing import List
import zmq
import sys
import os



class wordleClient:
    """Wordle client class to interact with the Wordle server."""

    def __init__(self, wordList: List[str], maxtries: int):
        """
        Initialize the Wordle client.

        Args:
            wordList (List[str]): List of valid words for the game.
            maxtries (int): Maximum number of tries allowed.
        """
        self.context = zmq.Context()
        self.client = self.context.socket(zmq.PAIR)
        self.client.connect("tcp://localhost:5555")

        self.wordList = wordList
        self.maxtries = maxtries

    def printScore(self, playerData: dict):
        """
        Print the scores of all players.

        Args:
            playerData (dict): Dictionary containing player scores.
        """
        # Sort the dictionary by values in descending order
        sorted_scores = sorted(playerData.items(),
                               key=lambda item: item[1],
                               reverse=True)

        winner = True

        # Print the scores
        for player, points in sorted_scores:
            if winner:
                print(f"{player} wins: {points} points")
                winner = False
            else:
                print(f"{player}: {points} points")

    def start(self):
        """Start the Wordle game session for the client."""

        # print the highest score
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                content = f.read()
                print(content)

        mode = input(
            "Input single for single player and multi for multi player: ")
        playerNum = 0

        try:
            while True:
                if mode == "single":
                    self.client.send_json({"single": 1})
                    break
                elif mode == "multi":
                    while True:
                        try:
                            playerNum = int(
                                input(
                                    "Please input the number of people(1-10): "
                                ))

                            if playerNum > 0 and playerNum <= 10:
                                self.client.send_json({"multi": playerNum})
                                break
                        except:
                            print("Please input numbers from 1-10")

                    break
                else:
                    mode = input(
                        "Input single for single player and multi for multi player: "
                    )

            # single player
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

            # multi player
            elif mode == "multi":
                print("win within", str(self.maxtries),
                      "tries and get more points then your opponent")
                print("When playing, don't show your screen to the others")
                print("If your score ends up the same, then its a tie")

                counter = 0

                while counter >= 0:
                    # Prevent integer overload
                    if counter >= 1000 * playerNum:
                        counter == 0

                    player = counter % playerNum
                    wordInput = input(
                        f"player {player} please input a word to the wordle: ")

                    self.client.send_json({player: wordInput})
                    response = self.client.recv_string()

                    # if response from server is success, win the game
                    if response == "success":
                        print("wordle success")
                        break

                    # if response from server is failed, lose the game
                    elif response == "failed":
                        print("wordle fails")
                        break

                    # if response from server is error, don't count the round
                    elif response == "error":
                        continue

                    # Next person/round and print the player score
                    else:
                        print("player", player, "current score is: ", response)
                        counter += 1

                # receive player data from server
                playerData = self.client.recv_json()
                self.printScore(playerData)

                # Find the highest numbered value in the dictionary
                max_value = max(playerData.values())

                # Read the existing content
                with open("highscore.txt", "r") as f:
                    content = f.readlines()

                # Extract the current highest score from the first line
                current_high_score = int(content[0].strip().split(": ")[1])

                # Check if the new score is greater than the current highest score
                if max_value > current_high_score:
                    # Update the first line with the new highest score
                    content[0] = "Highest Score: " + str(max_value) + "\n"

                    # Write the updated content back to the file
                    with open("highscore.txt", "w") as f:
                        f.writelines(content)

        except KeyboardInterrupt as e:
            print("\nGame interrupted. Exiting gracefully.")
            self.client.close()
            self.context.term()
