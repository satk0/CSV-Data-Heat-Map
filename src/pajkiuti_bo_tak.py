import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#import seaborn as sbn
#import pandas as pd
#import matplotlib.pyplot as plt


def button1_clicked():
    fileName = QFileDialog.getOpenFileName(self, 'Open csv', '/home')


def window():
    app=QApplication(sys.argv)
    win=QMainWindow()
    win.setGeometry(200, 200, 400, 300)
    #Pierwsze 2x 200 pozycje pokazania na ekranie monitora.
    #Pozostałe 400 i 300 to rozmiar okna
    win.setWindowTitle("Wizualizacja plików .csv")

    label=QtWidgets.QLabel(win)
    label.setText("Wybierz plik")
    label.move(160,5)

    button1 = QPushButton(win)
    button1.setText("Wybierz plik")
    button1.move(1,50)
    button1.clicked.connect(button1_clicked)

    button2 = QPushButton(win)
    button2.setText("Wyjdź")
    button2.move(1,90)
    button2.clicked.connect(QApplication.instance().quit)
    
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   window()
