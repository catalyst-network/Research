import bloom_filter as bf
import random

def create_global_bf(num_of_producers):
    global_bf = bf.BloomFilter(num_of_producers)
    return global_bf


def return_ratio(value, ratio):
    ratio = int(ratio * 100)
    value = int((value / 100) * ratio)
    return value


def create_array_of_bf(num_of_producers, ratio):

    array_of_bf = []
    
    #for each producer in the worker pool 
    for prod in range(num_of_producers):
        #create a known size bf
        global_bf = create_global_bf(num_of_producers)
        #from the producers select a random set of other producer to have recieved a message from 
        pids = random.sample(range(num_of_producers), return_ratio(num_of_producers, ratio))
        #for each of these add a new element to the bloom filter
        for j in pids:
            global_bf.add(j, False)
        array_of_bf.append([prod, global_bf])
      

    return(array_of_bf)

'''

def group_bfs(pids, array_of_bfs):
    #unique BFs should be [[weighting, bf, [identities]] . . . ]
    unique_bfs = [] 
    for i in pids:
        
        prod_bf = array_of_bfs[i]
        unique_bfs.append(prod_bf)

    merged_bfs = []
    for j in unique_bfs:


        if merged_bfs != []:
            for k in merged_bfs:
                
                if j[1].compare_bits(k[1]) == True:
                    k.append(j[0])
                    k[2] + 1

                else:
                    j.append(1)
                    merged_bfs.append(j)

        elif merged_bfs == []:
            j.append(1)
            merged_bfs.append(j)

    print(merged_bfs)
    '''


def prod_check_arrays(array_of_bf, num_of_producers, ratio):
    '''
    Each prod gens new random list
    checks each associated bf 
    if a peer appears in >= 50% of lists then tick them off

    Create a grouping function 

    '''
    failed_run = 0

    for i in range(num_of_producers):
        
        
        #create array in the form [[pid_0, 0] . . . [pid_n, 0]]
        check_list = []
        for peer in range(num_of_producers): 
            check_list.append([peer, 0])


        pids = random.sample(range(num_of_producers), return_ratio(num_of_producers, ratio))
        
        for j in pids:
            # Load the bloom filter for each of the peers that a prod has recieved a bf from.
            prod_bf = array_of_bf[j]
            
            

            for k in range(num_of_producers):
                if prod_bf[1].check(k) == True:
                    check_list[k][1] += 1
        
        final_list = []
        for prods in range(num_of_producers):
            val = int(check_list[prods][1])
            if val > int(num_of_producers/2):
                final_list.append(check_list[prods][0])
        
        
        
        if len(final_list) < len(range(num_of_producers)):
            failed_run += 1

    return(failed_run)