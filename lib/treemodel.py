from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget
from typing import Optional

# custom types
type StandardItemList = list[QStandardItem]

class TreeModel(QStandardItemModel):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        # headers
        self.setHorizontalHeaderLabels(['Key', 'Type', 'Value'])
        self.most_recent = None

    def addNode(self, key: str, _type: str, value: str, parent: QWidget=None):
        if not parent:
            parent = self.invisibleRootItem()

        row: StandardItemList = [
            QStandardItem(key),
            QStandardItem(_type),
            QStandardItem(value)
        ]

        parent.appendRow(row)
        if self.most_recent != row[0]:
            self.most_recent = row[0]
        
    def getMostRecent(self) -> Optional[QStandardItem]:
        return self.most_recent