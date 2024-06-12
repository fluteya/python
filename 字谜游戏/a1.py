"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
finish date:3/4/2024
"""

from a1_support import *


# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

size = 0

def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.

    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.

    Returns:
        (str): a solvable shuffled game with an empty tile at the
               bottom right corner.

    References:
        - https://en.wikipedia.org/wiki/15_puzzle#Solvability
        - https://www.youtube.com/watch?v=YI1WqYKHi78&ab_channel=Numberphile

    Note: This function uses the swap_position function that you have to
%          implement on your own. Use this function when the swap_position
          function is ready
    """
    shuffled_solution = solution[:-1]

    # Do more shuffling for bigger puzzles.
    swaps = len(solution) * 2
    for _ in range(swaps):
        # Pick two indices in the puzzle randomly.
        index1, index2 = random.sample(range(len(shuffled_solution)), k=2)
        shuffled_solution = swap_position(shuffled_solution, index1, index2)

    return shuffled_solution + EMPTY


def swap_position(puzzle: str, from_index: int, to_index: int) -> str:
    """
    puzzle = list(puzzle)
    from_char = puzzle[from_index]
    puzzle[from_index] = puzzle[to_index]
    puzzle[to_index] = from_char
    puzzle = "".join(puzzle)
    return puzzle
    """
    if any(x not in range (0,len(puzzle)) for x in (from_index, to_index)):
        return None
    if from_index > to_index:
        from_index,to_index = to_index, from_index
    return puzzle[:from_index] + puzzle[to_index] + puzzle[from_index+1:to_index] + puzzle[from_index] + puzzle[to_index+1:]
    
def check_win(puzzle: str, solution: str) -> bool:
    if puzzle[-1] == " " and puzzle[:-1] == solution[:-1]:
        return True
    else:
        return False

def move(puzzle: str, direction: str):
    index = puzzle.index(" ")
    if direction == "U":
        return swap_position(puzzle,index,index - size)
    if direction == "D":
        return swap_postion(puzzle,index, index + size)
    if direction == "R":
        return swap_postioin(puzzle,index, index + 1)
    if direction == "L":
        return swap_position(puzzle,index, index - 1)

def print_grid(puzzle: str):
    global size
    size = int(size)
    row = "+---" * size + "+\n"
    grid = row
    for x in range (size):
        line = ""
        for y in range (size):
            index = size * x + y
            line += "|" + " " + puzzle[index]+ " "
        line += "|\n"
        grid += line + row
    
    return grid

def print_grids(solution, puzzle):
    return "Solution:\n" + print_grid(solution) + "\n" +"Current position\n" + print_grid(puzzle)

def main():
    global size
    print(WELCOME_MESSAGE)
    size = input(BOARD_SIZE_PROMPT)
    while size.isdigit() is not True:
        size = input(BOARD_SIZE_PROMPT)
    size = int(size)
    solution = get_game_solution("words.txt",size)
    puzzle =  shuffle_puzzle(solution)
    print(print_grids(solution, puzzle))
    instruction = input(DIRECTION_PROMPT)
    while instruction != "GU" or check_win(puzzle,solution) != True:
        if instruction == "H":
            print(HELP_MESSAGE + print_grids(solution, puzzle))
            instruction = input(DIRECTION_PROMPT)
        if instruction in ["U","D","R","L"]:
            if move(puzzle,instruction) == None:
                print(INVALID_MOVE_FORMAT.format(instruction))
                print(print_grids(solution, puzzle))
                instruction = input(DIRECTION_PROMPT)
            else:
                puzzle = move(puzzle,instruction)
                print(print_grids(solution, puzzle))
                instruction = input(DIRECTION_PROMPT)
        
    
    print( )
    
    


if __name__ == "__main__":
    main()
