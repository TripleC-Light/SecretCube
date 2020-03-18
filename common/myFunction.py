# -*- coding: utf-8 -*-
import subprocess
import os
import math
from os.path import exists

def getStrFromStartToEnd(_inputStr, _StrstStr, _EndStr):
    _strTmp = _inputStr.split(_StrstStr)
    _strTmp = _strTmp[1].split(_EndStr)
    return _strTmp[0]

def exeCMD(_cmd):
    p = subprocess.Popen(_cmd, creationflags=0x08, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _stdoutput, _erroutput = p.communicate()
    p.wait()
    p.terminate()
    p.kill()
    return _stdoutput, _erroutput

def ifFileExistReturnNewName(_filePathAndName):
    _newName = _filePathAndName
    _tryTimes = 0
    while os.path.exists(_newName):
        _tryTimes += 1
        _onlyFileName, _extensionName = os.path.splitext(_filePathAndName)
        _onlyFileName += '[' + str(_tryTimes) + ']' + _extensionName
        _newName = _onlyFileName
    return _newName

def secToStdTimeFormat(_sec):
    _duration = _sec
    _durationHour = math.floor(_duration / 60 / 60)
    _durationMin = math.floor(_duration / 60) - (_durationHour * 60)
    _durationSec = math.floor(_duration % 60)
    if len(str(_durationHour)) < 2:
        _durationHour = '0' + str(_durationHour)
    if len(str(_durationMin)) < 2:
        _durationMin = '0' + str(_durationMin)
    if len(str(_durationSec)) < 2:
        _durationSec = '0' + str(_durationSec)

    if _durationHour == 0:
        return str(_durationMin) + ':' + str(_durationSec)
    else:
        return str(_durationHour) + ':' + str(_durationMin) + ':' + str(_durationSec)

def creatTempTxtForVideoCombine(_tempPath, _splitVideoNum):
    _openFile = open(_tempPath + '\combineList.txt', 'w')
    _str = ''
    for _i in range(_splitVideoNum):
        _str += "file 'tmp" + str(_i) + ".mp4'\n"
    _openFile.write(_str)
    _openFile.close()

class PlayVideo:
    def __init__(self, _cmd):
        self.p = subprocess.Popen(_cmd, creationflags=0x08, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def close(self):
        self.p.terminate()
        self.p.kill()

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

class UpdateMakeTrailerStatus:
    def __init__(self):
        self.settingPath = r'./static/temp/makeTrailerStatus.ini'
        if not exists(self.settingPath):
            self.clearText()

    def clearText(self):
        _openFile = open(self.settingPath, 'w', encoding='utf-8')
        _openFile.close()

    def setStatus(self, _status):
        _openFile = open(self.settingPath, 'a+', encoding='utf-8')
        _openFile.write(str(_status) + '\n')
        _openFile.close()

    def getStatus(self):
        _openFile = open(self.settingPath, 'r', encoding='utf-8')
        _status = _openFile.read()
        _openFile.close()
        return str(_status)
