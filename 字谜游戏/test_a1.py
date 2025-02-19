#!/usr/bin/env python3

"""
Full test suite for CSSE1001 / 7030 Assignment 1 marking
"""

__author__ = "Richard Thomas, Brae Webb and Mike Pham"

import inspect
import random
from pathlib import Path
from typing import Tuple

from testrunner import AttributeGuesser, OrderedTestCase, RedirectStdIO, \
                       TestMaster, skipIfFailed

SEED = 1001.2021


class A1:
    """ Just used for type hints """

    @staticmethod
    def shuffle_puzzle(solution: str) -> str:
        pass

    @staticmethod
    def print_grid(puzzle: str) -> None:
        pass

    @staticmethod
    def swap_position(puzzle: str, from_index: int, to_index: int) -> str:
        pass

    @staticmethod
    def move(puzzle: str, direction: str) -> str:
        pass

    @staticmethod
    def check_win(puzzle: str, solution: str) -> bool:
        pass

    @staticmethod
    def main() -> None:
        pass


class TestA1(OrderedTestCase):
    """ Base for all a1 test cases """

    a1: A1
    a1_support: ...


class TestDesign(TestA1):
    """ Checks A1 design compliance """

    def test_clean_import(self):
        """ test no prints on import """
        self.assertIsCleanImport(self.a1,
                                 msg="You should not be printing on import for a1.py")

    def test_functions_defined(self):
        """ test all functions are defined correctly """
        a1 = AttributeGuesser.get_wrapped_object(self.a1)
        for func_name, func in inspect.getmembers(A1,
                                                  predicate=inspect.isfunction):
            num_params = len(inspect.signature(func).parameters)
            self.aggregate(self.assertFunctionDefined, a1, func_name,
                           num_params, tag=func_name)

        self.aggregate_tests()

    def test_doc_strings(self):
        """ test all functions have documentation strings """
        a1 = AttributeGuesser.get_wrapped_object(self.a1)
        for attr_name, _ in inspect.getmembers(a1,
                                               predicate=inspect.isfunction):
            self.aggregate(self.assertDocString, a1, attr_name)

        self.aggregate_tests()


