#!/usr/bin/python3
"""
Perform language parsing and game logic
"""

from abc import ABCMeta, abstractmethod
from re import match
from functools import partial
from collections import namedtuple
from util import unique, INPUT, OUTPUT, log, HEDGES

Command = namedtuple("Command", ("action", "target", "options"))

class Engine:
    # Map player ids to their entities
    def __init__(self, PlayerType, RootContainer):
        self.players = dict()
        self.containers = set()
        self.world = World()
        self.rootContainer = RootContainer
        self.PlayerType = PlayerType
        self.containers.add(self.world)

    def run(self):
        "Execute game loop"
        while True:
            id, text = get_id(INPUT.readline())
            #try:
            if id not in self.players:
                self.new_player(id)
            command = parse_command(text)
            self.execute_command(id, command)
            #except:
             #   self.write_client("server", "Invalid command")

    def execute_command(self, id, command):
        "Execute a command for every matched target"
        log("Player(", id, ") executes (", command.action, ") with (", *command.options, ")")
        player = self.players[id]
        for target in self.get_targets(player, command):
            player.invoke(command, partial(self.write_client, id))

    def write_client(self, id, text):
        "Write text for client with id"
        print("{}: {}\n".format(id, text), file=OUTPUT)

    def get_targets(self, player_ent, command):
        "Return valid targets for command"
        return filter(lambda x: x != None,
                unique(map(lambda cont: cont.resolve_target(player_ent, command),
                    self.containers)))

    def new_player(self, id):
        "Create and register a new player"
        self.players[id] = self.PlayerType()
        self.players[id].attach(self.world)
        command = Command(internal("create_player"),
                          "self", ("Person{}".format(id),))
        self.execute_command(id, command)
        self.rootContainer.add_entity(self.players[id])


def parse_command(command):
    "Return the action, target and options parts of the command"
    action, target, * \
        options = filter(lambda c: c not in HEDGES, command.split())
    return Command(action, target, options)


def get_id(command):
    "Extract player id from command"
    result = match("(^.*):\s*(.*)", command)
    return result[1], result[2]


class Entity:
    def __init__(self):
        self.components = []
        self.id = -1

    def invoke(self, command, respond):
        """Pass command to each of entity's components
        respond: function to send client text"""
        for component in self.components:
            component.execute_action(
                lambda command: self.invoke(command, respond),
                respond, command)

    def attach(self, component):
        "Attach a action component to entity"
        self.components.append(component)


class ActionComponent(metaclass=ABCMeta):
    "Part of entity that can execute an action"
    @abstractmethod
    def execute_action(self, recurse, client, command):
        """
        new_command(command): create a new command and issue it to all components
        client(text): send text to client
        action: to perform (text)
        target: entity perform action on
        options: additional options for action (text tuple)
        """
        pass


class Container(metaclass=ABCMeta):
    """Enables actions between entities by resolving targets
    Keeps track of entities"""
    @abstractmethod
    def resolve_target(self, from_entity, command):
        """Return entity for target in command
        from_entity: entity that issued command
        command: Command with target in text form"""
        pass

    @abstractmethod
    def add_entity(self, entity):
        """Add entity to container"""
        pass


def internal(cmd):
    "Format text to be internal"
    return "!${}$!".format(cmd)


class World(ActionComponent, Container):
    "Mapping of player names to their entities"
    def __init__(self):
        self.players = dict()

    def execute_action(self, recurse, client, command):
        "Handle global player creation and naming"
        action, target, options = command
        if action == internal("create_player"):
            self.players[options[0]] = target
        if action == "name":
            name = self.get_name(target)
            del self.players[name]
            self.players[options[0]] = target

    def get_name(self, entity):
        "Get the global name for an entity"
        for name, other_entity in self.players.items():
            if entity == other_entity:
                return name

    def add_entity(self, entity):
        raise Exception("Entities must be added to world by engine")

    def resolve_target(self, from_entity, command):
        "Match a players name globally"
        if command.target == "self":
            return from_entity
        if command.target in self.players:
            return self.players[command.target]
