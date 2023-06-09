import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTimeEdit, QLineEdit, QTextEdit, QPushButton, QMessageBox
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import sqlite3

list_clients = []

month_text = {'ene.' : '01', 'feb.' : '02', 'mar.' : '03', 
              'abr.' : '04', 'may.' : '05', 'jun.' : '06',
              'jul.' : '07', 'ago.' : '08', 'sep.' : '09',
              'oct.' : '10', 'nov.' : '11', 'dic.' : '12'}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Carga el archivo .ui
        uic.loadUi('mainwindow.ui', self)

        # search elements of Documentation in file .ui
        self.calendar = self.findChild(QCalendarWidget, 'widget_calendar')
        self.hour = self.findChild(QTimeEdit, 'time_hour')
        self.client_doc = self.findChild(QLineEdit, 'client_doc')
        self.employee_doc = self.findChild(QLineEdit, 'employee_doc')
        self.comment_doc = self.findChild(QTextEdit, 'comment_doc')
        self.button_add = self.findChild(QPushButton, 'button_add')
        self.button_create_documents = self.findChild(QPushButton, 'button_create_docs')
        
        # connection function for elements Documentation
        self.calendar.selectionChanged.connect(self.change_date)
        self.hour.editingFinished.connect(self.change_time)
        self.button_add.clicked.connect(self.get_data_documentation)
        self.button_create_documents.clicked.connect(self.create_documentation)

        # search elements of Edit in file .ui
        self.search_edit = self.findChild(QLineEdit, 'text_edit_search')
        self.button_search = self.findChild(QPushButton, 'button_search')
        self.button_create = self.findChild(QPushButton, 'button_create')
        self.button_update = self.findChild(QPushButton, 'button_update')
        self.button_delete = self.findChild(QPushButton, 'button_delete')
        self.client_edit = self.findChild(QLineEdit, 'text_edit_client')
        self.phone_edit = self.findChild(QLineEdit, 'text_edit_phone')
        self.name_edit = self.findChild(QLineEdit, 'text_edit_name')
        self.address_edit = self.findChild(QLineEdit, 'text_edit_address')
        self.city_edit = self.findChild(QLineEdit, 'text_edit_city')

        # connection function for elements Edit
        self.button_search.clicked.connect(self.search_id)
        self.button_create.clicked.connect(self.create_client)
        self.button_update.clicked.connect(self.update_client)
        self.button_delete.clicked.connect(self.delete_client)

        # element to warn the user
        self.dialog = QMessageBox(self)

        # date related items
        self.dateSelected = self.dateModified(self.calendar.selectedDate().toString().split(' '))
        self.timeSelected = self.hour.time().toString()


    # function in charge of modifying the month of numerical type
    def dateModified(self, dateActual):
        day = dateActual[2]
        month = month_text[dateActual[1]]
        age = dateActual[3]

        if int(day) < 10:
            day = '0' + day

        dateActual = day + '/' + month + '/' + age

        return dateActual


    # function in charge of removing the text from the text boxes of the editing tab
    def delete_info_edit(self):
        self.client_edit.setText("")
        self.phone_edit.setText("")
        self.name_edit.setText("")
        self.address_edit.setText("")
        self.city_edit.setText("")


    # function in charge of consulting the client's id in the database
    def consult_db(self, id):
        try: 
            miConexion = sqlite3.connect('./client', timeout = 5)
            miCursor = miConexion.cursor()
            miCursor.execute('SELECT * FROM client WHERE id_client={}'.format(id))
            Query = miCursor.fetchone()
            miConexion.close()
            self.delete_info_edit()
            if(Query == None):
                self.message_dialog('No existe el cliente')
            else:
                self.message_dialog('Cliente Consultado Satisfactorimente')
                return Query
            
        except:
            self.message_dialog('Error Conexión Base Datos')
        

    # function responsible for inserting a customer in the database
    def insert_db(self):        

        text_client = self.client_edit.text()
        text_phone = self.phone_edit.text()
        text_name = self.name_edit.text()
        text_address = self.address_edit.text()
        text_city = self.city_edit.text()

        if text_client != "" and text_phone != "" and text_name != "" and text_address != "" and text_city != "":
            
            try:
                SQL = 'INSERT INTO client (id_client, phone, name, address, city) VALUES ({}, {}, "{}", "{}", "{}")'.format(int(text_client), int(text_phone), text_name, text_address, text_city)
                self.conection_db(SQL)
                self.message_dialog('Cliente Creado Satisfactorimente')
            except:
                self.message_dialog('Error Conexión Base Datos')

        else:
            self.message_dialog('Error Información Incompleta')
            print("Inf")

        
    # function responsible for storing the date when the user modifies it
    def change_date(self):
        self.dateSelected = self.dateModified(self.calendar.selectedDate().toString().split(' '))


    # function responsible for storing the time when the user modifies it
    def change_time(self):
        self.timeSelected = self.hour.time().toString()


    # function responsible for notifying the user of any warnings
    def message_dialog(self, message):
        self.dialog.setWindowTitle('Advertencia')
        self.dialog.setText(message)
        self.dialog.exec()


    # function responsible for storing the data for each of the documents in the list
    def get_data_documentation(self):
        text_client_doc = self.client_doc.text()
        text_employee_doc = self.employee_doc.text()
        text_comment_doc = self.comment_doc.toPlainText()
        
        if text_client_doc != '' and  text_comment_doc != '' and self.timeSelected != '00:00:00':
            Query = self.consult_db(text_client_doc)

            if(Query != None):
                list_clients.append([Query[0], Query[1], Query[2], Query[3], Query[4], self.dateSelected + ' ' + self.timeSelected, text_employee_doc, text_comment_doc])
                print(list_clients)

        else:
            self.message_dialog('Información Incompleta')


    # function responsible for creating all documents that have been registered
    def create_documentation(self):
        for item in list_clients:
            doc = DocxTemplate("plantilla.docx")
            context = { 'fecha' : item[5],
                        'id_cliente' : item[0],
                        'cliente' : item[2],
                        'celular' : item[1],
                        'empleado' : item[6],
                        'direccion' : item[3],
                        'ciudad' : item[4],
                        'comentario' : item[7],
                        'imagen_evidencia': InlineImage(doc, "./capture/" + str(item[0]) + ".png", width = Mm(150))
                        }
            doc.render(context)
            doc.save("./evidence/Evidencia ID " + str(item[0]) + " " + str(self.dateSelected).replace('/', '_') + ".docx")


    # function responsible for obtaining and displaying customer data
    def search_id(self):
        id = self.search_edit.text()
        if id != None:
            Query = self.consult_db(id)
            self.client_edit.setText(str(Query[0]))
            self.phone_edit.setText(str(Query[1]))
            self.name_edit.setText(str(Query[2]))
            self.address_edit.setText(str(Query[3]))
            self.city_edit.setText(str(Query[4]))

    
    # function responsible for creating a customer in the database
    def create_client(self):
        self.insert_db()


    # general function that allows you to create, update and delete a client.
    def conection_db(self, sql):
        miConexion = sqlite3.connect('./client', timeout = 5)
        miCursor = miConexion.cursor()
        miCursor.execute(sql)
        miConexion.commit() 
        miCursor.close()  


    # function that allows you to update a customer's data
    def update_client(self):
        text_client = self.client_edit.text()
        text_phone = self.phone_edit.text()
        text_name = self.name_edit.text()
        text_address = self.address_edit.text()
        text_city = self.city_edit.text()

        try:
            SQL = 'UPDATE client SET phone = {}, name = "{}", address = "{}", city = "{}" WHERE id_client = {};'.format(int(text_phone), text_name, text_address, text_city, int(text_client))
            self.conection_db(SQL) 
            self.message_dialog('Cliente Actualizado Satisfactorimente')
        except:
            self.message_dialog('Error Conexión Base Datos')


    # function to delete a customer record
    def delete_client(self):
        text_client = self.client_edit.text()
        try:
            SQL = 'DELETE FROM client WHERE id_client={}'.format(int(text_client))
            self.conection_db(SQL) 
            self.message_dialog('Cliente Eliminado Satisfactorimente')
        except:
            self.message_dialog('Error Conexión Base Datos')



app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())
