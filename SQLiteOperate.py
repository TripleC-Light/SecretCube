# -*- coding: utf-8 -*-
import sqlite3

"""
setTable
    Type: INTEGER, FLOAT, REAL, NUMERIC, BOOLEAN, TIME, DATE, TIMESTAMP, VARCHAR, NVARCHAR, TEXT, BLOB
    Option: PRIMARY KEY, AUTOINCREMENT, NOT NULL, UNIQUE
"""

class SQLiteOperate:

    def __init__(self):
        self.conn = ''

    def connectOrCreatDB(self, _name):
        self.conn = sqlite3.connect(_name + '.sqlite')

    def newTable(self, _name, _setTable):
        _SQL = ''
        for _setTableValue in _setTable:
            if _setTableValue['Default']:
                _setTableValue['Default'] = 'DEFAULT ' + _setTableValue['Default']
            _SQL += _setTableValue['name'] + ' ' + _setTableValue['Type'] + ' ' + _setTableValue['Default'] + ' ' + _setTableValue['Option']
            _SQL += ','
        _SQL = _SQL.rstrip(',')
        self.conn.execute('''CREATE TABLE ''' + _name + '''(''' + _SQL + ''');''')

    def addData(self, _tableName, _fields='', _value=''):
        if _fields:
            _SQL = "INSERT INTO " + _tableName + " (" + _fields + ") VALUES (" + _value + ")"
        else:
            _SQL = "INSERT INTO " + _tableName + " VALUES (" + _value + ")"
        # print('addData SQL = ' + _SQL)
        self.conn.execute(_SQL)
        self.conn.commit()

    def getData(self, _tableName, _fields, _allocate=''):
        # print('_allocate= ' + _allocate)
        _SQL = "SELECT " + _fields + " from " + _tableName
        if _allocate:
            if _allocate.find('LIKE') < 0 and _allocate.find('ORDER BY') >= 0:
                _SQL += _allocate
            else:
                _SQL += " where " + _allocate
        # print('getData= ' + _SQL)
        return self.conn.execute(_SQL)

    def updateData(self, _tableName, _updateValue, _allocate=''):
        _SQL = "UPDATE " + _tableName + " set " + _updateValue
        if _allocate:
            _SQL += " where " + _allocate
        # print(_SQL)
        self.conn.execute(_SQL)
        self.conn.commit()

    def deleteData(self, _tableName, _allocate):
        _SQL = "DELETE from " + _tableName + " where " + _allocate
        self.conn.execute(_SQL)
        self.conn.commit()

    def getFieldName(self, _tableName):
        _SQL = "PRAGMA table_info(" + _tableName + ")"
        _cursor = self.conn.execute(_SQL)
        # _fields = []
        _fields = ''
        for _row in _cursor:
            # _fields.append(_row[1])
            _fields += _row[1] + ','
        _fields = _fields.rstrip(',')
        return _fields

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    SQ3 = SQLiteOperate()
    SQ3.connectOrCreatDB('.\static\\temp\\videoDB')
    setTable = [{'name': 'ID', 'Type': 'INTEGER', 'Default': '', 'Option': 'PRIMARY KEY AUTOINCREMENT'},
                {'name': 'VideoPath', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                {'name': 'VideoName', 'Type': 'TEXT', 'Default': '', 'Option': 'NOT NULL'},
                {'name': 'Score', 'Type': 'INTEGER', 'Default': '0', 'Option': 'NOT NULL'},
                {'name': 'Views', 'Type': 'INTEGER', 'Default': '0', 'Option': 'NOT NULL'}]

    # SQ3.newTable('firstTry7', setTable)
    # SQ3.addData('firstTry7', 'VideoPath, VideoName, Score, Views', _str)
    # SQ3.addData('firstTry7', _value='4, "C:/", "testVideo.mp4", 95, 10')
    # cursor = SQ3.getData('firstTry7', 'ID, VideoPath, VideoName, Score, Views')
    # SQ3.updateData('firstTry7', 'VideoPath="F:/", Score=50', 'ID=2')
    # cursor = SQ3.getData('firstTry7', 'ID, VideoPath, VideoName, Score, Views', 'ID=2')
    cursor = SQ3.getData('videoList', '*', 'dbVideoName LIKE "%AOA%"')
    # cursor = SQ3.getFieldName('videoList')
    print(cursor)
    for row in cursor:
        print("ID = ", row[0])
        print("VideoPath = ", row[1])
        print("VideoName = ", row[2])
        print("Score = ", row[3])
        print("Views = ", row[4])

    # SQ3.deleteData('firstTry7', 'ID=2')

    SQ3.close()
