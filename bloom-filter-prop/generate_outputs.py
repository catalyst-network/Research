import numpy
import create_consensus_outputs as cco
import argparse
import os.path
import multiprocessing as mp
import excel_file_manipulation as ma


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

            while spec['prop_collected_quantities'] <= end_rate:
                print("Generating result for (", ind_p, ", ", spec['prop_correct_producers'], ", ",
                      spec['prop_collected_quantities'], ")")
                results = numpy.array([cco.create_consensus_output(**spec) for _ in range(runs)])

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

            spec['prop_correct_producers'] *= 100
            spec['prop_correct_producers'] += step_rate * 100
            spec['prop_correct_producers'] /= 100
            spec['prop_correct_producers'] = int(spec['prop_correct_producers'] * 10000)/10000



def run_test(spec):

    start_producer = spec['num_of_producers']
    start_rate = spec['prop_correct_producers']

    spec['prop_collected_quantities'] = start_rate
    spec['prop_collected_candidates'] = start_rate
    spec['prop_collected_votes'] = start_rate

    #print("Generating result for (", start_producer, ", ", spec['prop_correct_producers'], ", ",
    #      spec['prop_collected_quantities'], ")")
    cco.create_consensus_output(**spec)
    #output the results. Count cumulative run where out = Cn, out > 0.5*P, out includes fp.

