from functions import read_sausage


if __name__ == '__main__':
    print("Hello world")

    sausage_data = read_sausage('SausageTest.fasta', 51)

    print(sausage_data[0])
