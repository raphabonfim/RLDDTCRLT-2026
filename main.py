import pygame
import sys

HEIGHT = 320
WIDTH = 180
FPS = 60
TILE_SIZE = 10

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("r/roguelikedev does the tutorial 2026")
clock = pygame.time.Clock()

# === COLORS === #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)


# === PLAYER === #
PLAYER_HEIGHT = TILE_SIZE
PLAYER_WIDTH = TILE_SIZE
PLAYER_START_POS_X = 2 * TILE_SIZE
PLAYER_START_POS_Y = 2 * TILE_SIZE
PLAYER_COLOR = WHITE

def draw(player):
    pygame.draw.rect(screen, PLAYER_COLOR, player)


all_sprites = pygame.sprite.Group()


running = True
clock.tick(FPS)
    
player = pygame.Rect(
    PLAYER_START_POS_X,
    PLAYER_START_POS_Y,
    PLAYER_HEIGHT,
    PLAYER_WIDTH
    )


while running:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(f'player.y={player.y}, player.x={player.x}')
            
            elif event.key in (pygame.K_UP, pygame.K_k):
                player.y -= TILE_SIZE
            elif event.key in (pygame.K_DOWN, pygame.K_j):
                player.y += TILE_SIZE
            elif event.key in (pygame.K_LEFT, pygame.K_h):
                player.x -= TILE_SIZE
            elif event.key in (pygame.K_RIGHT, pygame.K_l):
                player.x += TILE_SIZE



        # === UPDATE GAME STATE === #
        all_sprites.update()
        
        # === DRAWING AND RENDERING === #
        screen.fill(BLACK)
        
        all_sprites.draw(screen) 
        draw(player)


        pygame.display.flip()
        
pygame.quit()
sys.exit()
