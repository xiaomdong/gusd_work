from ui.gusd_client_ui import Ui_clientWindow
from ui.login_dialog_ui import Ui_login_Dialog

from PySide2 import QtCore, QtGui, QtWidgets



class clientWindows(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(clientWindows, self).__init__()
        self.ui = Ui_clientWindow()
        self.ui.setupUi(self)


class loginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(loginDialog, self).__init__()
        self.ui = Ui_login_Dialog()
        self.ui.setupUi(self)

    def accept(self):
        print("accept")
        user     = self.ui.user.text()
        password = self.ui.password.text()
        if(user != "" and password != "" ):
            self.done(QtWidgets.QDialog.Accepted)


    def reject(self):
        print("reject")
        self.done(QtWidgets.QDialog.Rejected)


def showMain():
    mainWin = clientWindows()
    mainWin.show()

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = loginDialog()
    dialog.setModal(True);
    res = dialog.exec_()
    if( res == QtWidgets.QDialog.Accepted):
        dialog.hide()
        mainWin = clientWindows()
        mainWin.show()
        mainWin.move((QtWidgets.QApplication.desktop().width() - mainWin.width()) / 2, (QtWidgets.QApplication.desktop().height() - mainWin.height()) / 2);
        print(res)
    else:
        print(res)
        exit(1)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()