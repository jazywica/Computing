"""
Python definition of basic Tree class
IMPORTANT: Some class methods assume that instances of the Tree class always have a single parent (or no parent for the root). See problem #8 on homework #3 for more details.
"""


class Tree:
    """ Recursive definition for trees plus various tree methods """
    def __init__(self, value, children): # 'value' is the data we are going to attach to the root node, 'children' is the list of children
        """ Create a tree whose root has specific value (a string). Children is a list of references to the roots of the subtrees. """
        self._value = value
        self._children = children

    def __str__(self): # this is a smart recursive method for printing the tree structure with brackets: [[], [[],[]], []] etc
        """ Generate a string representation of the tree. Use an pre-order traversal of the tree """
        ans = "["
        ans += str(self._value) # this will retrieve the value of the root first, and then parents for all subtrees recursively

        for child in self._children: # this will print the children, if children are parents to other nodes, this will call '__str__' again recursively
            ans += ", "
            ans += str(child) # this is going to be called recursively if there are subtrees
        return ans + "]"

    def get_value(self):
        """ Getter for node's value """
        return self._value

    def children(self):
        """ Generator to return children """
        for child in self._children:
            yield child

    def num_nodes(self): # thanks to the 'child.num_nodes()' we can call this function recursively and explore all its elements
        """ Compute number of nodes in the tree """
        ans = 1 # for each recursion on the way down this variable will be initialized to 1. This function never touches the root so for the first element ans = 2 and when we get to the root the answer is already correct
        for child in self._children: # this will make sure that we first scan the children before we start returning anything
            ans += child.num_nodes() # for the 'tree_dcabe' tree: the recursion will stop at 'a' as it is the deepest to the left, then 'b' which is to the right, then we go one level up
        return ans

    def num_leaves(self):
        """ Count number of leaves in tree """
        if len(self._children) == 0: # when we get to a childless node, we return '1'
            return 1

        ans = 0 # all nodes in this case are initialized to '0', the BASE CASE takes care of adding 1 to the general count
        for child in self._children:
            ans += child.num_leaves() # this will pass and add up either 0 (for parents) or 1 (for leafs)
        return ans

    def height(self):
        """ Compute height of a tree rooted by self """
        height = 0 # since we don't count the root as a height, we start from 0. This is going to be initialized at every leaf and updated for each subtree all the way up to the root
        for child in self._children: # this will start and end with the children, we will not going to have anything to do with the root
            height = max(height, child.height() + 1) # this is to comare what we have from different subtrees, each of them starts from 0 so if one went deeper that is going to be the answer
        return height
