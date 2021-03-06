import time


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
    print("Reading Sausage Data")
    print("This function returns an array of Sausage data. Call this function inside another script!")
