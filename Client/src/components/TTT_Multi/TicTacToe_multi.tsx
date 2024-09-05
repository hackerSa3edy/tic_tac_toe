import React, { useState, useEffect, useRef, useCallback } from "react";
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
  const [grid, setGrid] = useState(squares);
  const [winner, setWinner] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [gameId, setGameId] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  const socketRef = useRef<Socket | null>(null);
  const opponentSymbolRef = useRef<number | null>(null);
  const opponentRef = useRef<string | null>(null);
  const currentTurnRef = useRef<number | null>(null);
  const gameStateRef = useRef(gameState)

  useEffect(() => {
    gameStateRef.current = gameState;
  }, [gameState]);


  useEffect(() => {
    console.log("--------------------- TicTacToe_multi ---------------------");
    console.log("Game State: ", gameState);
    console.log("Player Symbol: ", playerSymbol);
    console.log("Opponent Symbol: ", opponentSymbolRef.current);
    console.log("Opponent: ", opponentRef.current);
    console.log("Current Turn: ", currentTurnRef.current);
    console.log("Winner: ", winner);
    console.log("Modal Open: ", modalOpen);
    console.log("Game ID: ", gameId);
    console.log("Error: ", error);
    console.log("Socket: ", socketRef.current);
  }, [
    gameState,
    playerSymbol,
    opponentSymbolRef.current,
    opponentRef.current,
    currentTurnRef.current,
    winner,
    modalOpen,
    gameId,
    error,
    socketRef.current
  ]);

  // Game logic
  useEffect(() => {
    // Socket setup
    const socket = io("/");
    socketRef.current = socket;

    const setupGame = () => {
      console.log("Socket connection established. ID:", socket.id);
      console.log("Joining game...");
      socket.emit("join_game");
    };

    const handleGameJoined = (data: { game_id: string }) => {
      setGameId(data.game_id);
      setPlayerSymbol(PLAYER_X);
      setGameState(GAME_STATES.waiting);
      console.log("handleGameJoined");
    };

    const handleOpponentJoined = (data: { opponent: string }) => {
      opponentRef.current = data.opponent;
      opponentSymbolRef.current = PLAYER_O;
      setGameState(GAME_STATES.inProgress);
      currentTurnRef.current = PLAYER_X;
      console.log("handleOpponentJoined");
    };

    const handleGameStarted = (data: { game_id: string; opponent: string }) => {
      setGameId(data.game_id);
      opponentSymbolRef.current = PLAYER_X;
      setPlayerSymbol(PLAYER_O);
      currentTurnRef.current = PLAYER_X;
      opponentRef.current = data.opponent;
      setGameState(GAME_STATES.inProgress);
      console.log("handleGameStarted");
    };

    const handleMoveMade = (data: { position: number }) => {
      console.log("Move made by opponent", opponentSymbolRef.current);
      move(data.position, opponentSymbolRef.current);
      currentTurnRef.current = currentTurnRef.current === PLAYER_X ? PLAYER_O : PLAYER_X;
      console.log("handleMoveMade");
    };

    const handleGameOver = (data: { result: string; winner: string }) => {
      setWinner(data.result === 'draw' ? 'draw' : (data.winner === opponentRef.current ? opponentRef.current : 'You') + ' won!');
      setGameState(GAME_STATES.over);
      console.log("handleGameOver");
    };

    socket.on("connect", setupGame);
    socket.on('game_joined', handleGameJoined);
    socket.on('opponent_joined', handleOpponentJoined);
    socket.on('game_started', handleGameStarted);
    socket.on("move_made", handleMoveMade);
    socket.on('game_over', handleGameOver);

    socket.on('error', (data) => {
      setError(data.message);
    });

    return () => {
      socket.off("connect");
      socket.off("game_joined");
      socket.off("opponent_joined");
      socket.off("game_started");
      socket.off("move_made");
      socket.off("game_over");
      socket.off("error");
      socket.close();
    };
  }, []);

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
      setTimeout(() => setModalOpen(true), 300);
    }
  }, [gameState, grid]);

  // Sound effects
  useEffect(() => {
    if (currentTurnRef.current !== null) {
      clickSound.play();
    }
  }, [currentTurnRef.current]);

  useEffect(() => {
    if (gameState !== GAME_STATES.inProgress) {
      gameOverSound.play();
    }
  }, [gameState]);

  // Move function
  const move = useCallback(
    (index: number, player: number | null) => {
    console.log("Move made ", index, player);
    console.log("Game State: ", gameStateRef.current, player, " made a move at ", index);
    if (player !== null && gameStateRef.current === GAME_STATES.inProgress) {
        setGrid(grid => {
        const gridCopy = grid.concat();
        gridCopy[index] = player;
        return gridCopy;
        });
    }
  }, [gameState]);

  // Human move function
  const humanMove = (index: number) => {
    if (!grid[index] && currentTurnRef.current === playerSymbol) {
      console.log("MOVE_VALID", index, playerSymbol);
      move(index, playerSymbol);
      currentTurnRef.current = playerSymbol === PLAYER_O ? PLAYER_X : PLAYER_O;

      if (socketRef.current) {
        socketRef.current.emit("make_move", { position: index, game_id: gameId });
      }
    }
  };

  // New game function
  const startNewGame = () => {
    setGameState(GAME_STATES.waiting);
    setGrid(INITIAL_GRID);
    setModalOpen(false);

    if (socketRef.current) {
      socketRef.current.emit("join_game");
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
