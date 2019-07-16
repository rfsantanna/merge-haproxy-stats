#!/usr/bin/env python

import os
import csv
import glob
import json
import socket
from io import StringIO


class Config():

    conf_file = 'merge_config.json'
    conf_dir = os.path.dirname(os.path.realpath(__file__))
    conf = json.load(open(f'{conf_dir}/{conf_file}', 'r'))

    sockets_dir = conf.get('socket_dir', '/var/run/haproxy')
    merged_sock = (
        f'{sockets_dir}/{conf.get("merged_socket", "info.sock")}'
    )
    proc_sock_list = glob.glob(
        f'{sockets_dir}/'
        f'{conf.get("proc_socket_mask", "hastat-proc*.sock")}'
    )
    header = conf.get('header')
    avg_list = conf.get('avg_list')
    fix_list = conf.get('fix_list')
    sum_list = conf.get('sum_list')
    enum_stats = dict(enumerate(header, 1))


class HPSockets():
    
    def __init__(self):
        self.result = {}
        self.procs_data = {}
        self.avg_count = {}

    def _update_proc_stats(self):
        procs_data = {
            os.path.basename(sock):{} for sock in Config.proc_sock_list
        }
        for socket_path in Config.proc_sock_list:
            socket = os.path.basename(socket_path)
            updated_dict = self.run_show_stats(socket_path)
            procs_data[socket] = updated_dict
        self.procs_data = procs_data

    def _include_missing_stat(self, srv_num, stat_num):
        if self.result.get(srv_num):
            if self.result[srv_num].get(stat_num):
                return False
            else:
                self.result[srv_num][stat_num] = ''
        else:
            self.avg_count[srv_num] = {}
            self.result[srv_num] = {}
            self.result[srv_num][stat_num] = ''
        return True

    def _merge_stat(self, srv_num, stat_num, value):
        is_updated = self._include_missing_stat(srv_num, stat_num)
        if is_updated:
            if stat_num in Config.fix_list:
                self.result[srv_num][stat_num] = value
            elif stat_num in Config.avg_list:
                if self.avg_count[srv_num].get(stat_num):
                    self.avg_count[srv_num][stat_num] += 1
                else:
                    self.avg_count[srv_num][stat_num] = 1

        if stat_num in Config.sum_list + Config.avg_list:
            if self.result[srv_num][stat_num] == '':
                self.result[srv_num][stat_num] = 0
            if not value:
                value = 0
            tmp = int(self.result[srv_num][stat_num])
            self.result[srv_num][stat_num] = tmp
            self.result[srv_num][stat_num] += int(value)
            if stat_num in Config.avg_list:
                self.avg_count[srv_num][stat_num] += 1          

    def _update_average(self):
        for srv_num, avg_stats in self.avg_count.items():
            for stat_num, count in avg_stats.items():
                average = self.result[srv_num][stat_num] // count
                self.result[srv_num][stat_num] = average

    def create_unix_socket(self):
        if os.path.exists(Config.merged_sock):
            os.remove(Config.merged_sock)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(Config.merged_sock)
        server.listen(5)
        os.chmod(Config.merged_sock, 0o666)
        return server
    
    def wait_unix_socket_request(self):
        connection, client_address = self.server.accept()
        data  = connection.recv(1024)
        if data.startswith(b'show stat'):
            self.get_stats()
            csv = bytes(self.generate_csv() + '\n\n', 'utf-8')
            connection.sendall(csv)

    def run_show_stats(self, sock):
        if os.path.exists(sock):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(sock)
            client.send(b'show stat\n')
            response = StringIO(client.recv(8192).decode('utf-8'))
            client.close()
            return csv.DictReader(response)

    def generate_csv(self):
        csv_response = []
        csv_response.append(','.join(Config.header))
        for server_num in self.result:
            server_values = []
            for stat in self.result[server_num]:
                server_values.append(str(self.result[server_num][stat]))
            csv_response.append(','.join(server_values))
        return '\n'.join(csv_response)

    def get_stats(self):
        self._update_proc_stats()
        for proc in self.procs_data:
            for srv_num, srv_data in enumerate(self.procs_data[proc]):
                for stat_num, value in enumerate(srv_data, 1):
                    self._merge_stat(srv_num, stat_num, srv_data[value])
        self._update_average()


if __name__ == '__main__':
    hpsock = HPSockets()
    hpsock.server = hpsock.create_unix_socket()
    while True:
        hpsock.wait_unix_socket_request()
        hpsock.__init__()
