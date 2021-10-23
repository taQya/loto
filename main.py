#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import os
import Loto

# ロガー設定
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

# CSVフォーマット
# 0 開催回
# 1 日付
# 2 第1数字
# 3 第2数字
# 4 第3数字
# 5 第4数字
# 6 第5数字
# 7 第6数字
# 8 第7数字
# 9 BONUS数字1
# 10 BONUS数字2
# other 1等口数	2等口数	3等口数	4等口数	5等口数	6等口数	1等賞金	2等賞金	3等賞金	4等賞金	5等賞金	6等賞金	キャリーオーバー
header_column = [
    "日付",
    "第1数字",
    "第2数字",
    "第3数字",
    "第4数字",
    "第5数字",
    "第6数字",
    "第7数字",
    "BONUS数字1",
    "BONUS数字2",
]

OUTPUT_DIR = os.getcwd()

def get_string(v, default_value=""):
    s = v
    return default_value if not s else s

def get_int(v):
    s = get_string(v)
    return 0 if not s else int(s)

def output(data_list):
    # ヘッダ
    header = ""
    for h in header_column:
        header += '\"' + h + '\"' + '\t'
    header += '\n'

    # ファイル名
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    output = OUTPUT_DIR + "/loto7_hitdata_" + yyyymmdd + ".csv"
    logger.info(output + " に出力します。")

    # 出力
    with open(output, "w") as f:
        f.write(header)
        for data in data_list:
            for d in data:
                f.write(d)
                f.write(',')
            f.write('\n')

def output_binary(bin_list):
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    output = OUTPUT_DIR + "/loto7_bindata_" + yyyymmdd + ".csv"
    logger.info(output + " に出力します。")

    # 出力
    with open(output, "w") as f:
        for data in bin_list:
            f.write(data)
            f.write('\n')

def conv_hitdata(f):
    '''
    当選数字のみを抜き出す
    '''
    header = next(f)
    hitdata = []
    for row in f:
        oneday = []
        oneday.append(row[1])
        oneday.append(row[2])
        oneday.append(row[3])
        oneday.append(row[4])
        oneday.append(row[5])
        oneday.append(row[6])
        oneday.append(row[7])
        oneday.append(row[8])
        oneday.append(row[9])
        oneday.append(row[10])
        hitdata.append(oneday)

    output(hitdata)

def conv_bindata(f):
    '''
    1~MAXで当選した数字を1、非当選が0で出力
    '''

    l = Loto.Loto()

    header = next(f)
    bin_list = []
    for row in f:
        oneday = []
        oneday.append(get_int(row[1]))
        oneday.append(get_int(row[2]))
        oneday.append(get_int(row[3]))
        oneday.append(get_int(row[4]))
        oneday.append(get_int(row[5]))
        oneday.append(get_int(row[6]))
        oneday.append(get_int(row[7]))
        bindata = l.conv_bindata(oneday)
        bin_list.append(bindata)

    output_binary(bin_list)

def main():
    l = Loto.Loto()
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    filename = OUTPUT_DIR + "/loto_" + yyyymmdd + ".csv"


    if os.path.exists(filename) == False:
        l.download(filename)

    csv_file = open(filename, "r")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    conv_hitdata(f)

    hitdata = OUTPUT_DIR + "/loto7_hitdata_" + yyyymmdd + ".csv"

    csv_file = open(hitdata, "r")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    conv_bindata(f)

if __name__ == '__main__':
    main()
