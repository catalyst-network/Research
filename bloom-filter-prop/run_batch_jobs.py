import multiprocessing as mp
import generate_outputs as re
import bloom_filter as bf
import random
import create_consensus_outputs as cco
import argparse
import os.path
import multiprocessing as mp
import excel_file_manipulation as ma
import numpy


#This should be called from somewhere else where we clean the folder structure (pre-process) and later on post-process data


def setup_initial_parameters():

    spec_init = {
        'num_of_producers': 100,
        'prop_correct_producers': 0.78,
        'prop_collected_quantities': 0.78,
        'prop_collected_candidates': 0.78,
        'prop_collected_votes': 0.78
    }

    return spec_init


def setup_step_parameters():

    step_producer = 100
    step_rate = 0.01

    end_producer = 200
    end_rate = 0.8

    return step_producer, step_rate, end_producer, end_rate

def setup_bloom_filter(num_prod):

    bf.gb_fp_prob = 0.001
    bf.gb_hash_count = 4

    seed_init = random.randint(1, 10000)
    bf.init_seed(seed_init)
    #print("Seed: ", bf.gb_rand)

    bf_sample = bf.BloomFilter(num_prod)

    #print("Parameter for Bloom Filter:"
    #      " [n = ", num_prod, ", "
    #      " k = ", bf.gb_hash_count, ", "
    #      " p = ", bf.gb_fp_prob, ", "
    #      " m = ", bf_sample.get_size(num_prod, bf.gb_fp_prob), "]")
    #print("NB: optimal k = ", bf_sample.get_hash_count(bf_sample.get_size(num_prod, bf.gb_fp_prob), num_prod))


def run_multiprocessing(spec_init, step_producer, end_producer, step_rate, end_rate, runs, jobs):

    for __ in range(jobs):
        mp.Process(target=re.run_exp, args=(spec_init, step_producer, end_producer, step_rate, end_rate, runs)).start()



def run_exp(spec, step_producer, end_producer, step_rate, end_rate, runs):

    process_id = os.getpid()

    start_producer = spec['num_of_producers']
    start_rate = spec['prop_correct_producers']
    for ind_p in range(start_producer, end_producer+1, step_producer):
        spec['num_of_producers'] = ind_p
        spec['prop_correct_producers'] = start_rate
        spec['prop_collected_quantities'] = start_rate
        spec['prop_collected_candidates'] = start_rate
        spec['prop_collected_votes'] = start_rate
        while spec['prop_correct_producers'] < end_rate:
            threshold_cn = int(spec['prop_collected_quantities'] * spec['num_of_producers'])
            print("Generating result for (", ind_p, ", ", spec['prop_correct_producers'], ", ",
                  spec['prop_collected_quantities'], ", threshold = ", threshold_cn, ", runs = ", runs, ")")
            results = numpy.zeros(runs, int)
            fps = numpy.zeros(runs, int)
            for it_r in range(runs):
                setup_bloom_filter(spec['num_of_producers'])
                res_temp, fp_temp = cco.create_consensus_output(**spec)
                results[it_r] = res_temp
                fps[it_r] = fp_temp
            print(" Results: mean, median, #=Cn, #>0.5*P, <fp>")
            print(numpy.mean(results), ", ", numpy.median(results), ", ", numpy.count_nonzero(results == threshold_cn),
                  ", ", numpy.count_nonzero(results > (0.5 * spec['num_of_producers'])), ", ", numpy.mean(fps))

                    #= numpy.array([cco.create_consensus_output(**spec) for _ in range(runs)])

                #outputs = get_result_output(spec['num_of_producers'], spec['prop_correct_producers'],
                #                            spec['prop_collected_votes'],
                #                            runs=runs, results=results)

                #name = "excel/Result_simulation_security_ledger_update" + str(process_id) + ".xlsx"

                #ma.write_results_to_excel_file(spec, runs=runs, output=outputs, process_id=process_id,path_name=name)

            spec['prop_collected_quantities'] *= 100
            spec['prop_collected_quantities'] += step_rate * 100
            spec['prop_collected_quantities'] /= 100
            spec['prop_collected_candidates'] = spec['prop_collected_quantities']
            spec['prop_collected_votes'] = spec['prop_collected_quantities']
            spec['prop_correct_producers'] = spec['prop_collected_quantities']



