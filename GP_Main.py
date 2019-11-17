# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 20:56:06 2019

To run this file, provide 2 arguments after the script name: First, 
the path to the data file being used. Second, the path to an output file. 
E.g. python3 GP_Main.py <path to data>.csv <path to output>.txt

@author: Savannah Rogers
"""

import sys
import pandas 
from tree import rand_list_item, Node, rand_dict_key, create_tree
import random
import numpy as np

RAW_DATA = None
#RAW_DATA = pandas.read_csv("C:/Users/Savannah Rogers/Documents/SpatDistModelingfa18/full_grizz_dataset.csv", usecols = [ "bio1","bio2","bio3","bio4","bio5", "bio6","bio7","bio8","bio9","bio10","bio11","bio12","bio13","bio14","bio15","bio16","bio17","bio18","bio19","Census_HomeDensity_AOI","Dist2ForestEdge_m","Dist2Road_Hwy_m","Dist2Stream_Rivers_m","Elevation_meters","Forest","NDVI","NLCD2011","presence","lati","long","AID","ID2","SEX","Cohort","AGEnum","birth.year","TelemDate","Location_Status","FixStatus","PDOP","HDOP","VDOP","TDOP","TransInf"], dtype = {'lati': np.float64, 'long': np.float64,'AID': 'category', 'AGEnum': np.float64, 'VDOP':np.float64, 'FixStatus':'category'})
#RAW_DATA = pandas.read_csv(".\dummydata.csv")    
#RAW_DATA["mean_temp"] = RAW_DATA["bio1"]
#RAW_DATA["max_temp"] = RAW_DATA["bio5"]
#RAW_DATA["annual_precip"] = RAW_DATA["bio12"]
#VARS = RAW_DATA.iloc[:,[19,20,21,22,23,24,25,26,44,45,46]]
#Decide which variables to use
#VARS = RAW_DATA.iloc[:,[1,5,12,19,20,21,22,23,24,25,26]]
# VARS = RAW_DATA.iloc[:,[38,39,40,41,42,43,45,46,47,48,49,50]]
VARS = None
enviro_vars = {}

    
#print(enviro_vars)

       
    
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
    pop_fits = []
    for i in range(0, pop_size):
        n = create_tree(variables, max_height, data, pres, abse)
        #print(n)
        #n.print_tree_data()
        population.append(n)
        #print(n.fitness)
        pop_fits.append(n.fitness)
    population.sort(reverse=True)
    avg_pop_fit = sum(pop_fits)/pop_size
    sd_fit = np.std(pop_fits)
    best_ind = population[0]
    best_fit = population[0].fitness
    
    return(population, avg_pop_fit, sd_fit, best_ind, best_fit)
        


def same_fit_smaller_size(subset, proximity):
        """
        Looks for all members of list with best fitness, chooses the
        smallest tree of those members. 
        """
#        proximity = 0
        subset.sort(reverse=True)
        fitcheck = subset[0].fitness #fitness of the best individual
        fitcheckmin = fitcheck-proximity #set range of fitnesses close to it
        fitcheckmax = fitcheck+proximity
        topfits = [] #new list to add individuals with the same fitness to
        sizes = []
        topfits.append(subset[0]) #add best individual
        sizes.append(subset[0].get_tree_size())
        for i in range(1,len(subset)): #for all the other individuals in tournament
            if subset[i].fitness > fitcheckmin and subset[i].fitness < fitcheckmax: #if individual's fitness is within range 
                topfits.append(subset[i]) #add that individual to topfits list
                sizes.append(subset[i].get_tree_size()) #add the size of that individual to size list
        chosen = topfits[np.argmin(sizes)]
        size = len(topfits)
        return chosen, size

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(converged_pop_counter=0)
def population_reproduction(population, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, full_df, total_pres, total_abs, variables):
    """
    Tournament style reproduction. Selects tournament subset, chooses two most fit parents,
    then performs mutation once on each, selects nodes for crossover, and appends
    two new offspring to new population until new population reaches desired
    pop size.
    """
    newpop = []
    fits = []
    if len(population)==0:
        raise Exception('Attempted reproduction with empty population')
    if not population:
        raise Exception('No population passed into reproduction')
    #elitism, copies two best from previous generation into new population
    population.sort(reverse=True)
    survivor1 = Node(variables)
    survivor2 = Node(variables)
    winner, choices = same_fit_smaller_size(population, .000002)
    if choices < len(population):
        winner2, choices2 = same_fit_smaller_size(population[choices:], .000002)
    else:
        print("identical fitness for entire population")
        population_reproduction.converged_pop_counter += 1
        winner2 = winner
    winner.copy_tree(survivor1, variables)
    winner2.copy_tree(survivor2, variables)
    newpop.append(survivor1)
    survivor1.eval_fitness(full_df, total_pres, total_abs)
    #print(survivor1.fitness)
    newpop.append(survivor2)
    survivor2.eval_fitness(full_df, total_pres, total_abs)
    ##print(survivor2.fitness)

    
    while len(newpop) <= pop_size: #2 individuals are appended to the population each generation
        subset = []
 #       print("Tournament")
        for i in range(0,tournament_size):
            i = rand_list_item(population)
            subset.append(i)
#            print(i.fitness)
        subset.sort(reverse=True)
        
        #create empty nodes for copying to
        parent1 = Node(variables)
        parent2 = Node(variables)

        #add something to keep individual with smaller tree if fitness close
        #check if other members of subset have same fitness as top individual and set those into new list
        chosen, samefits_length = same_fit_smaller_size(subset, .0002)



        #if topfits is 1 long, then do this again for the rest of tournament
        if samefits_length == 1:
            remaining = subset[1:]
            chosen2, samefits_legth2 = same_fit_smaller_size(remaining, .0002)
            chosen2.copy_tree(parent2, variables)
        #if topfits is longer than 1, just use the chosen twice
        else:
            chosen.copy_tree(parent2, variables)       

        
              
        chosen.copy_tree(parent1, variables) 
#        print("""Parent 1 fitness: {}
#        Parent 2 fitenss: {}""".format(parent1.fitness, parent2.fitness)
#        )
        #mutate each
        mutate_ind(mut_prob, parent1, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        mutate_ind(mut_prob, parent2, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        #perform crossover
        offspring1, offspring2 = cross_over(parent1, parent2, leaf_probability, full_df, total_pres, total_abs, variables)
        
        newpop.append(offspring1)
        newpop.append(offspring2)
    newpop.sort(reverse=True)
    newpop = newpop[0:pop_size]
    #print("Length of population: {}".format(len(newpop)))
    #print(newpop)
    for i in range(0,len(newpop)):
        fits.append(newpop[i].fitness)
    avg_pop_fit = (sum(fits)/(pop_size))
    sd_pop_fit = np.std(fits)
    best_ind = newpop[0]
    best_fit = newpop[0].fitness
    #print(fits)
    return(newpop, avg_pop_fit, sd_pop_fit, best_ind, best_fit)



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
    
#    print("""
#          Node 1:{}  Parent: {}  Position: {}""".format(node1, node1.parent, node1.position))
#    print("""
#          Node 2:{}  Parent: {}  Position: {}""".format(node2, node2.parent, node2.position))

    parent1 = node1.parent #parent node, not parent tree
    parent2 = node2.parent
    if node1.parent and node2.parent:
 #       print("case 1")
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
#        print("case 2")
        if node1.position == "left":
            node1.parent.left = node2o
            node2o.parent = parent1
            node2o.position = "left"
        if node1.position == "right":
            node1.parent.right = node2o
            node2o.parent = parent1
            node2o.position = "right"
        tree2 = node1o   
        tree2.parent = None
        tree2.position = None
    elif node2.parent:
#        print("case 3")
        if node2.position == "left":
            node2.parent.left = node1o
            node1o.parent = parent2
            node1o.position = "left"
        if node2.position == "right":
            node2.parent.right = node1o
            node1o.parent = parent2
            node1o.position = "right"
        tree1 = node2o 
        tree1.parent = None
        tree1.position = None
    else:
#        print("swap trees")
        tree1 = node2o
        tree1.parent = None
        tree1.position = None
        tree2 = node1o
        tree2.parent = None
        tree2.position = None
    tree1.eval_fitness(full_df, total_pres, total_abs)
    tree2.eval_fitness(full_df, total_pres, total_abs)
    #print("""
    #      Offspring 1 fitness:  {}
    #      Offspring 2 fitness:  {}
    #      """.format(tree1.fitness, tree2.fitness))
    return(tree1, tree2)
       
        
#mutation

def mutate_node(node, variables):
    """
    Causes given node to mutate. If node is an operator, changes to random
    operator. If node is a leaf, will change either variable name, min,
    or range. 
    """
    if node.operator:
        if random.randint(0,100) >= (10):
            node.operator = rand_list_item(operators)
#           print()
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
        raise Exception("mutate node failure")
    return(node)

#def mutate_ind(mut_prob, ind, variables, leaf_mut_prob, full_df, total_pres, total_abs):
#    """
#    Decides whether mutation occurs on individual with mut_prob. Chooses a node at random
#    (with probability for selecting a leaf), mutates it, then reevaluates 
#    fitness for tree at the root. Mutation change is in place.
#    """
#    if random.randint(1, 100) <= (100*mut_prob):
#        mutated1 = ind.get_node(leaf_mut_prob) #choosing node for mutation
#        if mutated1.position == "left":
#            mutated1.parent.left = mutate_node(mutated1, variables)
#        if mutated1.position == "right":
#            mutated1.parent.right = mutate_node(mutated1, variables)
#        mutated1.get_root().eval_fitness(full_df, total_pres, total_abs)

def mutate_ind(mut_prob, ind, variables, leaf_mut_prob, full_df, total_pres, total_abs):
    #leaf mut prob currently does nothing, can add something so its more likely to mutate leaf than operator
    if ind.left:
        mutate_ind(mut_prob, ind.left, variables, leaf_mut_prob, full_df, total_pres, total_abs)
    if random.randint(1,100) <= (100*mut_prob):
        if ind.position == "left":
            ind.parent.left = mutate_node(ind, variables)
        if ind.position == "right":
            ind.parent.right = mutate_node(ind, variables) #root node is not mutated
    if ind.right:
        mutate_ind(mut_prob, ind.right, variables, leaf_mut_prob, full_df, total_pres, total_abs)
























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
 


def test_get_node():
    
    max_height = 10
    raw_data =RAW_DATA
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abs = raw_data[raw_data.presence == 0].count()[0]
    for i in range(1,100):
        testtree = create_tree(enviro_vars, max_height, RAW_DATA, data_pres, data_abs)
       # testtree.print_tree_data()
        for i in range(1,100):
            node = testtree.get_node(.5)
        #print(node)

def test_find_node():
    max_height = 4
    raw_data = RAW_DATA
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abs = raw_data[raw_data.presence == 0].count()[0]
    testtree = create_tree(enviro_vars, max_height, RAW_DATA, data_pres, data_abs)
    node, step = testtree.find_node(False, 1)
    testtree.print_tree()
    print("----------------------------------------------------")
    node.print_tree()

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
 
def test_samefitsmallersize():
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abse = raw_data[raw_data.presence == 0].count()[0]
    pop_size = 10
    variables = enviro_vars
    max_height = 8
    tournament_size = 4
    leaf_probability = .5
    mut_prob = 1
    leaf_mut_prob = .9
    
    pop, fit, sdfit, best, best_fit  = pop_generate(raw_data, data_pres, data_abse, pop_size, variables, max_height)
    for i in range(0,len(pop)):
        #pop[i].print_tree_data()
        print("Tree {} fitness:".format(i))
        print(pop[i].fitness)
    winner, choices = same_fit_smaller_size(pop, .5)
    print("Choices:{}  Tree fitness:{}".format(choices, winner.fitness))
    winner2, choices2 = same_fit_smaller_size(pop[choices:], .005)
    print("Choices 2:{}  Tree fitness:{}".format(choices2, winner2.fitness))
    winner3, choices3 = same_fit_smaller_size(pop[(choices2+choices):], .005)
    print("Choices 3:{}  Tree fitness:{}".format(choices3, winner3.fitness))
    winner4, choices4 = same_fit_smaller_size(pop[(choices2+choices3+choices):], .05)
    print("Choices 4:{}  Tree fitness:{}".format(+choices4, winner4.fitness))
    print("Chosen trees:")
    #winner.print_tree_data()
    print("----")
    #winner2.print_tree_data()

    
    
    
def test_reprod():
    raw_data = RAW_DATA
    #raw_data = pandas.read_csv(".\dummydata.csv")
    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abse = raw_data[raw_data.presence == 0].count()[0]
    pop_size = 10
    variables = enviro_vars
    max_height = 8
    tournament_size = 4
    leaf_probability = .5
    mut_prob = 1
    leaf_mut_prob = .9
    
    pop, fit, sdfit, best, best_fit  = pop_generate(raw_data, data_pres, data_abse, pop_size, variables, max_height)
    print("""
          Initial fitness = {}
          """.format(fit))
#    print(pop[0].fitness)
#    print(pop[1].fitness)
    newpop, new_fit, new_sd, new_best, new_best_fit = population_reproduction(pop, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
    print("""
          Gen 1 fitness = {}
          """.format(new_fit))

    newpop2, new_fit2, new_sd2, new_best2, new_best_fit2 = population_reproduction(newpop, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
    print("""
          Gen 2 fitness = {}
          """.format(new_fit2))

    newpop3, new_fit3, new_sd3, new_best3, new_best_fit3 = population_reproduction(newpop2, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
    print("""
          Gen 3 fitness = {}
          """.format(new_fit3))






def mult_gen():
    
    raw_data = RAW_DATA

    data_pres = raw_data[raw_data.presence == 1].count()[0]
    data_abse = raw_data[raw_data.presence == 0].count()[0]
    pop_size = 1000
    variables = enviro_vars
    max_height = 5
    tournament_size = 3
    leaf_probability = .5
    mut_prob = .05
    leaf_mut_prob = .9
    generations = 50
    avg_fitnesses = []
    sd_fitnesses = []
    best_inds = []
    best_fits = []
    generation = [0]
    
    pop, fit, sd, best_ind, best_fit = pop_generate(raw_data, data_pres, data_abse, pop_size, variables, max_height)
    avg_fitnesses.append(fit)
    sd_fitnesses.append(sd)
    best_inds.append(best_ind)
    best_fits.append(best_fit)
    
    for i in range(1,generations):
        if population_reproduction.converged_pop_counter > 5:
            break
        #print("Popultaion {} fitnesses of individuals".format(i+1))
        pop, avg_pop_fit, sd_pop_fit, best_ind, best_fit = population_reproduction(pop, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
        #print("Average fitness of population {}: {}".format(i+1, fit))
        avg_fitnesses.append(avg_pop_fit)
        sd_fitnesses.append(sd_pop_fit)
        best_inds.append(best_ind)
        best_fits.append(best_fit)
        generation.append(i)
        print(".........................{}".format(i))
#    print("Best individual: ")
#    pop[0].print_tree_data()
#    print("Worst individual: ")
#    pop[pop_size-1].print_tree_data()
    print("""Genetic Program result: 
        Pop Size: {}
        Tournament Size: {}
        Leaf Crossover Probability (given crossover occurs): {}
        Mutation Probability (per individual): {}
        Leaf Mutation Probability (given mutation per individual):{}
        Generations:{}
        Fitnesses:
            {}
          """.format(pop_size, tournament_size, leaf_probability, mut_prob, leaf_mut_prob, generation, avg_fitnesses))
    df = pandas.DataFrame()
    # df['Gen'] = generations  # Not working
    df['Avg Fitness'] = avg_fitnesses
    df['SD Fitness'] = sd_fitnesses
    df['Best Fitness'] = best_fits
    for i in range(0,len(best_inds)):
        with open("{}/best_tree_gen_{}.txt".format(sys.argv[2], i), 'w') as f:
            best_inds[i].print_tree_data(file = f)
    df.to_csv("{}/data.csv".format(sys.argv[2]), sep = ',')


if __name__ == "__main__":
    RAW_DATA = pandas.read_csv(sys.argv[1])
    VARS = RAW_DATA.iloc[:,[38,39,40,41,42,43,45,46,47,48,49,50]] #update this to just be all columns except presence
    for i in list(VARS):
    #for i in list(RAW_DATA)[0:5]:
        title = i
        mini = min(RAW_DATA[i])
        maxi = max(RAW_DATA[i])
        enviro_vars[title] = {'min': mini, 'max':maxi}
    #test_pop_creation()
    #test_getting_node_for_crossover()
    #test_crossover()
    #test_reprod()
    #test_get_node()
    mult_gen()
    #test_find_node()
    #test_samefitsmallersize()