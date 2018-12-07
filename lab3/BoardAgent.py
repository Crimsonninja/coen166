#!/usr/bin/env python

"""
This file defines the BoardAgent class which can generate tree of valid board (representation is
a tuple) combinations, check if a board is safe, and generate solutions for the N Queens problem (
given a tree)

DISCLAIMER: YOU WILL NEED THE ANYTREE PYTHON PACKAGE
To install the package run:
pip3 install anytree

If you'd like to visualize the graph, you will need GraphViz, To install GraphViz, execute (you will need brew):
brew install graphviz
"""

from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph

__author__ = "Jonathan Trinh"
__version__ = "10242018"
__credits = ["Jonathan Trinh, Andreas Adolfsson, Ying Liu"]

class BoardAgent:

  def __init__(self):
    self.solution = []  # instance variable

  def isSafe(self, some_tuple, index):
    """ Checks the current position and every position behind it to see if there is a collision

    Four cases are required for safety:
    1. For each column, the value cannot be or exceed N
    2. If the board is filled, there are no -1's
    3. If there is ever a value that repeats itself, then it is in the same row (not wanted)
    4. We check diagonally upward to the left and diagonally left to the left
    If these four conditions pass, then return True, else False.

    Parameters
    ----------
    some_tuple : tuple of integer
    index : int
      the position at which the function will check collisions

    Returns
    -------
    bool
      an indication as to whether the current and previous positions are "safe" or not
    """

    queen_position = some_tuple[index]

    for i in range(0,index):
      if some_tuple[i] >= len(some_tuple):  # Out of bounds
        return False

      if some_tuple[i] == -1: # check for -1's
        return False

      if some_tuple[i] == queen_position: # row check
        return False

      if (some_tuple[i] + (index - i) == some_tuple[index]) or (some_tuple[i] - (index - i) == some_tuple[index]):  # diagonal check
        return False

    return True

  def boardIsSafe(self, some_tuple):
    """ Checks if the entire board is safe

    This function calls on the isSafe method on the last position of the board (the tuple)

    Parameters
    ----------
    some_tuple : tuple of integer

    Returns
    -------
    bool
      an indication as to whether the entire board/tuple is "safe" or not
    """
    tuple_length = len(some_tuple)
    return self.isSafe(some_tuple, len(some_tuple)-1)

  def generate_children(self, initial_node,pos=1):
    """ A recursive function that generates the N (length of the node) immediate children of the node

    This function iterates and creates a possible child tuple. If the tuple is valid than a node is
    created with its value being the tuple. This is done N times.

    Parameters
    ----------
    initial_node : Node
      A node from the anytree class whose value (or "name") is a tuple of integers
    pos : int
      The depth of the current node + 1 (SHOULD NOT REALLY BE TOUCHED AS IT IS ONLY FOR RECURSIVE PURPOSES)

    Returns
    -------
    Nothing is explicitly returned, but the initial node is now populated with valid children and
    descendants
    """
    for i in range(0,len(initial_node.name)):
      tup = initial_node.name[0:pos-1] + (i, ) + (-1,) * (len(initial_node.name)-pos) # this is a generated tuple
      if self.isSafe(tup,pos-1):    # Check if current position is safe
        subNode = Node(tup,parent=initial_node,depth=pos)   # If so, generate a child node and link to current node
        if pos < len(initial_node.name):    # Continue to recurse as long as the depth does not exceed tuple length
          self.generate_children(subNode,pos+1)

  # generate_tree creates the initial node specified by length and creates the children
  def generate_tree(self, length):
    """ A function that calls on the generate_children function

    Parameters
    ----------
    length : int
      Length is the same as N. It specifies how many queens we want placed on the board

    Returns
    -------
      initial_node : Node
        A tree where only valid nodes have been explored
    """
    initial_tuple = (-1,) * length
    initial_node = Node(initial_tuple, depth=0)
    self.generate_children(initial_node)
    return initial_node

  def populate_solutions(self, root):
    """ Given a tree, populate solutions retrieves the solutions that are located at depth N (length of the root's tuple)

    Parameters
    ----------
    root : Node

    Returns
    -------
    Nothing is returned but the "solution" instance variable (which was initially an empty list) is
    now populated with all solutions for the N Queens
    """
    for child in root.children:
      if child.depth==len(root.name):
        self.solution.append(child.name)
      self.populate_solutions(child)

