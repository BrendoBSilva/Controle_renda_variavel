import mysql.connector

def connectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='I6x8h5c9@',
        database='controle_renda_variavel'
    )


