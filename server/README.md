# ALX TicTacToe Server

This is the server-side application for the ALX TicTacToe project. It is built using Flask, a lightweight WSGI web application framework in Python. The server handles user authentication, game logic, and real-time communication using Socket.IO. It also interfaces with a MongoDB database to store user data, game states, and leaderboards.

## Table of Contents

- [Project Structure](#project-structure)
- [Functionalities](#functionalities)
- [Installation](#installation)
- [Development](#development)
- [Building](#building)
- [Environment Variables](#environment-variables)
- [Docker](#docker)
- [Security Notes](#security-notes)
- [Scaling](#scaling)
- [License](#license)

## Project Structure

```text
server
├── README.md
├── api
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── game_routes.py
│   │   ├── leaderboard_routes.py
│   │   └── user_routes.py
│   └── utils.py
├── app.py
├── backend.Dockerfile
├── config
│   ├── __init__.py
│   ├── default.py
│   ├── development.py
│   └── production.py
├── database.py
├── docker-compose.yml
├── errors.py
├── example-dotenv-file
├── middleware.py
├── models
│   ├── __init__.py
│   ├── auth.py
│   ├── game.py
│   ├── leaderboard.py
│   └── user.py
├── mongo-init.js
├── multiplayer_socketIO
│   ├── __init__.py
│   └── events.py
├── requirements.txt
├── static
│   ├── assets/
│   ├── favicon.ico
│   ├── index.html
│   └── vite.svg
├── tests
│   ├── socketclient-test.py
│   └── test_api.py
└── web_dynamic
    ├── __init__.py
    └── template_renderer.py
```

## Functionalities

### User Authentication

- **Login**: Users can log in to their accounts using the login API endpoint.
- **Register**: New users can create an account by registering through the API.
- **Logout**: Users can log out of their accounts, ending their session.
- **Deregister**: Users can delete their accounts, removing all associated data.
- **Session Management**: User sessions are managed using Flask-Session and cookies.

### Game Logic

- **Multiplayer**: Supports real-time multiplayer games using Socket.IO.

### Real-Time Communication

- **Socket.IO**: Enables real-time communication between clients and the server for multiplayer games.

### Database Interaction

- **MongoDB**: Interfaces with a MongoDB database to store user data, game states, and leaderboards.
- **Database Initialization**: Initializes the database connection and sets up collections.

### API Endpoints

- **Auth Routes**: Handles user authentication-related endpoints.
- **User Routes**: Manages user-related endpoints.
- **Leaderboard Routes**: Provides endpoints for leaderboard functionalities.

### Web Dynamic

- **Template Renderer**: Serves dynamic web pages and handles routes for the web application.

## Installation

To install the dependencies for the server application, run the following command in the `server` directory:

```sh
pip install -r requirements.txt
```

## Development

To start the development server, run:

```sh
python app.py
```

This will start the Flask development server and enable hot-reloading for code changes.

## Building

To build the server application for production, use Docker:

```sh
docker build -t server-build -f backend.Dockerfile .
```

## Environment Variables

The server application uses environment variables to configure various settings. An example environment file is provided as `example-dotenv-file`. To use it, copy it to `.env` and update the values as needed:

```sh
cp example-dotenv-file .env
```

## Docker

The server application can be built and run using Docker. A `backend.Dockerfile` is provided for building the server application. To build the Docker container, use the following command:

```sh
docker build -t server-build -f backend.Dockerfile .
```

And to run it:

```sh
docker run --rm -v $(pwd)/server/static:/app/server/static server-build
```

This command is used to run a Docker container from the server-build image, with the server/static directory from the host machine mounted into the container, and ensures the container is removed after it stops. This setup is useful for serving static files and keeping the development environment clean.

Additionally, the `docker-compose.yml` file in the root directory can be used to manage the entire project, including the client, backend, and database services.

## Security Notes

- In a production environment, ensure to use strong, unique passwords for MongoDB.
- The `SECRET_KEY` should be a long, random string in production.
- Consider using a reverse proxy like Nginx in front of the backend for additional security.
- Restrict CORS origins to only the domains you trust.

## Scaling

This setup uses a single backend instance. For scaling:

1. Consider using a container orchestration system like Kubernetes.
2. Implement a load balancer in front of multiple backend instances.
3. Use a managed MongoDB service for better scalability and management.

## License

This project is licensed under the GNU General Public License. For more information, see the LICENSE file.
