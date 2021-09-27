from flask import Flask, render_template
app = Flask(__name__)

def Inicializa(Conexion, GUsuario, flash):
    global ConexionP
    ConexionP = Conexion
    global GUsuarioP
    GUsuarioP = GUsuario
    global render_templateP
    render_templateP = render_template
    global flashP 
    flashP = flash
    perfill()

@app.route('/perfill',  methods= ["GET"]) 
def perfill():
    print('Hola perfill')
    global ConexionP
    global GUsuarioP
    return( render_template('Perfil.html'))

@app.route('/perfiil',  methods= ["GET"]) 
def perfiil():
    global ConexionP
    global GUsuarioP

    print('Holafdgsdfg')
    #return render_template('Perfil.html')