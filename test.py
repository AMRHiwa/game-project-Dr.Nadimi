import pygame


# Initialize Pygame
pygame.init()

# Define board attributes
board_size = (680, 680) # size of the board
slot_size = 60 # size of each slot
rows = 7 # number of rows
cols = 7 # number of columns
gap = 34 # gap between each slot

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode(board_size)
pygame.display.set_caption("Morabaraba Board")

# Set up a clock for the game loop
clock = pygame.time.Clock()

board_list = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2),
              (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5),
              (3, 6), (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5),
              (6, 0), (6, 3), (6, 6)]

# Draw the board
def draw_board():
    screen.fill(WHITE) # fill the screen with white
    # for r in range(rows):
    #     for c in range(cols):


    # pygame.draw.rect(screen, "darkGreen",(0, 0, 680,680 ))
    
    # rect1
    pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    pygame.draw.line(screen, 'Black', (64, 64), (64, 680 - 64), 4)

    pygame.draw.line(screen, 'Black', (680 - 50, 64), (680 - 50,680 - 64), 4)
    pygame.draw.line(screen, 'Black', (64, 680 - 64), (680 - 50,680 - 64), 4)

    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    # pygame.draw.line(screen, 'Black', (64, 64), (680 - 64, 64), 4)
    for (r,c) in board_list:
            
        x = c * slot_size + gap * (c + 1)
        y = r * slot_size + gap * (r + 1)
        # if r != 4 or c != 4:
        pygame.draw.circle(screen, "Gray", (x+30, y+30), 20)

# Draw the beads
def draw_beads(red_beads, blue_beads):
    for r in range(rows):
        for c in range(cols):
            x = c * slot_size + gap * (c + 1)
            y = r * slot_size + gap * (r + 1)
            # if (r, c) in red_beads:
            #     pygame.draw.circle(screen, RED, (x+slot_size//2, y+slot_size//2), slot_size//3)
            # elif (r, c) in blue_beads:
            #     pygame.draw.circle(screen, BLUE, (x+slot_size//2, y+slot_size//2), slot_size//3)

# Create the initial bead positions
red_beads = {(0, 0), (0, 3), (0, 5), (3, 0), (3, 3), (3, 5)}
blue_beads = {(1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (2, 4)}

# Main game loop
run = True
while run:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the board
    draw_board()

    # Draw the beads
    draw_beads(red_beads, blue_beads)

    # Update the screen
    pygame.display.update()

    # Set a tick rate to the loop (60 FPS)
    clock.tick(60)

# Quit Pygame
pygame.quit()