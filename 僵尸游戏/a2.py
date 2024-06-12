"""
End of Dayz
Assignment 2
Semester 1, 2021
CSSE1001/CSSE7030

A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List

from a2_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"


class Entity:
    def step(self, position: "Position", game: "Game") -> None:
        raise NotImplementedError

    def display(self) -> str:
        raise NotImplementedError
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
        
        
class Player(Entity):
    def display(self):
        return "P"
    

class Hospital(Entity):
    def display(self):
        return "H"
class Grid:
    def __init__(self, size):
        self.size = size
        self.dict = {}

    def get_size(self) -> int:
        return self.size

    def in_bounds(self, position:Position) -> bool:
        x = position.get_x()
        y = position.get_y()
        return  self.size > x >= 0 and self.size > y >= 0
    def add_entity(self, position, entity):
        self.dict[position] = entity

    def remove_entity(self, position: Position) -> None:
        self.dict.pop(position)

    def get_entity(self, position: Position) -> Optional[Entity]:
        return self.dict.get(position)

    def get_mapping(self) -> Dict[Position, Entity]:
        return self.dict

    def get_zombies(self):
        z_dict = {}
        for x,y in self.dict.items():
            if y.display() == "Z" or y.display() == "T":
                z_dict[x] = y
        return z_dict
    def get_entities(self) -> List[Entity]:
        return self.dict.values()

    def move_entity(self, start: Position, end: Position) -> None:
        self.add_entity(end, self.get_entity(start))
        self.remove_entity(start)
    
    

    def find_player(self) -> Optional[Position]:
        entities = list(self.dict.items())
        for position, entity in entities:
            if entity.display() == "P":
                return position
        return None
    def serialize(self) -> Dict[Tuple[int, int], str]:
        serialized_dict = {}
        entities = list(self.dict.items())
        for position, entity in entities:
            serialized_dict[(position.get_x(),position.get_y())] = entity.display()
        return serialized_dict

class MapLoader:
    def load(self, filename: str) -> Grid:
        map_info = load_map(filename)
        grid = Grid(map_info[1])
        Dict = map_info[0]
        for x, y in Dict.items():
            token = self.create_entity(y)
            position = Position(x[0],x[1])
            grid.add_entity(position, token)
        return grid

    def create_entity(self, token: str) -> Entity:
        raise NotImplementedError

class BasicMapLoader(MapLoader):
    def create_entity(self, token: str) -> Entity:
        if token == "P":
            return Player()
        elif token == "H":
            return Hospital()
        else:
            raise ValueError

class Game:
    def __init__(self,grid):
        self.grid = grid
        self.steps = 0
        self.hos = []
        for x, y in self.grid.get_mapping().items():
            if isinstance(y, Hospital):
                self.hos.append(x)
    def get_grid(self) -> Grid:
        return self.grid

    def get_player(self) -> Optional[Player]:
        pos = self.grid.find_player()
        return self.grid.get_entity(pos)

    def step(self):
        Dict = self.grid.get_mapping().items()
        for x, y in list(Dict):
            try:
                y.step(x,self)
            except Exception:
                pass
        self.steps += 1

    def get_steps(self):
        return self.steps

    def move_player(self, offset):
        start = self.grid.find_player()
        if start != None:
            end = start.add(offset)
            if self.grid.in_bounds(end):
                if isinstance(self.grid.get_entity(end),Zombie):
                    self.get_player().infect()
                else:
                    self.grid.move_entity(start,end)

    def move_zombie(self,position,offset):
        end = position.add(offset)
        player_pos = self.grid.find_player()
        player = self.grid.get_entity(player_pos)
        if end == player_pos:
            print("ss")
            player.infect()
            return 2
        elif isinstance(self.grid.get_entity(end),Hospital):
            return 3
        elif isinstance(self.grid.get_entity(end),Zombie):
            return 3
        elif self.grid.in_bounds(end):
            self.grid.move_entity(position,end)
            return 1
        else:
            return 0
        
    def direction_to_offset(self, direction: str):
        Dict = {"W":Position(0, -1),"S":Position(0, 1), "A":Position(-1, 0), "D":Position(1,0)}
        return Dict.get(direction)

    def has_won(self):
        player_pos = self.grid.find_player()
        if player_pos == None:
            return False
        for z in self.hos:
            if z.get_x() == player_pos.get_x() and z.get_y() == player_pos.get_y():
                return True
        return False

    def has_lost(self):
        return False

class TextInterface:
    def __init__(self,size):
        self.size = size

    def draw(self, game: Game) -> None:
        grid = game.get_grid()
        top_botton = BORDER * (self.size + 2)
        middle = BORDER + " " * self.size + BORDER
        
        final_list = []
        for x in range(self.size):
            final_list.append(list(middle))
        Dict = grid.serialize()
        for x,y in Dict.items():
            final_list[x[1]][x[0]+1] = y
        print(top_botton)
        for x in range(self.size):
            print("".join(final_list[x]))
        print(top_botton)
        
    def play(self, game: Game) -> None:
        self.draw(game)
        while(game.has_won() != True and game.has_lost() != True):
            action = input("Enter your action:")
            
            self.handle_action(game, action)
        if game.has_won() == True:
            print("You won!!!")
        else:
            print("You lost!!!")
            
    def handle_action(self, game: Game, action: str) -> None:
        offset = game.direction_to_offset(action)
        if offset != None:
            game.move_player(offset)
        game.step()
        self.draw(game)

class VulnerablePlayer(Player):
    def __init__(self):
        self.state = False

    def infect(self):
        self.state = True

    def is_infected(self):
        print(self.state)
        return self.state

class Zombie(Entity):
    def step(self,position,game):
        direction_list = random_directions()
        for z,(x,y) in enumerate(direction_list):
            a = Position(0,0)
            a._x = x
            a._y = y
            direction_list[z] = a
        for x in direction_list:
            a = game.move_zombie(position, x)
            if a != 0:
                break

    def display(self):
        return "Z"

class IntermediateGame(Game):
    def has_lost(self):
        return self.get_player().is_infected()

class IntermediateMapLoader(BasicMapLoader):
    def create_entity(self, token: str) -> Entity:
        if token == "P":
            return VulnerablePlayer()
        elif token == "H":
            return Hospital()
        elif token == "Z":
            return Zombie()
        elif token == "T":
            return TrackingZombie()
        else:
            raise ValueError
    
class TrackingZombie(Zombie):
    def step(self,position,game):
        direction_list = random_directions()
        for z,(x,y) in enumerate(direction_list):
            a = Position(0,0)
            a._x = x
            a._y = y
            direction_list[z] = a
        player = game.get_grid().find_player()
        
        direction_list.sort(key = lambda x:x.add(position).distance(player))
        

        for x in direction_list:
            a = game.move_zombie(position, x)
            if a != 0:
                break
    def display(self):
        return 'T'
        

class Pickup(Entity):
    def __init__(self):
        self.lifetime = self.get_durability()

    def get_durability(self):
        raise NotImplementedError

    def get_lifetime(self):
        return self.lifetime

    def hold(self):
        self.lifetime -= 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.lifetime}"

class Garlic(Pickup):
    def get_durability(self):
        return 11

    def display(self):
        return "G"
    
        
class Crossbow(Pickup):
    def get_durability(self):
        return 6

    def display(self):
        return "C"

class Inventory():
    def __init__(self):
        self.inventory = []

    def step(self):
        for x in self.inventory:
            x.hold()
            if x.get_lifetime() == 0:
                self.inventory.remove(x)
    def add_item(self, item):
        self.inventory.append(item)

    def get_item(self):
        return self.inventory

    def contains(self,pickup_id):
        for x in self.inventory:
            if x.display() == pickup_id:
                return True
        return False

class HoldingPlayer(VulnerablePlayer):
    def __init__(self):
        self.state = False
        self.inventory = Inventory()

    def get_inventory(self):
        return self.inventory

    def infect(self):
        if self.inventory.contain("G") == False:
            self.state = True

    def step(self, position: Position, game: Game):
        self.inventory.step()

class AdvancedGame(IntermediateGame):
    def move_player(self, offset):
        start = self.grid.find_player()
        if start != None:
            end = start.add(offset)
            end_entity = self.grid.get_entity(end)
            if self.grid.in_bounds(end):
                if isinstance(end_entity,Zombie):
                    self.get_player().infect()
                elif isinstance(self.grid.get_entity(end),Pickup):
                    self.get_player().get_inventory().add_item(end_entity)
                    self.grid.move_entity(start,end)
                    
                    
                else:
                    self.grid.move_entity(start,end)
class AdvancedMapLoader(IntermediateMapLoader):
    def create_entity(self, token: str) -> Entity:
        if token == "P":
            return HoldingPlayer()
        elif token == "H":
            return Hospital()
        elif token == "Z":
            return Zombie()
        elif token == "T":
            return TrackingZombie()
        elif token == "G":
            return Garlic()
        elif token == "C":
            return Crossbow()
        else:
            raise ValueError

class AdvancedTextInterface(TextInterface):
    def draw(self, game: Game) -> None:
        grid = game.get_grid()
        top_botton = BORDER * (self.size + 2)
        middle = BORDER + " " * self.size + BORDER
        
        final_list = []
        for x in range(self.size):
            final_list.append(list(middle))
        Dict = grid.serialize()
        for x,y in Dict.items():
            final_list[x[1]][x[0]] = y
        print(top_botton)
        for x in range(self.size):
            print("".join(final_list[x]))
        print(top_botton)
       
        player = game.get_player()
        position = grid.find_player()
        inv = player.get_inventory()
        print(inv.get_item())

    def handle_action(self, game: Game, action: str) -> None:
        offset = game.direction_to_offset(action)
        fire = 1
        grid = game.get_grid()
        player_pos = grid.find_player()
        z_dict = grid.get_zombies()
        if offset != None:
            game.move_player(offset)
        player = game.get_player()
        inv = player.get_inventory()
        if action == "F":
            if inv.contains("C"):
                direction = input("which direction to fire:")
                if direction == "A":
                    zombie = None
                    pos = None
                    left = player_pos.get_x()
                    for x in z_dict.keys():
                        if x.get_x() < left:
                            if pos == None:
                                pos = x
                            else:
                                if pos.get_x() < x.get_x():
                                    pos = x
                    if pos != None:
                        grid.remove_entity(pos)
            else:
                fire = 0
            
            
        game.step()
        self.draw(game)
        if fire == 0:
            print("nothing to fire")
    
        
        
    
def main():
    grid = AdvancedMapLoader().load("basic4.txt")
    game = AdvancedGame(grid)
    AdvancedTextInterface(grid.get_size()).play(game)
    
    #print(grid.get_mapping())   
if __name__ == "__main__":
    main()
