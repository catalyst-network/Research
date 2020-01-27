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
    
    for i in range(num_of_producers):
        global_bf = create_global_bf(num_of_producers)
        pids = random.sample(range(num_of_producers), return_ratio(num_of_producers, ratio))
        for j in pids:
            global_bf.add(j, False)
        array_of_bf.append([i, global_bf])
         

    return(array_of_bf)


if __name__ == '__main__':

    m_prop_ratio = 0.75
    num_of_producers = 10 
    bf_array = create_array_of_bf(num_of_producers, m_prop_ratio)
    print (bf_array)