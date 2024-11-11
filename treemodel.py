from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget

# custom types
type StandardItemList = list[QStandardItem]

class TreeModel(QStandardItemModel):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        # headers
        self.setHorizontalHeaderLabels(['Key', 'Type', 'Value'])

    def addNode(self, key: str, _type: str, value: str, parent: QWidget=None):
        if not parent:
            parent = self.invisibleRootItem()

        row: StandardItemList = [
            QStandardItem(key),
            QStandardItem(_type),
            QStandardItem(value)
        ]

        parent.appendRow(row)
        
    def addNodeRow(self, row: list[QStandardItem], parent: QWidget=None):
        if not parent:
            parent = self.invisibleRootItem()
            
        parent.appendRow(row)