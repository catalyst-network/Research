'''
Generate worker pool (list of n prods)
for each prod in list add a bloom filter with ratio x random other producers added to the bloom filter
Each prod should then check the bloom filter from ratio x other producers  
    Check should be, for each prod in full list prods check that they are in the bf
    if they are increment one 
    if not do not 
    if the number they are in is more than x*n/2 lists then add them to the bf 
At end will have a complete bf for each prod 
For each complete bf check how many elements have been added. If == n correct 
If < n print how many and why it failed.
'''

import gen_bf as gen
import numpy as np
import csv


if __name__ == '__main__':

    

    min_prop_ratio = 0.75
    max_prop_ratio = 0.81
    min_num_producers = 100
    max_of_producers = 200
    tests = 100
    full_list_fails = []
    with open('fail_data.csv', mode='w') as fail_data:
        fail_writer = csv.writer(fail_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fail_writer.writerow(["No. Runs", "No. Fails", "No. Prods", "Ratio", "% Fail"])
        for j in range(min_num_producers, max_of_producers, 100):

            for k in np.arange(min_prop_ratio, max_prop_ratio, 0.01):
                total_fail = 0
                list_of_fails = []  
                print("Begining test with", tests, "runs at mp ratio", k, "and", j, "producers")
                for i in range(tests):
                
                    
        
                    #print("begin run", i)

                    prod_bfs = gen.create_array_of_bf(j, k) 


                    failed_run = gen.prod_check_arrays(prod_bfs, j, k)
                    total_fail += failed_run
                    #print("run", i, "had", failed_run, "failures")
                list_of_fails.append(tests)
                list_of_fails.append(total_fail)
                list_of_fails.append(j)
                list_of_fails.append(k)
                list_of_fails.append((total_fail / (j * tests)) * 100)
                print(list_of_fails)
                
                fail_writer.writerow([list_of_fails])
