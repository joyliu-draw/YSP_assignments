'''imports'''
from random import *
import matplotlib.pyplot as plt
import numpy as np
import re
import statistics

'''Extract FASTA Gene Lengths'''
def extract(file_name):
    length_data = []
    with open (file_name, 'r') as myfile:
        gene_length = 0
        is_header = False
        stop_count = 0
        total_length = 0

        for i, line in enumerate(myfile):
            if i>0:
                if line.startswith('>'):
                    is_header = True
                else:
                    is_header = False

                if is_header == False:
                    gene_length = gene_length + len(line)

                else:
                    length_data.append(gene_length)
                    total_length = total_length+gene_length
                    stop_count = stop_count + 1
                    gene_length = 0
        stop_probability = stop_count/total_length
        print('Total Length: '+str(total_length))
        print('Stop Probability: '+str(stop_probability))
        return length_data


'''Sort Lists of Codons for Start and Stop'''
def sim(total_amino_count, CG_prob):
    #TAG, TAA, TGA
    length_data = []
    curr_length = 0
    stop_prob = 2*((1-CG_prob)/2)*((1-CG_prob)/2)*((1-CG_prob)/2)+((1-CG_prob)/2)*((1-CG_prob)/2)*((1-CG_prob)/2)
    print('Stop Prob: '+str(stop_prob))
    for i in range(0,total_amino_count):
        if random()<stop_prob:
            length_data.append(curr_length)
            curr_length = 0
        else:
            curr_length = curr_length + 1
    return length_data

'''Analyze Gene Length'''
def analyze(data):
    average = sum(data)/len(data)
    maximum = max(data)
    Q3 = np.percentile(data, 75)
    med = statistics.median(data)
    Q1 = np.percentile(data, 25)
    minimum = min(data)

    plt.hist(data, bins = 'auto')
    plt.title('Overall Length Distribution')
    plt.xlabel('Lengths (# of Proteins)')
    plt.ylabel('Frequency (Count)')
    plt.xlim(0,average*2)
    plt.show()
    print('Mean: ' + str(average))
    print('Min: ' + str(minimum))
    print('Q1: ' + str(Q1))
    print('Median: ' + str(med))
    print('Q3: ' + str(Q3))
    print('Max: ' + str(maximum))

'''Execute Analysis on Data'''
def exe(is_sim,file,total_amino,CG_prob):
    if is_sim == True:
        lengths = sim(total_amino,CG_prob)
    else:
        lengths = extract(file)
    graph = analyze(lengths)

real_graph = exe(False,'scratch/b_malayi.PRJNA10729.WS270.protein.fa',None,None)
sim_graph = exe(True,None,7000,0.5)
