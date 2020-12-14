from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QPalette, QColor, Qt
from PySide2.QtWidgets import QMainWindow, QInputDialog, QWidget, QPushButton, QFormLayout, QLineEdit, QScrollArea
# import Main
import sys
import Sources


class UIApp(object):

    # make a window for search results
    def searchResults(self):
        self.inputWindow = inputDialog()
        animeTitle = self.inputWindow.gettext()
        # if the user entered anything
        if animeTitle is not None:
            # create and format a window that displays the results
            self.searchResults = QMainWindow()
            self.searchResults.resize(1000, 1000)
            self.searchResults.setWindowTitle("Search Results for " + animeTitle)
            label = QtWidgets.QLabel(self.searchResults)
            label.move(50, 50)
            # label.setText(Main.<SEND IN THE ANIME TITLE TO A SEARCH FUNCTION)
            label.setStyleSheet("QLabel {font: 22pt Calibri}")
            label.adjustSize()
            self.searchResults.show()


# make dialog when user clicks button or searches
class inputDialog(QWidget):

    def __init__(self, parent = None):
        super(inputDialog, self).__init__(parent)

        infoList = ['', '', '']

        layout = QFormLayout()

        self.le = QLineEdit()
        layout.addRow(self.btn, self.le)
        self.btn1 = QPushButton("get name")
        self.btn1.clicked.connect(self.gettext)

    def gettext(self, prompt = "Enter The Anime Name: "):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', prompt)

        if ok:
            self.le1.setText(str(text))
            return str(text)
        else:
            return None


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Change palette to allow for dark theme
    app.setStyle('Windows')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(82, 81, 81))  # HEX 525151
    palette.setColor(QPalette.Button, QColor(82, 81, 81))  # HEX 525151
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    Application = QtWidgets.QWidget()
    ui = UIApp()
    ui.setupUi(Application)
    Application.show()
    sys.exit(app.exec_())


# -------------------------------------------------------------------------------------------------------------------- #
main()
