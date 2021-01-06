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


if __name__ == "__main__":
    print("Organizing Sausage Data")
    print("This function returns 4 sets of Sausage data, organized by first nucleotide (AGCT).")
    print("Call this function inside another script!")
