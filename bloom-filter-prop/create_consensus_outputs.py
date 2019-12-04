import numpy
import math
import random
from itertools import chain
import create_bfs as bf
import time


def generate_collected_data_id_lists(num_producers, num_collected_data):
    list_ids = numpy.zeros((num_producers, num_collected_data), int)

    for i in range(num_producers):
        list_ids[i, 0] = i
        list_ids[i, 1:num_collected_data] = random.sample(list(chain(range(0, i), range(i + 1, num_producers))),
                                                          num_collected_data - 1)

    return list_ids


def exec_construction_phase(num_of_producers, prop_correct_producers):

    num_of_correct_updates = math.floor(prop_correct_producers * num_of_producers)

    # C_n
    correct_update_ids = numpy.zeros(num_of_correct_updates, int)

    for i in range(num_of_correct_updates):
        correct_update_ids[i] = i

    return correct_update_ids


def exec_campaigning_phase(num_of_producers, correct_update_ids, prop_collected_quantities):

    num_of_collected_quantities = math.floor(prop_collected_quantities * num_of_producers)

    collected_quantities_ids = generate_collected_data_id_lists(num_of_producers, num_of_collected_quantities)

    # print("list of collected quantities ", collected_quantities_ids)

    lj_prod_bfs = bf.create_list_of_bfs(num_of_producers, collected_quantities_ids, correct_update_ids)

    return lj_prod_bfs


def exec_voting_phase(num_of_producers, correct_update_ids, prop_collected_candidates, lj_prod_bfs):


    num_of_collected_candidates = math.floor(prop_collected_candidates * num_of_producers)

    merging_threshold_prod = num_of_collected_candidates * 0.51  # amend later

    collected_candidates_ids = generate_collected_data_id_lists(num_of_producers, num_of_collected_candidates)

    ln_prod_bfs = bf.merge_bfs_with_threshold_pool(num_of_producers, collected_candidates_ids, correct_update_ids,
                                                   lj_prod_bfs, merging_threshold_prod)

    return ln_prod_bfs


def create_consensus_output(num_of_producers, prop_correct_producers, prop_collected_quantities,
                            prop_collected_candidates,
                            prop_collected_votes):


    # construction phase:
    # input : num_of_producers, prop_correct_producers
    # output : correct_update_ids
    correct_update_ids = exec_construction_phase(num_of_producers, prop_correct_producers)
    # print("list of correct producers", correct_update_ids)

    # campaigning phase:
    # input : num_of_producers, correct_update_ids, prop_collected_quantities
    # out: list of BFs associated to each lj_prod
    starttime = time.time()
    lj_prod_bfs = exec_campaigning_phase(num_of_producers, correct_update_ids, prop_collected_quantities)
    #print("Campaigning: ", time.time() - starttime, " seconds")

    # voting phase:
    # input : num_of_producers, correct_update_ids, prop_collected_candidates, lj_prod_bfs
    # output: list of BFs associated to each ln_prod
    starttime = time.time()
    ln_prod_bfs = exec_voting_phase(num_of_producers, correct_update_ids, prop_collected_candidates, lj_prod_bfs)
    #print("Voting: ", time.time() - starttime, " seconds")

    cn_bf = bf.create_bf_from_list(num_of_producers, correct_update_ids)

    #count_good_bf = bf.count_matching_bfs(ln_prod_bfs, cn_bf)
    #print("Good BF count: ", count_good_bf)
    #For each producer, number of good and wrong producer
    starttime = time.time()

    res_match, fb_num = bf.evaluate_bfs(ln_prod_bfs, num_of_producers, correct_update_ids, cn_bf)
    #print("Output: ", res_match, " (", fb_num, ")")

    return res_match, fb_num
    #print(time.time() - starttime, " seconds")
    #print("Output: ", list_pos_bf)

    #bf0 = ln_prod_bfs[0]

