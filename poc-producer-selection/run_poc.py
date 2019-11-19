import worker_pool as wp
import smart_contract as sc

def run_PoC():
    """
    Runs the PoC. Change vairiables here:
    seed = bytes of a string (any string can be input)
    no_worker = the nuber of nodes in the worker pool
    no_prod = Number of producer nodes to be selected from the worker pool
    """
    seed = bytes("Catalyst",'utf-8')
    prev_ledg_update = wp.gen_rand_no(seed)
    no_worker = 100000
    no_prod = 500

    list_of_workers = wp.setup_worker_lists(no_worker, prev_ledg_update)
    sc.run_sc(no_worker, prev_ledg_update, list_of_workers, no_prod)

if __name__ == '__main__':
    run_PoC()