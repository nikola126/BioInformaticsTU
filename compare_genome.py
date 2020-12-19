import time
from datetime import datetime


def compare_genome(gen_filename, A_seq, G_seq, C_seq, T_seq, sequence_length):

    # check for available recovery file
    try:
        recovery = open('Recovery.txt', 'r')
    except FileNotFoundError:
        print("Recovery file not found. Starting from beginning.")
        rec_matches = 0
        rec_pointer_pos = 0
        rec_checked = 0
    else:
        # get last file pointer position
        line = recovery.readline()
        line = line.strip('\n')
        line = line.split('|')
        print(line)
        rec_matches = int(line[0][8:])
        rec_pointer_pos = int(line[1][17:])
        rec_checked = int(line[2][18:])
        print("Recovery file found. Continuing search...")
        print("Matches:", rec_matches)
        print("Pointer position:", rec_pointer_pos)
        print("Sequences checked:", rec_checked)
        # print("End")
        # return

    # create recovery file
    recovery = open('Recovery.txt', 'w')

    # Get data for summary later
    search_start_time = datetime.now()

    count_valid = rec_checked
    matches = rec_matches
    previous_sequence = ''
    checked = rec_checked

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

        # get initial read pointer position
        offset = gen_file.tell() + rec_pointer_pos
        EOF_reached = False
        while not EOF_reached:
            # read 51 characters
            genome_sequence = ''
            valid = True
            chars_read = 0
            over_new_line = False
            while len(genome_sequence) != sequence_length and valid:
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
                    over_new_line = True
                    continue
                # check for invalid characters
                if char not in ['A', 'T', 'G', 'C']:
                    # read forward and start over
                    offset = gen_file.tell()
                    valid = False
                else:
                    genome_sequence += char
            if valid:
                count_valid += 1

                # TODO SOME SEQUENCES ARE READ TWICE
                # SEEK GOES TOO FAR BACK, WHICH LEADS TO DUPLICATES
                # Check for End of File
                next_char = gen_file.read(1)
                if next_char == '':
                    print("EOF reached")
                    EOF_reached = True
                else:
                    offset += 1
                    gen_file.seek(offset)

                if genome_sequence == previous_sequence:
                    count_valid -= 1
                else:
                    previous_sequence = genome_sequence

                    # ANALYSIS
                    # get first char
                    if genome_sequence[0] == 'A':
                        for sequence in A_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'G':
                        for sequence in G_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'C':
                        for sequence in C_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    elif genome_sequence[0] == 'T':
                        for sequence in T_seq:
                            if sequence == genome_sequence:
                                matches += 1
                    else:
                        # dotuk dano ne se stiga 🙏
                        print(genome_sequence, "is not a valid sequence.")
                        print("Check reading in compare_genome.py")
                        EOF_reached = True

                    checked += 1
            # Periodically save recovery information
            if checked % (10 ** 4) == 0:
                print("Genome Sequences Compared:", count_valid)
                recovery.seek(0)
                recovery.write(f'Matches:{matches}|Pointer position:{offset}|Sequences checked:{count_valid}\n')
                # Break here to stop earlier
            # if matches:
            #     print("Match found. Test recovery")
            #     break

    # After EOF
    recovery.close()

    # Print Stats
    # print("Valid Genome Sequences Found:", count_valid)
    # print("Matches:", matches)
    # print(f"Searching took", round((time.time() - start_time), 2), "seconds")

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
