from sys import path
from threading import get_ident

from werkzeug.utils import secure_filename
import os
from bd import *
from flask import Flask, render_template, request, redirect, url_for, flash
from random import gammavariate, randrange
from Perfil import Inicializa

# iniciando
app = Flask(__name__)

#Secion
app.secret_key = 'mysecretkey'
@app.route('/')
def index():
    global GUsuario
    global GApellido
    GApellido = ""
    GUsuario = ""

    Cursor = Conexion.cursor()
    Cursor.execute('Select * from Contactos')
    Date = Cursor.fetchall()
    return render_template('login.html')

@app.route('/',  methods= ["POST"]) 
def login():
    try:
        with Conexion.cursor() as cursor:
            
            Usuario = request.form['Usuario']
            Contraseña = request.form['Contraseña']
            global GUsuario
            GUsuario = Usuario
            if Usuario != '' and Contraseña != '':
                Consulta = "Select top 1 id, Usuario, Contraseña, Apellido from Clientes where Usuario = '" + Usuario + "' and Contraseña = '" + Contraseña + "'"
                cursor.execute(Consulta)
                Datos = cursor.fetchall()
                for Dato in Datos:
                    DatoUsuario = str(Dato.Usuario)
                    DatoContraseña = str(Dato.Contraseña)
                    global GApellido
                    global GId
                    GId = str(Dato.id)
                    GApellido = str(Dato.Apellido)

                if Usuario.strip() == DatoUsuario.strip() and Contraseña.strip() == DatoContraseña.strip():
                    #flash('Inicio sesión exitosa, ¡Bienvenido!')
                    return render_template('menu.html' , GUsuario = GUsuario , GApellido = GApellido)
                else:   
                    print('Inicio sesión fallida, la contraseña o el usuario no son validos')
                    flash('Inicio sesión fallida, la contraseña o el usuario no son validos')
                    return(redirect(url_for('index')))
            else:
                flash("Por favor intente iniciar sesión de nuevo")
                return(redirect(url_for('login')))

    except Exception as e:
        flash("Ocurrió un error al Inicio sesión: ")
        print("Ocurrió un error al Inicio sesión: ", e)
        return(redirect(url_for('index')))

#Menu-----------------------------------------------------------------------------------------------------------------
@app.route('/menu',  methods= ["POST"]) 
def menu():
    global GUsuario
    global GApellido
    if GUsuario != "":
        
        fields = [k for k in request.form]                                      
        values = [request.form[k] for k in request.form]
        modulo = dict(zip(fields, values))

        if modulo == {'AgregarContacto': 'AgregarContacto'}:
            return redirect('/agenda')
        elif modulo == {'AgregarCliente': 'AgregarCliente'}:
            return redirect('/cliente')
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))

@app.route('/menusistema')
def menusistema():
    global GUsuario
    global GApellido
    if GUsuario != '':
        return render_template('menu.html'  , GUsuario = GUsuario, GApellido = GApellido )
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))
#Cliente --------------------------------------------------------------------------- 
@app.route('/cliente',  methods= ["GET"]) 
def cliente():
    global GUsuario
    if GUsuario != "":
        Consulta = "Select id, Nombre, Apellido, Email,NumeroDocumento from Cliente"
        Cursor = Conexion.cursor()
        Cursor.execute(Consulta)
        Date = Cursor.fetchall()
        Cursor.execute('Select * from TipoDocumentos')
        Date1 = Cursor.fetchall()

        return render_template('AgregarCliente.html' , contactos = Date , TipoDocumentos = Date1)

