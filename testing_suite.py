

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