#!/usr/bin/python3
"""
Higher level game logic
"""

from engine import Engine, ActionComponent, Container, Entity, log

class Player(Entity):
    def __init__(self):
        pass

class Speech:
    pass

def Room(Container):
    def resolve_target(self, from_entity, command):
        pass

def create_game():
    game = Engine(Player)
    game.run()

if __name__ == "__main__":
    create_game()
