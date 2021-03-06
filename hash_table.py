'''
Speaker recognition with custom Hash Table and Markov Model implementation

Egemen Pamukcu
'''
import copy

TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hashtable:

    def __init__(self, cells, defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.m = cells
        self.defval = defval
        self.table =[[None, copy.deepcopy(self.defval), True] for i in range(self.m)]
        self.n = 0

    def __getitem__(self, key):
        '''
        Similiar to the __getitem__ method for a Python dictionary, this function
        retrieves the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        index = self.hash_function(key)
        for i in range(self.m):
            hash_index = (i + index) % self.m
            k = self.table[hash_index][0]
            if not self.table[hash_index][2]:
                continue
            if k == None or k == key:
                return self.table[hash_index][1]
        return self.defval

    def __setitem__(self, key, value):
        '''
        Similiar to the __setitem__ method for a Python dictionary, this function
        will change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table, insert it with
        value "val".
        '''
        index = self.hash_function(key)
        for i in range(self.m):
            hash_index = (i + index) % self.m
            k = self.table[hash_index][0]
            valid = self.table[hash_index][2]
            if (k == None or k == key) and valid:
                self.table[hash_index][0] = key
                self.table[hash_index][1] = value
                if k == None:
                    self.n += 1
                break
        if self.n / self.m > TOO_FULL:
            self.rehash()

    def rehash(self):
        '''
        This function rehashes the hashtable by growing it by a constant rate and
        migrates the existing key-value pairs to the new table.
        '''
        self.m = self.m * GROWTH_RATIO
        self.old_table = self.table.copy()
        self.table =[[None, copy.deepcopy(self.defval), True] for i in range(self.m)]
        self.n = 0
        for row in self.old_table:
            if row[0] != None and row[2]:
                self.__setitem__(row[0], row[1])


    def __delitem__(self, key):
        '''
        Similiar to the __delitem__ method for a Python dictionary, this will
        "remove" the key-value pairing inside the hash table. Remember this function
        will not actually remove the key-value pairing from the table but "mark" for
        removal during a rehashing.

        If the key is not found inside the table. Then you must raise the following
        error:
             raise RuntimeError("Key was not found in table")
        '''
        index = self.hash_function(key)
        for i in range(self.m):
            hash_index = (i + index) % self.m
            k = self.table[hash_index][0]
            valid = self.table[hash_index][2]
            if k == key and valid:
                self.table[hash_index][2] = False
                self.n -= 1
                return

        raise RuntimeError("Key was not found in table")

    def __contains__(self, key):
        '''
        Similiar to the __contains__ method for a Python dictionary, this will
        return true if the key is inside the hash table; otherwise, if not
        then return false.
        '''
        index = self.hash_function(key)
        for i in range(self.m):
            hash_index = (i + index) % self.m
            valid = self.table[hash_index][2]
            k = self.table[hash_index][0]
            if k == key and valid:
                return True
        return False

    def keys(self):
        '''
        Returns a list with all the keys inside the hashtable.
        '''
        return [row[0] for row in self.table if row[0] != None and row[2]]

    def values(self):
        '''
        Returns a list with all the values inside the map.
        '''
        return [row[1] for row in self.table if row[0] != None and row[2]]

    def __len__(self):
        '''
           Returns the number key-value pairings inside the hashtable.
        '''
        return self.n

    def hash_function(self, string, k=37):
        '''
        Finds the appropriate hashtable index for a given string using using
        k = 37 as default.
        '''
        r = ord(string[0]) % self.m
        for i in string[1:]:
            r = (k * r + ord(i)) % self.m
        return r