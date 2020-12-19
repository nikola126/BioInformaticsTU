import time
from read_sausage import *
from split_genome import *
from organize_sausage import *
from compare_genome import *

if __name__ == '__main__':
    print("Hello world")
    print("Bioinformatics 2020/2021")

    # Check if file is available
    try:
        test = open('SausageTest.fasta', 'r')
    except FileNotFoundError:
        print("Can't open the SausageTest.fasta file!")
        input("Press any key to continue")
    else:
        test.close()

    # get sausage data, divide in windows with length 51
    sausage_length = 51
    sausage_data = read_sausage('SausageTest.fasta', sausage_length)

    # split Genome data in multiple files
    user_split_choice = input("Would you like to split the big genome file in multiple smaller files? [y/n] >>> ")
    user_parts = ' '
    if user_split_choice in ['yes', 'YES', 'y']:
        while not user_parts.isdigit():
            user_parts = input("Enter number of parts: ")
        else:
            split_genome('pig_1.fasta', user_parts)
    else:
        pass

    A_seq, G_seq, C_seq, T_seq = organize_sausage(sausage_data)

    print("Enter Genome File Name")
    print("Example: genome_split_8.txt")
    genome_filename = input(">>> ")

    # Check if file is available
    try:
        test = open(genome_filename, 'r')
    except FileNotFoundError:
        print(genome_filename, "not found!")
        input("Press any key to continue")
    else:
        test.close()
        compare_genome(genome_filename, A_seq, G_seq, C_seq, T_seq, sausage_length)
