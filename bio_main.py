import time
from read_sausage import *
from split_genome import *
from organize_sausage import *
from compare_genome import *

if __name__ == '__main__':
    print("Hello world")
    print("Bioinformatics 2020/2021")

    # Open Sausage File
    print("Enter Sausage File Name")
    print("Example: SausageTest.fasta")
    user_sausage_filename = input(">>> ")

    # Check if file is available
    try:
        test = open(user_sausage_filename, 'r')
    except FileNotFoundError:
        print(f"Can't open {user_sausage_filename}!")
        input("Press any key to continue")
        quit()
    else:
        test.close()

    # Split Sausage File to Sequences
    # get sausage data, divide in windows with length 51
    sausage_length = 51
    sausage_data = read_sausage(user_sausage_filename, sausage_length)
    A_set, G_set, C_set, T_set = organize_sausage(sausage_data)

    # Open and Split Genome File
    print(
        "Would you like to split a big genome file (from the database, not necessarily a split)\n"
        "in multiple smaller files? [y/n]")
    user_split_choice = input(">>> ")
    user_parts = ' '
    if user_split_choice in ['yes', 'YES', 'y']:
        # get name of file
        print("Enter Genome File Name")
        user_genome_filename = input(">>> ")
        # check if such file exists
        try:
            test = open(user_genome_filename, 'r')
        except FileNotFoundError:
            print(f"Can't open {user_genome_filename}!")
            input("Press any key to continue")
            quit()
        else:
            test.close()

        # get number of parts
        while not user_parts.isdigit():
            user_parts = input("Enter number of parts: ")
        else:
            user_parts = int(user_parts)
            split_genome(user_genome_filename, user_parts)
    else:
        pass

    # Compare Sequences
    print("Enter Genome Split File Name")
    print("Example: genome_split_6_20.txt")
    user_split_filename = input(">>> ")

    # Check if file is available
    try:
        test = open(user_split_filename, 'r')
    except FileNotFoundError:
        print(user_split_filename, "not found!")
        input("Press any key to continue")
    else:
        test.close()
        compare_genome(user_split_filename, A_set, G_set, C_set, T_set, sausage_length)
