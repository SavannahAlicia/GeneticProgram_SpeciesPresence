# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 09:38:51 2018
Tree module containing tree functions and classes

    Classes: Node
    Functions: rand_list_item, rand_dict_key, create_tree
    Global Variables: operators, node_prob



@author: Savannah Rogers
"""

import pandas
import random
import sys
import copy


##user inputs

operators = [
        'AND',
        'OR',
        'AND NOT',
        'OR NOT']

node_prob = 55


#sys.getrecursionlimit()
#sys.setrecursionlimit()


def rand_list_item(curr_list):
    """Return a random item from a list.
    """
    return curr_list[random.randint(0, (len(curr_list) -1))]

def rand_dict_key(curr_dict):
    """Return a random key from a dictionary.
    """
    return rand_list_item(list(curr_dict.keys()))

#creating tree structures for genome

class Node():
    """
A Node in a tree is either an operator with branches or a variable leaf.
    
        Initialization begins with the root node and grows a tree of height 
        between 1 and user defined max
        Nodes can be either operators from a list or class Variable, which 
        contains a variable
        from user data with a min value and a range.
        
        Member functions: get_tree_height, get_tree_size, 
        print_tree, print_tree_data, apply_tree, and eval_fitness
        
        Attributes: root, fitness, right, left, operator, variable
        
        Member class: Variable
    """
    root = False # defaults to false, root will be set to true
    fitness = 0
    right = None
    left = None
    operator = None
    variable = None
    #subtree_hash = None
    class Variable():
        """A Variable has a variable with a min and range value.
        """
        def __init__(self, variables):  #variables is a dictionary passed through the node
            self.name = rand_dict_key(variables)
            self.min = random.uniform(variables[self.name]['min'], variables[self.name]['max'])
            self.range = random.uniform(0, variables[self.name]['max']-self.min)
            
        def __repr__(self):
            return '{0}: min:{1} max:{2} ran:{3}'.format(self.name, self.min, self.min + self.range, self.range)
    
    def __init__(self, variables):
        self.parent = None
        self.position = None  
    
    def init_tree(self, variables, max_height, parent=None, position=None, curr_height=1):
        self.parent = parent
        self.position = position
        if curr_height == 1:
            self.root = True
            self.right = Node(variables)
            self.right.init_tree(variables, max_height, self, 'right', curr_height + 1)
            self.left = Node(variables)
            self.left.init_tree(variables, max_height, self, 'left', curr_height + 1)
            self.operator = rand_list_item(operators)
        elif curr_height == max_height:
            self.variable = self.Variable(variables)
        else:
            if (random.randint(0, 100) <= node_prob):   #Create a branch node_prob % of time
                self.right = Node(variables)
                self.right.init_tree(variables, max_height, self, 'right', curr_height + 1) #pass in current depth so can be incrememnted each time, if depth is above some cutoff go to leaf node
                self.left = Node(variables)
                self.left.init_tree(variables, max_height, self, 'left', curr_height + 1)
                self.operator = rand_list_item(operators)
            else:   #Create a leaf otherwise
                self.variable = self.Variable(variables)
    
    def __lt__(self, other): #defines sorting behavior of trees
        return self.fitness < other.fitness
            
    def __repr__(self):
        if self.operator:
            # Because 'NOT's are not passed down through operators, 
            # they essentially don't exist unless their right-hand
            # children are variables
            if self.right.variable:
                return self.operator
            else:
                return self.operator.replace('NOT', '')
        elif self.variable:
            return '{}'.format(self.variable)
        else:
            raise Exception('Node neither variable nor operator')

    def get_tree_height(self, height=1, _max = 0):
        """Returns height of tree.
            Goes step by step down tree, adding 1 to height each step and 
            replacing max any time height is greater than max
        """
        if height > _max:
            _max = height
        
        if self.left:
            _max = self.left.get_tree_height(height + 1, _max)
        if self.right:
            _max = self.right.get_tree_height(height + 1, _max)
        return _max
    
    def get_tree_size(self, size = 1):
        """Traverses tree and adds 1 to size each step. Returns size.
        """
        if self.left:
            size = self.left.get_tree_size(size + 1)
        if self.right:
            size = self.right.get_tree_size(size + 1)
        return size
    
    def get_root(self):
        if self.parent:
            root = self.parent.get_root()
        else:
            root = self
        return root

    def print_tree(self, depth = 0, file = sys.stdout):
        """Prints the right side of tree first rotated so that upper nodes.
            are left and lower nodes are indented
        """
        indent = 4 * depth
        try:
            self.right.print_tree(depth + 1, file = file)
        except AttributeError:
            pass
        print(' ' * indent, self, file=file)
        try:
            self.left.print_tree(depth + 1, file = file)
        except AttributeError:
            pass
        
    def print_tree_data(self, file = sys.stdout):
        """In addition to print_tree, also prints fitness and height.
        """
        self.print_tree(file = file)
        print("""
              Fitness:{0}
              Height: {1}""".format(self.fitness, self.get_tree_height()), file=file)

     
    def apply_tree(self, curr_df, is_not = False):
        ''' Returns a subset of user dataframe that obeys the node ruleset
            
            Attributes: curr_df
            
            Checks node type.
                For AND operator, subsets df based on left node and passes that
                    to right node as curr_df
                For OR operator, subsets full df based on left node, right node, 
                    and concats the two
                For either NOT operator, is_not = True triggers different 
                    df subset procedure 
            Finds rows of dataframe that values in the node's variable column 
                are between node values
        '''
        if self.operator == 'AND':
            left_df = self.left.apply_tree(curr_df)
            if left_df.empty:
                return left_df                             #if the left side is empty, "AND" inclusive will be empty
            curr_df = self.right.apply_tree(left_df) #take subset that follows rules on left and find parts of it that also obey rules on right
            return curr_df
        elif self.operator == 'OR':
            left_df = self.left.apply_tree(curr_df.copy()) #"curr_df" will be passed in as "opy"
            right_df = self.right.apply_tree(curr_df.copy())
            curr_df = pandas.concat([left_df, right_df]).drop_duplicates().reset_index(drop=True)
            return curr_df
        elif self.operator == 'AND NOT':
            left_df = self.left.apply_tree(curr_df)
            if left_df.empty:
                return left_df
            curr_df = self.right.apply_tree(left_df, True)
            return curr_df
        elif self.operator == 'OR NOT':
            left_df = self.left.apply_tree(curr_df.copy())
            right_df = self.right.apply_tree(curr_df.copy(), True)
            curr_df = pandas.concat([left_df, right_df]).drop_duplicates().reset_index(drop=True)
            return curr_df
        elif self.variable:
            if not curr_df.empty: #if curr_df is empty, just return empty
                if is_not:
                    curr_df = curr_df[~(curr_df[self.variable.name] > self.variable.min) | ~(curr_df[self.variable.name] < (self.variable.min + self.variable.range))]
                
                else:
                    curr_df = curr_df[(curr_df[self.variable.name] > self.variable.min) & (curr_df[self.variable.name] < (self.variable.min + self.variable.range))]
            return curr_df
        else:
            raise Exception('Found node with no type')
            
            
    def eval_fitness(self, full_df, total_pres, total_abs):
        '''Sets fitness as the accuracy of the node's statement at predicting 
            "Presence" (checked against 1 and 0 in dataframe column)
            
            Args: 
                full_df(pandas df):
                total_pres():
                total_abs():
        
            Calls apply_tree on full_df.
            Calculates accuracy as true positives + true negatives/total
            Weights empty dataframe fitness as -1 since accuracy of empty df
                would actually be true negatives/total
        '''
        #find the subset dataframe that fits the tree statement
        #here put piece that takes random 10% of full dataframe to use instead of full thing for computation 
        res_df = self.apply_tree(full_df)
        #print(res_df)
        if not res_df.empty:
            true_pos = res_df[res_df.presence == 1].count()[0] 
            true_neg = total_abs - res_df[res_df.presence == 0].count()[0] 
            self.fitness = (true_pos + true_neg)/(total_pres+total_abs)
        else:
            self.fitness=-1
    
    def get_node(self, leaf_probability):
        """
        Returns a random node
        
        Args:
            leaf_probability(dec float): allows user to choose probability that 
            random node chosen is a leaf or operator.
        
                Randomly decides whether to return a leaf or operator, then randomly 
        chooses how many steps to traverse tree. Calls find_node() to return
        the node, which remembers its own position in relation to its parent
        """

        want_leaf = random.randint(1, 100) < (100*leaf_probability) #true or false value, determined via probability
        #print('want leaf', want_leaf)
        num_steps = random.randint(1, self.get_tree_size()) #choosing a random node means traversing a random number of steps
        #print('number of steps', num_steps)
        node, steps_taken = self.find_node(want_leaf = want_leaf, num_steps = num_steps)
        if self.get_tree_size() < 2: # If tree is only a leaf, return that leaf
            return self        
        if not node:
            self.print_tree()
            print('want leaf', want_leaf)
            print(self.get_tree_size())
            print('number of steps', num_steps)
            raise Exception('find_node did not return a node')
        return node
    
    def copy_tree(self, destination_node, variables, destination_parent=None):
        """Iteratively copies nodes of tree into new tree
        
        """
        if self.left:
            destination_node.left = Node(variables)
            self.left.copy_tree(destination_node.left, variables, destination_node)
        destination_node.root = copy.deepcopy(self.root) # defaults to false, root will be set to true
        destination_node.fitness = copy.deepcopy(self.fitness)
        destination_node.operator = copy.deepcopy(self.operator)
        destination_node.variable = copy.deepcopy(self.variable)
        destination_node.parent = destination_parent
        destination_node.position = copy.deepcopy(self.position)
        if self.right:
            destination_node.right = Node(variables)
            self.right.copy_tree(destination_node.right, variables, destination_node)

            
    
    def find_node(self, want_leaf, num_steps, parent=None, curr_step=0):
        """
        Finds a node in tree that is leaf or operator as specified at or after
        specified number of steps.
        
        Args:
            want_leaf(bool): does user want leaf or operator
            num_steps(int): how many steps to traverse tree (at least)
            parent(Node): default None, allows function to pass back parent
            node 
            
        
        """
        node = None
        if self.left:
            node, curr_step = self.left.find_node(want_leaf, num_steps, self, curr_step)
            if node: #found correct node if node is returned
                return (node, curr_step)
        curr_step +=1
        if curr_step >= num_steps: #if you're at or past the correct # of steps
            if is_correct_type(want_leaf, self):
                return(self, curr_step)
            elif want_leaf: #want leaf but node is operator
                pass #keep going (will hit a leaf)
            else: #want operator but node is leaf
#                if not parent:
#                    raise Exception('find_node failed to return a parent')
                return(parent, curr_step) #parent of leaf will always be an operator 
        
        if self.right:
            node, curr_step = self.right.find_node(want_leaf, num_steps, self, curr_step)
            if node: #found correct node if node is returned
                return (node, curr_step)
        return (None, curr_step) #if we didn't find anything, keep going


    
def create_tree(variables, max_height, data, presence, absence):
    '''Create a root Node, from which sprouts an entire tree.
    
    Args:
        variables (dict): created from user input (soon to be function that extracts from dataset)
            level 1 keys are environmental variable names
            level 2 keys are 'min' and 'max' possible values for those variables (to limit search space)
        max_height (int): the user specified maximum tree height
        
    Returns:
        n (Node): a root node 
    '''
    n = Node(variables)
    n.init_tree(variables, max_height)
    n.eval_fitness(data, presence, absence)
    if n:
        # print("tree created")
        pass
    else:
        print("tree failed")
        raise Exception('Tree creation failed')
    return n
 
def is_correct_type(want_leaf, node):
    """
    Returns boolean based on if node is of the desired type.
    
    Args:
        want_leaf(bool): do you want a leaf?
        node(Node): node to test
    """
    if want_leaf and node.variable:
        return True
    elif not want_leaf and node.operator:
        return True
    else:
        return False
    
    
#
#    
#            
    
    #if one is whole tree
    #if both whole tree
    
    