from code.Platform import Platform
from code.Player import Player
from code.Portal import Portal


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=None, next_level=None):
        match entity_name:
            # level 1
            case 'Level1Plat':
                return [
                    Platform('Level1Plat0', (0, 0), -1),  # always spawn
                    Platform('Level1Plat1', (0, 0), 0),  # world state 0
                    Platform('Level1Plat2', (0, 0), 1)  # world state 1
                ]
            # level 2
            case 'Level2Plat':
                return [
                    Platform('Level2Plat0', (0, 0), -1),  # always spawn
                    Platform('Level2Plat1', (0, 0), 0),  # world state 0
                    Platform('Level2Plat2', (0, 0), 1)  # world state 1
                ]

            case 'Player':
                return Player('Player', position)

            case 'Portal':
                return Portal('Portal', position, next_level)
