def read_sausage(filename, sequence_length):
    sausage_data = []
    read_sequences = 0
    valid_sequences = 0
    # load a line of sausage data in memory
    for line in open(filename, 'r').readlines():
        line = line.strip('\n')

        # skip every 2nd line
        if line[0] == '>':
            continue
        read_sequences += 1
        # check length
        if len(line) != sequence_length:
            print("Invalid line length:", len(line))
            print(line)
            break
        # check for invalid characters
        if line.count('A') + line.count('T') + line.count('G') + line.count('C') != len(line):
            pass
        else:
            sausage_data.append(line)
            valid_sequences += 1

    print(f"Valid:{valid_sequences}/{read_sequences} ({round((read_sequences / valid_sequences) / 100, 3)}%)")
    return sausage_data

