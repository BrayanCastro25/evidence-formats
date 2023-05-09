# Evidence Formats
## Descripción

Este proyecto consiste en agilizar el proceso de la creación de los archivos que sirven como evidencia para las llamadas que se gestionan en una empresa. Los lenguajes que se utilizan en este proyecto son Python y su herramienta PyQt5 para facilitar la interacción del usuario junto con el gestor de base de datos SQLite.



## Instalación

### Instalación PyQt5 (Ubuntu)

``sudo apt install python3-pyqt5``

### Instalación Qt Designer (Ubuntu)

``sudo apt-get install qttools5-dev-tools``



## Creación de interfaz

Con la herramienta Qt Designer se diseña la siguiente interfaz gráfica (HMI):

![](./img/interfaz.png)

![](./img/interfaz2.png)

## Creación base de datos (SQLite)

Para la empresa es indispensable la siguiente información: identificador del cliente, nombre, celular, dirección y la ciudad en la que reside, para almacenar esta información es necesario usar SQLite, se crea la tabla como se ve en la siguiente imagen:

![Base de datos clientes](./img/table_database.png)

