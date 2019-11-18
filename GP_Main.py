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
from utils.log import log

# global scope variables (defined in `if __name__` block) 
RAW_DATA = None
VARS = None
enviro_vars = {}
operators = [
        'AND',
        'OR',
        'AND NOT',
        'OR NOT']



def pop_generate(data, pres, abse, pop_size, variables, max_height):
    """
    Creates a list of trees
    """
    population = []
    pop_fits = []
    for i in range(0, pop_size):
        n = create_tree(variables, max_height, data, pres, abse)
        log(n) #prints n if verbose set to true
        if log.is_verbose:
            n.print_tree_data()
        population.append(n)
        log(n.fitness)
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
    log('survivor1 fitness: ', end='')
    log(survivor1.fitness)
    newpop.append(survivor2)
    survivor2.eval_fitness(full_df, total_pres, total_abs)
    log('survivor2 fitness:', end='')
    log(survivor2.fitness)

    
    while len(newpop) <= pop_size: #2 individuals are appended to the population each generation
        subset = []
        for i in range(0,tournament_size):
            i = rand_list_item(population)
            subset.append(i)
            log(i.fitness)
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
        log("""Parent 1 fitness: {}
        Parent 2 fitenss: {}""".format(parent1.fitness, parent2.fitness)
        )
        #mutate each
        mutate_ind(mut_prob, parent1, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        mutate_ind(mut_prob, parent2, variables, leaf_mut_prob, full_df, total_pres, total_abs)
        #perform crossover
        offspring1, offspring2 = cross_over(parent1, parent2, leaf_probability, full_df, total_pres, total_abs, variables)
        
        newpop.append(offspring1)
        newpop.append(offspring2)
    newpop.sort(reverse=True)
    newpop = newpop[0:pop_size]
    log("Length of population: {}".format(len(newpop)))
    log(newpop)
    for i in range(0,len(newpop)):
        fits.append(newpop[i].fitness)
    avg_pop_fit = (sum(fits)/(pop_size))
    sd_pop_fit = np.std(fits)
    best_ind = newpop[0]
    best_fit = newpop[0].fitness
    log(fits)
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
    log("""
         Node 1:{}  Parent: {}  Position: {}""".format(node1, node1.parent, node1.position))
    log("""
         Node 2:{}  Parent: {}  Position: {}""".format(node2, node2.parent, node2.position))

    parent1 = node1.parent #parent node, not parent tree
    parent2 = node2.parent
    if node1.parent and node2.parent: #if both node1 and node2 are not root (so they do have parents)
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
    elif node1.parent: #node2 is a root
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
    elif node2.parent: #node 1 is a root
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
    else: #both node1 and node2 are roots so we just swap trees
        tree1 = node2o
        tree1.parent = None
        tree1.position = None
        tree2 = node1o
        tree2.parent = None
        tree2.position = None
    tree1.eval_fitness(full_df, total_pres, total_abs)
    tree2.eval_fitness(full_df, total_pres, total_abs)
    log("""
          Offspring 1 fitness:  {}
          Offspring 2 fitness:  {}
          """.format(tree1.fitness, tree2.fitness))
    return(tree1, tree2)
       


def mutate_node(node, variables):
    """
    Causes given node to mutate. If node is an operator, changes to random
    operator. If node is a leaf, will change either variable name, min,
    or range. 
    """
    if node.operator:
        if random.randint(0,100) >= (10):
            node.operator = rand_list_item(operators)
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
    generations = 40
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
        log("Popultaion {} fitnesses of individuals".format(i+1))
        pop, avg_pop_fit, sd_pop_fit, best_ind, best_fit = population_reproduction(pop, pop_size, tournament_size, mut_prob, leaf_mut_prob, leaf_probability, raw_data, data_pres, data_abse, enviro_vars)
        log("Average fitness of population {}: {}".format(i+1, fit))
        avg_fitnesses.append(avg_pop_fit)
        sd_fitnesses.append(sd_pop_fit)
        best_inds.append(best_ind)
        best_fits.append(best_fit)
        generation.append(i)
        print(".........................{}".format(i))
        log("Best individual: ")
        if log.is_verbose:
            pop[0].print_tree_data()
        log("Worst individual: ")
        if log.is_verbose:
            pop[pop_size-1].print_tree_data()
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
    df['Avg Fitness'] = avg_fitnesses
    df['SD Fitness'] = sd_fitnesses
    df['Best Fitness'] = best_fits
    for i in range(0,len(best_inds)):
        with open("{}/best_tree_gen_{}.txt".format(sys.argv[2], i), 'w') as f:
            best_inds[i].print_tree_data(file = f)
    df.to_csv("{}/data.csv".format(sys.argv[2]), sep = ',')



if __name__ == "__main__":
    for arg in sys.argv:
        if arg == '--verbose':
            log.is_verbose = True
            sys.argv.remove(arg)
            break
    RAW_DATA = pandas.read_csv(sys.argv[1])
    VARS = RAW_DATA.iloc[:,[38,39,40,41,42,43,45,46,47,48,49,50]] #update this to just be all columns except presence
    for i in list(VARS):

        title = i
        mini = min(RAW_DATA[i])
        maxi = max(RAW_DATA[i])
        enviro_vars[title] = {'min': mini, 'max':maxi}

    mult_gen()
