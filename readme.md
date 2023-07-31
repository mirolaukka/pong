# Pong Game (AI vs AI)

This is a simple implementation of the classic game "Pong" using the Tkinter library in Python. The game is designed to be played by two AI-controlled paddles. The paddles follow the ball's vertical position to simulate the gameplay.

## How to Play

1. Run the Python script in your Python environment.
2. The game window will appear, and the AI-controlled paddles will start playing immediately.
3. The AI paddles will move up and down to prevent the ball from passing their side of the screen.
4. The game continues indefinitely as the AI paddles continue to play.

## Game Components

### Ball Class

This class represents the ball object in the game. It is responsible for its movement, collision detection, and resetting after scoring.

### Paddle Class

This class represents the AI-controlled paddles used by the game. The AI follows the ball's vertical position to move the paddles up and down.

### Score Class

This class keeps track of the AI players' scores and updates the score display on the canvas.

### GameController Class

The GameController class manages the game's logic, including updating the paddles' AI to follow the ball's position, handling ball-paddle collisions, checking if the ball is out of bounds, and moving the ball and paddles.

### PongGame Class

This class sets up the game environment, including creating the Tkinter canvas, AI-controlled paddles, ball, and score objects. The game starts automatically, and the AI paddles play against each other.

## AI Paddles

The game includes two simple AI paddles (`simple_ai_paddle_a` and `simple_ai_paddle_b`). These AI paddles follow the ball's vertical position, but they move at different speeds to add some variability to their behavior.

## Customization

You can customize the game's appearance and behavior by modifying the constants defined at the end of the script:

- `WIDTH`: Set the width of the game window (default is 600).
- `HEIGHT`: Set the height of the game window (default is 400).
- `PADDLE_WIDTH`: Set the width of the AI paddles (default is 10).
- `PADDLE_HEIGHT`: Set the height of the AI paddles (default is 80).
- `BALL_SIZE`: Set the size of the ball (default is 15).

Feel free to experiment and make modifications to the AI behavior or the game rules according to your preferences.

Enjoy watching the AI-controlled paddles play Pong!