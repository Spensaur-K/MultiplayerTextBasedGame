#!/usr/bin/python3
"""
Higher level game logic
"""

from engine import Engine, ActionComponent, Container, Entity
from util import log

class Player(Entity):
    def __init__(self):
        super().__init__()

class Speech:
    pass

def Room(Container):
    """Room that players can be in
    - facilitates speech between players
    - players can only be in one room at a time
    """
    def resolve_target(self, from_entity, command):
        pass

def create_game():
    game = Engine(Player)
    game.run()

if __name__ == "__main__":
    create_game()
