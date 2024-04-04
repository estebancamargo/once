from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Agenda777"
)


cursor = db.cursor()

def encripcontra(password):
    encriptar = generate_password_hash(password)
    return encriptar

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT usuarioper, contraper, roles FROM personas WHERE usuarioper = %s"
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['contraper'], password):
            session['usuario'] = usuario['usuarioper']
            session['rol'] = usuario['roles']

            if usuario['roles'] == 'administrador':
                return redirect(url_for('lista'))  # Corrección aquí
            else:
                return redirect(url_for('listar_canciones'))
        else:
            flash("Credenciales incorrectas. Por favor, intenta nuevamente.", 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def lista():
    if 'usuario' in session:
        cursor.execute('SELECT * FROM personas')
        personas = cursor.fetchall()
        return render_template('index.html', personas=personas)
    else:
        return redirect(url_for('login'))

@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombres = request.form.get('nombre')
        apellidos = request.form.get('apellido')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('txtrol')

        # Encripta la contraseña antes de almacenarla en la base de datos
        contrasena_encriptada = encripcontra(contrasena)

        try:
            # Inserta el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO personas (nombreper, apellidoper, emailper, dirper, telper, usuarioper, contraper, roles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (nombres, apellidos, email, direccion, telefono, usuario, contrasena_encriptada, rol))
            db.commit()
            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error al crear usuario', 'error')

    return render_template('Registrar.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    if request.method == 'POST':
        nombreper = request.form.get('nombreper')
        apellidoper = request.form.get('apellidoper')
        emailper = request.form.get('emailper')
        dirper = request.form.get('direccionper')
        telper = request.form.get('telefonoper')
        usuarioper = request.form.get('usuarioper')
        passper = request.form.get('passwordper')

        sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, dirper=%s, telper=%s, usuarioper=%s, contraper=%s WHERE userId=%s"
        cursor.execute(sql, (nombreper, apellidoper, emailper, dirper, telper, usuarioper, passper, id))
        db.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('lista'))
    else:
        cursor.execute('SELECT * FROM personas WHERE userId = %s', (id,))
        data = cursor.fetchone()
        if data:
            return render_template('Editar.html', personas=data)
        else:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('lista'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if request.method == 'POST':
        cursor.execute('DELETE FROM personas WHERE userId = %s', (id,))
        db.commit()
        flash('Usuario eliminado correctamente', 'success') 
        return redirect(url_for('lista'))



@app.route('/canciones', methods=['GET', 'POST'])
def canciones():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')
        
        # Obtener la imagen del formulario correctamente
        imagen = request.files['imagen']
        imagenblob = imagen.read()
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO canciones (titulo, artista, genero, precio, duracion, lanzamiento, img) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (titulo, artista, genero, precio, duracion, lanzamiento, imagenblob))
        db.commit()
        
        flash('Canción agregada correctamente', 'success')
        
        # Redirigir a la lista de canciones después de agregar la canción
        return redirect(url_for('lista_canciones'))
        
    else:
        cursor = db.cursor()
        cursor.execute('SELECT idCan, titulo, artista, genero, precio, duracion, lanzamiento FROM canciones')
        canciones = [{'idCan': row[0], 'titulo': row[1], 'artista': row[2], 'genero': row[3], 'precio': row[4], 'duracion': row[5], 'lanzamiento': row[6]} for row in cursor.fetchall()]
        return render_template('canciones.html', canciones=canciones)



    
@app.route('/lista_canciones')
def listar_canciones():
    cursor = db.cursor()

    cursor.execute("SELECT idCan, titulo, artista, genero, precio, duracion, lanzamiento, img FROM canciones")
    canciones = cursor.fetchall()

    if canciones:
        # Crear una lista para almacenar los datos de las canciones
        canciones_data = []
        for cancion in canciones:
            # Convertir la imagen a base64
            imagen_base64 = base64.b64encode(cancion[7]).decode('utf-8')
            # Agregar los datos de la canción junto con la imagen a la lista de canciones
            canciones_data.append({
                'idCan': cancion[0],
                'titulo': cancion[1],
                'artista': cancion[2],
                'genero': cancion[3],
                'precio': cancion[4],
                'duracion': cancion[5],
                'lanzamiento': cancion[6],
                'img': imagen_base64
            })
        return render_template('lista_canciones.html', canciones=canciones_data)
    else:
        if 'rol' in session and session['rol'] == 'administrador':
            return redirect(url_for('index'))  # Redirigir al index si el usuario es administrador
        else:
            return "No se encontraron canciones"

@app.route('/editar_cancion/<int:id>', methods=['POST', 'GET'])
def editar_cancion(id):
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')

        cursor.execute("UPDATE canciones SET titulo=%s, artista=%s, genero=%s, precio=%s, duracion=%s, lanzamiento=%s WHERE idCan=%s",
                       (titulo, artista, genero, precio, duracion, lanzamiento, id))
        db.commit()
        flash('Canción actualizada correctamente', 'success')
        return redirect(url_for('canciones'))
    else:
        cursor.execute('SELECT * FROM canciones WHERE idCan = %s', (id,))
        cancion = cursor.fetchone()
        if cancion:
            return render_template('editar_cancion.html', cancion=cancion)
        else:
            flash('Canción no encontrada', 'error')
            return redirect(url_for('canciones'))



@app.route('/lista_canciones')
def lista_canciones():
    cursor.execute('SELECT idCan, titulo, artista, genero, precio, duracion, lanzamiento FROM canciones')
    canciones = [{'idCan': row[0], 'titulo': row[1], 'artista': row[2], 'genero': row[3], 'precio': row[4], 'duracion': row[5], 'lanzamiento': row[6]} for row in cursor.fetchall()]
    return render_template('lista_canciones.html', canciones=canciones)


@app.route('/eliminar_cancion/<int:id>', methods=['POST'])
def eliminar_cancion(id):
    if request.method == 'POST':
        # Eliminar primero los registros relacionados en la tabla compras
        cursor.execute("DELETE FROM compras WHERE idCan = %s", (id,))
        db.commit()

        # Luego, eliminar la canción
        cursor.execute("DELETE FROM canciones WHERE idCan = %s", (id,))
        db.commit()

        flash('Canción eliminada correctamente', 'success')
        return redirect(url_for('lista_canciones'))



@app.route('/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        fechaCompra = request.form.get('fecha_compra')
        precio = request.form.get('precio')
        metodoPago = request.form.get('metodo_pago')




        cursor.execute("INSERT INTO compras (fechaCompra, precio, metodoPago) VALUES (%s, %s, %s)",
                           (fechaCompra, precio, metodoPago))
        db.commit()
        flash('Compra realizada correctamente', 'success')
        return redirect(url_for('compras')) 

    else:
        cursor.execute('SELECT pk_id_compra, fechaCompra, precio, userId, idCan, metodoPago FROM compras')
        compras = cursor.fetchall()
        # Corregir la consulta para devolver un diccionario en lugar de una tupla
        compras = [{'pk_id_compra': row[0], 'fechaCompra': row[1], 'precio': row[2], 'userId': row[3], 'idCan': row[4], 'metodoPago': row[5]} for row in compras]
        return render_template('compras.html', compras=compras)







@app.route('/editar_compra/<int:id>', methods=['POST', 'GET'])
def editar_compra(id):
    if request.method == 'POST':
        fecha_compra = request.form.get('fecha_compra')
        precio = request.form.get('precio')
        user_id = request.form.get('user_id')
        cancion_id = request.form.get('cancion_id')
        metodo_pago = request.form.get('metodo_pago')

        cursor.execute("UPDATE compras SET fechaCompra=%s, precio=%s, userId=%s, id_cancion=%s, metodoPago=%s WHERE id_compra=%s",
                       (fecha_compra, precio, user_id, cancion_id, metodo_pago, id))
        db.commit()
        flash('Compra actualizada correctamente', 'success')
        return redirect(url_for('compras'))
    else:
        cursor.execute('SELECT * FROM compras WHERE id_compra = %s', (id,))
        compra = cursor.fetchone()
        if compra:
            return render_template('editar_compra.html', compra=compra)
        else:
            flash('Compra no encontrada', 'error')
            return redirect(url_for('compras'))

@app.route('/eliminar_compra/<int:id>', methods=['POST'])
def eliminar_compra(id):
    if request.method == 'POST':
        cursor.execute('DELETE FROM compras WHERE id_compra = %s', (id,))
        db.commit()
        flash('Compra eliminada correctamente', 'success') 
        return redirect(url_for('compras'))


if __name__ == '__main__':
    app.run(debug=True, port=5005)