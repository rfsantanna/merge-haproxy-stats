#!/usr/bin/env python

import os
import glob

sockets_dir = '/var/run/haproxy'
merged_socket = f'{sockets_dir}/info.sock'
proc_sockets = glob.glob(f'{sockets_dir}/hastat-proc*.sock')

numbered_stats = {
    1: '# pxname',
    2: 'svname',
    3: 'qcur',
    4: 'qmax',
    5: 'scur',
    6: 'smax',
    7: 'slim',
    8: 'stot',
    9: 'bin',
    10: 'bout',
    11: 'dreq',
    12: 'dresp',
    13: 'ereq',
    14: 'econ',
    15: 'eresp',
    16: 'wretr',
    17: 'wredis',
    18: 'status',
    19: 'weight',
    20: 'act',
    21: 'bck',
    22: 'chkfail',
    23: 'chkdown',
    24: 'lastchg',
    25: 'downtime',
    26: 'qlimit',
    27: 'pid',
    28: 'iid',
    29: 'sid',
    30: 'throttle',
    31: 'lbtot',
    32: 'tracked',
    33: 'type',
    34: 'rate',
    35: 'rate_lim',
    36: 'rate_max',
    37: 'check_status',
    38: 'check_code',
    39: 'check_duration',
    40: 'hrsp_1xx',
    41: 'hrsp_2xx',
    42: 'hrsp_3xx',
    43: 'hrsp_4xx',
    44: 'hrsp_5xx',
    45: 'hrsp_other',
    46: 'hanafail',
    47: 'req_rate',
    48: 'req_rate_max',
    49: 'req_tot',
    50: 'cli_abrt',
    51: 'srv_abrt',
    52: 'comp_in',
    53: 'comp_out',
    54: 'comp_byp',
    55: 'comp_rsp',
    56: 'lastsess',
    57: 'last_chk',
    58: 'last_agt',
    59: 'qtime',
    60: 'ctime',
    61: 'rtime',
    62: 'ttime'
}

procs_data = {os.path.basename(sock):[] for sock in proc_sockets}
result = {}

med_list = [
    24, 25, 39, 58, 59, 60, 62,
]
fixed_list = [
    1, 2, 7, 18, 19, 20, 21, 26, 28, 
    29, 30, 32, 33, 35, 37, 38, 56,
]
sum_list = [
    3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 
    14, 15, 16, 17, 22, 23, 31, 34, 35, 
    36, 40, 41, 42, 43, 44, 45, 46, 47, 
    48, 49, 50, 51, 52, 53, 54, 55, 61,
]
