from constants import *

class Entity:
    def __init__(self, x, y, hp, sprite):
        self.x = x
        self.y = y
        self.hp = hp
        self.sprite = sprite
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))

def get_blocking_entity(x, y, entities):
    for entity in entities:
        if entity.x == x and entity.y == y:
            return entity
    return None
