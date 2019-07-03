from random import *
import re
import time

class Gene:
    def __init__(self,start,stop):
        self.start=start
        self.stop=stop

'''1. Make a Overlap File'''
def make_file(file_name,rows,total_chrom_count,total_nuc_count):
    f = open(file_name,'w+')
    f.write('Chrom    Start   End\r\n')
    for i in range(rows):
        start = randint(0,total_nuc_count)
        end = start + randint(0,1000)
        f.write('%d'%randint(0,total_chrom_count) +'\t%d'%start+'\t%d'%end+'\r\n')
make_file('f1.txt',3000,10,3.2e9)
make_file('f2.txt',3000,6,1e4)

before = time.time()

'''2. Extract Data from File'''
def extract_file(file_name):
    file_data = {}
    with open (file_name, 'r') as myfile:
        for i, myline in enumerate(myfile):
            if i>0:
                myline = myline.split()
                chromosome = 'chrom_'+str(myline[0])
                gene_name = 'gene_'+str(i)
                gene_name = Gene(myline[1],myline[2])
                file_data.setdefault(chromosome, []).append(gene_name)
        return file_data

'''3. Determine Overlap for 1 Chromosome'''
def find_chrom_overlap(chrom_f1,chrom_f2):
    chrom_overlap = []
    for gene_f1 in chrom_f1:
        for gene_f2 in chrom_f2:
            '''Overlap Condition: S2/E2 between [S1,E2]'''
            if (gene_f2.start>=gene_f1.start and gene_f2.start<=gene_f1.stop):
                chrom_overlap.append([gene_f2.start,gene_f1.stop])
            elif (gene_f2.stop>=gene_f1.start and gene_f2.stop<=gene_f1.stop):
                chrom_overlap.append([gene_f2.stop,gene_f1.start])
    return chrom_overlap

'''4. Loop and Execute'''
def find_all_overlap(data_f1,data_f2):
    all_overlap = {}
    for chrom in data_f1:
        if chrom in data_f2:
            all_overlap.update({chrom:find_chrom_overlap(data_f1[chrom],data_f2[chrom])})
    print('All Overlap: '+str(all_overlap))
    return all_overlap

find_all_overlap(extract_file('f1.txt'),extract_file('f2.txt'))
after = time.time()
print("It took: ", after-before, " seconds")
