from PySide6.QtWidgets import QStyledItemDelegate

class ValueChange(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            pass

        return super().createEditor(parent, option, index)