import bloom_filter as blf
import numpy as np
import math
import multiprocessing as mp
from itertools import chain


def evaluate_bfs(list_bfs, num_of_producers, correct_update_ids, bf_to_compare):
    wrong_update_ids = np.zeros(num_of_producers-len(correct_update_ids), int)
    for i in range(num_of_producers-len(correct_update_ids)):
        wrong_update_ids[i] = len(correct_update_ids)+i
    #result = []
    #result_out = 0
    result_match_bf = 0
    fb_num = 0
    #itt = 0
    for id_bf in list_bfs:
        count_good = 0
        count_bad = 0


        for it in correct_update_ids:
            if id_bf.check(it):
                count_good += 1
        for it in wrong_update_ids:
            if id_bf.check(it):
                count_bad += 1

        if bf_to_compare.compare_bits(id_bf):
            result_match_bf = result_match_bf + 1
            #print("matching item ", itt, " : ", [count_good, count_bad])
            if count_bad != 0:
                fb_num = count_bad
        #itt = itt + 1

        #if count_good == len(correct_update_ids) and count_bad == 0:
            #result_out = result_out + 1
        #result.append([count_good, count_bad])
    return result_match_bf, fb_num


def count_matching_bfs(list_bfs, bf_to_compare):
    count_match = 0
    it = 0
    #print("The real BF has ", sum(bf_to_compare.bit_array), " bits to 1")
    for id_bf in list_bfs:

        #print("The  BF ",id_bf," has ", sum(id_bf.bit_array), " bits to 1")
        if bf_to_compare.compare_bits(id_bf):
            print("matching ", it )
            count_match += 1
        it = it + 1
    return count_match


def create_bf_from_list(num_of_producers, correct_producers_id):
    bf = blf.BloomFilter(num_of_producers)
    for id in correct_producers_id:
        bf.add(id, False)
    return bf


def is_majority_found(collected_quantities_id, correct_producers_id, num_collected_quantities):
    collected_correct_quantities_id = set(collected_quantities_id).intersection(correct_producers_id)
    ratio_maj = len(collected_correct_quantities_id)/num_collected_quantities
    ratio_threshold = 0.5 + 4.22 * math.sqrt(ratio_maj * (1 - ratio_maj) / num_collected_quantities)
    isMajFound = True if ratio_maj > ratio_threshold else False
    return isMajFound


def create_list_of_bfs(num_of_producers, collected_quantities_ids, correct_producers_id):

    producers_bf = []

    for i in range(num_of_producers):
        #print("producer ", i)
        collected_quantities_id = collected_quantities_ids[i, :]
        isMajFound = is_majority_found(collected_quantities_id, correct_producers_id, len(collected_quantities_id))

        collected_quantities_bf = blf.BloomFilter(num_of_producers)

        if isMajFound:
            collected_correct_quantities_id = set(collected_quantities_id).intersection(correct_producers_id)
            for j in collected_correct_quantities_id:
                collected_quantities_bf.add(j, False)

        producers_bf.append(collected_quantities_bf)

    return producers_bf


def create_merged_bf_pool(ind_prod, num_of_producers, collected_candidates_ids, correct_update_ids, lj_prod_bfs,
                          merging_threshold):

    collected_candidates_bf = blf.BloomFilter(num_of_producers)
    collected_candidates_id = collected_candidates_ids[ind_prod, :]

    isMajFound = is_majority_found(collected_candidates_id, correct_update_ids, len(collected_candidates_id))

    if isMajFound:
        #print("producer ", ind_prod, "has a majority ")
        collected_correct_candidates_id = set(collected_candidates_id).intersection(correct_update_ids)
        # Loop over the ID of each producer. for each producer, check in how many BFS it is found in these ID.
        # If above threshold, ass the ID of the producer to a new BF.
        '''for id_prod in range(num_of_producers):
            count_id = 0
            for id_cand in collected_correct_candidates_id:
                id_bf = lj_prod_bfs[id_cand]
                if id_bf.check(id_prod):
                    count_id += 1
            if count_id > merging_threshold:
                collected_candidates_bf.add(id_prod, False)
                #print("found producer ", id_prod, "in ", count_id, " BFs")
        '''
        #alternatively, merge the BF with count:
        collected_quantitities_merged_bf = blf.BloomFilter(num_of_producers)
        for id_cand in collected_correct_candidates_id:
            collected_quantitities_merged_bf.merge_additive(lj_prod_bfs[id_cand])
        for id_prod in range(num_of_producers):
            if collected_quantitities_merged_bf.check_additive(id_prod, merging_threshold):
                collected_candidates_bf.add(id_prod, False)
                #ind_prod == 5 and
                #if id_prod not in correct_update_ids:
                #    print("Passing a wrong id (",id_prod,") into merged BF")
                #collected_candidates_bf.add_additive(id_prod)
        #print("The BF or producer ",ind_prod," has ", sum(collected_candidates_bf.bit_array), " bits to 1")

        #print("Producer ",ind_prod, " BF merged : ", collected_quantitites_merged_bf.num_array)

    return collected_candidates_bf


def merge_bfs_with_threshold_pool(num_of_producers, collected_candidates_ids, correct_update_ids, lj_prod_bfs,
                                  merging_threshold):

    pool = mp.Pool(mp.cpu_count())

    merged_producers_bf = pool.starmap(create_merged_bf_pool, [(i, num_of_producers, collected_candidates_ids,
                                                                correct_update_ids, lj_prod_bfs, merging_threshold)
                                       for i in range(len(correct_update_ids))])
    pool.close()

    return merged_producers_bf


