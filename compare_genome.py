import time
from datetime import datetime


def compare_genome(gen_filename, sausage_data, A_seq, G_seq, C_seq, T_seq, sequence_length):
    # Get data for summary later
    search_start_time = datetime.now()

    count_valid = 0
    matches = 0
    previous_sequence = ''
    checked = 0

    start_time = time.time()

    with open(gen_filename, 'r') as gen_file:
        print(f"Reading Through {gen_filename}...")

        # check if first line is header line or contains genetic information
        first_line = gen_file.readline()
        if first_line[0] == '>':
            # skip this line
            pass
        else:
            # seek again from beginning
            gen_file.seek(0)

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
            while len(genome_sequence) != sequence_length and valid:
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
                    # print("Valid Sequence:", genome_sequence)
                    previous_sequence = genome_sequence

                    # ANALYSIS
                    # TODO Optimize this, compare only sequences with the same first nucleotide!
                    # get first char
                    if genome_sequence[0] == 'A':
                        # print("Comparing with A sequences")
                        for sequence in A_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'G':
                        # print("Comparing with G sequences")
                        for sequence in G_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'C':
                        # print("Comparing with C sequences")
                        for sequence in C_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'T':
                        # print("Comparing with T sequences")
                        for sequence in T_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    else:
                        # dotuk dano ne se stiga (pray)
                        print(genome_sequence, "is not a valid sequence.")
                        print("Check reading in compare_genome.py")
                        EOF_reached = True

                    checked += 1
            # Progress Report
            if checked % (10 ** 6) == 0:
                print("Genome Sequences Compared:", checked)
                # Break here to stop earlier

    # Print Stats
    print("Valid Genome Sequences Found:", count_valid)
    print("Matches:", matches)
    print(f"Searching took", round((time.time() - start_time), 2), "seconds")

    # Save to File
    with open('Summary.txt', 'w') as summary:
        search_end_time = datetime.now()
        dt_start = search_start_time.strftime("%d/%m/%Y %H:%M:%S")
        dt_end = search_end_time.strftime("%d/%m/%Y %H:%M:%S")

        summary.write(f"Genome Data File: {gen_filename}\n")
        summary.write(f"Search Start: {dt_start}\n")
        summary.write(f"Search End:   {dt_end}\n")
        summary.write(f"Valid Genome Sequences Found and Compared: {count_valid}\n")
        summary.write(f"Matches Found: {matches}\n")


if __name__ == "__main__":
    print("Comparing Sequence in Genome to Sequence in Sausage FASTA File")
    print("Call this function inside another script!")
