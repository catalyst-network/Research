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

def create_list_of_bf(list_of_prod):
    prod_bfs = gen.create_array_of_bf(num_of_producers)

