import os
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen, QMessageBox
import gui_main
from config import base_path


# from qt_material import apply_stylesheet


class QWidgetCl(QWidget):
    def __init__(self, parent=None):
        super(QWidgetCl, self).__init__(parent)

    def closeEvent(self, e):
        self.box = QMessageBox(QMessageBox.Warning, "提示信息", "请确认是否关闭软件？")
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(base_path, 'img', 'ict-logo.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.box.setWindowIcon(icon)
        qyes = self.box.addButton(self.tr("是"), QMessageBox.YesRole)
        qno = self.box.addButton(self.tr("否"), QMessageBox.NoRole)
        self.box.exec_()
        if self.box.clickedButton() == qyes:
            e.accept()
            return super(QWidgetCl, self).closeEvent(e)
        else:
            e.ignore()


def password_UI():
    pwapp = QApplication(sys.argv)
    MainWindow = QWidget()
    MainWindow.setWindowTitle("ICT预审表")
    MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                              QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    icon = QIcon()
    icon.addPixmap(QPixmap(os.path.join(base_path, 'img', 'ict-logo.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)
    pw = gui_main.pwdUI(MainWindow)
    MainWindow.resize(500, 60)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
    MainWindow.show()
    return pwapp.exec()


def main_exec(start_wait=True):
    app = QApplication(sys.argv)
    # import ctypes
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    if start_wait:
        splash = QSplashScreen(QPixmap(os.path.join(base_path, 'img', 'start.svg')))  # 启动界面图片地址
        splash.show()  # 展示启动图片
        splash.showMessage("<h1><font color='black'>启动中</font></h1>",
                           QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        app.processEvents()
    # apply_stylesheet(app, theme='light_amber.xml')
    MainWindow = QWidgetCl()
    icon = QIcon()
    icon.addPixmap(QPixmap(os.path.join(base_path, 'img', 'ict-logo.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)
    # MainWindow.setFont(QtGui.QFont("ZYSong18030", 12))  # 全局字体
    # MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowMaximizeButtonHint)
    ui = gui_main.UiForm(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    if start_wait:
        splash.finish(MainWindow)
    return app.exec_()


def while_reset():
    exit_code = main_exec(True)
    while exit_code == 11950:
        exit_code = main_exec(False)
    sys.exit(0)


if __name__ == '__main__':
    if password_UI() == 1:
        while_reset()
    else:
        sys.exit(0)
