import time

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

    print(f"Valid Sequences: {valid_sequences}/{read_sequences}")
    print("Percentage Invalid:", round((read_sequences / valid_sequences) / 100, 3), "%")
    print("Example Sequence:", sausage_data[0])
    print("-----" * 10)
    return sausage_data


def genome_splitter(filename, parts):
    lines = 0
    header_line = ''
    genome_file = open(filename, 'r')
    for line in genome_file.readlines():
        # save first line as header line
        if lines == 0:
            header_line = line
        lines += 1
    genome_file.close()

    print("Lines in file:", lines)
    sub_file_lines = int(lines / parts)
    try:
        lines % sub_file_lines
    except ZeroDivisionError:
        print(f"There are only {lines} in the file, which can't be split in {parts} parts.")
        return
    print("Lines in Sub-Division File:", sub_file_lines)

    # START WRITING
    start_time = time.time()

    lines = 0
    sub_count = 1
    sub_file_name = 'genome_split_1.txt'
    # Open first file
    sub_file = open(sub_file_name, 'w')
    print("New file:", sub_file_name)
    print("Writing to sub-files")
    for line in open(filename, 'r').readlines():
        sub_file.write(line)
        if lines % sub_file_lines == 0:
            # close file
            sub_file.close()
            # change file name
            sub_file_name = "genome_split_%s.txt" % sub_count
            sub_count += 1
            # open new file
            print("New file:", sub_file_name)
            sub_file = open(sub_file_name, 'w')
        lines += 1

    print("Data Split Complete --- %s seconds" % round((time.time() - start_time), 2))

