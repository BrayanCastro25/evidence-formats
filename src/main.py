import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTimeEdit, QLineEdit, QTextEdit, QPushButton, QMessageBox
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import sqlite3

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
        self.hour = self.findChild(QTimeEdit, 'time_hour')
        self.client_doc = self.findChild(QLineEdit, 'client_doc')
        self.comment_doc = self.findChild(QTextEdit, 'comment_doc')
        self.button_adjunt = self.findChild(QPushButton, 'button_adjunt')

        self.dialog = QMessageBox(self)

        # connection function when change selection calendar Widget
        self.calendar.selectionChanged.connect(self.change_date)
        self.hour.editingFinished.connect(self.change_time)
        self.button_adjunt.clicked.connect(self.get_data_documentation)

        self.dateSelected = self.dateModified(self.calendar.selectedDate().toString().split(' '))
        self.timeSelected = self.hour.time().toString()


    def dateModified(self, dateActual):
        day = dateActual[2]
        month = month_text[dateActual[1]]
        age = dateActual[3]

        if int(day) < 10:
            day = '0' + day

        dateActual = day + '/' + month + '/' + age

        return dateActual


    def change_date(self):
        self.dateSelected = self.dateModified(self.calendar.selectedDate().toString().split(' '))


    def change_time(self):
        self.timeSelected = self.hour.time().toString()


    def message_dialog(self, message):
        self.dialog.setWindowTitle('Advertencia')
        self.dialog.setText(message)
        self.dialog.exec()


    def get_data_documentation(self):
        text_client_doc = self.client_doc.text()
        text_comment_doc = self.comment_doc.toPlainText()
        
        if text_client_doc != '' and  text_comment_doc != '' and self.timeSelected != '00:00:00':
            try: 
                miConexion = sqlite3.connect('client')
                miCursor = miConexion.cursor()
                miCursor.execute('SELECT * FROM client WHERE id_client={}'.format(text_client_doc))
                Query = miCursor.fetchone()
            except:
                self.message_dialog('Error Conexión Base Datos')
            miConexion.close()
            print(Query)

            if(Query == None):
                self.message_dialog('No existe el cliente')


            print(self.dateSelected, self.timeSelected, text_client_doc, text_comment_doc)
        else:
            self.message_dialog('Información Incompleta')


app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())
