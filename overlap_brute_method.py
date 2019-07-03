from random import *
import re
import time

class Gene:
    def __init__(self,chrom,start,stop):
        self.chrom=chrom
        self.start=start
        self.stop=stop

'''1. Make a Overlap File'''
def make_file(file_name,rows,total_chrom_count,total_nuc_count):
    f = open(file_name,'w+')
    f.write('Chrom    Start   End\r\n')
    for i in range(rows):
        start = randint(0,total_nuc_count)
        end = start + randint(0,1000) #Next time: can personalize further w/ probability that decreases exponentially
        f.write('%d'%randint(0,total_chrom_count) +'\t%d'%start+'\t%d'%end+'\r\n')
make_file('f1.txt',3000,23,3.2e9)
make_file('f2.txt',3000,6,1e4)

before = time.time()

'''2. Extract Data from File'''
def extract_file(file_name):
    file_data = []
    with open (file_name, 'r') as myfile:
        for i, myline in enumerate(myfile):
            if i>0:
                myline = myline.split()
                gene_name = 'gene_'+str(i)
                gene_name = Gene(myline[0],myline[1],myline[2])
                file_data.append(gene_name)
        file_data.sort()
        return file_data

'''3. Determine Overlap for 1 Gene'''
def find_chrom_overlap(gene_1,gene_2):
    gene_overlap = []
    '''Overlap Condition: S2/E2 between [S1,E2]'''
    if (gene_2.chrom==gene_1.chrom):
        if (gene_2.start>=gene_1.start and gene_2.start<=gene_1.stop):
            chrom_overlap.append([gene_2.start,gene_1.stop])
        elif (gene_2.stop>=gene_1.start and gene_2.stop<=gene_1.stop):
            chrom_overlap.append([gene_2.stop,gene_1.start])
    return gene_overlap

'''4. Loop and Execute'''
def find_all_overlap(data_f1,data_f2):
    all_overlap = {}
    for gene in data_f1:
        if gene in data_f2:
            all_overlap.update({gene:find_chrom_overlap(data_f1[gene],data_f2[gene])})
    print('All Overlap: '+str(all_overlap))
    return all_overlap

find_all_overlap(extract_file('f1.txt'),extract_file('f2.txt'))
after = time.time()
print("It took: ", after-before, " seconds")
