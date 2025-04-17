import pygame

# Initialize pygame
pygame.init()

# Canvas size define karein
CANVAS_WIDTH, CANVAS_HEIGHT = 400, 400
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Eraser Canvas")

# Colors define karein
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

# Grid create karein
CELL_SIZE = 40
ERASER_SIZE = 20
rows = CANVAS_HEIGHT // CELL_SIZE
cols = CANVAS_WIDTH // CELL_SIZE

# Rectangles store karne ke liye list
rectangles = []

# Grid draw karein
for row in range(rows):
    for col in range(cols):
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        rectangles.append(rect)
        pygame.draw.rect(screen, BLUE, rect)

pygame.display.update()

# Eraser initialize karein
eraser = pygame.Rect(200, 200, ERASER_SIZE, ERASER_SIZE)

running = True
while running:
    pygame.time.delay(50)  # Small delay
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Loop ko break karna
        
    # Mouse ka position lein
    mouse_x, mouse_y = pygame.mouse.get_pos()
    eraser.topleft = (mouse_x, mouse_y)
    
    # Jo cells touch ho rahi hain unhe white karein
    for rect in rectangles:
        if eraser.colliderect(rect):
            pygame.draw.rect(screen, WHITE, rect)

    # Eraser ko pink color do
    pygame.draw.rect(screen, PINK, eraser)
    
    pygame.display.update()

pygame.quit()  # Pygame properly close karna
