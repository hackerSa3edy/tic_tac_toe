# ALX TicTacToe Client

## Remaining Tasks

- [ ] Profile page.
- [ ] Leaderboard page.
- [ ] Panel during the game illustrates whose turn is, name of the opponnet, and the player's "X" or "O" assigned.
- [ ] Necassary buttons, for logout, back and forth, ...etc.
- [ ] More clear errors pop-up.

## Overview

This is the client-side application for the ALX TicTacToe project, built using React, TypeScript, and Vite. It offers a user-friendly interface for playing TicTacToe in multiple modes: local play, AI play, and multiplayer.

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Development](#development)
6. [Configuration](#configuration)
7. [Deployment](#deployment)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- **User Authentication**: Secure login and registration system
- **Multiple Game Modes**:
  - Local Play: Two players on the same device
  - AI Play: Challenge an AI opponent
  - Multiplayer: Online matches against other players
- **Interactive Game Board**: Responsive design with hover effects and win indicators
- **Responsive Design**: Optimized for various screen sizes, including mobile devices

## Technology Stack

- React
- TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- Socket.IO (Real-time communication for multiplayer)
- Docker (Containerization)

## Project Structure

The project follows a modular structure with separate directories for components, assets, and configuration files. Key directories include:

- `src/`: Source code, including React components and TypeScript files
- `public/`: Static assets
- `src/assets/`: Fonts, images, and stylesheets
- `src/components/`: React components for different game modes and pages

## Getting Started

1. Clone the repository
2. Install dependencies: `npm install`
3. Set up environment variables: Copy `example-dot-env` to `.env` and adjust as needed
4. Start the development server: `npm run dev`

## Development

- **Development Server**: Run `npm run dev` for hot-module replacement
- **Building**: Execute `npm run build` to create a production build
- **Linting**: Use `npm run lint` to run ESLint

## Configuration

### Vite Configuration

The `vite.config.ts` file configures the build tool and development server:

- Enables React support
- Configures Tailwind CSS
- Sets up a proxy for API requests during development

### Environment Variables

The `.env` file contains important configuration settings:

- `SERVER_API_URL`: Specifies the backend server URL that is used in `vite.config.ts` to handle CORS issues during development.
- Loaded using `dotenv` for secure and flexible configuration management

## Deployment

### Docker

- Use `client.Dockerfile` to build the client application
- A `docker-compose.yml` file in the root directory manages the entire project stack

### Building for Production

Run `npm run build` to create optimized production files in the `dist/` directory

## Contributing

Contributions are welcome! Please refer to the contributing guidelines for more information.

## License

This project is licensed under the GNU General Public License. See the LICENSE file for details.