'''


def run_exp(spec, step_producer, end_producer, step_rate, end_rate, runs):

    process_id = os.getpid()

    start_producer = spec['num_of_producers']
    start_rate = spec['prop_correct_producers']
    for ind_p in range(start_producer, end_producer+1, step_producer):
        spec['num_of_producers'] = ind_p
        spec['prop_correct_producers'] = start_rate
        while spec['prop_correct_producers'] < end_rate:
            spec['prop_collected_quantities'] = start_rate
            spec['prop_collected_candidates'] = start_rate
            spec['prop_collected_votes'] = start_rate
            threshold_cn = int(spec['prop_collected_quantities'] * spec['num_of_producers'])
            while spec['prop_collected_quantities'] <= end_rate:
                print("Generating result for (", ind_p, ", ", spec['prop_correct_producers'], ", ",
                      spec['prop_collected_quantities'], ", threshold = ", threshold_cn, ")")
                results = numpy.zeros(runs, int)
                fps = numpy.zeros(runs, int)
                for it_r in range(runs):
                    setup_bloom_filter(spec['num_of_producers'])
                    res_temp, fp_temp = cco.create_consensus_output(**spec)
                    results[it_r] = res_temp
                    fps[it_r] = fp_temp
                print(" Results:")
                print("mean : ", numpy.mean(results))
                print("median : ", numpy.median(results))
                print(" # = Cn : ", numpy.count_nonzero(results == threshold_cn))
                print(" # > 0.5*P : ", numpy.count_nonzero(results > (0.5 * spec['num_of_producers'])))
                print("Average fp : ", numpy.mean(fps))

                    #= numpy.array([cco.create_consensus_output(**spec) for _ in range(runs)])

                #outputs = get_result_output(spec['num_of_producers'], spec['prop_correct_producers'],
                #                            spec['prop_collected_votes'],
                #                            runs=runs, results=results)

                #name = "excel/Result_simulation_security_ledger_update" + str(process_id) + ".xlsx"

                #ma.write_results_to_excel_file(spec, runs=runs, output=outputs, process_id=process_id,path_name=name)

                spec['prop_collected_quantities'] *= 100
                spec['prop_collected_quantities'] += step_rate * 100
                spec['prop_collected_quantities'] /= 100
                spec['prop_collected_candidates'] = spec['prop_collected_quantities']
                spec['prop_collected_votes'] = spec['prop_collected_quantities']
                print(results)
            spec['prop_correct_producers'] *= 100
            spec['prop_correct_producers'] += step_rate * 100
            spec['prop_correct_producers'] /= 100
            spec['prop_correct_producers'] = int(spec['prop_correct_producers'] * 10000)/10000
'''
if __name__ == '__main__':

    spec = setup_initial_parameters()
    step_producer, step_rate, end_producer, end_rate = setup_step_parameters()

    #Number of tests per set of parameters
    runs = 10

    run_exp(spec, step_producer, end_producer, step_rate, end_rate, runs)

    #Number of processes per set of parameters
    #jobs = 1
    #Total number of jobs per set of parameters: runs*jobs


    '''run_multiprocessing_runs = mp.Process(target=run_multiprocessing, args=(spec, step_producer, end_producer,
                                                                            step_rate, end_rate, runs, jobs))
    run_multiprocessing_runs.start()
    run_multiprocessing_runs.join()'''
    #for i in range(runs):
    #    setup_bloom_filter(spec['num_of_producers'])
    #    re.run_test(spec)
