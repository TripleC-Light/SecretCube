# -*- coding: utf-8 -*-
from MakeTrailer import MakeTrailer
import threading
import datetime
from SQLiteOperate import SQLiteOperate
from findPlayer import FindPlayer
import diskInfo
import os
from os.path import exists
import random

class SettingOperate:
    def __init__(self):
        self.settingPath = r'./static/temp/setting.ini'
        if not exists(self.settingPath):
            _openFile = open(self.settingPath, 'w', encoding='utf-8')
            _openFile.close()

    def setSettingPath(self, _settingPath):
        self.settingPath = _settingPath

    def setDefaultPlayerPath(self, _playerPath=''):
        if _playerPath == '':
            _openFile = open(self.settingPath, 'a+', encoding='utf-8')
            _openFile.close()

            _settingTxt = ''
            _hasSetted = False
            with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
                for line in _openFile:
                    _line = line
                    _tmp = _line.split('*')
                    if _tmp[0] == 'videoPath':
                        _hasSetted = True
                    _settingTxt += _line
            _openFile.close()

            if not _hasSetted:
                _openFile = open(self.settingPath, 'a+', encoding='utf-8')
                _findPlayer = FindPlayer()
                _playerList = _findPlayer.find()
                _openFile.write('videoPath*' + _playerList[0][1] + '\n')
                _openFile.close()
        else:
            _settingTxt = ''
            with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
                for line in _openFile:
                    _line = line
                    _tmp = _line.split('*')
                    if _tmp[0] == 'videoPath':
                        _line = _tmp[0] + '*' + _playerPath + '\n'
                    _settingTxt += _line
            _openFile.close()
            _openFile = open(self.settingPath, 'w', encoding='utf-8')
            _openFile.write(str(_settingTxt))
            _openFile.close()

    def getPlayerPath(self):
        _playerPath = ''
        with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
            for line in _openFile:
                _line = line
                _tmp = _line.split('*')
                if _tmp[0] == 'videoPath':
                    _playerPath = _tmp[1]
            _openFile.close()
            return _playerPath

    def addScanPath(self, _scanPath):
        _openFile = open(self.settingPath, 'a+', encoding='utf-8')
        _openFile.write(_scanPath + '\n')
        _openFile.close()

    def getVideosPath(self):
        _videosPathList = []
        with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
            for line in _openFile:
                _line = line
                _tmp = _line.split('*')
                if len(_tmp) < 2:
                    _videosPathList.append(_line.rstrip('\n'))
        _openFile.close()
        return _videosPathList

    def setVideoNum(self, _videoNum):
        _settingTxt = ''
        _hasSetted = False
        with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
            for line in _openFile:
                _line = line
                _tmp = _line.split('*')
                if _tmp[0] == 'videoNum':
                    _hasSetted = True
                    _line = _tmp[0] + '*' + str(_videoNum) + '\n'
                _settingTxt += _line
        _openFile.close()

        if not _hasSetted:
            _openFile = open(self.settingPath, 'a+', encoding='utf-8')
            _openFile.write('videoNum*' + str(_videoNum) + '\n')
            _openFile.close()
        else:
            _openFile = open(self.settingPath, 'w', encoding='utf-8')
            _openFile.write(_settingTxt)
            _openFile.close()

    def getVideoNum(self):
        _videoNum = ''
        with open(self.settingPath, 'r', encoding='utf-8') as _openFile:
            for line in _openFile:
                _line = line
                _tmp = _line.split('*')
                if _tmp[0] == 'videoNum':
                    _videoNum = _tmp[1]
            _openFile.close()
            return _videoNum

def startMakeTrailer(_videoPath):
    print(_videoPath)
    _v2MP4 = MakeTrailer()
    _t1 = threading.Thread(target=_v2MP4.MakeTrailerAutoRunInDefaultSetting, args=(_videoPath,))  # 建立一個子執行緒
    _t1.start()

