import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
TRANSPARENT_OVERLAY = (0, 0, 0, 128)  # Semi-transparent black

# Display settings
width = 1000  # Set the width to 1000
height = 800
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Slither')

clock = pygame.time.Clock()

# Snake settings
snake_block = 20  # Increase the snake block size from 10 to 20
snake_speed = 12

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
game_over_font = pygame.font.SysFont("bahnschrift", 65)  # Larger font for "Game Over"

# Global variable to track the highest score
highest_score = 0

# Score function
def display_score(score, high_score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    high_score_value = score_font.render("High Score: " + str(high_score), True, YELLOW)
    dis.blit(value, [10, 10])
    dis.blit(high_score_value, [width - 250, 10])  # Keep high score 250px from the right edge

# Draw the snake
def draw_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(dis, GREEN, [segment[0], segment[1], snake_block, snake_block])

# Button function
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(dis, color, [x, y, width, height])
    text_surface = font_style.render(text, True, text_color)
    dis.blit(text_surface, [(x + (width / 2 - text_surface.get_width() / 2)),
                            (y + (height / 2 - text_surface.get_height() / 2))])

    return pygame.Rect(x, y, width, height)  # Return the button's rect

# Game over message with buttons
def game_over_screen(score, high_score):
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height))  # Create overlay
    overlay.set_alpha(150)  # Set transparency
    overlay.fill(BLACK)  # Fill the overlay with black
    dis.blit(overlay, (0, 0))

    # Display the large "Game Over" text
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    
    # Center the "Game Over" text at the top
    game_over_x = (width / 2) - (game_over_text.get_width() / 2)
    game_over_y = height / 4 - (game_over_text.get_height() / 2)
    dis.blit(game_over_text, [game_over_x, game_over_y])

    # Display score and high score below the "Game Over" text
    points_text = font_style.render(f"Score: {score} | High Score: {high_score}", True, WHITE)
    points_x = (width / 2) - (points_text.get_width() / 2)
    points_y = game_over_y + game_over_text.get_height() + 20  # Positioned slightly below the "Game Over" text
    dis.blit(points_text, [points_x, points_y])

    # Draw buttons
    button_width = 200
    button_height = 50
    play_button_x = width / 2 - button_width - 20  # Button centered horizontally with some gap
    quit_button_x = width / 2 + 20  # Right of play button with some gap

    play_button = draw_button("Play Again", play_button_x, height / 2, button_width, button_height, GREEN, WHITE)
    quit_button = draw_button("Quit", quit_button_x, height / 2, button_width, button_height, RED, WHITE)

    pygame.display.update()
    return play_button, quit_button

# Main game loop
def gameLoop():
    global highest_score  # Use the global highest score

    game_over = False
    game_close = False

    while not game_over:
        # Reset the game state
        x1 = width / 2
        y1 = height / 2
        x1_change = 0
        y1_change = 0
        snake_list = []
        length_of_snake = 1

        # Randomly position food and align it to the grid
        foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0  # Align food to new snake_block size (20)
        foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

        while not game_close:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(BLACK)

            pygame.draw.rect(dis, RED, [foodx, foody, snake_block, snake_block])

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_close = True

            draw_snake(snake_block, snake_list)
            display_score(length_of_snake - 1, highest_score)  # Always display the highest score

            pygame.display.update()

            # Check if the snake eats the food
            if x1 == foodx and y1 == foody:
                # Re-align food to grid on new random placement
                foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
                length_of_snake += 1

            clock.tick(snake_speed)

        # Update high score if necessary
        if length_of_snake - 1 > highest_score:
            highest_score = length_of_snake - 1

        # Show game over screen with buttons
        play_button, quit_button = game_over_screen(length_of_snake - 1, highest_score)

        # Wait for user input to retry or quit
        while game_close:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        gameLoop()  # Restart the game
                    elif quit_button.collidepoint(event.pos):
                        game_over = True
                        game_close = False
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

    pygame.quit()
    quit()

gameLoop()