@app.route('/clientebuscar',  methods= ["POST"]) 
def clientebuscar():
    global GUsuario
    if GUsuario != "":
        
        Buscar = request.form['Buscar']
        if Buscar != "":
            Consulta = "Select id, Nombre, Apellido, Email,NumeroDocumento from Cliente where Nombre = '" + Buscar + "'"
        else:
            Consulta = "Select id, Nombre, Apellido, Email,NumeroDocumento from Cliente"
        Cursor = Conexion.cursor()
        Cursor.execute(Consulta)
        Date = Cursor.fetchall()
        Cursor.execute('Select * from TipoDocumentos')
        Date1 = Cursor.fetchall()

        return render_template('AgregarCliente.html' , contactos = Date , TipoDocumentos = Date1)


@app.route('/agregarcliente', methods=['POST'])
def agregarcliente():
    try:
        with Conexion.cursor() as cursor:
            #if request.method  == 'POST':
                Nombre = request.form['Nombre']
                Apellido = request.form['Apellido']
                Email = request.form['Email']
                TipoDocumento = request.form['TipoDocumento']
                Documento = request.form['Documento']

                #Validar() 
                Codigo = str(randrange(10000, 11000, 2))
                Cursor = Conexion.cursor()
                #if Validar == True:
                #cv2.imwrite('/static/Imagenes/{{ Imagen }}', Imagen)
                Consulta = "insert into Cliente (NumeroCliente, Nombre, Apellido, Email, idTipoDocumento, NumeroDocumento) Values ('" + Codigo + "', '" + Nombre + "',  '" + Apellido + "', '" + Email + "' , '" + TipoDocumento + "' , '" + Documento + "')"
                print(Consulta)
                cursor.execute(Consulta)  
                flash('Cliente Agregado')
                return(redirect(url_for('cliente')))
                    
                #else:
                #    return(redirect(url_for('cliente')))
    except Exception as e:
        print("Ocurrió un error al grabar el cliente : ", e)
        return("Ocurrió un error al grabar el cliente : ", e)

@app.route('/eliminarcliente/<string:id>')
def eliminarcliente(id):
    try:
        with Conexion.cursor() as cursor:
            #cursor = Conexion.cursor()
            Consulta = "delete from Clientes where id = " + id + ""
            cursor.execute(Consulta)
            print(Consulta)
            flash('Contacto Eliminado')
            return(redirect(url_for('cliente')))
            #return('Eliminar Cliente')
    except Exception as e:
        print("Ocurrió un error al eliminarr el cliente : ", e)
        return("Ocurrió un error al eliminar el cliente : ", e)

@app.route('/editarcliente/<string:id>')
def editarcliente(id):
    global GUsuario
    if GUsuario != '':
        try:
            with Conexion.cursor() as cursor:
                cursor.execute("Select * from clientes where id = '" + id + "'")
                dato = cursor.fetchall()
                return( render_template('EditCliente.html', Contacto = dato[0]))
                
        except Exception as e:
            print("Ocurrió un error al editar el cliente : ", e)
            return("Ocurrió un error al editar el cliente : ", e)
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))

@app.route('/editarC/<id>',  methods= ["POST"]) 
def editarC(id):
    #if request.method == 'POST':
        try:
            with Conexion.cursor() as cursor:
                #if request.method  == 'POST':
                    Nombre = request.form['Nombre']
                    Apellido = request.form['Apellido']
                    Documento = request.form['Documento']
                    Email = request.form['Email']
                    #Cursor =  Conexion.cursor()

                    Consulta = "update Clientes set  Nombre = '" + Nombre + "' , Apellido = '" + Apellido + "' , Documento = '" + Documento + "', Email = '" + Email + "' where id = '" + id + "'"
                    print(Consulta)
                    flash('Contacto Editado')
                    cursor.execute(Consulta)  
                    return(redirect(url_for('cliente')))

        except Exception as e:
            print("Ocurrió un error al Editar el cliente : ", e)
            return("Ocurrió un error al Editar el cliente: ", e)
# Contacto---------------------------------------------------------------
@app.route('/agenda',  methods= ["GET"]) 
def agenda():
    global GUsuario
    if GUsuario != "":
        Cursor = Conexion.cursor()
        Cursor.execute('Select * from Contactos')
        Date = Cursor.fetchall()
        return render_template('index.html' , contactos = Date)
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))

