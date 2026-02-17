# main.py
# ------------------------------------------------------------
# This file connects the gesture‑based camera controller with
# the Snake game. It imports:
# - run_game() from snake_game.py  → starts and manages the game
# - get_direction() from camera_movement.py → reads gestures
#
# The game is launched with direction_callback=get_direction,
# meaning the snake's movement is controlled by the camera.
# ------------------------------------------------------------

from snake_game import run_game
from camera_movement import get_direction

# Start the game and pass the camera gesture function.
# run_game() will call get_direction() every frame to update
# the snake's direction based on hand movement.
run_game(direction_callback=get_direction)