import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTimeEdit
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
        self.hour = self.findChild(QTimeEdit, 'timeEdit')

        # connection function when change selection calendar Widget
        self.calendar.selectionChanged.connect(self.change_date)
        self.hour.editingFinished.connect(self.change_time)

        self.dateSelected = self.calendar.selectedDate().toString().split(' ')
        self.timeSelected = self.hour.time().toString()


    def change_date(self):

        self.dateSelected = self.calendar.selectedDate().toString().split(' ')

        day = self.dateSelected[2]
        month = month_text[self.dateSelected[1]]
        age = self.dateSelected[3]

        if int(day) < 10:
            day = '0' + day

        self.dateSelected = day + '/' + month + '/' + age
        print(self.dateSelected, self.timeSelected)


    def change_time(self):

        self.timeSelected = self.hour.time().toString()
        print(self.dateSelected, self.timeSelected)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())
