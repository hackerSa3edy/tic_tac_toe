# Tic-Tac-Toe Game (NOT yet completed)

![s1](Client/src/assets/Images/Text_Logo.png)

## Screenshots

![s1](.assets/s1.png)

![s2](.assets/s2.png)

![s3](.assets/s3.png)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Socket.IO Events](#socketio-events)
7. [Setup and Installation](#setup-and-installation)
8. [Configuration](#configuration)
9. [License](#license)

## Introduction

This project is a multiplayer Tic-Tac-Toe game implemented using Flask for the backend, Socket.IO for real-time communication, and MongoDB for data persistence. It allows users to register, login, play games against each other in real-time, and track their performance on a leaderboard.

## Features

- User authentication (register, login, logout)
- Real-time multiplayer gameplay
- Leaderboard system
- Game history tracking
- Responsive design for various screen sizes

## Technology Stack

- Backend: Flask (Python)
- Database: MongoDB
- Real-time Communication: Socket.IO
- Frontend: React, TypeScript, Vite
- Styling: Tailwind CSS
- Authentication: Flask sessions
- WSGI Server: Gunicorn
- Web Server: Nginx (for production deployment)
- Containerization: Docker

## Database Schema

Refer to the [schema documentation](server/docs/schema.md) for detailed information about the database collections and their schemas.

## API Endpoints

Refer to the [API routes documentation](server/docs/API_routes.md) for detailed information about the available API endpoints, their descriptions, request bodies, and responses.

## Socket.IO Events

### `connect`

- **Description**: Triggered when a client connects to the server.
- **Behavior**:
  - Retrieves the player's ID from the session.
  - If the player is not logged in, emits an error message and denies the connection.
  - Checks if the player is already in a waiting or ongoing game. If so, emits an error message and denies the connection.
  - If the player is successfully connected, prints a connection message.

### `disconnect`

- **Description**: Triggered when a client disconnects from the server.
- **Behavior**:
  - Retrieves the player's ID from the session.
  - Handles the disconnection by updating the game state.
  - If the player was in a game, emits a `game_over` event indicating the opponent's win due to disconnection.
  - Updates the user's win/loss statistics.

### `join_game`

- **Description**: Triggered when a player joins a game.
- **Behavior**:
  - Retrieves the player's ID from the session.
  - Checks if the player is already in a waiting or ongoing game. If so, emits an error message.
  - Searches for a waiting game. If found, the player joins the game and the game starts.
  - If no waiting game is found, creates a new game and the player joins it, waiting for an opponent.

### `make_move`

- **Description**: Triggered when a player makes a move in the game.
- **Behavior**:
  - Retrieves the game ID, player ID, and move position from the data.
  - Validates the game state and the player's turn.
  - Processes the move and updates the game board.
  - Emits a `move_made` event to update the game state for all players.
  - If the game ends event and updates the user and leaderboard statistics accordingly.

### `game_over`

- **Description**: Triggered when the game ends.
- **Behavior**:
  - This event is emitted internally by the server when a game concludes due to a win, loss, or draw.
  - Updates the game state and user statistics.
  - Notifies all players in the game room about the game result.

## Setup and Installation

### Using Docker Compose

To set up and run the application using Docker Compose, follow these steps:

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone the repository:

   ```sh
   git clone https://github.com/hackersa3edy/tic_tac_toe.git
   cd tic-tac-toe
   ```

3. Create a `.env` file in the server directory to add your environment variables. Refer to the [example file](./server/example-dotenv-file).

4. Run the application using Docker Compose:

   ```sh
   docker-compose -f docker-compose.yml up --build
   ```

Using Docker Compose is preferred because:

- **Consistency**: Ensures the application runs in the same environment across different machines.
- **Isolation**: Keeps the application dependencies isolated from the host system.
- **Ease of Setup**: Simplifies the setup process by handling dependencies and configurations automatically.
- **Scalability**: Makes it easier to scale services and manage multiple containers.

### Manual Setup (Without Docker)

If you prefer not to use Docker, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/hackersa3edy/tic_tac_toe.git
   cd tic-tac-toe
   ```

2. Set up a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

   For me, I'm using virtualenvwrapper. It's cool. Give it a try: [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up MongoDB:

   - Install MongoDB on your system.
   - Initialize it with a username and password, if needed.

5. Set up environment variables:
   Create a `.env` file in the server directory to add your environment variables. Refer to the [example file](./server/example-dotenv-file).

6. Build the client:

   ```sh
   cd Client
   npm install
   npm run build
   cd ..
   ```

7. Copy the built static files to the server to be served.

   ```sh
   cp -r Client/dist/* server/static
   ```

8. Run the application:

   For development:

   ```sh
   cd server
   python app.py
   ```

   For production:

   ```sh
   cd server
   gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:3000
   ```

## Configuration

Configuration settings are managed in `config.py`. Different configurations are available for development, testing, and production environments.

## Authors

- Noor Amjad - [GitHub](https://github.com/Justxd22) / [Twitter](https://twitter.com/_xd222) / [LinkedIn](https://www.linkedin.com/in/noor-amjad-xd)
- Amr Abdelfattah - [GitHub](https://github.com/0x3mr) / [Twitter](https://twitter.com/an0n_amr) / [LinkedIn](https://www.linkedin.com/in/amrabdelfattah/)
- Ahmed Shalaby - [GitHub](https://github.com/Madiocre) / [Twitter](https://twitter.com/Ahmed_K_Shalaby) / [LinkedIn](https://www.linkedin.com/in/ahmed-shalaby-31a03a235/)
- Ahmed Aboalesaad - [GitHub](https://github.com/Ahmed-Aboalasaad) / [Twitter](https://x.com/Aboalesaad_) / [LinkedIn](https://www.linkedin.com/in/ahmed-aboalesaad/)
- Abdelrahman Mohamed - [GitHub](https://github.com/hackerSa3edy) / [Twitter](https://x.com/hackersa3edy) / [LinkedIn](https://linkedin.com/abdelrahmanm0)
- Kedir Jabir - [GitHub](https://github.com/IbnuJabir) / [Twitter](https://x.com/Ibnu_J1) / [LinkedIn](https://www.linkedin.com/in/ibnu-jabir/)

## License

Copyright (C) 2024
Licensed under the GPLv3 License
