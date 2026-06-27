from code.Entity import Entity


class Portal(Entity):
    def __init__(self, name: str, position: tuple, next_level: str):
        super().__init__(name,position)
        self.next_level = next_level