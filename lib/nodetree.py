from datetime import datetime

from PySide6.QtGui import QStandardItem


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
    def __init__(self, name, parent, child, nextNode, data):
        super().__init__(name)
        self.parentNode = parent
        self.childNode = child
        self.nextNode = nextNode
        self.nodeData = data

        self.isContainer = isinstance(self.nodeData, list) or isinstance(self.nodeData, dict)
        self.isItem = not isinstance(self.nodeData, list) and not isinstance(self.nodeData, dict)

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
        #if self.childNode is not node:
        node.add_next(self.childNode)
        self.childNode = node
        # last = self.get_last(self.childNode)
        # last.add_next(node)

    def update_type(self, newType: str):
        print(f'current type: {type(self.nodeData)}')
        print(f'update_type() New Type: {newType}')

        if isinstance(self.nodeData, dict) or isinstance(self.nodeData, list):
            self.childNode.clear()

        if newType in 'Dictionary':
            self.nodeData = dict()
        elif newType in 'Array':
            self.nodeData = list()
        elif newType in 'Boolean':
            self.nodeData = bool(False)
        elif newType in 'Date':
            self.nodeData = datetime.min
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

    def node_to_string(self):
        return f'Name: {self.text()} Value: {self.nodeData} Type: {type(self.nodeData)} Container: {self.isContainer} Item: {self.isItem}'

    def node_tree_string(self):
        return f'parent: {self.parentNode} child: {self.childNode} next: {self.nextNode}'


class TypeNode(QStandardItem):
    def __init__(self, name, head=None, value=None):
        super().__init__(name)
        self.head = head
        self.value = value

    def update_head(self):
        print('update_head()')
        self.head.update_type(self.text())
        self.value.setText(str(self.head.nodeData))
