# installation
`pip install zmq`

# How to play the game
1. `python main.py`
2. `choose the mode(single or multiplayer)`

### Single Player
1. Guess the word from the list within the allowed tries
2. If you fail to guess, you lose the game
3. If you guess correctly, you win the game

### Multi player
1. Choose the number of players who would like to play
2. Guess the word from the list within the allowed tries
3. The person with the highest score wins the game

### Point system
1. ? means that the letter is in the correct word but not in the correct order
2. _ means the word is not in the correct answer
3. 0 means the word is in the correct answer and correct order

# Trade-offs / Considerations

### 1. ZeroMQ (ZMQ) for Communication:

#### The project uses ZeroMQ's PAIR pattern for client-server communication, which is simple but limits scalability to only two peers (one client and one server). More scalable patterns like REQ-REP or PUB-SUB were considered but not implemented in this version for simplicity.

### 2. Simple Word List:

#### A fixed word list is used for guessing. This limits word variety but simplifies the game logic. In future versions, a dynamic word list (from a file or API) could be implemented.

### 3. Sequential Player Turns in Multiplayer:

#### In multiplayer mode, players take turns guessing, which is easy to implement but can be slow for larger groups. Handling multiple players concurrently would require more complex threading or asynchronous solutions, which were not prioritized for this version.

### 4. Basic Scoring System:

#### The scoring system is simple, with points awarded based on correctly guessed letters. This was chosen to keep the game intuitive, but more complex scoring systems could be introduced in future iterations.

### 5. High Score Storage:

#### High scores are stored in a text file, which works for small-scale games but doesn't scale well. A database solution could be considered for future development.

# Development

### File structure

```
├── server.py              # Contains the wordleServer class
├── client.py              # Contains the wordleClient class
├── highscore.txt          # File to store high scores
├── main.py                # Script to run the server and client
└── README.md              # Basic project description
```

### Why thread?

#### Server and client is launched differently. For the server, threads are used so that I can use the main script to run both files. For the client, it is ran in the main thread.

#### Since the game primarily involves I/O-bound tasks (server-client communication, handling player input), threads are a suitable choice. However, if the game logic becomes more computationally intensive, using multiprocessing might be a better option to fully utilize multiple CPU cores.

### Which task is done?

### Completed: Task 1, Task 2, Task 4, Bonus (Highest Score Storage)

### TODO

1. Task 3 is not implemented
2. Shutting down gracefully is not complete, some bugs are still present
3. Adding a user interface for the users
4. Optimising code
