from code.Entity import Entity


class Platform(Entity):
    def __init__(self, name: str, position: tuple, state: int):
        super().__init__(name, position)
        self.state = state

    def move(self):
        pass