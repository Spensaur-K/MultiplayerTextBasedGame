#!/usr/bin/python3
"""
Higher level game logic
"""

from engine import Engine, ActionComponent, Container, Entity
from util import log

class Player(Entity):
    def __init__(self):
        super().__init__()

class Speech(ActionComponent):
    "Allows players to talk to eachother"
    def execute_action(self, recurse, client, command):
        if command.action == "say":
            pass

class Door(ActionComponent):
    "Allows players to travel between rooms"
    pass

class Room(Container):
    """Room that players can be in
    - facilitates interactions between players
    - players can only be in one room at a time
    """
    def __init__(self):
        self.entities = set()

    def resolve_target(self, from_entity, command):
        if command.target == "room":
            return self.entities

    def add_entity(self, entity):
        self.entities.add(entity)
        

def create_game():
    game = Engine(Player, Room())
    game.run()

if __name__ == "__main__":
    create_game()
