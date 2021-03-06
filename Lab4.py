# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 12:26:38 2018

@author: danie
"""

# helper function to create a list out of the file for easier hash insertions
def build_list(file):
    alist = []
    
    # opens and reads file line by line
    with open(file) as f:
        alist = f.read().splitlines()
      
    # creates linked list of the word and embeddings that i'll put into the table    
    for i in range(len(alist)):
        temp_a = alist[i].split(" ")
        temp_w = temp_a[0]
        
        if temp_w.isalpha():
            embedding = []
            
            for j in range(len(temp_a -1)):
                embedding.append(temp_a[j+1])
                
    return alist

# returns the index at which the words needs to be inserted
def hashing_function(index): return index % 25000

#inserts based on the index calculated by the hashing function
def insert(atable, hash_val, value): atable[hashing_function(hash_val)].append(value)

# Searches for an item with matching word in the hash table.
# Returns the item if found, or None if not found.
def search(atable, index, word):
    
    # get the bucket list where this word would be.
    bucket = hashing_function(index)
    bucket_list = atable[bucket]

    # search for the word in the bucket list
    if word in bucket_list:
        
        # find the item's index and return the item that is in the bucket list.
        word_index = bucket_list.index(index)
        return bucket_list[word_index]
    else:
        # the word is not found.
        return None
        
# function that builds a table with the list of words
def build_table(alist):
    hash_val = 0
    
    atable = [[None] for _ in range(25000)]
    
    for i in range(len(alist)):
        
        # word_val is the ascii value of the current word, which is needed to
        # determine what index it will be stored at
        word_val = calc_ascii_val(alist[i])
        
        # hash_val is the hashed value of the ascii value, the index where
        # the word will be stored
        hash_val = hashing_function(word_val)
        insert(atable, hash_val, alist[i])
        
    return atable

# function that reads the appendix file and calculates and returns the similarities
# in a list        
def read_appendix(file, atable):
    alist = []
    
    with open(file) as f:
        alist = f.read().splitlines()
        
    i = 0
    j = 0
    
    # splits the words in the list to compare
    for i in range(len(alist)):
        blist = alist[i].split(' ')
        sim_list = []
    
        # calculates the ascii value of the word in the appendix to search the hash table    
        for j in range(len(blist)):
            ascii_list = []
            ascii_list = calc_ascii_val(blist[j])
    
        # calls method that calculates the similarity
        sim_list[i] = calc_similarity(atable, ascii_list, blist)
    
    return sim_list

# function that calculates the similarity between the two words given in the appendix
def calc_similarity(atable, ascii_list, blist):
    word_list = []
    
    for i in range(len(ascii_list)):
        word_list[i] = search(atable, ascii_list[i], blist[i])
        
    sim_top = word_list[0].embedding * word_list[1].embedding()
    sim_bot = word_list[0].embedding().abs() * word_list[1].embedding().abs()
    sim = sim_top // sim_bot
        
    return sim
    
# function that calculates the ascii value for a given word
def calc_ascii_val(word):
    word_sum = 0
    
    for char in range(len(word)):
        word_sum += char.ord()
        
    return word_sum

def main():
    alist = build_list('glove.6B.50d.txt')
    atable = build_table(alist)
    blist = read_appendix('appendix.txt', atable)
    for i in range(len(blist)):
        print(blist[i])