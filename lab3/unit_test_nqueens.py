#!/usr/bin/env python

"""
This is a unit test for the NQueens problem. The class tests two of the functions.

DISCLAIMER: YOU WILL NEED THE ANYTREE PYTHON PACKAGE
To install the package run:
pip3 install anytree
"""

from BoardAgent import BoardAgent
import unittest
from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph

__author__ = "Jonathan Trinh"
__version__ = "10252018"
__credits = ["Jonathan Trinh, Andreas Adolfsson, Ying Liu"]


class TestNQueens(unittest.TestCase):

  def test_five(self):
    """Uses the unit test to check if certain board configurations of 5 queens are safe as well as
    It also calls on an instantiation of BoardAgent() and populates the object's instance
    variable (in this case called "solution") with the appropriate solutions
    """

    # N = 5 Case
    five_queen_board = BoardAgent()
    five_queen_board.populate_solutions(five_queen_board.generate_tree(5))

    self.assertTrue(five_queen_board.boardIsSafe((0, 2, 4, 1, 3)))
    self.assertTrue(five_queen_board.boardIsSafe((0, 3, 1, 4, 2)))

    self.assertFalse(five_queen_board.boardIsSafe((0, 2, 4, 2, 5))) # Out of bounds
    self.assertFalse(five_queen_board.boardIsSafe((0, 2, 4, 2, -1))) # Board is not completely filled
    self.assertFalse(five_queen_board.boardIsSafe((0, 2, 4, 2, 3))) # In the same row

    self.assertEqual(five_queen_board.solution,[(0, 2, 4, 1, 3), (0, 3, 1, 4, 2), (1, 3, 0, 2, 4), (1, 4, 2, 0, 3), (2, 0, 3, 1, 4), (2, 4, 1, 3, 0), (3, 0, 2, 4, 1), (3, 1, 4, 2, 0), (4, 1, 3, 0, 2), (4, 2, 0, 3, 1)])
    self.assertTrue((2,0,3,1,4) in five_queen_board.solution)
    self.assertEqual(len(five_queen_board.solution),10)
    print('\nN = 5: ')
    print(five_queen_board.solution)

  def test_eight(self):
    """Uses the unit test to check if certain board configurations of 8 queens are safe as well as
    It also calls on an instantiation of BoardAgent() and populates the object's instance
    variable (in this case called "solution") with the appropriate solutions
    """

    # N = 8 Case
    eight_queen_board = BoardAgent()
    eight_queen_board.populate_solutions(eight_queen_board.generate_tree(8))

    self.assertTrue(eight_queen_board.boardIsSafe((0, 4, 7, 5, 2, 6, 1, 3)))
    self.assertTrue(eight_queen_board.boardIsSafe((0, 5, 7, 2, 6, 3, 1, 4)))

    self.assertFalse(eight_queen_board.boardIsSafe((0, 5, 7, 2, 6, 3, 10, 4))) # Out of bounds
    self.assertFalse(eight_queen_board.boardIsSafe((0, 5, 7, 2, 6, -1, 1, 4))) # Board is not completely filled
    self.assertFalse(eight_queen_board.boardIsSafe((0, 5, 7, 2, 6, 3, 1, 0))) # In the same row

    self.assertTrue((7, 3, 0, 2, 5, 1, 6, 4) in eight_queen_board.solution)
    self.assertEqual(len(eight_queen_board.solution),92)
    print('\nN = 8: ')
    print(eight_queen_board.solution)

if __name__ == '__main__':
   unittest.main()