@app.route('/agregarcontacto', methods=['POST'])
def agregarcontacto():
    try:
        with Conexion.cursor() as cursor:
            #if request.method  == 'POST':
                Nombre = request.form['Nombre']
                Apellido = request.form['Apellido']
                Telefono = request.form['Telefono']
                Email = request.form['Email']
                Validar() 
                Codigo = str(randrange(10000, 11000, 2))
                #Cursor =  Conexion.cursor()
                if Validar == True:
                    Consulta = "insert into Contactos (Codigo, Nombre, Apellido, Telefono, Email) Values ('" + Codigo + "', '" + Nombre + "',  '" + Apellido + "', '" + Telefono + "' , '" + Email + "')"
                    #print(Consulta)
                    flash('Contacto Agregado')
                    cursor.execute(Consulta)  
                    return(redirect(url_for('agenda')))
                    
                else:
                    return(redirect(url_for('agenda')))
    except Exception as e:
        print("Ocurrió un error al grabar el contacto : ", e)
        return("Ocurrió un error al grabar el contacto: ", e)

@app.route('/eliminar/<string:id>')
def eliminarcontacto(id):
    try:
        with Conexion.cursor() as cursor:
            #cursor = Conexion.cursor()
            Consulta = "delete from Contactos where id = " + id + ""
            cursor.execute(Consulta)
            flash('Contacto Eliminado')
            return(redirect(url_for('agenda')))
            #return('Eliminar Cliente')
    except Exception as e:
        print("Ocurrió un error al eliminarr el contacto : ", e)
        return("Ocurrió un error al eliminar el contacto: ", e)

@app.route('/editar/<string:id>')
def editarcontacto(id):
    global GUsuario
    if GUsuario != '':
        try:
            with Conexion.cursor() as cursor:
                cursor.execute("Select * from contactos where id = '" + id + "'")
                dato = cursor.fetchall()
                return( render_template('EditContacto.html', Contacto = dato[0]))
                
        except Exception as e:
            print("Ocurrió un error al eliminarr el contacto : ", e)
            return("Ocurrió un error al eliminar el contacto : ", e)
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))

@app.route('/editar/<id>',  methods= ["POST"]) 
def editar(id):
    #if request.method == 'POST':
        try:
            with Conexion.cursor() as cursor:
                #if request.method  == 'POST':
                    Nombre = request.form['Nombre']
                    Apellido = request.form['Apellido']
                    Telefono = request.form['Telefono']
                    Email = request.form['Email']
                    #Cursor =  Conexion.cursor()

                    Consulta = "update Contactos set  Nombre = '" + Nombre + "' , Apellido = '" + Apellido + "' , Telefono = '" + Telefono + "', Email = '" + Email + "' where id = '" + id + "'"
                    flash('Contacto Editado')
                    cursor.execute(Consulta)  
                    return(redirect(url_for('agenda')))

        except Exception as e:
            print("Ocurrió un error al Editar el contacto : ", e)
            return("Ocurrió un error al Editar el contacto: ", e)
