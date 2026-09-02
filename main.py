import pygame
import sys

from constants import *
from entities import Entity, get_blocking_entity
from game_map import Tile, Room, is_walkable, carve_room, carve_h_corridor, carve_v_corridor, generate_dungeon

# === Standard Game Loop Structure in 5 steps: === #

# 1. Initialize and set up the window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("r/roguelikedev does the tutorial 2026")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20) # None = Default font


PLAYER_SPRITE = pygame.image.load("./assets/player.png").convert_alpha()
MONSTER_SPRITE = pygame.image.load("./assets/monster.png").convert_alpha()

floor_map, rooms = generate_dungeon(50, 4, 6)

#TEMPORARY: JUST FOR TESTING FOV

for x in range(MAP_WIDTH):
    for y in range(MAP_HEIGHT):
        floor_map[x][y].visible = False
        floor_map[x][y].explored = True

messages = []

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
                        messages.append(f"You kick the monster. It makes a funny face.")
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
                    messages.append(f"The monster bites you! Ouch!")
                    if player.hp <= 0:
                        messages.append("Game over!")
                        running = False
                    break

                if is_walkable(dest_x, dest_y, floor_map) and get_blocking_entity(dest_x, dest_y, entities) is None:
                    entity.x += cdx
                    entity.y += cdy
                    break
        del messages[:-50] # deleting older messages from index 0 up to the 50th item from the end

    # 3. Clear/Fill BG so the sprites won't leave trails
    screen.fill(BLACK)

    # 4. Draw your objects here (blit sprites, draw shapes, render fonts)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            tile = floor_map[x][y]
            if tile.visible:
                color = tile.color
            elif tile.explored:
                color = tile.color_dim
            else:
                continue
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    
    for entity in entities:
        entity.draw(screen)
    
    text_surf = font.render(f"HP: {player.hp}", True, WHITE) # True turns on antialiasing
    screen.blit(text_surf, (1 * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))

    for index, message in enumerate(messages[-3:]):
        message_surf = font.render(message, True, WHITE)
        screen.blit(message_surf, (1 * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + TEXT_HEIGHT + index * TEXT_HEIGHT))


    # 5. Update the display so the player can see the new frame
    pygame.display.flip()

    # 6. Tick the clock so the game runs at the capped FPS
    clock.tick(FPS)
    
pygame.quit()
sys.exit()
