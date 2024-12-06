import os
import plistlib
import datetime
import faulthandler

from PySide6.QtWidgets import QApplication, QWidget, QMenuBar, QToolBar, QHeaderView, \
    QFileDialog, QDialog
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QFileInfo

from lib import nodetree
# customs
from lib.generate import Parser
from lib.treemodel import TreeModel
from lib.treeview import TreeView

faulthandler.enable()


def testData() -> dict:
    pl = dict(
        aString="Doodah",
        aList=['A', 'B', 12, 32.1, [1, 2, 3]],
        aFloat=0.1,
        anInt=728,
        aDict=dict(
            anotherString="<hello & hi there!>",
            aThirdString="M\xe4ssig, Ma\xdf",
            aTrueValue=True,
            aFalseValue=False,
        ),
        someData=b"<binary gunk>",
        someMoreData=b"<lots of binary gunk>" * 10,
        aData=datetime.datetime.now()
    )

    plist = plistlib.loads(plistlib.dumps(pl))

    return plist


class PSlice(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.treeView: TreeView = None
        self.allowEdit: bool = False
        self.fileLoaded: bool = False
        self.currentFile: QFileInfo = None
        self.parser: Parser = Parser(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PSlice")

        # create the tree view
        self.treeView = TreeView(self)
        self.treeView.setModel(None)

        # set layout
        layout: QVBoxLayout = QVBoxLayout(self)

        self.toolBar = QToolBar("Main Toolbar")

        # Add actions to the toolbar
        expandAction = QAction(QIcon(), "Expand", self)
        collapseAction = QAction(QIcon(), "Collapse", self)
        editAction = QAction(QIcon(), "Edit", self)

        # Connect actions to methods
        expandAction.triggered.connect(self.on_expand_triggered)
        collapseAction.triggered.connect(self.on_collapse_triggered)
        editAction.triggered.connect(self.on_edit_triggered)

        # Add actions to the toolbar
        self.toolBar.addAction(expandAction)
        self.toolBar.addAction(collapseAction)
        self.toolBar.addAction(editAction)

        # create the menu bar
        menuBar = QMenuBar(self)
        fileMenu = menuBar.addMenu("File")
        openAction = QAction("Open", self)
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open_file_dialog)
        saveAction = QAction("Save", self)
        fileMenu.addAction(saveAction)
        layout.setMenuBar(menuBar)

        # add widgets to vbox layout
        # layout.addWidget(self.menu_bar)
        layout.addWidget(self.toolBar)
        layout.addWidget(self.treeView)

        # resize the window based on the tree view size
        self.treeView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(self.treeView.sizeHint())
        # adjust the size of the window to fit the content
        self.adjustSize()

        # disable editing by default
        self.treeView.setEditTriggers(QTreeView.NoEditTriggers)

        self.setLayout(layout)

    def on_expand_triggered(self):
        if self.treeView.model() is None:
            return

        print("Expand ToolBar triggered")
        self.treeView.expandAll()

    def on_collapse_triggered(self):
        if self.treeView.model() is None:
            return

        print("Collapse ToolBar triggered")
        self.treeView.collapseAll()

    def on_edit_triggered(self):
        if self.treeView.model() is None:
            return

        print(self.treeView.model().root.nodeData)

        print("Edit ToolBar triggered")
        if self.allowEdit:
            self.treeView.disable_editing()
            self.allowEdit = False
        else:
            self.treeView.enable_editing()
            self.allowEdit = True

    def set_model(self, model):
        # clear the current model
        self.treeView.setModel(None)
        self.parser = Parser()

        # set new model
        self.treeView.setModel(model)
        print(nodetree.to_dict(self.treeView.model().root))
        self.treeView.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.treeView.setEditTriggers(QTreeView.NoEditTriggers)

        model.type_change_signal.connect(self.on_type_changed)

        # setup connections
        self.treeView.set_connections()

        # disable editing by default
        self.treeView.disable_editing()

    def on_type_changed(self):
        print('type changed !!!!!')
        model: TreeModel = self.parser.parsePlist(self.treeView.model().root.nodeData)
        self.set_model(model)

    def open_file_dialog(self):
        fileDialog: QFileDialog = QFileDialog(self)
        fileDialog.setDirectory(os.getcwd())
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setNameFilter("Property List Files (*.plist)")

        if fileDialog.exec() == QDialog.DialogCode.Accepted:
            selectedFile: QFileInfo = QFileInfo(fileDialog.selectedFiles()[0])
            print(f'Selected: {selectedFile.fileName()}')
            self.parse_plist(selectedFile)
        else:
            print("File dialog was closed or cancelled.")

    def parse_plist(self, file: QFileInfo):
        plistData: dict = None
        try:
            with open(file.absoluteFilePath(), 'rb') as f:
                plistData = plistlib.load(f)
        except Exception as e:
            print('Error reading plist file:', e)

        if plistData is not None:
            model: TreeModel = self.parser.parsePlist(plistData)
            self.set_model(model)

if __name__ == '__main__':
    try:
        app: QApplication = QApplication([])
        window: PSlice = PSlice()

        # parser = Parser(window)
        # window.set_model(parser.parsePlist(testData()))

        window.show()
        app.exec()

    except Exception as e:
        print(f"Exception: {e}")
    except:
        print("Unknown exception occurred")
