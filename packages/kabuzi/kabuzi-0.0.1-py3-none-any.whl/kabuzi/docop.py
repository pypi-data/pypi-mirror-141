import os
import re
import time

import numpy as np


class SaveTxt:
    """保存字符到 txt 文件中"""

    def __init__(self, file, mode='w'):
        self.f = open(file, mode, encoding='utf-8')

    def write_str(self, l):
        self.f.write(l)

    def close_file(self):
        self.f.close()


class Timer:
    """Record multiple running times."""
    def __init__(self):
        self.times = []
        self.start()

    def start(self):
        """Start the timer."""
        self.tik = time.time()

    def stop(self):
        """Stop the timer and record the time in a list."""
        self.times.append(time.time() - self.tik)
        return self.times[-1]

    def avg(self):
        """Return the average time."""
        return sum(self.times) / len(self.times)

    def sum(self):
        """Return the sum of time."""
        return sum(self.times)

    def cumsum(self):
        """Return the accumulated time."""
        return np.array(self.times).cumsum().tolist()


class Accumulator:
    """For accumulating sums over `n` variables."""
    def __init__(self, n):
        self.data = [0.0] * n

    def add(self, *args):
        self.data = [a + float(b) for a, b in zip(self.data, args)]

    def reset(self):
        self.data = [0.0] * len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


def isrepeated(path, mark='-dup'):
    """ 假如保存的文件重名，则在名字后面增加 “-dup” """
    while os.path.exists(path):
        dir_ = re.findall("(.*)\.", path)
        file_type = re.findall("(\.[a-z].*)", path)
        path = os.path.join(dir_[0] + mark + file_type[0])
    return path


def time_file(path):
    """ 在给定的路径下按 “年-月/日/时-分-秒” 创建文件夹并返回 """
    year_month = time.strftime('%Y-%m', time.localtime())
    day = time.strftime('%d', time.localtime())
    hour_min = time.strftime('%H-%M-%S', time.localtime())
    # 用时间创建文件夹
    file_root = os.path.join(path, '{}/{}/{}'.format(year_month, day, hour_min))

    # 判断路径是否存在，不存在创建文件夹
    if not os.path.exists(file_root): os.makedirs(file_root)
    return file_root
