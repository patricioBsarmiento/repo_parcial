#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap


from forms import LoginForm, SaludarForm, RegistrarForm, ConsultaPaisForm



app = Flask(__name__)
bootstrap = Bootstrap(app)





app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


#@app.route('/saludar', methods=['GET', 'POST'])
#def saludar():
    #formulario = SaludarForm()
    #if formulario.validate_on_submit():  # Acá hice el POST si es True
        #print(formulario.usuario.name)
        #return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    #return render_template('saludar.html', form=formulario)


#@app.route('/saludar/<usuario>')
#def saludar_persona(usuario):
    #return render_template('usuarios.html', nombre=usuario)

@app.route('/sobre')       # Creo la ruta '/sobre'.
def sobre():
    return render_template('sobre.html')   # Defino una funcion que retorne la plantilla renderizada.


@app.route('/clientes', methods=['GET']) # Creo la ruta '/clientes'.
def clientes():                          # Defino la funcion clientes().
    with open("clientes", encoding="utf-8") as f:          # Abro el archivo en modo w.
        reader = csv.reader(f)           # Creo la variable reader y le asigno = csv.reader(f).
        vercontenido = list(reader)      # Creo la variable vercontenido asignandole = list(reader).
        return render_template("clientes.html", tabla=vercontenido)   # Le digo que retorne la plantilla renderizada en forma de tabla.



@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+', newline="") as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)



@app.route('/buscarporpais')
def busquedaporpais():
    if 'username' in session:
        pais = request.args.get("pais")
        if pais:
            rows = []
            with open("clientes", encoding="utf-8") as archivo:
                archivo_csv = csv.reader(archivo)
                headers = next(archivo_csv)
                registro = next(archivo_csv, None)
                paisarg = str(pais).lower()
                while registro:
                    reg = str(registro[3]).lower()
                    if paisarg in reg:
                        rows.append(registro)
                    registro = next(archivo_csv, None)
                if len(rows) < 1:
                    flash('No se encontraron registros relacionados a la búsqueda.')
                return render_template("busquedaporpais.html", headers = headers, rows = rows)
        return render_template("busquedaporpais.html")
    return redirect(url_for('ingresar'))





@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
