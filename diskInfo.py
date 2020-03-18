# -*- coding: utf-8 -*-
import time
import os

def getDiskList():
    _diskID = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    _diskList = ['C']
    for diskIDind in _diskID:
        try:
            _openFile = open(diskIDind + ':\\scan.txt', 'w')
            _openFile.close()
            os.remove(diskIDind + ':\\scan.txt')
            _diskList.append(diskIDind)
        except IOError:
            pass
    return _diskList

if __name__ == "__main__":
    print(getDiskList())
    print('--------------------------------')
    time.sleep(5)
