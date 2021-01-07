from datetime import datetime


def compare_genome(gen_filename, A_set, G_set, C_set, T_set, sequence_length):
    # check for available recovery file
    # isolate file extension
    # TODO Cleanup
    source_name = []
    for char in gen_filename:
        if char == '.':
            break
        source_name.append(char)
    file_name_no_extension = ''.join(source_name)
    rec_file_name = f'Recovery_{file_name_no_extension}.txt'
    summary_file_name = f'Summary_{file_name_no_extension}.txt'

    recovery_save_interval = 150000  # after this many checked windows, the recovery file is updated

    # Open recovery file for pointer position and matches information
    try:
        recovery = open(rec_file_name, 'r')
    except FileNotFoundError:
        print(f"Main recovery file not found.")
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
            print("Main recovery file empty or corrupted.")
            # empty file contents
            recovery.close()
            recovery = open(rec_file_name, 'w')
            recovery.close()
        else:
            print("Recovery file found.")
            recovery.close()

    # Open recovery files for unique sequences remaining
    # Attempt to open all Recovery_set files, if any fails, start over!
    set_recovery_file_missing = False
    try:
        recovery_A = open(f'Recovery_set_A_{file_name_no_extension}.txt', 'r')
    except FileNotFoundError:
        set_recovery_file_missing = True
    else:
        recovery_A.close()
    try:
        recovery_G = open(f'Recovery_set_G_{file_name_no_extension}.txt', 'r')
    except FileNotFoundError:
        set_recovery_file_missing = True
    else:
        recovery_G.close()
    try:
        recovery_C = open(f'Recovery_set_C_{file_name_no_extension}.txt', 'r')
    except FileNotFoundError:
        set_recovery_file_missing = True
    else:
        recovery_C.close()
    try:
        recovery_T = open(f'Recovery_set_T_{file_name_no_extension}.txt', 'r')
    except FileNotFoundError:
        set_recovery_file_missing = True
    else:
        recovery_T.close()

    if set_recovery_file_missing:
        # start over
        # reset file pointer and matches
        print("One or more recovery files are missing.")
        print("Full recovery impossible. Starting over.")
        rec_matches = 0
        rec_pointer_pos = 0
        rec_checked = 0
    else:
        # Recover information from set files
        # TODO Cleanup
        filenames = [f'Recovery_set_A_{file_name_no_extension}.txt', f'Recovery_set_C_{file_name_no_extension}.txt',
                     f'Recovery_set_G_{file_name_no_extension}.txt', f'Recovery_set_T_{file_name_no_extension}.txt']
        sets = [set(), set(), set(), set()]
        for i in range(0, 4):
            for line in open(filenames[i], 'r').readlines():
                line = line.strip('\n')
                if len(line) != 51:
                    print(line)
                sets[i].add(line)
        A_set = sets[0]
        C_set = sets[1]
        G_set = sets[2]
        T_set = sets[3]
        print("Full Recovery Complete")
        # print("Remaining A:", len(A_set))
        # print("Remaining C:", len(C_set))
        # print("Remaining G:", len(G_set))
        # print("Remaining T:", len(T_set))
        print("Matches:", rec_matches)
        print("Sequences checked:", rec_checked)
        # print("Pointer position:", rec_pointer_pos)

    # Get start time for summary later
    search_start_time = datetime.now()

    count_valid = rec_checked
    matches = rec_matches
    previous_sequence = ''

    # Show/Hide progress report
    show_progress_report = False
    print("Show progress while working? [y/n]")
    user_progress_choice = input(">>> ")
    if user_progress_choice in ['y', 'yes', 'YES']:
        show_progress_report = True

    with open(gen_filename, 'r') as gen_file:
        print(f"Progress is saved at every {recovery_save_interval} windows.")
        print("You can stop the search at any time and resume it later.")
        print("Don't delete the recovery files!")
        print(f"Reading {gen_filename}...")

        # check if first line is header line or contains genetic information
        # this is done only if recovery failed (or first time checking a file)
        if set_recovery_file_missing:
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
        # print("Tell:", gen_file.tell())
        # print("Initial Pointer position:", offset)
        gen_file.seek(offset)
        while not EOF_reached:
            # break earlier if all sequences are found
            if len(A_set) == 0 and len(G_set) == 0 and len(C_set) == 0 and len(T_set) == 0:
                print("All sequences are found.")
                break
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
                    count_valid += 1

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

                    # checked += 1
                    # count_valid += 1
            # Periodically save recovery information every few thousand checked windows
            if count_valid % recovery_save_interval == 0:
                recovery_time_data = datetime.now()
                recovery_time_string = recovery_time_data.strftime("%H:%M:%S")
                with open(rec_file_name, 'a') as recovery:
                    recovery.write(f'{matches}|{offset}|{count_valid}|{recovery_time_string}|OK\n')

                # save remaining sequences
                with open(f'Recovery_set_A_{file_name_no_extension}.txt', 'w+') as recovery_a:
                    for item in A_set:
                        recovery_a.write(f"{str(item)}\n")
                with open(f'Recovery_set_G_{file_name_no_extension}.txt', 'w+') as recovery_g:
                    for item in G_set:
                        recovery_g.write(f"{str(item)}\n")
                with open(f'Recovery_set_C_{file_name_no_extension}.txt', 'w+') as recovery_c:
                    for item in C_set:
                        recovery_c.write(f"{str(item)}\n")
                with open(f'Recovery_set_T_{file_name_no_extension}.txt', 'w+') as recovery_t:
                    for item in T_set:
                        recovery_t.write(f"{str(item)}\n")

                if show_progress_report:
                    print(
                        f'Matches Found: {matches} | Genome Sequences Compared: {count_valid} | {recovery_time_string}')
                    # print("Pointer position:", offset)
                    # print("Remaining A:", len(A_set))
                    # print("Remaining C:", len(C_set))
                    # print("Remaining G:", len(G_set))
                    # print("Remaining T:", len(T_set))
                # Break here to stop earlier

    # After EOF
    # Print Summary to Console Output
    search_end_time = datetime.now()
    dt_start = search_start_time.strftime("%d/%m/%Y %H:%M:%S")
    dt_end = search_end_time.strftime("%d/%m/%Y %H:%M:%S")

    print(f"Genome Data File: {gen_filename}")
    print(f"Search Start: {dt_start}")
    print(f"Search End:   {dt_end}")
    print(f"Valid Genome Sequences Found: {count_valid}")
    print(f"Matches Found: {matches}")

    # Save Summary to File
    with open(summary_file_name, 'w') as summary:
        summary.write(f"Genome Data File: {gen_filename}\n")
        summary.write(f"Search Start: {dt_start}\n")
        summary.write(f"Search End:   {dt_end}\n")
        summary.write(f"Valid Genome Sequences Found: {count_valid}\n")
        summary.write(f"Matches Found: {matches}\n")


if __name__ == "__main__":
    print("Comparing Sequence in Genome to Sequence in Sausage FASTA File")
    print("Call this function inside another script!")
