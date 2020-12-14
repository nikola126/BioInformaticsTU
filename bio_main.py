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

    print("Enter Genome File Name")
    print("Example: genome_split_8.txt")
    genome_filename = input(">>>")

    try:
        test = open(genome_filename, 'r')
    except FileNotFoundError:
        input("File Not Found. Press Enter.\n")
    else:
        test.close()
        compare_genome(genome_filename, sausage_data, A_seq, G_seq, C_seq, T_seq, sausage_length)


