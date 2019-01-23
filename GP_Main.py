# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 20:56:06 2019

@author: Savannah Rogers
"""

import pandas 
from tree import rand_list_item, Node, rand_dict_key, create_tree
import random
import numpy as np

RAW_DATA = pandas.read_csv("C:/Users/Savannah Rogers/Documents/SpatDistModelingfa18/full_grizz_dataset.csv", usecols = [ "bio1","bio2","bio3","bio4","bio5", "bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19","Census_HomeDensity_AOI","Dist2ForestEdge_m","Dist2Road_Hwy_m","Dist2Stream_Rivers_m","Elevation_meters","Forest","NDVI","NLCD2011","presence","lati","long","AID","ID2","SEX","Cohort","AGEnum","birth.year","TelemDate","Location_Status","FixStatus","PDOP","HDOP","VDOP","TDOP","TransInf"], dtype = {'lati': np.float64, 'long': np.float64,'AID': 'category', 'AGEnum': np.float64, 'VDOP':np.float64, 'FixStatus':'category'})
# = pandas.read_csv(".\dummydata.csv")    

enviro_vars = {}


for i in list(RAW_DATA)[0:27]:
    title = i
    mini = min(RAW_DATA[i])
    maxi = max(RAW_DATA[i])
    enviro_vars[title] = {'min': mini, 'max':maxi}
    
print(enviro_vars)

       
    
#enviro_vars = {
#        'TEMP':{
#                'min': -50,
#                'max': 150},
#        'PRECIP':{
#                'min': 0,
#                'max': 150},
#        'ELEVATION':{
#                'min': 0,
#                'max': 3000},
#        'HUMAN DENSITY':{
#                'min': 0,
#                'max': 50},
#        'DISTANCE TO RIVER':{
#                'min': 0,
#                'max': 150}}

operators = [
        'AND',
        'OR',
        'AND NOT',
        'OR NOT']


#check that dataset colnames match enviro_vars



#create a population as list of (root) nodes

def pop_generate(data, pres, abse, pop_size, variables, max_height):
    """
    Creates a list of trees
    """
    population = []
    pop_fit = 0
    for i in range(0, pop_size):
        n = create_tree(variables, max_height, data, pres, abse)
        #print(n)
        #n.print_tree_data()
        population.append(n)
        pop_fit =+ n.fitness
    population.sort(reverse=True)
    pop_fit = (pop_fit/(pop_size+1))
    return(population, pop_fit)
        





def population_reproduction(population, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, full_df, total_pres, total_abs, variables):
    """
    Tournament style reproduction. Selects tournament subset, chooses two most fit parents,
    then performs mutation once on each, selects nodes for crossover, and appends
    two new offspring to new population until new population reaches desired
    pop size.
    """
    newpop = []
    pop_fit = 0
    while len(newpop) <= pop_size:
        subset = []
        print("Tournament")
        for i in range(0,tournament_size):
            i = rand_list_item(population)
            subset.append(i)
            print(i.fitness)
        subset.sort(reverse=True)
        
        #create empty nodes for copying to
        parent1 = Node(variables)
        parent2 = Node(variables)
        #copy two best in tourny
        subset[0].copy_tree(parent1, variables) 
        subset[1].copy_tree(parent2, variables)
        print("""Parent 1 fitness: {}
        Parent 2 fitenss: {}""".format(parent1.fitness, parent2.fitness)
        )
        #mutate each
        mutate_ind(mut_prob, parent1, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        mutate_ind(mut_prob, parent2, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        #perform crossover
        offspring1, offspring2 = cross_over(parent1, parent2, leaf_probability, full_df, total_pres, total_abs, variables)
        
        newpop.append(offspring1)
        pop_fit =+ offspring1.fitness
        newpop.append(parent2)
        pop_fit =+ offspring2.fitness
    newpop.sort(reverse=True)
    pop_fit = (pop_fit /(pop_size))
    return(newpop, pop_fit)


        
#crossover
def cross_over(tree1, tree2, leaf_probability, full_df, total_pres, total_abs, variables):
    """
    Swaps two nodes between existing trees. Applies changes in place and 
    returns two trees.
    
    Args:
        tree1(Node): first tree
        tree2(Node): other tree
        leaf_probability: probability that leaf is selected for crossover
        instead of operator
        
    It is currently possible to evolve a single leaf tree. Consider if this 
    makes sense in context.
    """
    #if both nodes
    node1 = tree1.get_node(leaf_probability)
    node1o = Node(variables) #create second copy of node1
    node1.copy_tree(node1o, variables)
    node2 = tree2.get_node(leaf_probability)
    node2o = Node(variables) #create second copy of node2
    node2.copy_tree(node2o, variables)
    
    print("""
          Node 1:{}  Parent: {}  Position: {}""".format(node1, node1.parent, node1.position))
    print("""
          Node 2:{}  Parent: {}  Position: {}""".format(node2, node2.parent, node2.position))

    parent1 = node1.parent #parent node, not parent tree
    parent2 = node2.parent
    if node1.parent and node2.parent:
        print("case 1")
        if node1.position == "left":
            node1.parent.left = node2o
            node2o.parent = parent1
            node2o.position == "left"
        if node1.position == "right":
            node1.parent.right = node2o
            node2o.parent = parent1
            node2o.position == "right"
        if node2.position == "left":
            node2.parent.left = node1o
            node1o.parent = parent2
            node1o.position == "left"
        if node2.position == "right":
            node2.parent.right = node1o
            node1o.parent = parent2
            node1o.position == "right"
    elif node1.parent:
        print("case 2")
        if node1.position == "left":
            node1.parent.left = node2o
            node2o.parent = parent1
        if node1.position == "right":
            node1.parent.right = node2o
            node2o.parent = parent1
        tree2 = node1o   
        tree2.parent = None
    elif node2.parent:
        print("case 3")
        if node2.position == "left":
            node2.parent.left = node1o
            node1o.parent = parent2
        if node2.position == "right":
            node2.parent.right = node1o
            node1o.parent = parent2
        tree1 = node2o 
        tree1.parent = None
    else:
        print("swap trees")
        tree1 = node2o
        tree1.parent = None
        tree2 = node1o
        tree2.parent = None
    tree1.eval_fitness(full_df, total_pres, total_abs)
    tree2.eval_fitness(full_df, total_pres, total_abs)
    print("""
          Offspring 1 fitness:  {}
          Offspring 2 fitness:  {}
          """.format(tree1.fitness, tree2.fitness))
    return(tree1, tree2)
       
        
#mutation

def mutate_node(node, variables):
    """
    Causes given node to mutate. If node is an operator, changes to random
    operator. If node is a leaf, will change either variable name, min,
    or range. 
    """
    if node.operator:
        node.operator = rand_list_item(operators)
        print()
    elif node.variable:
        ran = random.randint(0,2)
        if ran == 0: #1/3 of time choose new variable, new min, or new range
            node.variable.name = rand_dict_key(variables) 
        elif ran == 1:
            node.variable.min = node.variable.min + random.randint(-20,20)
        elif ran == 2:
            node.variable.range = node.variable.range + random.randint(-20,20)
    else:
        print("Error: node has no type")
    return(node)

def mutate_ind(mut_prob, ind, variables, leaf_mut_prob, full_df, total_pres, total_abs):
    """
    Decides whether mutation occurs on individual with mut_prob. Chooses a node at random
    (with probability for selecting a leaf), mutates it, then reevaluates 
    fitness for tree at the root. Mutation change is in place.
    """
    if random.randint(1, 100) < (100*mut_prob):
        mutated1 = ind.get_node(leaf_mut_prob) #choosing node for mutation
        if mutated1.position == "left":
            mutated1.parent.left = mutate_node(mutated1, variables)
        if mutated1.position == "right":
            mutated1.parent.right = mutate_node(mutated1, variables)
        mutated1.get_root().eval_fitness(full_df, total_pres, total_abs)


























#################TESTING############################
def test_pop_creation():
    pop_size = 10
    max_tree_height = 9

    #mutation can replace whole node with new subtree, or just change values and operators (small changes to numbers often is fine, but operator changes should be less likely)
      #benchmark for fitness performance based on previous lda qda models
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")    
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abs = raw_data[raw_data.presence == 0].count()[0]
    population, fit = pop_generate(raw_data, data_pres, data_abs, pop_size, enviro_vars, max_tree_height)
    for i in population:
        #print("""      
        #      ------------------------------------------------------""")
        #i.print_tree_data()
        print(i.fitness)
 


