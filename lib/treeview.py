from PySide6.QtWidgets import QApplication, QWidget, QTreeView, QMenuBar, QToolBar, QHeaderView, QComboBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import Qt

from lib.combobox import TypeComboBox

class TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doubleIndex = None
        self.clicked.connect(self.on_item_clicked)
        self.doubleClicked.connect(self.on_item_double_click)
        self.originalContent = dict()
        delegate = TypeComboBox(self.originalContent, self)
        self.setItemDelegateForColumn(1, delegate)

    def on_item_clicked(self, index):
        #print(f'SINGLE Row: {index.row()} Column: {index.column()}')
        if self.doubleIndex != None and index.row() == self.doubleIndex.row():
            #print('match')
            #self.printOriginal()
            self.restore(self.doubleIndex)
            self.doubleIndex = None

    def on_item_double_click(self, index):
        if index.isValid() and (index.flags() & Qt.ItemIsEditable):
            #print('editing allowed')
            self.doubleIndex = index
            item = self.model().itemFromIndex(index)
            self.originalContent[index] = item.text()
            item.setText('')
        #print(f'DOUBLE Row: {index.row()} Column: {index.column()}')
        
    def on_selection_changed(self, selected, deselected):
        #print('TreeView.on_selection_changed')
        for index in deselected.indexes():
            if index in self.originalContent:
                self.restore(index)
        self.doubleIndex = None
                
    def setConnect(self):
        #print('TreeView.setConnect')
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def editorEvent(self, event, model, option, index):
        return False        

    def disable_editing(self):
        for row in range(self.model().rowCount()):
            for column in range(self.model().columnCount()):
                index = self.model().index(row, column)
                self.model().itemFromIndex(index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
    def enable_editing(self):
        self.setEditTriggers(QTreeView.DoubleClicked)
        for row in range(self.model().rowCount()):
            for column in range(self.model().columnCount()):
                index = self.model().index(row, column)
                self.model().itemFromIndex(index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                
    def printOriginal(self):
        for index in self.originalContent:
            print(f'Row: {index.row()} Col: {index.column()}')
            
    def restore(self, index):
        if index in self.originalContent:
            item = self.model().itemFromIndex(index)
            if item.text() in self.originalContent[index]:
                item.setText(self.originalContent[index])
                del self.originalContent[index]
