import pygame
from datetime import datetime

# - Constants -
WIDTH = 600
HEIGHT = 800
SPACE_V = 15
SPACE_H = 8
RADIUS = 60
BORDER = 4
CLOCK_WIDTH = 4 * 11 * 12
ROW_HEIGHT = 95
LEFT = WIDTH//2 - CLOCK_WIDTH//2

# Colors
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
DARK_ORANGE = (128, 65, 0)
DARK_RED = (128, 0, 0)
BLACK = (0,0,0)
BORDER_COLOR = (128, 128, 128)
BGCOLOR = (50, 50, 85)
WHITE = (255, 255, 255)

# - Pygame Setup -
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Berlin-Clock")
clock = pygame.time.Clock()
font = pygame.font.SysFont("", 40)

# - Class -
class BerlinClock:
    def __init__(self):
        self.draw(0,0,0)

    def draw_row(self, y, lamp_count = 4, on_color = RED, off_color = BLACK, border = 0, on = 0, is_five_min = False):
        # Draws a row with a given number of lamps (rectangles).
        
        x = LEFT + border
        lamp_width = (CLOCK_WIDTH - (lamp_count - 1) * SPACE_H) / lamp_count
        
        for i in range(lamp_count):
            pygame.draw.rect(screen, BORDER_COLOR, (x, y, lamp_width, ROW_HEIGHT))

            # Choose lamp color (on or off)
            color = on_color if i < on else off_color

            # in the 5-minute row, every 3rd lamp (15, 30, 45) is red
            if is_five_min and i % 3 == 2:
                color = RED if i < on else DARK_RED

            pygame.draw.rect(screen, color, (x + border, y + border, lamp_width - 2 * border, ROW_HEIGHT - 2 * border))
            x += lamp_width + SPACE_H

    def draw(self, sek, min, std):
        screen.fill(BGCOLOR)

        # The Seconds lamp (Top Circle)
        y_position = 2 * SPACE_V
        sec_color = DARK_ORANGE if sek % 2 else ORANGE 

        pygame.draw.circle(screen, BORDER_COLOR, (WIDTH // 2, y_position + RADIUS), RADIUS)
        pygame.draw.circle(screen, sec_color, (WIDTH // 2, y_position + RADIUS), RADIUS-BORDER)

        # Hours and Minutes Rows
        y_position += 2*RADIUS + SPACE_V
        self.draw_row(y_position, 4, RED, DARK_RED, BORDER, std // 5)
        y_position += ROW_HEIGHT + SPACE_V
        self.draw_row(y_position, 4, RED, DARK_RED, BORDER, std % 5)
        y_position += ROW_HEIGHT + SPACE_V
        self.draw_row(y_position, 11, ORANGE, DARK_ORANGE, BORDER, min // 5, True)
        y_position += ROW_HEIGHT + SPACE_V
        self.draw_row(y_position, 4, ORANGE, DARK_ORANGE, BORDER, min % 5)

myclock = BerlinClock()
running = True

while running:
    now = datetime.now()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False

    myclock.draw(now.second, now.minute, now.hour)

    # Display digital time
    text = font.render(now.strftime("%H:%M:%S"), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 60))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()