def test_getting_node_for_crossover():
    max_tree_height = 5
    pop_size = 1
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abs = raw_data[raw_data.presence == 0].count()[0]
   
    while True:
        pop, fit = pop_generate(raw_data, data_pres, data_abs, pop_size, enviro_vars, max_tree_height)
        tree = pop[0]
        tree.print_tree_data()
        gotten_node = tree.get_node(50)
        print("""
  Node received: {}
            Parent: {}
            {} of parent
        
        """.format(gotten_node, gotten_node.parent, gotten_node.position))
        print('Want to continue? Y/N')
        answer = input('> ')
        if answer.lower() == 'n':
            break
    print("Test concluded")
        
def test_crossover():
    max_tree_height = 4
    leaf_prob = 0.5
    pop_size = 2
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")
    data_abs = raw_data[raw_data.presence == 0].count()[0]
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    variables = enviro_vars
    
    while True:
        pop, fit = pop_generate(raw_data, data_pres, data_abs, pop_size, enviro_vars, max_tree_height)
        tree1 = pop[0]
        tree2 = pop[1]
        offspring1 = Node(variables)
        tree1.copy_tree(offspring1, variables)
        offspring2 = Node(variables)
        tree2.copy_tree(offspring2, variables)
        
        offspring1, offspring2 = cross_over(offspring1, offspring2, leaf_prob, raw_data, data_pres, data_abs, variables)
        
        print("""
              
        Parent 1:
            
            """)
        tree1.print_tree_data() 
        print("""
              
        Parent 2:
            
            """)
        tree2.print_tree_data()
        print("""
              
        Offspring 1:
            
            """)
        offspring1.print_tree_data()
        print("""
              
        Offspring 2:
            
            """)
        offspring2.print_tree_data()
              
        print('Want to continue? Y/N')
        answer = input('> ')
        if answer.lower() == 'n':
            break
    print("Test concluded")
    
    
def test_reprod():
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abse = raw_data[raw_data.presence == 0].count()[0]
    pop_size = 26 
    variables = enviro_vars
    max_height = 8
    tournament_size = 8
    leaf_probability = .5
    mut_prob = .2
    leaf_mut_prob = .9
    
    pop, fit = pop_generate(raw_data, data_pres, data_abse, pop_size, variables, max_height)
    print("""
          Initial fitness = {}
          """.format(fit))
    newpop, new_fit = population_reproduction(pop, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
    print("""
          Gen 1 fitness = {}
          """.format(new_fit))

if __name__ == "__main__":
    #test_pop_creation()
    #test_getting_node_for_crossover()
    #test_crossover()
    test_reprod()