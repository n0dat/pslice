from typing import Optional, Any

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget


class TreeModel(QStandardItemModel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # set headers
        self.setHorizontalHeaderLabels(['Key', 'Type', 'Value'])
        self.mostRecent = None

    def add_node(self, key: str, _type: str, value: str, parent = None):
        if not parent:
            parent = self.invisibleRootItem()

        row: list[QStandardItem] = [
            QStandardItem(key),
            QStandardItem(_type),
            QStandardItem(value)
        ]

        parent.appendRow(row)
        if self.mostRecent != row[0]:
            self.mostRecent = row[0]

    def get_most_recent(self) -> Optional[QStandardItem]:
        return self.mostRecent
