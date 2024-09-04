# MongoDB Schema Documentation

## Users Collection

**Collection Name:** `users`

**Description:** Stores user information.

**Schema:**

- `username`: (string, required): The username of the user.
- `email`: (string, required): The email address of the user.
- `password`: (string, required): The hashed password of the user.
- `wins`: (int, required): The number of games the user has won.
- `losses`: (int, required): The number of games the user has lost.
- `draws`: (int, required): The number of games that ended in a draw.
- `game_played`: (int, required): The total number of games played by the user.
- `score`: (int, required): The score of the user.
- `created_at`: (date, required): The date when the user was created.
- `avatar`: (string, optional): The URL of the user's avatar.

**Indexes:**

- `username`: (unique)
- `email`: (unique)
- `score`: (descending)
- `game_played`: (descending)
- `wins`: (descending)

## Games Collection

**Collection Name:** `games`

**Description:** Stores game information.

**Schema:**

- `players`: (object, required): Information about the players.
  - `player1`: (string, required): The username of player 1.
  - `player2`: (string, optional): The username of player 2.
- `status`: (string, required): The status of the game. Possible values: waiting, ongoing, completed.
- `winner`: (string, optional): The username of the winning player.
- `loser`: (string, optional): The username of the losing player.
- `is_draw`: (bool, optional): Indicates if the game ended in a draw.
- `notes`: (string, optional): Additional notes about the game.
- `created_at`: (date, required): The date when the game was created.
- `ended_at`: (date, optional): The date when the game ended.
- `current_turn`: (string, optional): The username of the player whose turn it is.
- `board`: (array of strings, required): The game board state. Possible values for each cell: X, O, "".

**Indexes:**

- `status`
- `status`, `players.player1`, `players.player2` (composed index)
- `created_at`: (descending)

## Leaderboard Collection

**Collection Name:** `leaderboard`

**Description:** Stores leaderboard information.

**Schema:**

- `username`: (string, required): The username of the player.
- `wins`: (int, required): The number of wins by the player.
- `draws`: (int, required): The number of draws by the player.
- `score`: (int, required): The score of the player.

**Indexes:**

- `username`: (unique)
- `score`: (descending)
