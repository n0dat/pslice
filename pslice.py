import plistlib
import datetime
import faulthandler
from PySide6.QtWidgets import QApplication, QWidget

# customs
import lib.util as util
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
        util.initUi(self)
    
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
