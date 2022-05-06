#!/usr/bin/python
# -*- coding: utf-8 -*-
from bloomfilter import BloomFilter
import sys
bf = BloomFilter(size=line_count, fp_prob=1e-16)

def count_lines(file):
	return sum(1 for line in open(file, 'r'))


def add_to_bf(file, nom, bf_filter):
    i = 0
    line_10 = 100000
    f = open(file)
    while i < nom:
        if line_10 == i:
            print("Total line ->" + str(line_10), end='\r')
            line_10 += 100000
        
        i += 1
    f.close()





if __name__ == "__main__":

    if len (sys.argv) < 3:
        print ("Mistake. Too few options.")
        sys.exit (1)

    if len (sys.argv) > 3:
        print ("Mistake. Too few options.")
        sys.exit (1)

    file_txt = sys.argv[1]
    file_bf = sys.argv[2]

    line_count = count_lines(file_txt)
    print("all lines -> " + str(line_count))
    bloom_filter()