class TestFunctionality(TestA1):
    """ Base for all A1 functionality tests """

    TEST_DATA = (Path(__file__).parent / 'test_data').resolve()

    @staticmethod
    def set_seed(seed=SEED, skip_numbers=0):
        """ helper method for settings random seed """
        random.seed(seed)
        for _ in range(skip_numbers):
            random.random()  # skip next random number

    def load_test_data(self, filename: str):
        """ load test data from file """
        with open(self.TEST_DATA / filename, encoding='utf8') as file:
            return file.read()

    def write_test_data(self, filename: str, output: str):
        """ write test data to file """
        with open(self.TEST_DATA / filename, 'w', encoding='utf8') as file:
            file.write(output)


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.swap_position.__name__)
class TestSwapPosition(TestFunctionality):
    """ Tests swap_position """

    def test_simple_swap(self):
        """ test swapping characters in middle of string """
        result = self.a1.swap_position('ABCDEF', 2, 4)
        self.assertEqual(result, 'ABEDCF')

    def test_swap_adjacent_chars(self):
        """ test swapping characters adjacent to each other """
        result = self.a1.swap_position('ABCDEF', 2, 3)
        self.assertEqual(result, 'ABDCEF')

    def test_swap_first_last_chars(self):
        """ test swapping first & last characters """
        result = self.a1.swap_position('ABCDEF', 0, 5)
        self.assertEqual(result, 'FBCDEA')

    def test_swap_same_char(self):
        """ test swapping the same characters at different indexes """
        result = self.a1.swap_position('ABCAD', 0, 3)
        self.assertEqual(result, 'ABCAD')

    def test_swap_same_index(self):
        """ test swapping characters at the same index """
        result = self.a1.swap_position('ABCDEF', 3, 3)
        self.assertEqual(result, 'ABCDEF')


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.swap_position.__name__)
class TestSwapPositionExtra(TestFunctionality):
    """ Tests swap_position """

    def test_swap_indices_descending_order(self):
        """ test swapping characters where index1 > index2 """
        result = self.a1.swap_position('ABCDEF', 4, 2)
        self.assertEqual(result, 'ABEDCF')

    def test_swap_two_char_string(self):
        """ test swapping characters in string with only two characters """
        result = self.a1.swap_position('AB', 0, 1)
        self.assertEqual(result, 'BA')

    def test_simple_lower(self):
        """ test swapping characters in lowercase """
        result = self.a1.swap_position('abcdefghi', 2, 6)
        self.assertEqual(result, 'abgdefchi')


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.check_win.__name__)
class TestCheckWin(TestFunctionality):
    """ Tests check_win """

    def test_simple_win_condition_true(self):
        """ test 3x3 puzzle grid string matches solution """
        result = self.a1.check_win('ABCDEFGH ', 'ABCDEFGHI')
        self.assertTrue(result)

    def test_simple_win_condition_false(self):
        """ test 3x3 puzzle grid string doesn't match solution """
        result = self.a1.check_win('ACBDEFGH ', 'ABCDEFGHI')
        self.assertFalse(result)

    def test_single_char_string(self):
        """ test edge case of a single character string """
        result = self.a1.check_win(' ', 'A')
        self.assertTrue(result)

    def test_unfinished_game(self):
        """ test unfinished game """
        result = self.a1.check_win('CBA GHDFE', 'ABCDEFGHI')
        self.assertFalse(result)

    def test_nearly_won_game(self):
        """ test unfinished game with one incorrect cell at the end """
        result = self.a1.check_win('ABCDEFG H', 'ABCDEFGHI')
        self.assertFalse(result)


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.check_win.__name__)
class TestCheckWinExtra(TestFunctionality):
    """ Tests check_win """

    def test_unfinished_game_one_wrong_cell(self):
        """ test unfinished game with one incorrect cell """
        result = self.a1.check_win('ABCD FGHE', 'ABCDEFGHI')
        self.assertFalse(result)

    def test_blank_at_beginning(self):
        """ test unfinished game with blank character at begginning of puzzle """
        result = self.a1.check_win(' BCDEFGHI', 'ABCDEFGHI')
        self.assertFalse(result)
        
    def test_duplicate_character_won(self):
        """ test won game with duplicate character """
        result = self.a1.check_win("ccc ", "cccc")
        self.assertTrue(result)

    def test_duplicate_character_not_won(self):
        """ test unfinished game with duplicate character """
        result = self.a1.check_win(" ccc", "cccc")
        self.assertFalse(result)

    def test_check_win_in(self):
        """ test check_win with trimmed puzzle in solution """
        result = self.a1.check_win("abc ", "dabc")
        self.assertFalse(result)

    def test_check_win_one_cell_wrong(self):
        """ test check_win with one cell in wrong position """
        result = self.a1.check_win("abcd fhie", "abcdefhij")
        self.assertFalse(result)


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.move.__name__)
class TestMove(TestFunctionality):
    """ Test move function """

    def test_move_left_valid_2x2(self):
        """ test moving left for a 2x2 grid """
        result = self.a1.move("abc ", "L")
        self.assertEqual(result, "ab c")

    def test_move_right_valid_2x2(self):
        """ test moving right for a 2x2 grid """
        result = self.a1.move("ab c", "R")
        self.assertEqual(result, "abc ")

    def test_move_up_valid_2x2(self):
        """ test moving up for a 2x2 grid """
        result = self.a1.move("ab c", "U")
        self.assertEqual(result, " bac")

    def test_move_down_valid_2x2(self):
        """ test moving down for a 2x2 grid """
        result = self.a1.move("a cb", "D")
        self.assertEqual(result, "abc ")

    def test_move_left_valid_3x3(self):
        """ test moving left for a 3x3 grid """
        result = self.a1.move("abcdefg i", "L")
        self.assertEqual(result, "abcdef gi")

    def test_move_right_valid_3x3(self):
        """ test moving right for a 3x3 grid """
        result = self.a1.move("abcd fghi", "R")
        self.assertEqual(result, "abcdf ghi")

    def test_move_up_valid_3x3(self):
        """ test moving up for a 3x3 grid """
        result = self.a1.move("abcde ghi", "U")
        self.assertEqual(result, "ab decghi")

    def test_move_down_valid_3x3(self):
        """ test moving down for a 3x3 grid """
        result = self.a1.move("a cdefghi", "D")
        self.assertEqual(result, "aecd fghi")

    def test_move_up_top_left(self):
        """ test invalid move up at top left corner """
        self.assertIsNone(self.a1.move(" bcdefghi", "U"))

    def test_move_left_top_left(self):
        """ test invalid move left at top left corner """
        self.assertIsNone(self.a1.move(" bcdefghi", "L"))

    def test_move_left_bottom_left(self):
        """ test invalid move left at bottom left corner """
        self.assertIsNone(self.a1.move("abcdef hi", "L"))

    def test_move_right_top_right(self):
        """ test invalid move right at top right corner """
        self.assertIsNone(self.a1.move("ab defghi", "R"))


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.move.__name__)
class TestMoveExtra(TestFunctionality):
    """ Test move function """

    def test_move_left_valid_4x4(self):
        """ test moving left for a 4x4 grid """
        result = self.a1.move("abcdefg ijklmnop", "L")
        self.assertEqual(result, "abcdef gijklmnop")

    def test_move_right_valid_4x4(self):
        """ test moving right for a 4x4 grid """
        result = self.a1.move("abcdefghi klmnop", "R")
        self.assertEqual(result, "abcdefghik lmnop")

    def test_move_up_valid_4x4(self):
        """ test moving up for a 4x4 grid """
        result = self.a1.move("abcde ghijklmnop", "U")
        self.assertEqual(result, "a cdebghijklmnop")

    def test_move_down_valid_4x4(self):
        """ test moving down for a 4x4 grid """
        result = self.a1.move("abcdefghijk mnop", "D")
        self.assertEqual(result, "abcdefghijkpmno ")

    def test_move_left_valid_14x14(self):
        """ test moving left for a 14x14 grid """
        grid_input = self.load_test_data("move_left_big_grid.in")
        grid_output = self.load_test_data("move_left_big_grid.out")
        self.assertEqual(grid_output, self.a1.move(grid_input, "L"))

    def test_move_right_valid_14x14(self):
        """ test moving right for a 14x14 grid """
        grid_input = self.load_test_data("move_right_big_grid.in")
        grid_output = self.load_test_data("move_right_big_grid.out")
        self.assertEqual(grid_output, self.a1.move(grid_input, "R"))

    def test_move_up_valid_14x14(self):
        """ test moving up for a 14x14 grid """
        grid_input = self.load_test_data("move_up_big_grid.in")
        grid_output = self.load_test_data("move_up_big_grid.out")
        self.assertEqual(grid_output, self.a1.move(grid_input, "U"))

    def test_move_down_valid_14x14(self):
        """ test moving down for a 14x14 grid """
        grid_input = self.load_test_data("move_down_big_grid.in")
        grid_output = self.load_test_data("move_down_big_grid.out")
        self.assertEqual(grid_output, self.a1.move(grid_input, "D"))

    def test_move_down_bottom_left(self):
        """ test invalid move down at bottom left corner """
        self.assertIsNone(self.a1.move("abcdef hi", "D"))

    def test_move_right_bottom_right(self):
        """ test invalid move right at bottom right corner """
        self.assertIsNone(self.a1.move("abcdefgh ", "R"))

    def test_move_down_bottom_right(self):
        """ test invalid move down at bottom right corner """
        self.assertIsNone(self.a1.move("abcdefgh ", "D"))

    def test_move_up_top_right(self):
        """ test invalid move up at top right corner """
        self.assertIsNone(self.a1.move(" bcdefghi", "U"))

    def test_move_up_duplicate_character(self):
        """ test move up puzzle with duplicate character """
        result = self.a1.move("ccc ", "U")
        self.assertEqual("c cc", result)

    def test_move_down_duplicate_character(self):
        """ test move down with duplicate character """
        result = self.a1.move("c cc", "D")
        self.assertEqual("ccc ", result)

    def test_move_left_duplicate_character(self):
        """ test move left with duplicate character """
        result = self.a1.move("c cc", "L")
        self.assertEqual(" ccc", result)

    def test_move_right_duplicate_character(self):
        """ test move right with duplicate character """
        result = self.a1.move(" ccc", "R")
        self.assertEqual("c cc", result)

    def test_move_down_last_cell(self):
        """ Test moving down to last cell """
        result = self.a1.move("a cb", "D")
        self.assertEqual("abc ", result)

    def test_move_up_first_cell(self):
        """ test moving up to first cell """
        result = self.a1.move("ab c", "U")
        self.assertEqual(" bac", result)



