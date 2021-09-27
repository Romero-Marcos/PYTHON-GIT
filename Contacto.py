from App import *

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
        print("Ocurrió un error al grabar: ", e)
        return("Ocurrió un error al grabar: ", e)

@app.route('/eliminar/<string:id>')
def eliminarcontacto(id):
    try:
        with Conexion.cursor() as cursor:
            #cursor = Conexion.cursor()
            Consulta = "delete from Contactos where id = " + id + ""
            cursor.execute(Consulta)
            print(Consulta)
            flash('Contacto Eliminado')
            return(redirect(url_for('agenda')))
            #return('Eliminar Cliente')
    except Exception as e:
        print("Ocurrió un error al eliminarr: ", e)
        return("Ocurrió un error al eliminar: ", e)

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
            print("Ocurrió un error al eliminarr: ", e)
            return("Ocurrió un error al eliminar: ", e)
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
                    print(Consulta)
                    flash('Contacto Editado')
                    cursor.execute(Consulta)  
                    return(redirect(url_for('agenda')))

        except Exception as e:
            print("Ocurrió un error al Editar: ", e)
            return("Ocurrió un error al Editar: ", e)

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