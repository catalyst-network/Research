import json
import worker_pool as wp


def gen_big_rand(list_of_rands):
    '''
        This finction creates big_rand. This is the global random number that the users
        random numbers are compared to in order to determine which workers are selected 
        as producers for that cycle. 

        It is calculated by extracting the random numbers from the users profiles and 
        adding together (around a modulo point)
    '''
    big_rand = 0
    for rand in list_of_rands:
        big_rand = (big_rand + rand) % (2**512)
    return (big_rand)


def check_fees(prod_info):

    """
        Simple bool to check whether user has paid fees
    """

    if prod_info == True:
        return (True)
    else:
        return(False)


def check_corr_rando(rand_no, personal_rand, prev_ledg_update):
    """
        Check to see whether workers have generated their random numbers fairly i.e. used the
        previous ledger cycle hash
    """

    combined_rand = bytes(str((personal_rand + prev_ledg_update) % 2**512),'utf-8') 
    combined_rand = wp.give_rand_no(combined_rand)
    if combined_rand == rand_no:
        return True
    else:
        return False


def find_prod_ids(dist_list, no_prod):
    """
        Finds the users with the closest random numbers to the global random.
        This gives us the list of producers for the next cycle.
    """
    list_of_prod = []
    for worker in dist_list:
        if len(list_of_prod) <= no_prod:
            list_of_prod.append(worker)
        else:
            for i in list_of_prod:
                if i[1] > worker[1]:
                    list_of_prod.remove(i)
                    list_of_prod.append(worker)
                    worker = i
                else:
                    continue
    print(list_of_prod)


def get_dist_from_big_rand(global_rand, list_of_prods):
    """
        Calculates the distance from the global random number. This must take into account the modulo points of the set. 
        It calculates which is a smaller value global random - workers random mod 2^512 or vice versa. Then extracts that
        number and forms a list with the PID of the worker
    """
    
    distance_list = []
    
    for prod_info in list_of_prods:
        check_list = [prod_info[0]]
        if (global_rand - prod_info[1]) % (2**512) > (prod_info[1] - global_rand )% (2**512):
            check_list.append((prod_info[1] - global_rand) % (2**512))
        else:
            check_list.append((global_rand - prod_info[1]) % (2**512))
        distance_list.append(check_list)
    return(distance_list)


def run_sc(no_prods, prev_ledg_update, list_of_prods, no_prod):

    """
        Main function for the smart contract sets out the steps as follows 
        1) for each worker check that they have paid fees 
        2) for each worker check that they performed the random number gen fairly 
        3) Create the global random number 
        4) Calculate the distance of the workers random to the global random 
        5) calculate which workers were closest 
    """
    
    list_of_rands = []

    for prod_info in list_of_prods:
        if check_fees(prod_info[3]) == True:
            print("Producer ", prod_info[0], "paid their fees")
        elif check_fees(prod_info[3]) == False:
            print("Producer ", prod_info[0], "did not pay their fees")
            continue
        
        if check_corr_rando(prod_info[1], prod_info[2], prev_ledg_update) == True:
            print("Producer ", prod_info[0], "has a well formed random")

        elif check_corr_rando(prod_info[1], prod_info[2], prev_ledg_update) == False:
            print("Producer ", prod_info[0], "failed to produce a well formed random")
            continue

        list_of_rands.append(prod_info[1])
    global_rand = gen_big_rand(list_of_rands)
    if global_rand == 0:
        print("Something went wrong global_rand was 0")
    dist_list = get_dist_from_big_rand(global_rand, list_of_prods) 
    find_prod_ids(dist_list, no_prod)
