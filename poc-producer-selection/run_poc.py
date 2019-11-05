import worker_pool as wp
import smart_contract as sc

seed = bytes("Catalyst",'utf-8')
prev_ledg_update = wp.give_rand_no(seed)
no_worker = 100
no_prod = 3

list_of_prods = []

for PiD in range(no_worker):
    
    work_info_list = wp.worker_info(PiD, prev_ledg_update)
    list_of_prods.append(work_info_list)


sc.run_sc(no_worker, prev_ledg_update, list_of_prods, no_prod)