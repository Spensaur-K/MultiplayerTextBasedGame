from engine import Engine, ActionComponent, Container, Entity



class Player(Entity):
    def __init__(self):
        pass

class Speech:
    pass

def Room(Container):
    def resolve_target(self, from_entity, action, target, options):
        pass

def create_game():
    game = Engine(Player)
    game.run()

if __name__ == "__main__":
    create_game()