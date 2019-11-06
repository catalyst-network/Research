import worker_pool as wp
import smart_contract as sc

def run_prod_selection():
    seed = bytes("Catalyst",'utf-8')
    prev_ledg_update = wp.give_rand_no(seed)
    no_worker = 10
    no_prod = 5

    list_of_workers = wp.setup_worker_lists(no_worker, prev_ledg_update)
    sc.run_sc(no_worker, prev_ledg_update, list_of_workers, no_prod)

if __name__ == '__main__':
    run_prod_selection()