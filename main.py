# 2026-08-22  
# to do next: the dungeon
# [x] floor tiles
# [x] walls
# [ ] rooms
# [ ] field of view
# next: 
# [x] border tiles as walls
# [x] walkable check
# 2026-08-23
# [ ] diagonal stuck fallback for monsters (pre-pathfinding)
# [ ] room generation
# [ ] create all walls
# [ ] carve rooms
# [ ] connect the rooms with corridors
# [ ] place the player in the first room

import pygame
import sys

# === Constants and other variables === #
TILE_SIZE = 16
MAP_HEIGHT = 18
MAP_WIDTH = 32
HEIGHT = MAP_HEIGHT * TILE_SIZE
WIDTH = MAP_WIDTH * TILE_SIZE
FPS = 60

# === COLORS === #
WHITE = (255, 255, 255)
DARK_GRAY = (85, 85, 85)
LIGHT_GRAY = (190, 190, 190)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)


# === Standard Game Loop Structure in 5 steps: === #

# 1. Initialize and set up the window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("r/roguelikedev does the tutorial 2026")
clock = pygame.time.Clock()

# === CLASSES === #
class Entity:
    def __init__(self, x, y, hp, sprite):
        self.x = x
        self.y = y
        self.hp = hp
        self.sprite = sprite
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Tile:
    def __init__(self, color, walkable):
        self.color = color
        self.walkable = walkable

PLAYER_SPRITE = pygame.image.load("./assets/player.png").convert_alpha()
MONSTER_SPRITE = pygame.image.load("./assets/monster.png").convert_alpha()

# === HELPER FUNCTIONS === #

def get_blocking_entity(x, y, entities):
    for entity in entities:
        if entity.x == x and entity.y == y:
            return entity
    return None

def is_walkable(x, y, floor_map):
    if x < 0 or x >= MAP_WIDTH:
        return False
    if y < 0 or y >= MAP_HEIGHT:
        return False
    return floor_map[x][y].walkable

player = Entity(2, 2, 10, PLAYER_SPRITE)
monster = Entity(5, 5, 5, MONSTER_SPRITE)
monster2 = Entity(10, 7, 5, MONSTER_SPRITE)


entities = [player, monster, monster2]

floor_map = [[Tile(DARK_GRAY, True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

for y in range(MAP_HEIGHT):
    floor_map[0][y] = Tile(LIGHT_GRAY, False)
    floor_map[MAP_WIDTH - 1][y] = Tile(LIGHT_GRAY, False)
for x in range(MAP_WIDTH):
    floor_map[x][0] = Tile(LIGHT_GRAY, False)
    floor_map[x][MAP_HEIGHT - 1] = Tile(LIGHT_GRAY, False)


running = True
turn_counter = 0

while running:
    # 2. Handle events so the game can receive input and respond to it

    turn_taken = False
    direction = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d: # for debug
                print(f'player.y={player.y}, player.x={player.x}')
                print(f'monster.y={monster.y}, monster.x={monster.x}')
                print(f'monster2.y={monster2.y}, monster2.x={monster2.x}')
                print(f'turn: {turn_counter}')
                print(f'entities: {entities}')

            elif event.key == pygame.K_SPACE: # wait
                direction = (0, 0)

            elif event.key in (pygame.K_UP, pygame.K_k):
                direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_j):
                direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_h):
                direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_l):
                direction = (1, 0)

            if direction is not None:
                dx, dy = direction
                dest_x, dest_y = player.x + dx, player.y + dy

                if is_walkable(dest_x, dest_y, floor_map): 

                    blocked_by = get_blocking_entity(dest_x, dest_y, entities)
                    if blocked_by:
                        blocked_by.hp -= 1
                        print(f"You kick the monster. {blocked_by.hp} HP left.")
                        if blocked_by.hp <= 0:
                            entities.remove(blocked_by) 
                    else:
                        player.x += dx
                        player.y += dy
                
                    turn_taken = True
                    turn_counter += 1

    if turn_taken: 
        for entity in list(entities):
            if entity is player:
                continue
        
            # an arithmetric trick to chase.
            # when player moves, we compare their relative position 
            # as True or False to understand the need to move
            # if the comparison != 0, then the monster needs to move 1 step
            # the direction is given by 
            # the sign of the difference between the 2 comparisons

            dx = (player.x > entity.x) - (player.x < entity.x)
            dy = (player.y > entity.y) - (player.y < entity.y)

            
            candidates = [(dx, dy), (dx, 0), (0, dy)]
            for cdx, cdy in candidates:
                dest_x, dest_y = entity.x + cdx, entity.y + cdy

                if get_blocking_entity(dest_x, dest_y, entities) is player:
                    player.hp -= 1
                    print(f"The monster bites you! {player.hp} HP left!")
                    if player.hp <= 0:
                        print("game over!")
                        running = False
                    break

                if is_walkable(dest_x, dest_y, floor_map) and get_blocking_entity(dest_x, dest_y, entities) is None:
                    entity.x += cdx
                    entity.y += cdy
                    break

    # 3. Clear/Fill BG so the sprites won't leave trails
    screen.fill(BLACK)

    # 4. Draw your objects here (blit sprites, draw shapes, render fonts)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            tile = floor_map[x][y]
            pygame.draw.rect(screen, tile.color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    
    for entity in entities:
        entity.draw(screen)

    
    # 5. Update the display so the player can see the new frame
    pygame.display.flip()

    # 6. Tick the clock so the game runs at the capped FPS
    clock.tick(FPS)
    
pygame.quit()
sys.exit()
