from read_swine import *

if __name__ == '__main__':
    print("Hello world")
    pig_data = read_swine('pig_1.fasta', 0)

    print("Pig data length:", len(pig_data))