class GenIndexWebData:
    def __init__(self, _allocate=''):
        _videoInfoListFromDB = self.getVideoInfoFromDB('videoList', '*',  _allocate)
        self._videoInfoToWeb = self.genVideoInfoToWeb(_videoInfoListFromDB)

    def getVideoInfoToWeb(self):
        return self._videoInfoToWeb

    def getAllTag(self):
        _allTagList = []
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('tagList', 'Tag')
        for rowData in _SQ3data:
            _allTagList.append(rowData[0])
        _SQ3.close()
        return _allTagList

    def getVideoInfoFromDB(self, _table, _fields, _allocate=''):
        _videoInfoList = []
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData(_table, _fields, _allocate)
        if _fields == '*':
            _fields = _SQ3.getFieldName(_table)
        else:
            _fields = _fields.replace(' ', '')
        _fields = _fields.split(',')
        for rowData in _SQ3data:
            _keyValue = ({})
            for _i in range(len(_fields)):
                _keyValue[_fields[_i]] = rowData[_i]
            _videoInfoList.append(_keyValue)

        if _allocate.find(' ORDER BY ID') >= 0:
            # print('ORDER BY RAND')
            random.shuffle(_videoInfoList)
        _SQ3.close()
        return _videoInfoList

    def genVideoInfoToWeb(self, _videoInfoListFromDB):
        _videoInfoToWeb = []
        for _videoInfo in _videoInfoListFromDB:
            _URLpath = self.getMidPath(_videoInfo['VideoAbsPath']) + _videoInfo['VideoAbsPath']
            _videoNameToHTML = self.getVideoNameToHTML(_videoInfo['VideoAbsPath'])
            _onlyFileName, _extensionName = os.path.splitext(_videoInfo['dbVideoName'])
            _views = _videoInfo['Views']
            _duration = _videoInfo['Duration']
            _tag = ''

            if _videoInfo['Tag']:
                _tag = _videoInfo['Tag'].strip("['']").split("', '")
            _videoInfoToWeb.append(
                {'videoInfo': _videoInfo, 'videoName': _onlyFileName, 'videoNameToHTML': _videoNameToHTML, 'videoAbsLink': _URLpath,
                 'Views': _views, 'Duration': _duration, 'Tag': _tag})
        return _videoInfoToWeb

    def genIndexLayout(self, Columns, Rows, videoWidth, videoHeight=''):
        if videoHeight == '':
            videoHeight = videoWidth * (9 / 16)
        _videoSize = ({'width': videoWidth, 'height': videoHeight})
        return {'ColumnNum': Columns, 'RowNum': Rows, 'VideoSize': _videoSize}

    def getMidPath(self, _filePath):
        diskList = diskInfo.getDiskList()
        _filePath = _filePath.split(':')
        _diskID = _filePath[0]
        _midPath = './path0/'
        for _compareDiskID in range(len(diskList)):
            if diskList[_compareDiskID] == _diskID:
                _midPath = './path' + str(_compareDiskID) + '/'
        return _midPath

    def getVideoNameToHTML(self, _name):
        _filePath, _name = os.path.split(_name)
        return _name

