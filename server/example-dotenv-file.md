# This file contains environment variables for the Flask application and MongoDB

## Flask Environment Variables

- **[`FLASK_ENV`]**:

  - **Purpose**: Specifies the environment in which the Flask application is running.
  - **Usage**: Common values are [`development`].

- **[`SECRET_KEY`]**:
  - **Purpose**: A secret key used by Flask to sign cookies and other security-related tasks.
  - **Usage**: Should be a long, random string to ensure security. It's crucial for session management and CSRF protection.

## Development and Debugging

- **[`HOST_NAME`]**:

  - **Purpose**: The hostname where the Flask application will run.
  - **Usage**: Typically set to [`localhost`] for local development.

- **[`APP_PORT`]**:
  - **Purpose**: The port on which the Flask application will listen.
  - **Usage**: Commonly set to [`3000`] or another port that is not in use.

## MongoDB Environment Variables

- **[`MONGO_ROOT_USERNAME`]**:

  - **Purpose**: The username for the MongoDB root user.
  - **Usage**: Used for administrative tasks and initial setup.

- **[`MONGO_ROOT_PASSWORD`]**:

  - **Purpose**: The password for the MongoDB root user.
  - **Usage**: Should be kept secure and used in conjunction with [`MONGO_ROOT_USERNAME`].

- **[`MONGO_NON_ROOT_USERNAME`]**:

  - **Purpose**: The username for a non-root MongoDB user.
  - **Usage**: Used by the application to interact with the database without root privileges.

- **[`MONGO_NON_ROOT_PASSWORD`]**:

  - **Purpose**: The password for the non-root MongoDB user.
  - **Usage**: Should be kept secure and used in conjunction with [`MONGO_NON_ROOT_USERNAME`].

- **[`MONGO_HOSTNAME`]**:

  - **Purpose**: The hostname or Docker container name where MongoDB is running.
  - **Usage**: In a Docker setup, this is typically the name of the MongoDB container.

- **[`MONGO_DATABASE`]**:
  - **Purpose**: The name of the MongoDB database to be used by the application.
  - **Usage**: Specifies which database the application will connect to.

## CORS Environment Variables

- **[`CORS_ORIGINS`]**:

  - **Purpose**: Specifies the origins that are allowed to make cross-origin requests.
  - **Usage**: Typically set to the URL of the frontend application, e.g., [`http://127.0.0.1:3000`] for local development.

- **[`CORS_SUPPORTS_CREDENTIALS`]**:

  - **Purpose**: Indicates whether or not the browser should include credentials (like cookies) in cross-origin requests.
  - **Usage**: Set to `True` or [`False`] depending on whether credentials are needed.

- **[`SESSION_COOKIE_SAMESITE`]**:
  - **Purpose**: Controls the `SameSite` attribute for session cookies.
  - **Usage**: Can be set to [`Lax`] allows cookies to be sent with same-site requests and some cross-site requests.

These environment variables help configure the Flask application and MongoDB, ensuring that the application runs correctly in different environments (development, production, etc.) and that security measures are in place.

## docker deployment env file example `docker compose up --build -d`

```text
FLASK_ENV=production
SECRET_KEY=FLASK-tic_tac_toe-APP


MONGO_ROOT_USERNAME=root
MONGO_ROOT_PASSWORD=toor

MONGO_NON_ROOT_USERNAME=app
MONGO_NON_ROOT_PASSWORD=passwd
MONGO_HOSTNAME=mongo # Docker container name, for production
MONGO_DATABASE=tic_tac_toe


CORS_ORIGINS=http://127.0.0.1:3000
CORS_SUPPORTS_CREDENTIALS=False
SESSION_COOKIE_SAMESITE='Lax' # Restrict cookie sending for cross-site requests
```

## development env file example `python app.py`

```text
FLASK_ENV=development
SECRET_KEY=FLASK-tic_tac_toe-APP
HOST_NAME=localhost
APP_PORT=3000


MONGO_NON_ROOT_USERNAME=app
MONGO_NON_ROOT_PASSWORD=passwd
MONGO_HOSTNAME=localhost
MONGO_DATABASE=tic_tac_toe


CORS_ORIGINS=http://127.0.0.1:3000
CORS_SUPPORTS_CREDENTIALS=False
SESSION_COOKIE_SAMESITE='Lax' # Restrict cookie sending for cross-site requests
```
