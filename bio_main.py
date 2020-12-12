from functions import *

if __name__ == '__main__':
    print("Hello world")
    sausage_length = 51

    # get sausage data, divide in windows with length 51
    sausage_data = read_sausage('SausageTest.fasta', sausage_length)

    # open big file
    count_valid = 0
    sausage_length = 51
    hits = 0
    previous_sequence = ''
    gen_filename = 'pig_1.fasta'
    checked = 0

    with open(gen_filename, 'r') as gen_file:
        print(f"Reading Through {gen_filename}...")
        # skip first line
        gen_file.readline()
        # get initial read pointer position TODO Fix this
        offset = gen_file.tell()
        EOF_reached = False
        while not EOF_reached:
            # print("Offset before reading next:",gen_file.tell())
            # read 51 characters
            genome_sequence = ''
            valid = True
            chars_read = 0
            over_new_line = False
            while len(genome_sequence) != sausage_length and valid:
                char = gen_file.read(1)
                # print(char, end= '')
                chars_read += 1
                # check for end of file
                if char == '':
                    print('EOF reached')
                    EOF_reached = True
                    valid = False
                    break
                # skip the new line character
                if char == '\n':
                    # print("New line")
                    over_new_line = True
                    continue
                # check for invalid characters
                if char not in ['A', 'T', 'G', 'C']:
                    # read forward and start over
                    offset = gen_file.tell()
                    # gen_file.read(skip_forward)
                    valid = False
                else:
                    genome_sequence += char
            if valid:
                count_valid += 1
                # print("Sequence:", genome_sequence)
                # print("Offset after reading:", gen_file.tell())

                # TODO SOURCE OF BUGS
                # Check for End of File
                next_char = gen_file.read(1)
                if next_char == '':
                    print("EOF reached")
                    EOF_reached = True
                else:
                    if over_new_line:
                        pass
                    offset += 1
                    gen_file.seek(offset)

                # TODO SOME SEQUENCES ARE READ TWICE, FIX THIS
                if genome_sequence == previous_sequence:
                    # print("Duplicate", genome_sequence)
                    count_valid -= 1
                    # previous_sequence = genome_sequence
                else:
                    # print("OK Sequence:", genome_sequence)
                    previous_sequence = genome_sequence

                    # ANALYSIS
                    # if a valid genome sequence is found, every sausage sequence is compared to it
                    # for i in range(0, len(sausage_data)):
                    #     if sausage_data[i] == genome_sequence:
                    #         hits += 1
                    #         print(f"Found {hits}!")
                    # checked += 1
            # if checked % 10**3 == 0:
            #     print("Genome Sequences Compared:", checked)
            #     break
            if count_valid % 10**6 == 0:
                print("Valid Genome Sequences Found:", count_valid)
    print("Valid Genome Sequences Found:", count_valid)
    print("Hits:", hits)
