import bloom_filter as bf
import random
import numpy
import multiprocessing as mp


def make_bfs(num_of_producers, prop_bf):
    
    seed_init = random.randint(1, 10000)
    bf.init_seed(seed_init)

    global_bf = bf.BloomFilter(num_of_producers)

    list_of_bfs = []

    num_prod_in_list = int(num_of_producers * prop_bf)
    num_item_added_to_bf = int(num_prod_in_list * prop_bf)
    list_of_corr_prod = [i for i in range(num_prod_in_list)]
    
    for i in range(num_of_producers):
        prod_list = random.sample(list_of_corr_prod, num_item_added_to_bf)
        prod_bf = global_bf
        for j in prod_list:
            prod_bf.add(j, False)
        list_of_bfs.append(prod_bf)
    
    return list_of_bfs



def merge_bfs(list_of_bfs, num_prod, prop_bf):
    num_bf_merge = int(float(num_prod) * prop_bf)
    
    list_of_merged_bfs = []
    for i in range(num_prod):
        prod_list = random.sample([j for j in range(num_prod)], num_bf_merge)
        merging_bf = list_of_bfs[i]
        
        for l in prod_list: 
            merging_bf.merge(list_of_bfs[l])
           
        list_of_merged_bfs.append(merging_bf)
    return list_of_merged_bfs



def gen_output(merged_bfs):
    print("In Progress")


def setup_initial_parameters():

    num_of_producers = 100
    prop_of_bf = 0.75

    return num_of_producers, prop_of_bf


def setup_step_parameters():

    step_producer = 100
    step_rate = 0.01
    end_producer = 200
    end_rate = 0.8

    return step_producer, step_rate, end_producer, end_rate



def itterate_bfs(num_of_producers, num_runs, prop_bf, fp_rate, hash_count):
    #num_runs = 200
    seed_init = random.randint(1, 10000)
    bf.init_seed(seed_init)
    bf.gb_fp_prob = fp_rate
    bf.gb_hash_count = hash_count
    global_bf = bf.BloomFilter(num_of_producers)
    num_prod_in_list = int(num_of_producers * prop_bf)
    fp_count = 0
    num_false_prod = num_of_producers - num_prod_in_list
   
    list_of_corr_prod = [i for i in range(num_prod_in_list)]
   
    for j in list_of_corr_prod:
        global_bf.add(j, False)
    

    print ("Run:",num_of_producers," producers, with ",num_false_prod," wrong prod for ",num_runs,"cycles, BF = [",fp_rate, ", ",hash_count, ", ",global_bf.size,"]")
    
    pool = mp.Pool(mp.cpu_count())

    fp_counts = pool.starmap(check_id_bf, [(num_of_producers+i, global_bf, seed_init) for i in range(num_runs*num_false_prod)])
    
    pool.close()

    fp_count = sum(fp_counts)

    '''for m in range(num_runs*num_false_prod):
        #bad_list = random.sample(range(100000),num_false_prod)
        for l in bad_list:
        if global_bf.check(random.randint(1,100000)) == True:
            fp_count += 1
    '''

    #sum of list fp_count
    print("False Positive ", fp_count, " --> <", fp_count / num_runs, ">")
    return fp_count

def check_id_bf(id, global_bf, seed_init):

    #bf.init_seed(seed_init)
    return global_bf.check(id, seed_init)

if __name__ == '__main__':

    #num_prod, prop_bf = setup_initial_parameters()
    #step_producer, step_rate, end_producer, end_rate = setup_step_parameters()

    runs = 30
    num_prod = 300
    prop_bf = 0.75
    fp_rate = 0.02
    hash_count = 5
    num_hyp = 50
    total_count = numpy.zeros(num_hyp, float)
    for hyp in range(num_hyp):
        count_temp = itterate_bfs(num_prod, runs, prop_bf, fp_rate, hash_count)
        total_count[hyp] = count_temp / runs 
    print(" Result : <",total_count.mean(), " +- ", total_count.std(), ">")
    #list_of_bfs = make_bfs(num_prod, prop_bf)
    #print (list_of_bfs)

    #merged_bfs = merge_bfs(list_of_bfs, num_prod, prop_bf)

    #output = gen_output(merged_bfs, num_prod, prop_bf)