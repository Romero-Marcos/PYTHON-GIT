import pyodbc

Server = '(LOCAL)\ALFA'
Base = 'MARCOSDB'
Usuario = 'MARCOSDB'
Contraseña = 'MARCOSDB'

try:
    Conexion = pyodbc.connect('DRIVER={SQL Server};SERVER='+Server+
                              ';DATABASE='+Base+
                              ';UID='+Usuario+
                              ';PWD='+Contraseña)
                              
    # OK! conexión exitosa
    print("Conexion exitosa")
except Exception as e:
    # Atrapar error
    
    print("Ocurrió un error al conectar a SQL Server: ", e)