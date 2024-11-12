from lib.treemodel import TreeModel
import datetime
import sys
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QStandardItem

class Parser:
    def __init__(self, parent: QWidget=None):
        self.treeModel = TreeModel(parent)

    def parseString(self, key, value, parent):
        self.treeModel.addNode(key, "String", value, parent)

    def parseInt(self, key, value, parent):
        self.treeModel.addNode(key, "Integer", str(value), parent)

    def parseReal(self, key, value, parent):
        self.treeModel.addNode(key, "Real", str(value), parent)

    def parseBool(self, key, value, parent):
        self.treeModel.addNode(key, "Boolean", str(value), parent)

    def parseDate(self, key, value, parent):
        self.treeModel.addNode(key, "Date", value, parent)

    def parseData(self, key, value, parent):
        self.treeModel.addNode(key, "Data", f'{len(bytes(value))} bytes', parent)

    def parseArray(self, value, parent):
        for i in range(len(value)):
            self.parse(f'Item{i + 1}', value[i], parent)

    def parseDict(self, value, parent):
        for key in value:
            self.parse(key, value[key], parent)

    def parse(self, key, value, parent):
        if isinstance(value, str):
            self.parseString(key, value, parent)
            
        elif isinstance(value, bool):
            self.parseBool(key, value, parent)
            
        elif isinstance(value, int):
            self.parseInt(key, value, parent)
            
        elif isinstance(value, float):
            self.parseReal(key, value, parent)
            
        elif isinstance(value, datetime.datetime):
            self.parseDate(key, str(value), parent)
            
        elif isinstance(value, bytes):
            self.parseData(key, value, parent)
            
        elif isinstance(value, list):
            root = parent
            if parent is None:
                root = self.treeModel.invisibleRootItem()

            self.treeModel.addNode(key, "Array", str(len(value)), parent)
            temp = self.treeModel.getMostRecent()
            self.parseArray(value, temp)
            
        elif isinstance(value, dict):
            root = parent
            if parent is None:
                root = self.treeModel.invisibleRootItem()

            self.treeModel.addNode(key, "Dictionary", str(len(value)), parent)
            temp = self.treeModel.getMostRecent()
            self.parseDict(value, temp)
            
        else:
            print('Unknown Type:', type(value))
            

    def parsePlist(self, plist: dict) -> TreeModel:        
        for key in plist.keys():
            self.parse(key, plist[key], None)

        return self.treeModel
    