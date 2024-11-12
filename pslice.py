import plistlib
import datetime
import faulthandler

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QMenuBar, QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QSizePolicy

# customs
from lib.generate import Parser

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
    
    plist = plistlib.loads(plistlib.dumps(pl).decode())
    
    return plist
    
class PSlice(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.treeView = None
        self.initUi()
        

    def initUi(self):
        self.setWindowTitle("PSlice")

        # create the tree view
        self.treeView = QTreeView(self)

        # set layout
        layout:QVBoxLayout = QVBoxLayout(self)
        
        self.toolbar = QToolBar("Main Toolbar")
        
        # Add actions to the toolbar
        action1 = QAction(QIcon(), "Test 1", self)
        action2 = QAction(QIcon(), "Test 2", self)
        action3 = QAction(QIcon(), "Test 3", self)

        # Connect actions to methods
        action1.triggered.connect(self.on_action1_triggered)
        action2.triggered.connect(self.on_action2_triggered)
        action3.triggered.connect(self.on_action3_triggered)
        
        # Add actions to the toolbar
        self.toolbar.addAction(action1)
        self.toolbar.addAction(action2)
        self.toolbar.addAction(action3) 
        
        # create the menu bar
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        file_menu.addAction(open_action)
        save_action = QAction("Save", self)
        file_menu.addAction(save_action)
        
        # add widgets to vbox layout
        layout.addWidget(self.menu_bar)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.treeView)
            
        # resize the window based on the tree view size
        self.treeView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(self.treeView.sizeHint())
        # adjust the size of the window to fit the content
        self.adjustSize()
        
        menubar = QMenuBar(self)
        filemenu = menubar.addMenu('File')
        openaction = QAction('Open', self)
        filemenu.addAction(openaction)
        saveaction = QAction('Save', self)
        filemenu.addAction(saveaction)
        layout.setMenuBar(menubar)

        self.setLayout(layout)
        
    def on_action1_triggered(self):
        print("Test 1 ToolBar triggered")

    def on_action2_triggered(self):
        print("Test 2 ToolBar triggered")

    def on_action3_triggered(self):
        print("Test 3 ToolBar triggered")
    
if __name__ == '__main__':
    try:
        app: QApplication = QApplication([])
        window: PSlice = PSlice()
        
        parser = Parser(window)
        window.treeView.setModel(parser.parsePlist(testData()))
        
        window.show()
        app.exec()
        
    except Exception as e:
        print(f"Exception: {e}")
    except:
        print("Unknown exception occurred")
