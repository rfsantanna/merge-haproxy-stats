#!/usr/bin/env python

import os
import csv
import glob
import json
import socket
from io import StringIO


class Config():

    def __init__(self, conf_file='merge_config.json'):
        conf_dir = os.path.dirname(os.path.realpath(__file__))
        conf = json.load(open(f'{conf_dir}/{conf_file}', 'r'))

        self.sockets_dir = conf.get('socket_dir', '/var/run/haproxy')
        self.merged_sock = (
            f'{self.sockets_dir}/{conf.get("merged_socket", "info.sock")}'
        )
        self.proc_sock_list = glob.glob(
            f'{self.sockets_dir}/'
            f'{conf.get("proc_socket_mask", "hastat-proc*.sock")}'
        )
        self.enum_stats = dict(enumerate(conf.get('header'), 1))
        self.avg_list = [24, 25, 39, 58, 59, 60, 62,]
        self.fix_list = [1, 2, 7, 18, 19, 20, 21, 26, 28,
                        29, 30, 32, 33, 35, 37, 38, 56,]
        self.sum_list = [3, 4, 5, 6, 8, 9, 10, 11, 12, 13,
                        14, 15, 16, 17, 22, 23, 31, 34, 35,
                        36, 40, 41, 42, 43, 44, 45, 46, 47,
                        48, 49, 50, 51, 52, 53, 54, 55, 61,]


def show_stat(sock):
    if os.path.exists(sock):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock)
        client.send(b'show stat\n')
        response = StringIO(client.recv(8192).decode('utf-8'))
        client.close()
        return csv.DictReader(response)

if __name__ == '__main__':
    conf = Config()
    procs_data = {os.path.basename(sock):[] for sock in conf.proc_sock_list}
    results = {}