@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.print_grid.__name__)
class TestPrintGrid(TestFunctionality):
    """ Tests print_grid """

    def _test_print_grid(self, to_print, out_file):
        with RedirectStdIO(stdout=True) as stdio:
            result = self.a1.print_grid(to_print)
        actual = stdio.stdout
        expected = self.load_test_data(out_file)
        self.assertEqual(actual, expected)
        self.assertIsNone(result)

    def test_print_puzzle_2x2(self):
        """ test display 2x2 game puzzle """
        self._test_print_grid("ca b", "print_grid_puzzle_2x2.out")

    def test_print_puzzle_3x3(self):
        """ test display 3x3 game puzzle """
        self._test_print_grid("abc efghi", "print_grid_puzzle_3x3.out")

    def test_print_big_grid_solution(self):
        """ test display big grid without blank character """
        big_grid = self.load_test_data("print_big_grid_solution.in")
        self._test_print_grid(big_grid, "print_big_grid_solution.out")

    def test_rick_roll_4x4(self):
        """ test rick rolling example 1 """
        self._test_print_grid("nevagonagiveu up", 'print_grid_rick_roll_1.out')

    def test_rick_roll_5x5(self):
        """ test rick rolling example 2 """
        self._test_print_grid("nevergonnalet udooooowwwn",
                              'print_grid_rick_roll_2.out')


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.print_grid.__name__)
class TestPrintGridExtra(TestFunctionality):
    """ Tests print_grid """

    def _test_print_grid(self, to_print, out_file):
        with RedirectStdIO(stdout=True) as stdio:
            result = self.a1.print_grid(to_print)
        actual = stdio.stdout
        expected = self.load_test_data(out_file)
        self.assertEqual(actual, expected)
        self.assertIsNone(result)

    def test_print_solution_2x2(self):
        """ test display 2x2 game solution """
        self._test_print_grid("abcd", "print_grid_solution_2x2.out")

    def test_print_solution_3x3(self):
        """ test display 3x3 game solution """
        self._test_print_grid("abcdefghi", "print_grid_solution_3x3.out")

    def test_print_big_grid_puzzle(self):
        """ test display big grid with blank character """
        big_grid = self.load_test_data("print_big_grid_puzzle.in")
        self._test_print_grid(big_grid, "print_big_grid_puzzle.out")


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.main.__name__)
class TestMain(TestFunctionality):
    """ Tests main """

    def setUp(self) -> None:
        TestFunctionality.set_seed()

    def _run_main(self, file_in: str, file_out: str, stop_early: bool):
        """ runs the main function and captures output """
        data_in = self.load_test_data(file_in)

        error = None
        result = None
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = data_in
            try:
                result = self.a1.main()
            except EOFError as err:
                error = err

        # self.write_test_data(file_out, stdio.stdinout)
        expected = self.load_test_data(file_out)
        if error is not None and not stop_early:
            last_output = "\n".join(stdio.stdinout.rsplit("\n")[-22:])
            raise AssertionError(
                f'Your program is asking for more input when it should have ended\nEOFError: {error}\n\n{last_output}'
            ).with_traceback(error.__traceback__)

        return expected, result, stdio

    def assertMain(self, file_in: str, file_out: str, stop_early: bool = False):
        """ assert the main function ran correctly """
        expected, result, stdio = self._run_main(file_in, file_out,
                                                 stop_early=stop_early)
        self.assertMultiLineEqual(stdio.stdinout, expected)
        if stdio.stdin != '':
            self.fail(msg="Not all input was read")
        self.assertIsNone(result,
                          msg="main function should not return value that is not None")

    def test_spec(self):
        """ test main example in the assignment sheet """
        self.assertMain('spec_example.in', 'spec_example.out', stop_early=True)

    def test_main_2x2_simple(self):
        """ test simple 2x2 gameplay """
        self.assertMain('test_main_2x2_simple.in', 'test_main_2x2_simple.out',
                        stop_early=True)

    def test_main_give_up(self):
        """ test main give up """
        self.assertMain("test_main_give_up.in", "test_main_give_up.out")

    def test_main_help(self):
        """ test main display help """
        self.assertMain("test_main_help.in", "test_main_help.out")

    def test_main_restart_y(self):
        """ test main restart with 'y' """
        self.assertMain("test_main_restart_1.in", "test_main_restart_1.out")

    def test_main_restart_Y(self):
        """ test main restart with 'Y' """
        self.assertMain("test_main_restart_2.in", "test_main_restart_2.out")


