#!/usr/bin/python3
"""
Perform language parsing and game logic
"""

from abc import ABCMeta, abstractmethod
from sys import stdin, stdout, stderr
from re import match
from functools import partial

INPUT = stdin
INPUT = open("testsession.game")
OUTPUT = stdout
LOG = stderr
HEDGES = tuple("the at of a on to by for as so from in are over".split())

class Game:
    # Map player ids to their entities
    players = dict()
    containers = set()
    def __init__(self):
        self.world = World()
        self.containers.add(self.world)
    def run(self):
        while True:
            id, command = get_id(INPUT.readline())
            if id not in self.players:
                self.new_player(id)
            try:
                action, target_text, options = parse_command(command)
                self.command(id, action, target_text, options)
            except:
                self.write_client(id, "Invalid command")
    def command(self, id, action, target_text, options):
        player = self.players[id]
        for target in self.get_targets(player, action, target_text, options):
            player.invoke((action, target, options), partial(self.write_client, id))
    def write_client(self, id, text):
        OUTPUT.write("{}: {}".format(id, text))
    def get_targets(self, player_ent, action, target_text, options):
        return filter(lambda x: x != None,
                map(lambda cont: cont.resolve_target(player_ent, action, target_text, options),
                    self.containers))
    def new_player(self, id):
        self.players[id] = Entity()
        self.players[id].attach(self.world)
        self.command(id, internal("create_player"), "self", "Person{}".format(id))
        
    

def parse_command(command):
    "Return the action, target and options parts of the command"
    action, target, *options = filter(lambda c: c not in HEDGES, command.split())
    return action, target, options

def get_id(command):
    "Extract player id from command"
    result = match("(^.*):\s*(.*)", command)
    return result[1], result[2]

def test():
    id, command = get_id("hello: full command here")
    assert id == "hello"
    assert command == "full command here"


class Entity:
    components = []
    def invoke(self, command_parts, respond):
        for component in self.components:
            component.execute_action(
                lambda action, target, options: self.invoke((action, target, options), respond),
                respond, *command_parts)
    def attach(self, component):
        self.components.append(component)

class ActionComponent(metaclass=ABCMeta):
    "Part of entity that can execute an action"
    @abstractmethod
    def execute_action(self, new_command, client, action, target, options):
        """
        new_command(action, target, options): create a new command and issue it to all components
        client(text): send text to client
        action: to perform
        target: to perform action on
        options: additional options for action
        """
        pass

class Container(metaclass=ABCMeta):
    """Enables actions between entities by resolving targets
    Keeps track of entities"""
    @abstractmethod
    def resolve_target(self, from_entity, action, target, options):
        pass

def internal(cmd):
    return "!${}$!".format(cmd)

class World(ActionComponent, Container):
    "Mapping of player names to their entities"
    players = dict()
    def execute_action(self, new_command, client, action, target, options):
        if action == internal("create_player"):
            print(":::New player created", file=LOG)
            self.players[options[0]] = target

    def resolve_target(self, from_entity, action, target, options):
        if target == "self":
            return from_entity
        if target in self.players:
            return self.players[target]

if __name__ == "__main__":
    game = Game()
    game.run()