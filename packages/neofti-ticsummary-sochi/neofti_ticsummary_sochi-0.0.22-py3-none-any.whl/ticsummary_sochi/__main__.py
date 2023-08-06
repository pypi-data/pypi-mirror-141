from ticsummary_sochi.ui.mainWindow import *
from ticsummary_sochi.readerCSV import *
from ticsummary_sochi.handlerData import *
from ticsummary_sochi.model import *

def startup():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    sys.exit(app.exec())

if __name__ == "__main__":
    startup()