from PySide6.QtWidgets import QWidget, QComboBox, QStyledItemDelegate

box_types = ['Dictionary', 'Array', 'Boolean', 'Date', 'Data', 'Integer', 'Real', 'String']

class TypeComboBox(QStyledItemDelegate):
    def __init__(self, original_content=None, parent: QWidget=None):
        super().__init__(parent)
        self.items = box_types
        self.original_content = original_content
        
    def createEditor(self, parent, option, index):
        if index.column() == 1:
            if index in self.original_content:
                box = QComboBox(parent)
                box.addItems(self.items)
                box.setCurrentIndex(self.items.index(self.original_content[index]))
                return box
        return super().createEditor(parent, option, index)
    
    def setEditorData(self, editor, index):
        # item = index.model().itemFromIndex(index)
        # print(f'Item Text: {item.text()}')
        # try:
        #     index = self.items.index(item.text())
        #     editor.setCurrentIndex(index)
        # except ValueError:
        #     print(f'Could not find: {item.text()} in {self.items}')
        return super().setEditorData(editor, index)
            
    def setModelData(self, editor, model, index):
        text = editor.currentText()
        item = model.itemFromIndex(index)
        item.setText(text)
        
    def getType(self):
        return self.currentText()

    def setType(self, _type):
        try:
            index = self.items.index(_type)
            self.setIndex(index)
        except ValueError:
            print(f'Could not find: {_type}')