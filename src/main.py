import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QLabel, QTimeEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

month_text = {'ene.' : '01', 'feb.' : '02', 'mar.' : '03', 
              'abr.' : '04', 'may.' : '05', 'jun.' : '06',
              'jul.' : '07', 'ago.' : '08', 'sep.' : '09',
              'oct.' : '10', 'nov.' : '11', 'dic.' : '12'}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Carga el archivo .ui
        uic.loadUi('mainwindow.ui', self)

        # search elements in file .ui
        self.calendar = self.findChild(QCalendarWidget, 'widget_calendar')
        self.dateText = self.findChild(QLabel, 'label_text_date')

        self.calendar.selectionChanged.connect(self.change_date)

    def change_date(self):

        dateSelected = self.calendar.selectedDate().toString().split(' ')

        day = dateSelected[2]
        month = month_text[dateSelected[1]]
        age = dateSelected[3]

        if int(day) < 10:
            day = '0' + day

        date_actual = day + '/' + month + '/' + age
       
        self.dateText.setText(date_actual)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())
