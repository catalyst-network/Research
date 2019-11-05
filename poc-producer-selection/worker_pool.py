import hashlib as hash 
import random

def worker_info(PiD, last_ledger_value):

    """
    This generates the worker list, this includes 4 elements:
    - PID, this will be a number between 0 and the number of selected workers in the worker pool 
    - rand_no, this is the random number that is associated with the worker this is an int generated 
      from a hash of the user selected random int and the int of the hash of the previous ledger cycle
    - personal_rand, is the user selected random int
    - fee_paid, is a bool as to whether the fee has been paid 
    """

    work_info_list = []
    fee_paid = did_they_pay_fee()
    personal_rand = random.randint(1,2**512)
    combined_rand = bytes(str((personal_rand + last_ledger_value) % 2**512),'utf-8') 
    rand_no = give_rand_no(combined_rand)
    work_info_list.append(PiD)
    work_info_list.append(rand_no)
    work_info_list.append(personal_rand)
    work_info_list.append(fee_paid)
    #print(work_info_list)
    return (work_info_list)


def give_rand_no(combined_rand):

    """
    This function generates a randomised number after hashing an input. 
    """

    rand_no = hash.blake2b()
    rand_no.update(combined_rand)
    rand_no = rand_no.hexdigest()
    rand_no = int(rand_no, base=16)
    return (rand_no)



def did_they_pay_fee():
    odds = random.randint(0,9)
    if odds == 1:
        return False
    else:
        return True