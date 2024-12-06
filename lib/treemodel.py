from typing import Optional

from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QWidget

from lib.nodetree import Node, TypeNode, ValueNode, data_from_type, is_parent_container, str_from_data

TYPE_COLUMN = 1
VALUE_COLUMN = 2


class TreeModel(QStandardItemModel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # set headers
        self.setHorizontalHeaderLabels(['Key', 'Type', 'Value'])
        self.mostRecent = None

        self.dataChanged.connect(self.on_data_changed)

        self.root = Node('', None, None, None, dict(), True)

    def on_data_changed(self, index_top_left, index_bottom_right, roles):
        if roles is None or Qt.EditRole in roles:
            node = self.itemFromIndex(index_top_left)
            if node.text() not in '' and index_top_left.column() == TYPE_COLUMN:
                print(f'Text updated to: {node.text()}')
                print(f'Type: {type(node)}')
                print(f'Index: {index_top_left}')
                node.update_head()
            elif index_top_left.column() == VALUE_COLUMN:
                print('trying to change value node text')
                if node.update_head_data():
                    print(f'Value changed to: {node.text()}')
                    #print(node.head.nodeData)
                    #print(self.root.nodeData)
                    self.parse_tree()
                    print(self.root.nodeData)
                else:
                    print('Failed to set new data')

    def add_node_full(self, key: str, _type: str, value, parent=None) -> Node:
        setToRoot = False
        if not parent:
            setToRoot = True
            parent = self.invisibleRootItem()

        nodeParent = parent
        if setToRoot:
            nodeParent = self.root

        headNode = Node(key, nodeParent, None, None, data_from_type(_type, value))
        valueNode = ValueNode(str_from_data(value), headNode)
        typeNode = TypeNode(_type, headNode, valueNode)

        headNode.set_type_node(typeNode)

        # these are nodes that have "no" parent
        if setToRoot:
            self.root.add_child(headNode)

            if self.root.childNode is not headNode:
                self.root.add_node(headNode)

        # these nodes have a parent (aka children of the above if)
        if isinstance(parent, Node):
            parent.add_child(headNode)

            if is_parent_container(parent) and parent.childNode is not headNode:
                parent.add_node(headNode)

        row = [headNode, typeNode, valueNode]

        parent.appendRow(row)

        if self.mostRecent is not row[0]:
            self.mostRecent = row[0]

        return headNode

    def parse_tree(self):
        if not self.root.childNode:
            return

        self.root.nodeData = dict()

        print('re-parsing the tree')

        node = self.root.childNode
        while node is not None:
            self.root.nodeData[node.text()] = self.parse_node(node, self.root)
            node = node.nextNode

        self.root.nodeData = dict(reversed(list(self.root.nodeData.items())))

    def parse_node(self, node, parent):
        if node is None:
            return None

        print('node data:', node.nodeData)

        if isinstance(node.nodeData, list) or isinstance(node.nodeData, dict):
            print('is container')
            self.parse_container(node.childNode, node)

        return node.nodeData

    def parse_container(self, node, parent):
        if node is None:
            print('node is none')
            return None

        if isinstance(parent.nodeData, dict):
            parent.nodeData = dict()
        elif isinstance(parent.nodeData, list):
            parent.nodeData = list()

        while node is not None:
            if isinstance(parent.nodeData, dict):
                print('is a dict')
                parent.nodeData[node.text()] = self.parse_node(node, parent)
            elif isinstance(parent.nodeData, list):
                print('is a list')
                parent.nodeData.append(self.parse_node(node, parent))

            node = node.nextNode

        if isinstance(parent.nodeData, dict):
            parent.nodeData = dict(reversed(list(parent.nodeData.items())))
        elif isinstance(parent.nodeData, list):
            parent.nodeData = list(reversed(parent.nodeData))



    def get_most_recent(self) -> Optional[QStandardItem]:
        return self.mostRecent
