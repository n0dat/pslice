from lib.treemodel import TreeModel
import datetime
import sys
from PySide6.QtWidgets import QWidget


class Parser:
    def __init__(self, parent: QWidget = None):
        self.treeModel = TreeModel(parent)

    def parse_string(self, key, value, parent):
        self.treeModel.add_node_full(key, 'String', value, parent)

    def parse_int(self, key, value, parent):
        self.treeModel.add_node_full(key, 'Integer', value, parent)

    def parse_real(self, key, value, parent):
        self.treeModel.add_node_full(key, 'Real', value, parent)

    def parse_bool(self, key, value, parent):
        self.treeModel.add_node_full(key, 'Boolean', value, parent)

    def parse_date(self, key, value, parent):
        self.treeModel.add_node_full(key, 'Date', value, parent)

    def parse_data(self, key, value, parent):
        self.treeModel.add_node_full(key, 'Data', value, parent)

    def parse_array(self, value, parent):
        for i in range(len(value)):
            self.parse(f'Item{i + 1}', value[i], parent)

    def parse_dict(self, value, parent):
        for key in value:
            self.parse(key, value[key], parent)

    def parse(self, key, value, parent):
        if isinstance(value, str):
            self.parse_string(key, value, parent)

        elif isinstance(value, bool):
            self.parse_bool(key, value, parent)

        elif isinstance(value, int):
            self.parse_int(key, value, parent)

        elif isinstance(value, float):
            self.parse_real(key, value, parent)

        elif isinstance(value, datetime.datetime):
            self.parse_date(key, str(value), parent)

        elif isinstance(value, bytes):
            self.parse_data(key, value, parent)

        elif isinstance(value, list):
            root = parent
            if parent is None:
                root = self.treeModel.invisibleRootItem()

            self.treeModel.add_node_full(key, 'Array', value, parent)
            temp = self.treeModel.get_most_recent()
            self.parse_array(value, temp)

        elif isinstance(value, dict):
            root = parent
            if parent is None:
                root = self.treeModel.invisibleRootItem()

            self.treeModel.add_node_full(key, 'Dictionary', value, parent)
            temp = self.treeModel.get_most_recent()
            self.parse_dict(value, temp)

        else:
            print('Unknown Type:', type(value))

    def parsePlist(self, plist: dict) -> TreeModel:
        for key in plist.keys():
            self.parse(key, plist[key], None)

        return self.treeModel
