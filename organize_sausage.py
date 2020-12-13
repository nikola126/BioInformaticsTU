import time


def organize_sausage(data):
    start_time = time.time()

    A_seq = []
    G_seq = []
    C_seq = []
    T_seq = []
    for line in data:
        if line[0] == 'A':
            A_seq.append(line)
        if line[0] == 'G':
            G_seq.append(line)
        if line[0] == 'C':
            C_seq.append(line)
        if line[0] == 'T':
            T_seq.append(line)

    # Display Stats
    print(f"A sequences:", len(A_seq), round((len(A_seq) / len(data)) * 100, 2), "%")
    print(f"G sequences:", len(G_seq), round((len(G_seq) / len(data)) * 100, 2), "%")
    print(f"C sequences:", len(C_seq), round((len(C_seq) / len(data)) * 100, 2), "%")
    print(f"T sequences:", len(T_seq), round((len(T_seq) / len(data)) * 100, 2), "%")

    print(f"Data was organized in %s seconds" % round((time.time() - start_time), 2))
    print("-----" * 10)
    return A_seq, G_seq, C_seq, T_seq


if __name__ == "__main__":
    print("Organizing Sausage Data")
    print("This function returns 4 arrays of Sausage data, organized by first nucleotide (ATCG).")
    print("Call this function inside another script!")
