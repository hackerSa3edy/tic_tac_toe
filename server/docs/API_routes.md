# API Routes Documentation

## Authentication Routes

### `POST /api/auth/login`

- **Description**: Login a user.
- **Request Body**:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.
- **Responses**:
  - `200 OK`: If the user is already logged in.
  - `400 Bad Request`: If the request body is missing parameters or if the login credentials are incorrect.
  - `200 OK`: If the login is successful.

### `DELETE /api/auth/logout`

- **Description**: Logout a user.
- **Responses**:
  - `400 Bad Request`: If the user is not logged in.
  - `200 OK`: If the logout is successful.

### `POST /api/auth/register`

- **Description**: Register a new user.
- **Request Body**:
  - `username` (string): The desired username.
  - `email` (string): The email address of the user.
  - `password` (string): The desired password.
- **Responses**:
  - `200 OK`: If the user is already logged in.
  - `400 Bad Request`: If the request body is missing parameters or if there is an error during registration.
  - `200 OK`: If the registration is successful.

### `POST /api/auth/deregister`

- **Description**: Deregister a user.
- **Responses**:
  - `400 Bad Request`: If there is an error during deregistration.
  - `200 OK`: If the deregistration is successful.

### `GET /api/auth/check-session`

- **Description**: Check the session status of a user.
- **Responses**:
  - `200 OK`: If the user is logged in.
  - `400 Bad Request`: If the user is not logged in.

## Game Routes

### `GET /api/user/games`

- **Description**: Retrieve all games with pagination.
- **Query Parameters**:
  - `page` (int): The page number (default is 1).
  - `per_page` (int): The number of items per page (default is 10).
- **Responses**:
  - `200 OK`: Returns a list of games, total count, current page, items per page, next URL, and back URL.

## User Routes

### `GET /api/user/profile`

- **Description**: Retrieve user information.
- **Responses**:
  - `400 Bad Request`: If the user is not logged in.
  - `200 OK`: Returns the user information.

### `PUT /api/user/profile`

- **Description**: Update user information.
- **Request Body**:
  - `new_username` (string, optional): The new username.
  - `new_email` (string, optional): The new email address.
- **Responses**:
  - `400 Bad Request`: If the user is not logged in or if there are errors during the update.
  - `200 OK`: If the update is successful.

### `POST /api/user/update_password`

- **Description**: Update user password.
- **Request Body**:
  - `old_password` (string): The current password.
  - `new_password` (string): The new password.
- **Responses**:
  - `400 Bad Request`: If the user is not logged in or if there are errors during the update.
  - `200 OK`: If the update is successful.

## Leaderboard Routes

### `GET /api/leaderboard/`

- **Description**: Retrieve the leaderboard.
- **Responses**:
  - `400 Bad Request`: If the user is not logged in.
  - `200 OK`: Returns the top players and the current player's stats and rank.
