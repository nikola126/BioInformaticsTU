def compare_genome(gen_filename, A_set, G_set, C_set, T_set, sequence_length):
    # check for available recovery file
    # isolate file extension
    source_name = []
    for char in gen_filename:
        if char == '.':
            break
        source_name.append(char)

    recovery_save_interval = 1000000  # after this many checked windows, the recovery file is updated

    # Get start time for summary later

    # Show/Hide progress report

    with open(gen_filename, 'r') as gen_file:
        print(f"Progress is saved at every {recovery_save_interval} windows.")
        print("You can stop the search at any time and resume it later.")
        print("Don't delete the recovery files!")
        print(f"Reading {gen_filename}...")

        # check if first line is header line or contains genetic information
        # this is done only if recovery failed (or first time checking a file)
        first_line = gen_file.readline()
        if first_line[0] == '>':
            # skip this line
            pass
        else:
            # seek again from beginning
            gen_file.seek(0)

        count_valid = 0
        matches = 0

        # get initial read pointer position
        current_pos = gen_file.tell()
        EOF_reached = False

        # print("Initial Pointer position:", offset)
        gen_file.seek(current_pos)
        while not EOF_reached:
            # print("Tell:", gen_file.tell())
            # break earlier if all sequences are found
            if len(A_set) == 0 and len(G_set) == 0 and len(C_set) == 0 and len(T_set) == 0:
                print("All sequences are found.")
                break
            # read 51 characters
            genome_sequence = ''
            valid = True
            chars_read = 0
            while len(genome_sequence) < sequence_length and valid:
                char = gen_file.read(1)
                chars_read += 1
                # check for end of file
                if char == '':
                    print('EOF reached')
                    EOF_reached = True
                    valid = False
                    break
                # skip the new line character
                if char == '\n':
                    continue
                # check for invalid characters
                if char not in ['A', 'T', 'G', 'C']:
                    # read forward and start over
                    current_pos = gen_file.tell()
                    valid = False
                else:
                    genome_sequence += char

            if valid:
                count_valid += 1
                if count_valid % 100000 == 0:
                    print(f"Valid sequences found: {count_valid}")
                    print(f'Matches Found: {matches} | Sequences Compared: {count_valid}')
                # print(f"Valid sequence {count_valid}:\t{genome_sequence}")
                # print("Tell:", gen_file.tell())

                next_char = gen_file.read(1)
                if next_char == '':
                    print("EOF reached")
                    EOF_reached = True
                elif next_char == '\n' and current_pos != 0:
                    # print("Reading starts at a new line!")
                    current_pos += 3
                    gen_file.seek(current_pos)
                else:
                    current_pos += 1
                    gen_file.seek(current_pos)

                newline_skipped = False

                # ANALYSIS
                # get first char
                if genome_sequence[0] == 'A':
                    if genome_sequence in A_set:
                        # if a match is found, remove the sequence from the set, so it can't be "found" again
                        matches += 1
                        A_set.remove(genome_sequence)
                elif genome_sequence[0] == 'G':
                    if genome_sequence in G_set:
                        matches += 1
                        G_set.remove(genome_sequence)
                elif genome_sequence[0] == 'C':
                    if genome_sequence in C_set:
                        matches += 1
                        C_set.remove(genome_sequence)
                elif genome_sequence[0] == 'T':
                    if genome_sequence in T_set:
                        matches += 1
                        T_set.remove(genome_sequence)
                else:
                    print(genome_sequence, "is not a valid sequence.")
                    print("Check reading in compare_genome.py")
                    pass

    print(f'Matches Found: {matches} | Sequences Compared: {count_valid}')


if __name__ == "__main__":
    print("Comparing Sequence in Genome to Sequence in Sausage FASTA File")
    print("Call this function inside another script!")
