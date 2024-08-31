import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import io, { Socket } from "socket.io-client";
import styled from "styled-components";
import {
  PLAYER_X,
  PLAYER_O,
  SQUARE_DIMS,
  GAME_STATES,
  DIMENSIONS,
} from "./constants";
import Board from "./Board";
import { ResultModal } from "./ResultModal";
import { border } from "./styles";
import gameOverSoundAsset from "../../assets/sounds/game_over.wav";
import clickSoundAsset from "../../assets/sounds/click.wav";
import boardImage from "../../assets/Images/board.png";

// Types
interface UserInfo {
  game_played: number;
  wins: number;
  losses: number;
  draws: number;
}

interface Props {
  squares?: Array<number | null>;
}

// Constants
const INITIAL_GRID = new Array(DIMENSIONS ** 2).fill(null);
const board = new Board();

// Sound setup
const gameOverSound = new Audio(gameOverSoundAsset);
gameOverSound.volume = 0.2;
const clickSound = new Audio(clickSoundAsset);
clickSound.volume = 0.5;

const TicTacToe_multi: React.FC<Props> = ({ squares = INITIAL_GRID }) => {
  const navigate = useNavigate();

  // State
  const [gameState, setGameState] = useState(GAME_STATES.waiting);
  const [playerSymbol, setPlayerSymbol] = useState<number | null>(null);
  const [opponentSymbol, setOpponentSymbol] = useState<number | null>(null);
  const [opponent, setOpponent] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState<number | null>(null);
  const [grid, setGrid] = useState(squares);
  const [winner, setWinner] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [gameId, setGameId] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Socket setup
  useEffect(() => {
    const newSocket = io("http://localhost:3000/", { withCredentials: true });
    setSocket(newSocket);

    newSocket.on("connect", () => {
      console.log("Socket connection established. ID:", newSocket.id);
    });

    newSocket.on('error', (data) => {
      setError(data.message);
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Game logic
  useEffect(() => {
    if (!socket) return;

    const setupGame = () => {
      socket.emit("join_game");
      console.log("Joining game...");
    };

    const handleGameJoined = (data: { game_id: string }) => {
      setGameId(data.game_id);
      setPlayerSymbol(PLAYER_X);
      setGameState(GAME_STATES.waiting);
      console.log("You: ", PLAYER_X, "Game id: ", data.game_id);
    };

    const handleOpponentJoined = (data: { opponent: string }) => {
      setOpponent(data.opponent);
      setOpponentSymbol(PLAYER_O);
      setGameState(GAME_STATES.inProgress);
      setCurrentTurn(PLAYER_X);
      console.log("opponent: ", PLAYER_O);
    };

    const handleGameStarted = (data: { game_id: string; opponent: string }) => {
      setGameId(data.game_id);
      setOpponentSymbol(PLAYER_X);
      setPlayerSymbol(PLAYER_O);
      setCurrentTurn(PLAYER_X);
      setOpponent(data.opponent);
      setGameState(GAME_STATES.inProgress);
      console.log("Game id: ", data.game_id, "You: ", PLAYER_O, "opponent: ", PLAYER_X);
    };

    const handleMoveMade = (data: { position: number }) => {
      console.log("Move made by opponent", opponentSymbol);
      move(data.position, opponentSymbol);
      setCurrentTurn(currentTurn => currentTurn === PLAYER_X ? PLAYER_O : PLAYER_X);
    };

    const handleGameOver = (data: { result: string; winner: string }) => {
      setGameState(GAME_STATES.over);
      setWinner(data.result === 'draw' ? 'draw' : (data.winner === opponent ? opponent : 'You') + ' won!');
    };

    setupGame();

    socket.on('game_joined', handleGameJoined);
    socket.on('opponent_joined', handleOpponentJoined);
    socket.on('game_started', handleGameStarted);
    socket.on("move_made", handleMoveMade);
    socket.on('game_over', handleGameOver);

    return () => {
      socket.off("game_joined");
      socket.off("opponent_joined");
      socket.off("game_started");
      socket.off("move_made");
      socket.off("game_over");
    };
  }, [socket, opponent, opponentSymbol]);

  // User profile fetch
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await fetch("/api/user/profile", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setUserInfo(data);
      } catch (error) {
        console.log(error instanceof Error ? error.message : "An unknown error occurred");
      }
    };

    fetchUserProfile();
  }, []);

  useEffect(() => {
    if (error) {
      alert(error);
    }
  }, [error]);

  // Winner check
  useEffect(() => {
    board.getWinner(grid);

    if (gameState === GAME_STATES.over) {
    //   const winnerStr = boardWinner === DRAW ? "It's a draw" : `Player ${boardWinner === PLAYER_X ? 'X' : 'O'} wins!`;
      setWinner(winner);
      setTimeout(() => setModalOpen(true), 300);
    }
  }, [gameState]);

  // Sound effects
  useEffect(() => {
    if (currentTurn !== null) {
      clickSound.play();
    }
  }, [currentTurn]);

  useEffect(() => {
    if (gameState !== GAME_STATES.inProgress) {
      gameOverSound.play();
    }
  }, [gameState]);

  // Move function
  const move = useCallback(
    (index: number, player: number | null) => {
      if (player !== null && gameState === GAME_STATES.inProgress) {
        setGrid(grid => {
          const gridCopy = grid.concat();
          gridCopy[index] = player;
          return gridCopy;
        });
      }
    },
    [gameState]
  );

  // Human move function
  const humanMove = (index: number) => {
    if (!grid[index] && currentTurn === playerSymbol) {
      console.log("MOVE_VALID", index, playerSymbol);
      move(index, playerSymbol);
      setCurrentTurn(playerSymbol === PLAYER_O ? PLAYER_X : PLAYER_O);

      if (socket) {
        socket.emit("make_move", { position: index, game_id: gameId });
      }
    }
  };

  // New game function
  const startNewGame = () => {
    setGameState(GAME_STATES.waiting);
    setGrid(INITIAL_GRID);
    setModalOpen(false);

    if (socket) {
      socket.emit("join_game");
      console.log("Rejoining game...");
    }
  };

  // Modal close function
  const handleClose = () => {
    setModalOpen(false);
    navigate("/");
  };

  // Render functions
  const renderUserInfo = () => (
    userInfo ? (
      <div className="flex justify-center items-center w-screen">
        <div className="absolute top-[2%] sm:w-[70%] md:w-[35%] py-4 px-10 text-center bg-opacity-50 rounded-full grid grid-cols-2 gap-4 items-center justify-around bg-slate-700">
          <p className="font-bold text-white text-xl">Games Played: {userInfo.game_played}</p>
          <p className="font-bold text-white text-xl">Wins: {userInfo.wins}</p>
          <p className="font-bold text-white text-xl">Losses: {userInfo.losses}</p>
          <p className="font-bold text-white text-xl">Draws: {userInfo.draws}</p>
        </div>
      </div>
    ) : (
      <p>Loading user information...</p>
    )
  );

  const renderGrid = () => (
    grid.map((value, index) => (
      <Square
        data-testid={`square_${index}`}
        key={index}
        onClick={() => humanMove(index)}
      >
        {value !== null && <Marker>{value === PLAYER_X ? "X" : "O"}</Marker>}
      </Square>
    ))
  );

  return gameState === GAME_STATES.waiting ? (
    <div className="text-white font-newrocker">
      <p>Waiting For Opponent</p>
    </div>
  ) : (
    <>
      {renderUserInfo()}
      <Container dims={DIMENSIONS}>
        {renderGrid()}
        <Strikethrough
          styles={gameState === GAME_STATES.over ? board.getStrikethroughStyles() : ""}
        />
        <ResultModal
          isOpen={modalOpen}
          winner={winner}
          close={handleClose}
          startNewGame={startNewGame}
        />
      </Container>
    </>
  );
};


const Container = styled.div<{ dims: number }>`
  display: flex;
  justify-content: center;
  width: ${({ dims }) => `${dims * (SQUARE_DIMS + 5)}px`};
  flex-flow: wrap;
  position: relative;
  font-family: "ArtNouveauCaps", sans-serif;
  font-weight: bold;
  color: white;
  background-image: url(${boardImage});
  background-size: cover;
  background-repeat: no-repeat;
  filter: brightness(0) invert(1);
  transform: scale(1.5);

  @media (max-width: 768px) {
    transform: scale(1);
  }
`;

const Square = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: ${SQUARE_DIMS}px;
  height: ${SQUARE_DIMS}px;
  ${border};

  &:hover {
    cursor: pointer;
  }
`;

Square.displayName = "Square";

const Marker = styled.p`
  font-size: 68px;
`;

const Strikethrough = styled.div<{ styles: string | null }>`
  position: absolute;
  ${({ styles }) => styles}
  background-color: indianred;
  height: 5px;
  width: ${({ styles }) => !styles && "0px"};
`;

export default TicTacToe_multi;
