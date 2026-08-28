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
import random

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

class Room:
    def __init__(self, x1, y1, x2, y2):
        # normalizes so x1 and y1 are always the smaller
        # that means they are always the top-left corner
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2) 

    def center(self):
        # calculates the center of room position using math 
        return ((self.x2 - self.x1) // 2 + self.x1, (self.y2 - self.y1) // 2 + self.y1) 
    
    def intersects(self, other):
        if self.x2 < other.x1 or self.x1 > other.x2 or self.y2 < other.y1 or self.y1 > other.y2:
            return False
        return True


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

def carve_room(floor_map, x1, y1, x2, y2): # the +1 makes the room inclusive that means that we INCLUDE the coordinate in the room
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            floor_map[x][y] = Tile(DARK_GRAY, True)

def carve_h_corridor(floor_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        floor_map[x][y] = Tile(DARK_GRAY, True)

def carve_v_corridor(floor_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        floor_map[x][y] = Tile(DARK_GRAY, True)
 



# === ROOM GENERATION === # 

# setting all tiles to stone first
floor_map = [[Tile(LIGHT_GRAY, False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

rooms = []

for _ in range(50):
    room_valid = True

    # quick maths to ensure rooms are inside boundaries
    # defining room_w and room_h helps keep things under control
    # they go inside the loop because I want diff numbers every iteration

    room_width = random.randint(4,6)
    room_height = random.randint(4,6)
    x1 = random.randint(1, MAP_WIDTH - room_width - 1)
    y1 = random.randint(1, MAP_HEIGHT - room_height - 1)
    x2 = x1 + room_width
    y2 = y1 + room_height

    r = Room(x1, y1, x2, y2)
    for other in rooms:
        if r.intersects(other):
            room_valid = False
            break
    if room_valid:
        carve_room(floor_map, r.x1, r.y1, r.x2, r.y2)

        # connecting the room to the previous one
        if rooms:
            new_room_center_x, new_room_center_y = r.center()
            old_room_center_x, old_room_center_y = rooms[-1].center()
            carve_h_corridor(floor_map, new_room_center_x, old_room_center_x, old_room_center_y)
            carve_v_corridor(floor_map, new_room_center_y, old_room_center_y, new_room_center_x)
        rooms.append(r)


# add entities

first_room_center_x, first_room_center_y = rooms[0].center()

player = Entity(first_room_center_x, first_room_center_y, 10, PLAYER_SPRITE)
entities = [player]

for room in rooms[1:]:
    x, y = room.center()
    entities.append(Entity(x, y, 2, MONSTER_SPRITE))


# === GAME LOOP === #

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