#Perfil----------------------------------------------------------------------------------------------------------
@app.route('/perfil',  methods= ["GET"]) 
def perfil():
    global GUsuario
    global GApellido
    global GId
    if GUsuario != '':
        try:
            with Conexion.cursor() as cursor:

                Consulta = " select CLIENTES.ID, CLIENTES.Nombre, CLIENTES.Apellido, CLIENTES.Email, Provincias.Descripcion as'Provincia', TipoDocumentos.Descripcion as 'Tipo Documento', Empresas.Descripcion as ' Empresa', tipoUsuario.Descripcion as 'Tipo Usuario', Usuario, Contraseña from CLIENTES "
                Consulta = Consulta + " inner join Provincias on CLIENTES.IdProvincia = Provincias.IdProvincia "
                Consulta = Consulta + " inner join TipoDocumentos on CLIENTES.idTipoDocumento = TipoDocumentos.IdTipoDocumento "
                Consulta = Consulta + " inner join Empresas on CLIENTES.IDEmpreza = Empresas.IDEmpreza "
                Consulta = Consulta + " inner join tipoUsuario on CLIENTES.idTipo = tipoUsuario.idTipo "
                Consulta = Consulta + " where Id = '" + GId + "'"
                cursor.execute(Consulta)  
                clientes = cursor.fetchall()
                #for Dato in clientes:
                    #Email = str(Dato.Email)
                    #Provincia = str(Dato.Provincia)
                    #TipoDocumento = str(Dato[4])
                    #Empresa = str(Dato[5])
                    #TipoUsuario = str(Dato[6])
                    #Usuario = str(Dato.Usuario)
                return render_template('Perfil.html', GUsuario = GUsuario,  GApellido = GApellido, clientes = clientes ) 

        except Exception as e:

            print("Ocurrió un error al Consultar el perfil: ", e)
            flash("Ocurrió un error al Consultar el perfil: ", e)     
    else:
        flash("Tiene que Inicio sesión para poder usar el sistemas: ")
        return(redirect(url_for('index')))

@app.route('/perfilgrabar',  methods= ["POST"]) 
def perfilGrabar():
    global GUsuario
    global GApellido

    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form]
    modulo = str(dict(zip(fields, values)))

    #obtengo la imagen
    indice_c = modulo.index(' ') #obtenemos la posición del carácter :
    indice_h = modulo.index(',') #obtenemos la posición del carácter ,

    subvalue = str(modulo[indice_c:indice_h])

    #print(subvalue.split())

    #si queremos incluir en la subcadena el elemento de la posición 
    #indice_h basta con sumar 1 a esa posición
    app.config['UPLOAD_FOLDER'] = '/static/Imagenes'
    # obtenemos el archivo del input "archivo"
    f = request.form['archivo']
    print(f)
    filename = secure_filename(f)
    # Guardamos el archivo en el directorio "Archivos PDF"
    os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if subvalue.strip() == "'camara'":
        flash('Hola ' + GUsuario + ' ' + GApellido + subvalue)
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        return "<h1>Archivo subido exitosamente</h1>"

    #elif subvalue == "'WhatsApp" ',' 'Image' ',' '2021-08-27' ',' 'at' ',' '11.45.22' ',' "AM.jpeg'":
    return(redirect(url_for('perfil')))


@app.route('/nuevousuario',  methods= ["GET"]) 
def nuevousuario():
    global GUsuario
    if GUsuario != "":
        Cursor = Conexion.cursor()
        Cursor.execute('Select id, Nombre, Apellido, Email, Usuario from Clientes')
        Date = Cursor.fetchall()
        Cursor.execute('Select * from TipoDocumentos')
        Date1 = Cursor.fetchall()

        return render_template('nuevousuario.html' , contactos = Date , TipoDocumentos = Date1)

@app.route('/grabarusuario',  methods= ["POST"]) 
def grabarusuario():
    global ConexionP
    global GUsuarioP

    print('Holafdgsdfg')
    return(redirect(url_for('perfil')))

@app.errorhandler(NameError)
def Error(error):
    print('hola')
    return(redirect(url_for('index')))

def Validar():
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Telefono = request.form['Telefono']
    Email = request.form['Email']
    if len(Nombre) == 0:
        flash("Ingrese su nombre por favor")
        Validar = False
    elif len(Apellido) == 0:
        flash("Ingrese su apellido por favor")
        Validar = False
    elif len(Telefono) == 0:
        flash("Ingrese su apellido por favor")
        Validar = False
    elif len(Email) == 0:
        flash("Ingrese su email por favor")      
        Validar = False
    else:
        Validar = True

# iniciando la aplicación
if __name__ == "__main__":
    app.run(port=3000, debug=True)
else:
    login()
    render_template('Login.html')       
                