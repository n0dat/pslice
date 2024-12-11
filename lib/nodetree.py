from datetime import datetime
from PySide6.QtGui import QStandardItem
import re


def data_from_type(dataType: str, value):
    data = None
    if dataType in 'Dictionary':
        data = dict()
    elif dataType in 'Array':
        data = list()
    elif dataType in 'Boolean':
        data = bool(value)
    elif dataType in 'Date':
        data = datetime.fromisoformat(value)
    elif dataType in 'Data':
        data = bytes(value)
    elif dataType in 'Integer':
        data = int(value)
    elif dataType in 'Real':
        data = float(value)
    elif dataType in 'String':
        data = str(value)

    return data

def default_data_from_type(dataType: str):
    data = None

    if dataType in 'Dictionary':
        data = dict()
    elif dataType in 'Array':
        data = list()
    elif dataType in 'Boolean':
        data = bool(False)
    elif dataType in 'Date':
        data = datetime.now()
    elif dataType in 'Data':
        data = bytes(1)
    elif dataType in 'Integer':
        data = int(1)
    elif dataType in 'Real':
        data = float()
    elif dataType in 'String':
        data = str('')

    return data


def str_from_data(data):
    if isinstance(data, str):
        return str(data)
    elif isinstance(data, bool):
        return str(data)
    elif isinstance(data, datetime):
        return data
    elif isinstance(data, bytes):
        return f'{len(bytes(data))} bytes'
    elif isinstance(data, float):
        return str(data)
    elif isinstance(data, int):
        return str(data)
    elif isinstance(data, list) or isinstance(data, dict):
        length = len(data)
        return f'{length} item' if length == 1 else f'{length} items'
    else:
        return 'None'


def type_to_str(data):
    if isinstance(data, dict):
        return 'dict'
    elif isinstance(data, list):
        return 'list'
    elif isinstance(data, bool):
        return 'bool'
    elif isinstance(data, datetime):
        return 'date'
    elif isinstance(data, int):
        return 'int'
    elif isinstance(data, float):
        return 'real'
    elif isinstance(data, str):
        return 'string'

def is_parent_container(parent):
    return isinstance(parent.nodeData, list) or isinstance(parent.nodeData, dict)


class Node(QStandardItem):
    def __init__(self, name, parentNode, childNode, nextNode, data, isRoot=False):
        super().__init__(name)
        self.parentNode = parentNode
        self.childNode = childNode
        self.nextNode = nextNode
        self.nodeData = data
        self.typeNode = None

        self.isContainer = isinstance(self.nodeData, list) or isinstance(self.nodeData, dict)
        self.isItem = not isinstance(self.nodeData, list) and not isinstance(self.nodeData, dict)

        if not isRoot:
            if isinstance(parentNode.nodeData, dict):
                parentNode.nodeData[name] = data
            elif isinstance(parentNode.nodeData, list):
                parentNode.nodeData.append(data)

    def add_child(self, newChild):
        if self.childNode is None:
            print(f'add_child: {newChild.node_to_string()}')
            self.childNode = newChild

    def get_last(self, node):
        if node.nextNode is None:
            return node
        else:
            self.get_last(node.nextNode)

    def add_next(self, nextNode):
        print(f'add_next: {nextNode.node_to_string()}')
        self.nextNode = nextNode

    def add_node(self, node):
        print(f'add_node: {node.node_to_string()}')
        node.add_next(self.childNode)
        self.childNode = node

    def set_type_node(self, node):
        self.typeNode = node

    def update_type(self, newType: str):
        # here we will just generate some default values
        print(f'current type: {type(self.nodeData)}')
        print(f'update_type() New Type: {newType}')

        if isinstance(self.nodeData, dict) or isinstance(self.nodeData, list):
            if self.childNode:
                self.childNode.clear()

        self.nodeData = default_data_from_type(newType)
        if newType in 'Dictionary':
            self.nodeData = dict()
        elif newType in 'Array':
            self.nodeData = list()
        elif newType in 'Boolean':
            self.nodeData = bool(False)
        elif newType in 'Date':
            self.nodeData = datetime.now()
        elif newType in 'Data':
            self.nodeData = bytes(1)
        elif newType in 'Integer':
            self.nodeData = int(1)
        elif newType in 'Real':
            self.nodeData = float(1)
        elif newType in 'String':
            self.nodeData = str('')

        print('new data type set to: ', type(self.nodeData))

    def clear(self):
        print('clear()')
        self.node_to_string()
        self.node_tree_string()

        self.parentNode = None

        if self.childNode is not None:
            self.childNode.clear()
        else:
            print('child is None')
        if self.nextNode is not None:
            self.nextNode.clear()
        else:
            print('next is None')

    def node_to_string(self):
        return f'Name: {self.text()} Value: {self.nodeData} Type: {type(self.nodeData)} Container: {self.isContainer} Item: {self.isItem}'

    def node_tree_string(self):
        return f'parent: {self.parentNode} child: {self.childNode} next: {self.nextNode}'

    def set_data(self, data):
        self.nodeData = data


class TypeNode(QStandardItem):
    def __init__(self, name, head=None, value=None):
        super().__init__(name)
        self.head = head
        self.value = value

    def update_head(self):
        print('update_head()')
        self.head.update_type(self.text())
        self.value.setText(str_from_data(default_data_from_type(self.text())))
        #self.value.setText(str(self.head.nodeData))

    def get_type(self):
        return self.text()


class ValueNode(QStandardItem):
    def __init__(self, name, head=None):
        super().__init__(name)
        self.head = head

    def update_head_data(self) -> bool:
        status = True
        if self.text() in '':
            return False

        text = self.text()

        dataType = self.head.typeNode.get_type()
        validType = False
        typedData = None

        if dataType in 'Boolean':
            print("is bool")
            validType = text == 'True' or text == 'False'
        elif dataType in 'Date':
            print("is date")
            try:
                datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
                validType = True
            except ValueError:
                validType = False
        elif dataType in 'Data':
            print("is data")
            validType = isinstance(text, bytes)
        elif dataType in 'Integer':
            print('is int')
            validType = re.match(r"^-?\d+$", text.strip())
        elif dataType in 'Real':
            print('is float')
            validType = re.match(r"^-?\d*\.\d+$", text.strip())
        elif dataType in 'String':
            print('is string')
            validType = isinstance(text, str)
        elif dataType in 'Dictionary' or dataType in 'List':
            return True

        if validType:
            print('valid type')
            typedData = data_from_type(dataType, text)
            if typedData is not None:
                print('typed data')
                self.head.set_data(typedData)
            else:
                status = False
        else:
            status = False

        return status


def to_dict(root: Node) -> dict:
    tree = dict()

    for key in root.nodeData.keys():
        print(f'Key: {key} Data: {root.nodeData[key]}')

    return tree