@skipIfFailed(TestDesign, TestDesign.test_functions_defined.__name__,
              tag=A1.main.__name__)
class TestMainExtra(TestFunctionality):
    """ Tests main """

    def setUp(self) -> None:
        TestFunctionality.set_seed(7030.2021)

    def _run_main(self, file_in: str, file_out: str, stop_early: bool):
        """ runs the main function and captures output """
        data_in = self.load_test_data(file_in)

        error = None
        result = None
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.stdin = data_in
            try:
                result = self.a1.main()
            except EOFError as err:
                error = err

        # self.write_test_data(file_out, stdio.stdinout)
        expected = self.load_test_data(file_out)
        if error is not None and not stop_early:
            last_output = "\n".join(stdio.stdinout.rsplit("\n")[-22:])
            raise AssertionError(
                f'Your program is asking for more input when it should have ended\nEOFError: {error}\n\n{last_output}'
            ).with_traceback(error.__traceback__)

        return expected, result, stdio

    def assertMain(self, file_in: str, file_out: str, stop_early: bool = False):
        """ assert the main function ran correctly """
        expected, result, stdio = self._run_main(file_in, file_out,
                                                 stop_early=stop_early)
        self.assertMultiLineEqual(stdio.stdinout, expected)
        if stdio.stdin != '':
            self.fail(msg="Not all input was read")
        self.assertIsNone(result,
                          msg="main function should not return value that is not None")

    def test_main_3x3_simple(self):
        """ test simple 3x3 gameplay """
        self.assertMain('test_main_3x3.in', 'test_main_3x3.out',
                        stop_early=True)

    def test_main_invalid_command(self):
        """ test main invalid command """
        self.assertMain("test_main_invalid_command.in",
                        "test_main_invalid_command.out")

    def test_main_invalid_move(self):
        """ test main invalid move """
        self.assertMain("test_main_invalid_move.in",
                        "test_main_invalid_move.out")

    def test_main_restart_(self):
        """ test main restart with '' """
        self.assertMain("test_main_restart_3.in", "test_main_restart_3.out")

    def test_main_no_restart(self):
        """ test main no restart with any other input """
        self.assertMain("test_main_no_restart.in", "test_main_no_restart.out")

    def test_main_3_games(self):
        """ test running 3 games"""
        self.assertMain("test_main_3_games.in", "test_main_3_games.out")


def main():
    """ run tests """
    test_cases = [
        TestDesign,
        TestSwapPosition,
        TestSwapPositionExtra,
        TestCheckWin,
        TestCheckWinExtra,
        TestMove,
        TestMoveExtra,
        TestPrintGrid,
        TestPrintGridExtra,
        TestMain,
        TestMainExtra
    ]
    master = TestMaster(max_diff=None,
                        suppress_stdout=True,
                        timeout=1,
                        include_no_print=True,
                        scripts=[
                            ('a1', 'a1.py'),
                            ('a1_support', 'a1_support.py')
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()
