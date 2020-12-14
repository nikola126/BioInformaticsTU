import time


def split_genome(genome_filename, parts):
    """
    Splits a genome file in several parts
    TODO A few windows are lost when cutting. Need to add overlap between the different sub-files
    """
    lines = 0
    header_line = ''
    genome_file = open(genome_filename, 'r')
    for line in genome_file.readlines():
        # save first line as header line
        if lines == 0:
            header_line = line
        lines += 1
    genome_file.close()

    print(f"Lines in {genome_filename}:", lines)
    sub_file_lines = int(lines / parts) + 1
    try:
        lines % sub_file_lines
    except ZeroDivisionError:
        print(f"There are only {lines} in the file, which can't be split in {parts} parts.")
        return
    print("Lines in each sub-file:", sub_file_lines)

    # START WRITING
    start_time = time.time()

    lines = 1
    sub_count = 1
    sub_file_name = 'genome_split_1.txt'
    # Open first file
    sub_file = open(sub_file_name, 'w')
    print("Genome data will start in this file ->", sub_file_name)
    print("Splitting Data...")
    for line in open(genome_filename, 'r').readlines():
        sub_file.write(line)
        if lines % sub_file_lines == 0:
            # close file
            sub_file.close()
            # change file name
            sub_count += 1
            sub_file_name = "genome_split_%s.txt" % sub_count
            # open new file
            sub_file = open(sub_file_name, 'w')
        lines += 1

    print("Data Split Complete -> %s seconds" % round((time.time() - start_time), 2))
    print("-----" * 10)


if __name__ == "__main__":
    print("Genome Split")
    genome_filename = input("Enter name of genome FASTA file:")
    parts = input("Enter number of parts:")
    parts = int(parts)
    split_genome(genome_filename, parts)

