import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Game constants
WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 17
CROSS_WIDTH = 25
FONT_SIZE = 50

# Setup screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50)) 
pygame.display.set_caption('Tic Tac Toe AI')
font = pygame.font.Font(None, FONT_SIZE)

# Initialize board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines():
    """Draw the grid lines for the Tic Tac Toe board."""
    for i in range(1, BOARD_ROWS):
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw the shapes (circles and crosses) on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Player 1: Circle
            # pygame.draw.circle(surface, color, center, radius, width)
                pygame.draw.circle(screen, YELLOW, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:  # AI (Player 2): Cross
            # pygame.draw.line(surface, color, start_pos, end_pos, width)
                pygame.draw.line(screen, RED, 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 
                                 CROSS_WIDTH)
                pygame.draw.line(screen, RED, 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), 
                                 CROSS_WIDTH)

def display_message(message):
    """Display a message at the bottom of the screen."""
    text = font.render(message, True, WHITE)
    screen.fill(BLACK, (0, HEIGHT, WIDTH, 50))  # Clear message area
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT + 10))

def check_win(player):
    """Check if the given player has won."""
    # Check rows, columns, and diagonals
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        return True
    return False

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def minimax(depth, is_maximizing):
    """Minimax algorithm for AI decision making."""
    if check_win(2):  # AI wins
        return 1
    if check_win(1):  # Player wins
        return -1
    if is_board_full():  # Tie
        return 0

    if is_maximizing:  # AI's turn
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2  # Simulate AI move
                    score = minimax(depth + 1, False)
                    board[row][col] = 0  # Undo move
                    best_score = max(best_score, score) 
        return best_score
    else:  # Player's turn
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1  # Simulate player move
                    score = minimax(depth + 1, True)
                    board[row][col] = 0  # Undo move
                    best_score = min(best_score, score)
        return best_score

def best_move():
    """Determine the best move for the AI using Minimax."""
    best_score = -float('inf')
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2  # Simulate AI move
                score = minimax(0, False)
                board[row][col] = 0  # Undo move
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = 2  # Make the best move

def restart_game():
    """Reset the game state."""
    screen.fill(BLACK)
    draw_lines()
    global board, game_over, current_player
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    game_over = False
    current_player = 1
    display_message('')


screen.fill(BLACK)
draw_lines()
current_player = 1
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos[0] // SQUARE_SIZE, event.pos[1] // SQUARE_SIZE
            if board[mouseY][mouseX] == 0:  # If square is empty
                board[mouseY][mouseX] = 1  # Player's move
                if check_win(1):
                    display_message('Player 1 wins!')
                    game_over = True
                elif is_board_full():
                    display_message("It's a tie!")
                    game_over = True
                else:
                    best_move()  # AI's move
                    if check_win(2):
                        display_message('AI wins!')
                        game_over = True
                    elif is_board_full():
                        display_message("It's a tie!")
                        game_over = True
        # To restart tge game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    draw_figures()
    pygame.display.update()