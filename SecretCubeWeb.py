# -*- coding: utf-8 -*-
import sys
import tornado.ioloop
import tornado.web
import os
import math
import random
import diskInfo
from findPlayer import FindPlayer
import common.myFunction as myFunc
from common.myClass import SettingOperate
from MakeTrailer import MakeTrailer
import webbrowser
from common.myClass import startMakeTrailer
from common.myClass import GenIndexWebData
from common.myClass import TagManage
from common.myClass import StaticFunction
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
sys.path.append('./common')

class TopSearchHandler(tornado.web.RequestHandler):
    def get(self):
        _genIndexWebData = GenIndexWebData()
        _videoInfoToWeb = _genIndexWebData.getVideoInfoToWeb()
        _settingOperate = SettingOperate()
        _settingOperate.setVideoNum(len(_videoInfoToWeb))
        self.render("topSearch.html", fileNum=len(_videoInfoToWeb))

class SideMenuHandler(tornado.web.RequestHandler):
    def get(self):
        _tagManage = TagManage()
        _allTag = _tagManage.getAllTag()
        self.render("sideMenu.html", allTag=_allTag)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        _searchVideo = self.get_argument('searchVideo', '')
        _order = self.get_argument('order', '')
        if _order != '':
            _order = ' ORDER BY ' + _order

        if _searchVideo != '':
            _genIndexWebData = GenIndexWebData('dbVideoName LIKE "%' + _searchVideo + '%" or Tag Like "%' + _searchVideo + '%"' + _order)
            _URL = "index.html"
        else:
            _genIndexWebData = GenIndexWebData(_order)
            _URL = "index.html"

        _videoInfoToWeb = _genIndexWebData.getVideoInfoToWeb()
        _allTag = _genIndexWebData.getAllTag()
        _videoShowColumns = 5
        _layoutWeb = _genIndexWebData.genIndexLayout(Columns=_videoShowColumns, Rows=math.ceil(len(_videoInfoToWeb)/_videoShowColumns), videoWidth=180)
        self.render(_URL, videoInfoToWeb=_videoInfoToWeb, allTag=_allTag, fileNum=len(_videoInfoToWeb), layoutHTML=_layoutWeb, searchVideo=_searchVideo)

class ShowVideoHandler(tornado.web.RequestHandler):
    def get(self):
        _videoPath = self.get_argument('videoPath', '')
        _stFunc = StaticFunction()
        _videoAbsPath = _stFunc.getVideoAbsPathFromGET(_videoPath)
        _stFunc.updateUserViewInfo(_videoAbsPath)
        _genIndexWebData = GenIndexWebData('VideoAbsPath="' + _videoAbsPath + '"')
        _videoInfoToWeb = _genIndexWebData.getVideoInfoToWeb()
        _SQL = ''
        if len(_videoInfoToWeb[0]['Tag']) > 0:
            for _i in range(len(_videoInfoToWeb[0]['Tag'])):
                _SQL += 'Tag Like "%' + _videoInfoToWeb[0]['Tag'][_i] + '%" or '
        _SQL = _SQL.rstrip(' or ')
        # print('_SQL = ' + _SQL)
        _relateVideoData = GenIndexWebData(_SQL)
        _relateVideoData = _relateVideoData.getVideoInfoToWeb()
        random.shuffle(_relateVideoData)
        # print(_relateVideoData)
        self.render("showVideo.html", videoPath=_videoPath, videoInfoToWeb=_videoInfoToWeb, relateVideoData=_relateVideoData)

class PlayByPlayerHandler(tornado.web.RequestHandler):
    def get(self):
        _settingOperate = SettingOperate()
        _playerPath = _settingOperate.getPlayerPath()
        _playerPath = _playerPath.rstrip('\n')
        _tmp, _player = os.path.split(_playerPath)

        if _playerPath == '':
            self.write('No set player')
        else:
            _videoAbsPath = self.get_argument('videoPath', '')
            _stFunc = StaticFunction()
            _videoAbsPath = _stFunc.getVideoAbsPathFromGET(_videoAbsPath)
            _newViews, _newDate = _stFunc.updateUserViewInfo(_videoAbsPath)
            os.system('taskkill /f /im ' + _player)
            myFunc.PlayVideo([_playerPath, _videoAbsPath])
            self.write(str(_newViews) + ',' + str(_newDate))

class EditTagHandler(tornado.web.RequestHandler):
    def get(self):
        _action = self.get_argument('action', '')
        _id = self.get_argument('id', '')
        _videoPath = self.get_argument('videoPath', '')
        _newTag = self.get_argument('newTag', '')
        _stFunc = StaticFunction()
        _videoAbsPath = _stFunc.getVideoAbsPathFromGET(_videoPath)
        _tagManage = TagManage()
        if _action == 'add' or _action == 'editAdd':
            _tagManage.addNewTag(_videoAbsPath, _newTag)
        elif _action == 'delete':
            _tagManage.deleteTagFromOneVideo(_videoAbsPath, _newTag)
        elif _action == 'editDelete':
            _tagManage.deleteTagFromAllVideo(_newTag)
            _tagManage.deleteTagFromDB(_newTag)
        elif _action == 'editChange':
            _tagManage.changeTagFromAllVideo(_newTag)
            _tagManage.changeTagFromDB(_newTag)
        _videoTagList = _tagManage.getTagList(_videoAbsPath)
        _allTag = _tagManage.getAllTag()
        self.render("editTag.html", action=_action, videoPath=_videoPath, videoTagList=_videoTagList, allTag=_allTag, id=_id)

