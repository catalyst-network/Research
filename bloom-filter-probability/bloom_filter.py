import math
import mmh3
from bitarray import bitarray
import random

gb_fp_prob = 0.001
gb_hash_count = 5
#gb_seed = 1008
##random.seed(gb_seed)
#gb_rand = random.randint(0, 1000)




class BloomFilter(object):
    '''
    Class for Bloom filter, using murmur3 hash function
    '''


    def __init__(self, num_items):
        '''
        num_item : int
            Maximum number of items expected to be stored in bloom filter
        '''

        # False posible probability in decimal
        self.fp_prob = gb_fp_prob

        # Number of hash functions to use
        self.hash_count = gb_hash_count

        # Maximum number of items that should be stored in BF
        self.num_items = num_items

        # Size of bit array to use
        self.size = self.get_size(self.num_items, self.fp_prob)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        # initialize all integer bits as 0
        self.num_array = [0 for __ in range(self.size)]


    def manual_init(self, fp_prob, num_hash, num_items):
        '''
        num_item : int
            Maximum number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        num_hash : int
            Number of hash functions applied per item
        '''

        # False posible probability in decimal
        self.fp_prob = fp_prob

        # Number of hash functions to use
        self.hash_count = num_hash

        # Maximum number of items that should be stored in BF
        self.num_items = num_items

        # Size of bit array to use
        self.size = self.get_size(self.num_items, self.fp_prob)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        # initialize all integer bits as 0
        self.num_array = [0 for __ in range(self.size)]


    def auto_init(self, num_items):
        '''
        num_item : int
            Maximum number of items expected to be stored in bloom filter
        '''

        # Maximum number of items that should be stored in BF
        self.num_items = num_items

        # False possible probability in decimal
        self.fp_prob = gb_fp_prob

        # Number of hash functions to use
        self.hash_count = gb_hash_count

        # Size of bit array to use
        self.size = self.get_size(self.num_items, self.fp_prob)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        # initialize all integer bits as 0
        self.num_array = [0 for __ in range(self.size)]


    def add(self, item, unique):
        '''
        Add an item in the filter
        '''
        digests = []
        count_bit_used = 0
        #b_item = bytes(item*1000)

        b_item = bytes(item)

        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different

            digest = mmh3.hash(b_item, i) % self.size

            if self.bit_array[digest] == True:
                # print ("Bit {} (hash {}) already set to 1".format(digest,i))
                count_bit_used += 1
            digests.append(digest)
            # set the bit True in bit_array
        if unique == True:
            if count_bit_used == 0:
                for digest in digests:
                    self.bit_array[digest] = True
                return True
            '''else:
                print("Skipping this word: {} bits set to 1".format(count_bit_used))'''
        else:
            for digest in digests:
                self.bit_array[digest] = True
            return True
        return False


    def merge(self, bf2):
        '''
        merge two bloom filters (no bit counting)
        '''
        if self.size != bf2.size:
            print("Different BFs size: no comparison possible")
        else:
            for i in range(bf2.size):
                if (bf2.bit_array[i] == 1):
                    self.bit_array[i] = 1


    def merge_additive(self, bf2):
        '''
        merge two bloom filters (no bit counting)
        '''
        if self.size != bf2.size:
            print("Different BFs size: no comparison possible")
        else:
            for i in range(bf2.size):
                self.num_array[i] = self.num_array[i] + bf2.bit_array[i]


    def print_bf_bit(self, bit_i):
        print("Bit ", bit_i, " : ", self.bit_array[bit_i])


    def compare_bits(self, bf2):
        '''
        compare two bloom filters (no bit counting)
        '''
        if self.size != bf2.size:
            print("Different BFs size: no comparison possible")
            return False
        for i in range(self.size):
            if (self.bit_array[i] != bf2.bit_array[i]):
                return False
        return True


    def check_additive(self, item, threshold):
        '''
        Check for existence of an item in filter
        '''
        b_item = bytes(item*gb_rand)
        for i in range(self.hash_count):
            digest = mmh3.hash(b_item, i) % self.size
            if self.num_array[digest] < threshold:
                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True


    def print_item_bits(self, item):
        '''
        Check for existence of an item in filter
        '''
        b_item = bytes(item*gb_rand)
        str_out = "["
        for i in range(self.hash_count):
            digest = mmh3.hash(b_item, i) % self.size
            str_out += str(digest)
            if i < (self.hash_count-1):
                str_out += ", "
        str_out += "]"

        return str_out

    def check(self, item, gb_rand = 10000):
        '''
        Check for existence of an item in filter
        '''
        b_item = bytes(item*gb_rand)
        for i in range(self.hash_count):
            digest = mmh3.hash(b_item, i) % self.size
            if self.bit_array[digest] == False:
                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        '''
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        '''
        k = (m / n) * math.log(2)
        return int(k)

    @classmethod
    def set_size(self, m):
        '''
        Change the size of the bit array(m) to use,
        re-initialise the bits to 0
        '''

        # Size of bit array to use
        self.size = m

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