class TagManage:
    def addNewTag(self, _videoAbsPath, _newTag):
        if _videoAbsPath != '':
            self._addNewTag_toVideoData(_videoAbsPath, _newTag)
        self._addNewTag_toTagListOnDatabase(_newTag)
        return True

    def getAllTag(self):
        _allTagList = []
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('tagList', 'Tag')
        for rowData in _SQ3data:
            _allTagList.append(rowData[0])
        _SQ3.close()
        return _allTagList

    def _addNewTag_toVideoData(self, _videoAbsPath, _newTag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Tag', 'VideoAbsPath="' + _videoAbsPath + '"')
        _tagList = ''
        _addNewTagToDB = False
        for rowData in _SQ3data:
            if rowData[0]:
                _tagList = rowData[0].strip("['']").split("', '")
                _tagList.append(_newTag)
                _addNewTagToDB = True
            else:
                _addNewTagToDB = True
                _tagList = "['" + _newTag + "']"
        if _addNewTagToDB:
            # print('Tag not in this Video')
            _SQ3.updateData('videoList', 'Tag="' + str(_tagList) + '"', 'VideoAbsPath="' + _videoAbsPath + '"')
        else:
            pass
            # print('Tag has exist in this Video')
        _SQ3.close()
        return _addNewTagToDB

    def _addNewTag_toTagListOnDatabase(self, _newTag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _addNewTagToDB = True
        _SQ3data = _SQ3.getData('tagList', 'Tag')
        for rowData in _SQ3data:
            if _newTag == rowData[0]:
                _addNewTagToDB = False
                # print('Tag has exist in Database')
        if _addNewTagToDB:
            _SQ3.addData('tagList', 'Tag', '"' + _newTag + '"')
            # print('Tag not in Database')
        _SQ3.close()
        return True

    def changeTagFromAllVideo(self, _Tag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Tag, VideoAbsPath')
        _oldTag, _newTag = _Tag.split(',')
        _tagList = ''
        for rowData in _SQ3data:
            _tagList = rowData[0].strip("['']").split("', '")
            if _oldTag in _tagList:
                _tagList[_tagList.index(_oldTag)] = _newTag
                _SQ3.updateData('videoList', 'Tag="' + str(_tagList) + '"', 'VideoAbsPath="' + rowData[1] + '"')
        _SQ3.close()
        return _tagList

    def changeTagFromDB(self, _Tag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _oldTag, _newTag = _Tag.split(',')
        _SQ3.updateData('tagList', 'Tag="' + _newTag + '"', 'Tag="' + _oldTag + '"')
        _SQ3.close()
        return True

    def deleteTagFromDB(self, _Tag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3.deleteData('tagList', 'Tag="' + _Tag + '"')
        _SQ3.close()
        return True


    def deleteTagFromAllVideo(self, _Tag):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Tag, VideoAbsPath')
        _tagList = ''
        for rowData in _SQ3data:
            _tagList = rowData[0].strip("['']").split("', '")
            if _Tag in _tagList:
                if len(_tagList) == 1:
                    _tagList = ''
                else:
                    _tagList.remove(_Tag)
                _SQ3.updateData('videoList', 'Tag="' + str(_tagList) + '"', 'VideoAbsPath="' + rowData[1] + '"')
        _SQ3.close()
        return _tagList

    def deleteTagFromOneVideo(self, _videoAbsPath, _Tag):
        # print('_Tag= ' + _Tag)
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Tag', 'VideoAbsPath="' + _videoAbsPath + '"')
        _tagList = ''
        for rowData in _SQ3data:
            _tagList = rowData[0].strip("['']").split("', '")
            if _Tag in _tagList:
                if len(_tagList) == 1:
                    _tagList = ''
                else:
                    _tagList.remove(_Tag)
        _SQ3.updateData('videoList', 'Tag="' + str(_tagList) + '"', 'VideoAbsPath="' + _videoAbsPath + '"')
        _SQ3.close()
        return _tagList

    def getTagList(self, _videoAbsPath):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Tag', 'VideoAbsPath="' + _videoAbsPath + '"')
        _tagList = ''
        for rowData in _SQ3data:
            if rowData[0] == '':
                return ''
            else:
                _tagList = rowData[0].strip("['']").split("', '")
        _SQ3.close()
        return _tagList

class StaticFunction:
    def getVideoAbsPathFromGET(self, _videoPath):
        _videoAbsPath = _videoPath.split('/')
        _tmp = ''
        for i in range(2, len(_videoAbsPath)):
            _tmp += _videoAbsPath[i] + '/'
        return _tmp.strip('/')

    def updateUserViewInfo(self, _videoAbsPath):
        _views = self.setViewsAddOne(_videoAbsPath)
        _newDate = self.setLastSeeDateAsToday(_videoAbsPath)
        return _views, _newDate

    def setViewsAddOne(self, _videoAbsPath):
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3data = _SQ3.getData('videoList', 'Views', 'VideoAbsPath="' + _videoAbsPath + '"')
        _views = 0
        for rowData in _SQ3data:
            _views = rowData[0]
        _views += 1
        _SQ3.updateData('videoList', 'Views=' + str(_views), 'VideoAbsPath="' + _videoAbsPath + '"')
        _SQ3.close()
        return _views

    def setLastSeeDateAsToday(self, _videoAbsPath):
        _newDate = datetime.datetime.now().date()
        # print('_newDate = ' + str(_newDate))
        _SQ3 = SQLiteOperate()
        _SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
        _SQ3.updateData('videoList', 'LastSeeDate="' + str(_newDate) + '"', 'VideoAbsPath="' + _videoAbsPath + '"')
        _SQ3.close()
        return _newDate
