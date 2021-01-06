from datetime import datetime


def compare_genome(gen_filename, A_set, G_set, C_set, T_set, sequence_length):
    # check for available recovery file
    # isolate file extension
    source_name = []
    for char in gen_filename:
        if char == '.':
            break
        source_name.append(char)
    rec_file_name = ''.join(source_name)
    rec_file_name = f'Recovery_{rec_file_name}.txt'

    recovery_save_interval = 100000  # after this many checked windows, the recovery file is updated

    try:
        recovery = open(rec_file_name, 'r')
    except FileNotFoundError:
        print(f"Recovery file not found. Starting from beginning.")
        rec_matches = 0
        rec_pointer_pos = 0
        rec_checked = 0
    else:
        # get last file pointer position
        last_entry_reached = False
        rec_matches = 0
        rec_pointer_pos = 0
        rec_checked = 0

        while last_entry_reached is False:
            line = recovery.readline()
            line = line.strip('\n')
            line = line.split('|')
            if len(line) == 5:
                # update values
                rec_matches = int(line[0])
                rec_pointer_pos = int(line[1])
                rec_checked = int(line[2])
            else:
                last_entry_reached = True

        if rec_matches == 0 and rec_pointer_pos == 0 and rec_checked == 0:
            print("Recovery file empty or corrupted. Starting from beginning.")
        else:
            print("Recovery file found.")
            print("Matches:", rec_matches)
            print("Sequences checked:", rec_checked)

    # create recovery file
    recovery = open(rec_file_name, 'a')

    # Get data for summary later
    search_start_time = datetime.now()

    count_valid = rec_checked
    matches = rec_matches
    previous_sequence = ''
    checked = rec_checked

    # Show/Hide progress report
    show_progress_report = False
    print("Show progress while working? [y/n]")
    user_progress_choice = input(">>> ")
    if user_progress_choice in ['y', 'yes', 'YES']:
        show_progress_report = True

    with open(gen_filename, 'r') as gen_file:
        print(f"Progress is saved at every {recovery_save_interval} windows.")
        print("You can stop the search at any time and resume it later.")
        print("Don't delete the recovery file!")
        print(f"Reading {gen_filename}...")

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
                        if genome_sequence in A_set:
                            matches += 1
                    elif genome_sequence[0] == 'G':
                        if genome_sequence in G_set:
                            matches += 1
                    elif genome_sequence[0] == 'C':
                        if genome_sequence in C_set:
                            matches += 1
                    elif genome_sequence[0] == 'T':
                        if genome_sequence in T_set:
                            matches += 1
                    else:
                        print(genome_sequence, "is not a valid sequence.")
                        print("Check reading in compare_genome.py")
                        pass

                    checked += 1
            # Periodically save recovery information every few thousand checked windows
            if checked % recovery_save_interval == 0:
                # print("Genome Sequences Compared:", count_valid)
                recovery_time_data = datetime.now()
                recovery_time_string = recovery_time_data.strftime("%H:%M:%S")
                recovery.write(f'{matches}|{offset}|{count_valid}|{recovery_time_string}|OK\n')

                if show_progress_report:
                    print(f'Matches Found: {matches} | Genome Sequences Compared: {count_valid} | {recovery_time_string}')
                # Break here to stop earlier

    # After EOF
    recovery.close()

    # Print Summary to Console Output
    search_end_time = datetime.now()
    dt_start = search_start_time.strftime("%d/%m/%Y %H:%M:%S")
    dt_end = search_end_time.strftime("%d/%m/%Y %H:%M:%S")

    print(f"Genome Data File: {gen_filename}")
    print(f"Search Start: {dt_start}")
    print(f"Search End:   {dt_end}")
    print(f"Valid Genome Sequences Found and Compared: {count_valid}")
    print(f"Matches Found: {matches}")

    # Save Summary to File
    with open('SummarySets.txt', 'w') as summary:

        summary.write(f"Genome Data File: {gen_filename}\n")
        summary.write(f"Search Start: {dt_start}\n")
        summary.write(f"Search End:   {dt_end}\n")
        summary.write(f"Valid Genome Sequences Found and Compared: {count_valid}\n")
        summary.write(f"Matches Found: {matches}\n")


if __name__ == "__main__":
    print("Comparing Sequence in Genome to Sequence in Sausage FASTA File")
    print("Call this function inside another script!")
