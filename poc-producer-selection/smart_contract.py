import worker_pool as wp


def check_fees(prod_info):

    """
        Simple bool to check whether user has paid fees
        This function is currently redundent as it could as easily be checked earlier, 
        will update to check that the workers ammount paid is correct
    """
    if prod_info == True:

        return (True)

    else:

        return(False)


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



def check_corr_rando(rand_no, personal_rand, prev_ledg_update):
    """
        Check to see whether workers have generated their random numbers fairly i.e. used the
        previous ledger cycle hash
    """

    combined_rand = bytes(str((personal_rand + prev_ledg_update) % 2**512),'utf-8') 
    combined_rand = wp.gen_rand_no(combined_rand)

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

        if len(list_of_prod) < no_prod:
            list_of_prod.append(worker)

        else:

            for i in list_of_prod:

                if i[1] > worker[1]:
                    list_of_prod.remove(i)
                    list_of_prod.append(worker)
                    worker = i

                else:

                    continue
    PIDs = []
    for i in list_of_prod:
        PIDs.append(i[0])
    PIDs.sort()
    return (PIDs)



def get_dist_from_big_rand(global_rand, list_of_workers):
    """
        Calculates the distance from the global random number. This must take into account the modulo points of the set. 
        It calculates which is a smaller value global random - workers random mod 2^512 or vice versa. Then extracts that
        number and forms a list with the PID of the worker
    """
    
    distance_list = []
    
    for worker_info in list_of_workers:
        check_list = [worker_info[0]]

        if (global_rand - worker_info[1]) % (2**512) > (worker_info[1] - global_rand )% (2**512):
            check_list.append((worker_info[1] - global_rand) % (2**512))

        else:
            check_list.append((global_rand - worker_info[1]) % (2**512))
        distance_list.append(check_list)

    return(distance_list)


def run_sc(no_prods, prev_ledg_update, list_of_workers, no_prod):

    """
        Main function for the smart contract sets out the steps as follows 
        1) for each worker check that they have paid fees 
        2) for each worker check that they performed the random number gen fairly 
        3) Create the global random number 
        4) Calculate the distance of the workers random to the global random 
        5) calculate which workers were closest 
    """
    
    list_of_rands = []

    for worker_info in reversed(list_of_workers):
        print(worker_info[0])
        if check_fees(worker_info[3]) == True:
            print("Worker ", worker_info[0], "paid their fees")

        elif check_fees(worker_info[3]) == False:
            
            print("Worker ", worker_info[0], "did not pay their fees")
            list_of_workers.remove(worker_info)
            
            continue
            
            #This part is now skipping over the proceeding producer if the above chack fails    
        
        if check_corr_rando(worker_info[1], worker_info[2], prev_ledg_update) == True:
            print("Worker ", worker_info[0], "has a well formed random")
            

        elif check_corr_rando(worker_info[1], worker_info[2], prev_ledg_update) == False:
            print("Worker ", worker_info[0], "failed to produce a well formed random")
            list_of_workers.remove(worker_info)

            continue
            

        list_of_rands.append(worker_info[1])

    global_rand = gen_big_rand(list_of_rands)

    if global_rand == 0:
        print("Something went wrong global_rand was 0")

    dist_list = get_dist_from_big_rand(global_rand, list_of_workers) 
    PIDs = find_prod_ids(dist_list, no_prod)

    for producer in PIDs:
        print ("Worker -->", producer, "has been selected as a producer for this cycle")