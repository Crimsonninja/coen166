# @author: Jonathan Trinh
# @version 10222018
# Before you run this code, you need Anytree. To do this run the following (you'll need pip):
# pip install anytree
# If you'd like to visualize the graph (a line of code is commented that you can uncomment and execute),
# you will need GraphViz. To install GraphViz, execute (you will need brew):
# brew install graphviz

from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph

solution = []

def isSafe(some_tuple, index):
  queen_position = some_tuple[index]
  for i in range(0,index):
    if some_tuple[i] == -1: # check for -1's
      return False

    if some_tuple[i] == queen_position: # row check
      return False

    if (some_tuple[i] + (index - i) == some_tuple[index]) or (some_tuple[i] - (index - i) == some_tuple[index]):  # diagonal check
      return False

  return True

def boardIsSafe(some_tuple):
  tuple_length = len(some_tuple)
  for i in range(tuple_length):
    if isSafe(some_tuple,i)==False:
      return False
  return True

# generate_children is a recursive function that will create n (length of the node) children and for
# each of those children recursively call the same function
def generate_children(initial_node,pos=1):
  for i in range(0,len(initial_node.name)):
    tup = initial_node.name[0:pos-1] + (i, ) + (-1,) * (len(initial_node.name)-pos) # this is a tuple
    if isSafe(tup,pos-1):
      subNode = Node(tup,parent=initial_node,depth=pos)
      if pos < len(initial_node.name):
        generate_children(subNode,pos+1)

# generate_tree creates the initial node specified by length and creates the children
def generate_tree(length):
  initial_tuple = (-1,) * length
  initial_node = Node(initial_tuple, depth=0)
  generate_children(initial_node)
  return initial_node

def solutions(root):
  for child in root.children:
    if child.depth==len(root.name):
      solution.append(child.name)
    solutions(child)

test_tree = generate_tree(8)
solutions(test_tree)
print solution
print boardIsSafe((0, 2, 4, 1, 3))

# for pre,fill, node in RenderTree(test_tree):
#   print("%s%s" % (pre,node.name))

RenderTreeGraph(test_tree).to_picture("state_tree_3.png")
