def read_swine(file_name, max_lines=False):
    """
    :param file_name: ime na goleemiq fail
    :param max_lines: kolko reda da se 4etat, po default 4ete vsi4ki
    :return: masiv s cifrovi nukleotidni danni ATGC->1234
    """
    # PARAMETERS
    current_line = 0
    skipped_line = 0
    pig_data = []

    # INFO
    if max_lines:
        print(f"Reading {max_lines} lines from {file_name}...")
    else:
        print(f"Reading ALL lines from {file_name}...")

    # OPEN BIG FILE
    for line in open(file_name, 'r').readlines():
        line_buffer = []
        line_correct = True
        # skip first line
        if current_line == 0:
            pass
        else:
            # convert to numbers
            # A T G C -> 1 2 3 4
            line = line.strip('\n')
            for nucleotide in line:
                if nucleotide == 'A':
                    line_buffer.append(1)
                elif nucleotide == 'T':
                    line_buffer.append(2)
                elif nucleotide == 'G':
                    line_buffer.append(3)
                elif nucleotide == 'C':
                    line_buffer.append(4)
                else:
                    # print(f"Wrong character in {file_name} at line {current_line}")
                    line_correct = False
                    line_buffer = []
                    skipped_line += 1
                    pass
            # save numbers to big array
            if line_correct:
                for item in line_buffer:
                    pig_data.append(item)

        # Read only max lines (first line is header line)
        if max_lines:
            if current_line > max_lines - 1:
                break
        current_line += 1

    print(f"Reading Complete")
    print(f"Length of PIG_data:{len(pig_data)}")
    print(f"Enough for {round((len(pig_data) / 51), 1)} sausage sequences")
    print(f"Skipped lines: {skipped_line}")

    return pig_data
