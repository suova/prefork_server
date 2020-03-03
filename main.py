from config import config
from constants import HOST, PORT, QUEUE, DATA_SIZE, ROOT_DIR
from server import Server


def main():
    conf = config()
    count_cpu = int(conf['cpu_limit'])
    document_root = conf['document_root']
    #server = Server(HOST, PORT, QUEUE,  DATA_SIZE, count_cpu, document_root)
    print("server run")
    server = Server("127.0.0.1", 3333, QUEUE, DATA_SIZE, count_cpu, ROOT_DIR)
    server.launch()


if __name__ == '__main__':
    main()
