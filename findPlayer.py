# -*- coding: utf-8 -*-
from os.path import exists

class FindPlayer:
    def __init__(self):
        self.defaultPlayer = [['PotPlayer(64-bit)', r'C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe'],
                              ['PotPlayer(32-bit)', r'C:\Program Files (x86)\DAUM\PotPlayer\PotPlayerMini.exe'],
                              ['KMPlayer(32-bit)', 'C:\KMPlayer\KMPlayer.exe'],
                              ['KMPlayer(64-bit)', 'C:\Program Files\KMP64\KMPlayer64.exe'],
                              ['GOM Player', 'C:\Program Files (x86)\GRETECH\GOMPlayer\GOM.exe'],
                              ['Windows Media Player', 'C:\Program Files (x86)\Windows Media Player\wmplayer.exe']]

    def find(self):
        _playerList = []
        for _player in self.defaultPlayer:
            if exists(_player[1]):
            # if 1:
                _playerList.append(_player)
                # print(_player[0] + ': Exist')
            else:
                # _playerList.append(_player)
                # print(_player[0] + ': Not Exist')
                pass

        return _playerList

if __name__ == '__main__':
    findPlayer = FindPlayer()
    findPlayer.find()
