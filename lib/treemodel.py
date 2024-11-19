from typing import Optional

from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide6.QtWidgets import QWidget

from lib.nodetree import Node, TypeNode, data_from_type, is_parent_container

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
            item = self.itemFromIndex(index_top_left)
            if item.text() not in '' and index_top_left.column() == 1:
                print(f'Text updated to: {item.text()}')
                print(f'Type: {type(item)}')
                print(f'Index: {index_top_left}')
                item.update_head()

    def add_node(self, key: str, _type: str, value: str, parent=None):
        # if not parent:
        #     parent = self.invisibleRootItem()
        #
        # row: list[QStandardItem] = [
        #     QStandardItem(key),
        #     QStandardItem(_type),
        #     QStandardItem(value)
        # ]
        #
        # parent.appendRow(row)
        # if self.mostRecent != row[0]:
        #     self.mostRecent = row[0]
        pass

    def add_node_full(self, key:str, _type: str, value, parent=None) -> Node:
        setToRoot = False
        if not parent:
            setToRoot = True
            parent = self.invisibleRootItem()

        nodeParent = parent
        if setToRoot:
            nodeParent = self.root

        headNode = Node(key, nodeParent, None, None, data_from_type(_type, value))
        valueNode = QStandardItem(str(value))
        typeNode = TypeNode(_type, headNode, valueNode)

        if setToRoot:
            self.root.add_child(headNode)

            if self.root.childNode is not headNode:
                self.root.add_node(headNode)

        if isinstance(parent, Node):
            parent.add_child(headNode)

            if is_parent_container(parent) and parent.childNode is not headNode:
                parent.add_node(headNode)

        row = [headNode, typeNode, valueNode]

        parent.appendRow(row)

        if self.mostRecent is not row[0]:
            self.mostRecent = row[0]

        return headNode

    def get_most_recent(self) -> Optional[QStandardItem]:
        return self.mostRecent
