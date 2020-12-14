import time
from read_sausage import *
from split_genome import *
from organize_sausage import *
from compare_genome import *

if __name__ == '__main__':
    print("Hello world")

    sausage_length = 51

    # get sausage data, divide in windows with length 51
    sausage_data = read_sausage('SausageTest.fasta', sausage_length)

    # split Genome data in multiple files
    # split_genome('pig_1.fasta', 20)

    A_seq, G_seq, C_seq, T_seq = organize_sausage(sausage_data)

    compare_genome('genome_split_1.txt', sausage_data, A_seq, G_seq, C_seq, T_seq, sausage_length)
