#from App import *
import App
from re import A, U
from flask import render_template, request, redirect, url_for, flash
from random import randrange

#Cliente--------------------------------------------------------------------------------------------------------

App.app.route('/agregarcliente', methods=['POST'])
def agregarcliente():
    try:
        with App.Conexion.cursor() as cursor:
            #if request.method  == 'POST':
                Nombre = request.form['Nombre']
                Apellido = request.form['Apellido']
                Email = request.form['Email']
                TipoDocumento = request.form['TipoDocumento']
                Documento = request.form['Documento']
                Imagen = request.form['Imagen']
                #Validar() 
                Codigo = str(randrange(10000, 11000, 2))
                Cursor =  App.Conexion.cursor()
                if Validar == True:
                    #Consulta = "insert into Contactos (Codigo, Nombre, Apellido, TipoDocumento, Email) Values ('" + Codigo + "', '" + Nombre + "',  '" + Apellido + "', '" + TipoDocumento + "' , '" + Email + "')"
                    #print(Consulta)
                    #cursor.execute(Consulta)  
                    flash('Contacto Agregado')
                    return(redirect(url_for('agregarcliente')))
                    
                else:
                    return(redirect(url_for('agenda')))
    except Exception as e:
        print("Ocurrió un error al grabar: ", e)
        return("Ocurrió un error al grabar: ", e)

def Validar():
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Email = request.form['Email']
    TipoDocumento = request.form['TipoDocumento']
    Documento = request.form['Documento']

    if len(Nombre) == 0:
        flash("Ingrese su nombre por favor")
        Validar = False
    elif len(Apellido) == 0:
        flash("Ingrese su apellido por favor")
        Validar = False
    elif len(TipoDocumento) == 0:
        flash("Ingrese el tipo de Documento por favor")
        Validar = False
    elif len(Email) == 0:
        flash("Ingrese su email por favor")      
        Validar = False
    elif len(Documento) == 0:
        flash("Ingrese su Documento por favor")      
        Validar = False
    else:
        Validar = True