class SetPlayerHandler(tornado.web.RequestHandler):
    def get(self):
        _action = self.get_argument('action', '')
        _playerPath = self.get_argument('playerPath', '')
        _findPlayer = FindPlayer()
        _playerList = _findPlayer.find()
        if _action == 'selectPlayerPath':
            tk = Tk()
            myFunc.center_window(tk, 945, 595)
            tk.withdraw()
            tk.lift()
            tk.attributes("-topmost", True)
            _path = askopenfilename()
            tk.destroy()
            if _path != '':
                _settingOperate = SettingOperate()
                _settingOperate.setDefaultPlayerPath(_path)
                _tmp, _playerPath = os.path.split(_settingOperate.getPlayerPath())
                self.write(_playerPath)

        elif _action == 'showSetting':
            _json = "{'playerList':" + str(_playerList) + "}"
            self.write(str(_json))

        elif _action == 'setPlayerPath':
            print(_playerPath)
            _settingOperate = SettingOperate()
            _settingOperate.setDefaultPlayerPath(_playerPath)
            _tmp, _playerPath = os.path.split(_settingOperate.getPlayerPath())
            self.write(_playerPath)

class GetSysInfoHandler(tornado.web.RequestHandler):
    def get(self):
        _settingOperate = SettingOperate()
        _tmp, _playerPath = os.path.split(_settingOperate.getPlayerPath())
        _playerPath = _playerPath.rstrip('\n')
        _videoNum = _settingOperate.getVideoNum().rstrip('\n')
        _videoPathList = str(_settingOperate.getVideosPath())
        _videoPathList = _videoPathList.replace('/', r'\\')
        _json = "{'playerPath':'" + _playerPath + "', 'videoPathList':" + _videoPathList + ", 'videoNum':'" + _videoNum + "'}"
        # print('json' + _json)
        self.write(_json)

class OpenDirectoryHandler(tornado.web.RequestHandler):
    def get(self):
        _directory = self.get_argument('directory', '')
        _directory, _fileName = os.path.split(_directory)
        _directory = _directory.replace("/", "\\")
        myFunc.exeCMD('explorer "' + _directory + '"')

class ReLocationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("reLocation.html")

class AddNewVideoHandler(tornado.web.RequestHandler):
    def get(self):
        _action = self.get_argument('action', '')
        _updateMakeTrailerStatus = myFunc.UpdateMakeTrailerStatus()
        if _action == 'newPath':
            tk = Tk()
            myFunc.center_window(tk, 945, 595)
            tk.withdraw()
            tk.lift()
            tk.attributes("-topmost", True)
            _path = askdirectory()
            tk.destroy()
            if _path != '':
                _updateMakeTrailerStatus.clearText()
                startMakeTrailer(_path)
            else:
                self.write('cancel')
        elif _action == 'chkStatus':
            _status = _updateMakeTrailerStatus.getStatus()
            self.write(_status)

class testHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class test2Handler(tornado.web.RequestHandler):
    def get(self):
        _action = self.get_arguments('checknumber[]')
        print('test2.html')
        print(_action)
        self.render("test2.html")


if __name__ == "__main__":
    _v2MP4 = MakeTrailer()
    settingOperate = SettingOperate()
    settingOperate.setDefaultPlayerPath()

    diskList = diskInfo.getDiskList()
    handlers = [[r'/index', IndexHandler],
                [r'/showVideo', ShowVideoHandler],
                [r'/addNewVideo', AddNewVideoHandler],
                [r'/playByPlayer', PlayByPlayerHandler],
                [r'/topSearch', TopSearchHandler],
                [r'/sideMenu', SideMenuHandler],
                [r'/editTag', EditTagHandler],
                [r'/setPlayer', SetPlayerHandler],
                [r'/reLocation', ReLocationHandler],
                [r'/getSysInfo', GetSysInfoHandler],
                [r'/openDirectory', OpenDirectoryHandler],
                [r'/test\.html', testHandler],
                [r'/test2\.html', test2Handler],
                [r'/favicon.ico', tornado.web.StaticFileHandler, {'path': './static/favicon.ico'}]]
    for i in range(len(diskList)):
        addPathToTornado = [r"/path" + str(i) + r"/(.*)", tornado.web.StaticFileHandler, {"path": diskList[i] + ':/'}]
        handlers.append(addPathToTornado)
        print(addPathToTornado)
    handlers = tuple(handlers)

    webApp = tornado.web.Application(
        handlers,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    webApp.listen(8888)
    url = 'http://localhost:8888/index'
    webbrowser.open(url=url, new=0)
    tornado.ioloop.IOLoop.instance().start()
