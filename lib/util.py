import pslice

from PySide6.QtWidgets import QVBoxLayout, QTreeView, QMenuBar
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QSizePolicy

def initUi(pslice: pslice.PSlice):
    pslice.setWindowTitle("PSlice")

    # create the tree view
    pslice.treeView = QTreeView(pslice)

    # set layout
    layout:QVBoxLayout = QVBoxLayout(pslice)
    
    # create the menu bar
    menu_bar = QMenuBar(pslice)

    # add a 'File' menu to the menu bar
    file_menu = menu_bar.addMenu("File")

    # add actions to the 'File' menu
    open_action = QAction("Open", pslice)
    file_menu.addAction(open_action)

    save_action = QAction("Save", pslice)
    file_menu.addAction(save_action)

    # add the menu bar to the layout without setting it as the menu bar of the layout
    layout.addWidget(menu_bar)
    layout.addWidget(pslice.treeView)

    # set the layout for the main widget
    pslice.setLayout(layout)
        
    # resize the window based on the tree view size
    pslice.treeView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    pslice.setMinimumSize(pslice.treeView.sizeHint())
      # adjust the size of the window to fit the content
    pslice.adjustSize()
    
    menubar = QMenuBar(pslice)
    filemenu = menubar.addMenu('File')
    openaction = QAction('Open', pslice)
    filemenu.addAction(openaction)
    saveaction = QAction('Save', pslice)
    filemenu.addAction(saveaction)
    layout.setMenuBar(menubar)
    pslice.setLayout(layout)