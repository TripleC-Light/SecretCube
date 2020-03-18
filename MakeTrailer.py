# -*- coding: utf-8 -*-
from os.path import isfile, join
import os
import time
import datetime
import math
from SQLiteOperate import SQLiteOperate
import sys
sys.path.append('./common')
import common.myFunction as myFunc

class MakeTrailer:
    def __init__(self, _ffmpegAbsPath=r'./ffmpeg/bin/'):
        self.ffmpegPath = _ffmpegAbsPath
        self.supportVideoType = {'.mp4', ".mkv", ".ts", ".avi"}
        self.startTime = '0'
        self.CutLenth = '1'
        self.splitVideoNum = 10
        self.SourceVideosPath = ''
        self.OutVideosPath = ''
        self.FPS = 15
        self.Duration = ''
        self.Resolution = ''
        self.AspectRatio = ''
        self.setMaxSize = [320, 240]
        self.newName = ''
        self.scanFileNumLimit = 9999
        self.processDegree = ''
        self.afterScaleSize = {}
        self.videoListTableName = 'videoList'
        self.setVideoListTable = [{'name': 'ID', 'Type': 'INTEGER', 'Default': '', 'Option': 'PRIMARY KEY AUTOINCREMENT'},
                                  {'name': 'VideoAbsPath', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                                  {'name': 'dbVideoName', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                                  {'name': 'Duration', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                                  {'name': 'Score', 'Type': 'INTEGER', 'Default': '0', 'Option': 'NOT NULL'},
                                  {'name': 'Views', 'Type': 'INTEGER', 'Default': '0', 'Option': 'NOT NULL'},
                                  {'name': 'Tag', 'Type': 'TEXT', 'Default': '', 'Option': ''},
                                  {'name': 'CreateDate', 'Type': 'DATE', 'Default': '', 'Option': 'NOT NULL'},
                                  {'name': 'LastSeeDate', 'Type': 'DATE', 'Default': '', 'Option': ''},
                                  {'name': 'Comment', 'Type': 'TEXT', 'Default': '', 'Option': ''}]
        self.tagListTableName = 'tagList'
        self.setTagListTable = [{'name': 'ID', 'Type': 'INTEGER', 'Default': '', 'Option': 'PRIMARY KEY AUTOINCREMENT'},
                                {'name': 'Tag', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                                {'name': 'useNum', 'Type': 'INTEGER', 'Default': '0', 'Option': 'NOT NULL'}]
        self.errMsg = {'E001': '#E001 Directory has already exist',
                       'E002': '#E002 Video not in support video type',
                       'E003': '#E003 Can not make Trailer',
                       'E004': '#E004 Can not Creat Data Base',
                       'E005': '#E005 File has already exist',
                       'E006': "#E006 File name has error char like ', #, +"}
        # Initial
        self.videoOutPath = ".\static\\"
        self.creatTempDir(self.videoOutPath)
        self.creatTempDir(self.videoOutPath + 'temp')
        self.creatTempDir(self.videoOutPath + 'pic')
        self.creatTempDir(self.videoOutPath + 'trailer')
        self.SQ3 = SQLiteOperate()
        self.creatDataBase(self.videoOutPath + 'temp\\videoDB')
        myFunc.creatTempTxtForVideoCombine(self.videoOutPath+'temp', self.splitVideoNum)
        tmp = self.videoOutPath.replace('.\\', '')
        self.setOutVideosPath(os.path.join(os.getcwd(), tmp))

        self.setFPS(self.FPS)
        self.setSplitVideoNum(self.splitVideoNum)
        self.setTrailerLengthInSecond(self.CutLenth)
        self.setTrailerSize(self.setMaxSize)
        self.setStartCutTime(self.startTime)

    def creatDataBase(self, _name):
        try:
            self.SQ3.connectOrCreatDB(_name)
            self.SQ3.newTable(self.videoListTableName, self.setVideoListTable)
            self.SQ3.newTable(self.tagListTableName, self.setTagListTable)

            print('# Creat Data Base OK: ' + _name)
        except:
            print(self.errMsg['E004'])

    def creatTempDir(self, _tempPathAndName):
        try:
            os.mkdir(os.path.join(os.getcwd(), _tempPathAndName))
            print('# Creat directory OK: ' + _tempPathAndName)
        except:
            print(self.errMsg['E001'] + ': ' + _tempPathAndName)

    def setStartCutTime(self, _startTime='0'):
        # -ss 00:00:10 : 從00:00:10開始切割
        self.startTime = ' -ss ' + _startTime

    def setTrailerLengthInSecond(self, _CutLenth):
        # -t 00:00:3 : 切割00:00:3秒
        self.CutLenth = ' -t ' + str(_CutLenth)

    def setSourceVideosPath(self, _SourceVideosPath):
        self.SourceVideosPath = _SourceVideosPath

    def setOutVideosPath(self, _OutVideosPath):
        self.OutVideosPath = _OutVideosPath

    def setFPS(self, _fps):
        # -r 12 : 12fps
        self.FPS = ' -r ' + str(_fps)

    def setTrailerSize(self, _size):
        self.setWidth = _size[0]
        self.setHeight = _size[1]

    def setSplitVideoNum(self, _splitVideoNum):
        self.splitVideoNum = _splitVideoNum
        myFunc.creatTempTxtForVideoCombine(self.videoOutPath+'temp', self.splitVideoNum)

    def setOutVideoName(self, _newName):
        self.newName = _newName

    def _scaleSizeToSetSize(self):
        # -vf scale=min(704, trunc(480 * dar / 2 + 0.5) * 2):min(480, trunc(704 / dar / 2 + 0.5) * 2)
        _tmp = self.AspectRatio.split(':')
        _dar = int(_tmp[0])/int(_tmp[1])
        self.afterScaleSize['Width'] = str(min(self.setWidth, math.floor(self.setHeight * _dar / 2 + 0.5) * 2))
        self.afterScaleSize['Height'] = str(min(self.setHeight, math.floor(self.setWidth / _dar / 2 + 0.5) * 2))
        return " -vf scale=" + self.afterScaleSize['Width'] + ':' + self.afterScaleSize['Height']

    def getVideoInfo(self, _fileName):
        self.Duration = self._getDuration(_fileName)
        self.Resolution = self._getResolution(_fileName)
        self.AspectRatio = self._getAspectRatio()
        _infoAll = {'Duration': self.Duration,
                    'Resolution': self.Resolution,
                    'AspectRatio': self.AspectRatio}
        # print(_infoAll)
        return _infoAll

    def _getDuration(self, _fileName):
        # add '-sexagesimal' to display in format 00:00:00.0
        _ffmpegCMD = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '
        _cmd = self.ffmpegPath + _ffmpegCMD + '"' + _fileName + '"'
        _stdoutput, _erroutput = myFunc.exeCMD(_cmd)
        _duration = myFunc.getStrFromStartToEnd(str(_stdoutput), "'", "\\")
        return _duration

    def _getResolution(self, _fileName):
        _ffmpegCMD = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 '
        _cmd = self.ffmpegPath + _ffmpegCMD + '"' + _fileName + '"'
        _stdoutput, _erroutput = myFunc.exeCMD(_cmd)
        _stdoutput = myFunc.getStrFromStartToEnd(str(_stdoutput), "'", "\\")
        _stdoutput = _stdoutput.split(",")
        _resolution = {'width': _stdoutput[0],
                       'height': _stdoutput[1]}
        return _resolution

    def _getAspectRatio(self):
        return self.Resolution['width'] + ":" + self.Resolution['height']

    def clipVideo(self, _inVideoName):
        # 影片從 00:00:02 開始 3秒轉為無聲音的mp4短片
        # -i 輸入檔名: 影片名稱, -an: 將音訊取消, -y: 同檔名將直接覆蓋, -s 320x180: 變更解析度為320*180
        _ffmpegCMD = 'ffmpeg' + self.CutLenth + self.startTime
        _ffmpegCMD += r' -noautorotate -i ' + '"' + _inVideoName + '"'
        _ffmpegCMD += self.FPS + ' -an -y' + self._scaleSizeToSetSize() + ' ' + '"' + self.OutVideosPath + 'temp\\' + self.newName + '"'
        _cmd = self.ffmpegPath + _ffmpegCMD
        myFunc.exeCMD(_cmd)

    def makeTrailer(self, _fullFilePath):
        _fullFilePath = _fullFilePath.replace('\\', '/')
        _filePath, _fileName = os.path.split(_fullFilePath)
        _onlyFileName, _extensionName = os.path.splitext(_fileName)

        self.SQ3.connectOrCreatDB(self.videoOutPath + 'temp\\videoDB')
        _cursor = self.SQ3.getData('videoList', '*', 'VideoAbsPath="' + _fullFilePath + '"')
        _result = _cursor.fetchone()
        if _result:
            self.SQ3.close()
            return [True, _fileName + '   ' + self.errMsg['E005'], 0]

        if _fullFilePath.find("'") >= 0 or _fullFilePath.find("#") >= 0 or _fullFilePath.find("+") >= 0:
            return [True, _fileName + '   ' + self.errMsg['E006'], 0]

        if _extensionName.lower() in self.supportVideoType:
            _tStart = time.time()
            _videoInfo = self.getVideoInfo(_fullFilePath)
            _jumpToNextTimeGap = math.floor(float(_videoInfo['Duration']) / (self.splitVideoNum + 1))

            for _i in range(self.splitVideoNum):
                self.setOutVideoName('tmp' + str(_i) + '.mp4')
                self.clipVideo(_fullFilePath)
                self.setStartCutTime(str((_i + 1) * _jumpToNextTimeGap))

            self.setStartCutTime('0')
            _originalFileName = _onlyFileName
            _onlyFileName = _onlyFileName.replace(' ', '')
            _fileNameNoSpace = _onlyFileName + '.mp4'
            self.combineVideo(self.videoOutPath + 'temp/combineList.txt',
                              self.videoOutPath + 'trailer/' + _fileNameNoSpace)

            _trailerLength = self.CutLenth.split(" ")
            _startCaptureTime = str(round((self.splitVideoNum * float(_trailerLength[2])) / 2, 2))
            _captureSize = self.afterScaleSize
            _captureVideo = self.videoOutPath + 'trailer/' + _fileNameNoSpace
            _saveScreenShot = self.videoOutPath + 'pic/' + _onlyFileName + '.jpg'
            self.screenShot(_captureVideo, _saveScreenShot, _startCaptureTime, _captureSize)

            try:
                _mp4NewName = myFunc.ifFileExistReturnNewName(self.videoOutPath + 'trailer/' + _originalFileName + '.mp4')
                os.rename(self.videoOutPath + 'trailer/' + _onlyFileName + '.mp4', _mp4NewName)
                _jpgNewName = myFunc.ifFileExistReturnNewName(self.videoOutPath + 'pic\\' + _originalFileName + '.jpg')
                os.rename(self.videoOutPath + 'pic\\' + _onlyFileName + '.jpg', _jpgNewName)

                _filePath, _fileName = os.path.split(_mp4NewName)
                _duration = myFunc.secToStdTimeFormat(math.ceil(float(_videoInfo['Duration'])))
                self.SQ3.connectOrCreatDB(self.videoOutPath + 'temp\\videoDB')
                _fullFilePath = _fullFilePath.replace('\\', '/')
                _today = str(datetime.datetime.now().date())
                self.SQ3.addData('videoList', 'VideoAbsPath, dbVideoName, Duration,  Score, Views, Tag, CreateDate, LastSeeDate', '"' + _fullFilePath + '", "' + _fileName + '","' + _duration + '", 0, 0, "", "' + _today + '", "' + _today + '"')
                self.SQ3.close()
                _msg = ''
            except:
                print(_videoInfo)
                print(self.afterScaleSize)
                _msg = '   ' + self.errMsg['E003']

            _tEnd = time.time()
            return [True, _fileName + _msg, round((_tEnd - _tStart), 3)]
        else:
            return [False, _fileName]

    def scanAndMakeTrailer(self, _dirPath):
        _updateMakeTrailerStatus = myFunc.UpdateMakeTrailerStatus()
        _totalVideoNum = self.countVideoNum(_dirPath)
        _allDirAndFile = os.walk(_dirPath)
        _fileNum = 0
        if _totalVideoNum != 0:
            for _root, _dirs, _files in _allDirAndFile:
                for _f in _files:
                    _fullFilePath = join(os.path.join(_root, _f))
                    if isfile(_fullFilePath):
                        _response = self.makeTrailer(_fullFilePath)
                        if _response[0]:
                            _fileNum += 1
                            print('檔案' + str(_fileNum) + ': ' + _response[1] + '  #處理時間: ' + str(_response[2]) + '秒')
                            self.processDegree = str(_fileNum) + ',' + str(_totalVideoNum) + ',' + str(_response[1]) + ',' + str(_response[2])
                            _updateMakeTrailerStatus.setStatus(self.processDegree)
                    if _fileNum >= self.scanFileNumLimit:
                        break
                if _fileNum >= self.scanFileNumLimit:
                    break
        else:
            self.processDegree = str(_fileNum) + ',' + str(_totalVideoNum) + ',' + str('') + ',' + str('')
            _updateMakeTrailerStatus.setStatus(self.processDegree)
        return True, _fileNum

    def combineVideo(self, _combineListTxt, _savePathAndName):
        _ffmpegCMD = 'ffmpeg -f concat -noautorotate -i ' + _combineListTxt + ' -c copy -y ' + _savePathAndName
        _cmd = self.ffmpegPath + _ffmpegCMD
        myFunc.exeCMD(_cmd)

    def screenShot(self, _captureVideo, _saveScreenShot, _startCaptureTime, _captureSize):
        _ffmpegCMD = 'ffmpeg -ss ' + _startCaptureTime + ' -noautorotate -i ' + _captureVideo + ' -y -f image2 -vframes 1 -s ' + _captureSize['Width'] + 'x' + _captureSize['Height'] + ' ' + _saveScreenShot
        _cmd = self.ffmpegPath + _ffmpegCMD
        # print('_cmd = ' + _cmd)
        myFunc.exeCMD(_cmd)

    def countVideoNum(self, _path):
        _totalFileNum = 0
        _list_dirs = os.walk(_path)
        for _root, _dirs, _files in _list_dirs:
            for _f in _files:
                _onlyFileName, _extensionName = os.path.splitext(_f)
                if _extensionName.lower() in self.supportVideoType:
                    _totalFileNum += 1
        return _totalFileNum

    def MakeTrailerAutoRunInDefaultSetting(self, _path):
        from common.myClass import SettingOperate
        settingOperate = SettingOperate()
        _videoPathList = settingOperate.getVideosPath()
        print(_videoPathList)
        if _path not in _videoPathList:
            settingOperate.addScanPath(_path)

        _splitVideoNum = 5
        _trailerLengthInSecond = 0.8
        _FPS = 10
        # _trailerSize = [200, 113]
        _trailerSize = [212, 120]
        _scanFileNumLimit = 9999
        _videoSourcePath = _path + "\\"
        self.scanFileNumLimit = _scanFileNumLimit

        print('# 影像檔共: ' + str(self.countVideoNum(_videoSourcePath)) + '個')
        print('# 影像轉檔限制為: ' + str(self.scanFileNumLimit) + '個')

        self.setFPS(_FPS)
        self.setSplitVideoNum(_splitVideoNum)
        self.setTrailerLengthInSecond(_trailerLengthInSecond)
        self.setTrailerSize(_trailerSize)
        self.setStartCutTime('0')

        _processTimeStart = time.time()
        _processFileNum = self.scanAndMakeTrailer(_videoSourcePath)
        _processTimeEnd = time.time()  # 計時結束

        print('共處理: ' + str(_processFileNum[1]) + '個檔案, 全部處理時間: ' + str(round((_processTimeEnd - _processTimeStart), 3)) + '秒')
        # return True

if __name__ == '__main__':
    v2MP4 = MakeTrailer()
    v2MP4.MakeTrailerAutoRunInDefaultSetting(r"F:\動畫\forTest3")
