#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
from datetime import datetime
import os
import time

# お借りします
CSV_PATH = "https://loto7.thekyo.jp/data/loto7.csv"

MAX_NUM_LOTO_6 = 43
MAX_NUM_LOTO_7 = 37

class Loto:
    def download(self, filename):
        r = requests.get(CSV_PATH)

        if filename == '':
            filename = 'loto.csv'

        # ファイルの保存
        if r.status_code == 200:
            with open(filename, 'w') as f:
                f.write(r.content.decode('cp932'))
        return

    def conv_bindata(self, hit_numbers):
        maxnum = MAX_NUM_LOTO_6 if len(hit_numbers) == 6 else MAX_NUM_LOTO_7
        bindata = ""
        for n in hit_numbers:
            while len(bindata) + 1 < n:
                bindata += "0"
            bindata += "1"
        while len(bindata) < maxnum:
            bindata += "0"

        return bindata
        
