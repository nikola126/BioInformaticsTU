import time


def organize_sausage(data):
    start_time = time.time()

    A_set = set()
    G_set = set()
    C_set = set()
    T_set = set()
    for line in data:
        if line[0] == 'A':
            A_set.add(line)
        if line[0] == 'G':
            G_set.add(line)
        if line[0] == 'C':
            C_set.add(line)
        if line[0] == 'T':
            T_set.add(line)

    A_seqs = len(A_set)
    G_seqs = len(G_set)
    C_seqs = len(C_set)
    T_seqs = len(T_set)
    all_seqs = len(data)
    unique_seqs = A_seqs + G_seqs + C_seqs + T_seqs

    # Display Stats
    print(f"A sequences:", len(A_set), round((A_seqs / all_seqs) * 100, 2), "%")
    print(f"G sequences:", len(G_set), round((G_seqs / all_seqs) * 100, 2), "%")
    print(f"C sequences:", len(C_set), round((C_seqs / all_seqs) * 100, 2), "%")
    print(f"T sequences:", len(T_set), round((T_seqs / all_seqs) * 100, 2), "%")
    print(f"Duplicates:", all_seqs - unique_seqs, round((all_seqs / unique_seqs) * 100 - 100, 2), "%")
    print(f"Data was organized in %s seconds" % round((time.time() - start_time), 2))
    print("-----" * 10)

    return A_set, G_set, C_set, T_set


def read_sausage(filename, sequence_length):
    # Check if file is available
    try:
        test = open(filename, 'r')
    except FileNotFoundError:
        print(f"Can't open {filename}!")
        input("Press any key to continue")
    else:
        test.close()

    start_time = time.time()

    sausage_data = []
    read_sequences = 0
    valid_sequences = 0
    # load a line of sausage data in memory
    print(f"Reading from {filename}...")
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
    invalid_percentage = round((read_sequences / valid_sequences) / 100, 2)
    print("Invalid Sequences:", read_sequences - valid_sequences, f"({invalid_percentage} %)")
    print("Example Sequence:", sausage_data[0])

    print(f"Data from {filename} was read in", round((time.time() - start_time), 2), "seconds")
    print("-----" * 10)
    return sausage_data


if __name__ == "__main__":
    print("Call this function inside another script!")
