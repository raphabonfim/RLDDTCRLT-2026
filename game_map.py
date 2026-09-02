import random 
from constants import *

class Tile:
    def __init__(self, color, color_dim, walkable, transparent):
        self.color = color
        self.color_dim = color_dim
        self.walkable = walkable
        self.visible = False
        self.explored = False

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

############################
# === HELPER FUNCTIONS === # 
############################

def is_walkable(x, y, floor_map):
    if x < 0 or x >= MAP_WIDTH:
        return False
    if y < 0 or y >= MAP_HEIGHT:
        return False
    return floor_map[x][y].walkable

def carve_room(floor_map, x1, y1, x2, y2): # the +1 makes the room inclusive that means that we INCLUDE the coordinate in the room
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            floor_map[x][y] = Tile(DARK_GRAY, DARK_GRAY_DIM, True, True) # transform stone into floor tiles

def carve_h_corridor(floor_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        floor_map[x][y] = Tile(DARK_GRAY, DARK_GRAY_DIM, True, True) # transform stone into floor tiles
 

def carve_v_corridor(floor_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        floor_map[x][y] = Tile(DARK_GRAY, DARK_GRAY_DIM, True, True) # transform stone into floor tiles

 
def generate_dungeon(max_rooms,room_min_size, room_max_size):
    # this fills the map with stone walls
    floor_map = [[Tile(LIGHT_GRAY, LIGHT_GRAY_DIM, False, False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    rooms = []

    for _ in range(max_rooms):
        room_valid = True

        # quick maths to ensure rooms are inside boundaries
        # defining room_w and room_h helps keep things under control
        # they go inside the loop because I want diff numbers every iteration

        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
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
        
    return floor_map, rooms
