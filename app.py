import os
import sqlite3
import functools
from datetime import datetime, timedelta
from flask import Flask, g, request, session, redirect, url_for, render_template, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'lumiere_salon_super_secret_key_123')

DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'peluqueria.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Decorador para requerir autenticación de administrador
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario_id' not in session:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.path.startswith('/api/'):
                return jsonify({'error': 'No autorizado'}), 401
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# ==========================================
# RUTAS WEB PRINCIPALES (Vistas)
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        # Soporte tanto para formulario tradicional como para JSON
        if request.is_json:
            data = request.get_json()
            username = data.get('usuario')
            password = data.get('password')
        else:
            username = request.form.get('usuario')
            password = request.form.get('password')
            
        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE usuario = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['usuario_id'] = user['id']
            session['usuario'] = user['usuario']
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            return redirect(url_for('dashboard'))
        else:
            error_msg = 'Usuario o contraseña incorrectos'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg)
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/servicios')
@login_required
def servicios():
    return render_template('servicios.html')

# ==========================================
# API REST: SERVICIOS
# ==========================================

@app.route('/api/servicios', methods=['GET'])
def api_get_servicios():
    db = get_db()
    servicios_rows = db.execute('SELECT * FROM servicios ORDER BY id ASC').fetchall()
    return jsonify([dict(row) for row in servicios_rows])

@app.route('/api/servicios', methods=['POST'])
@login_required
def api_create_servicio():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')
    duracion = data.get('duracion')
    precio = data.get('precio')
    
    if not nombre or not duracion or precio is None:
        return jsonify({'error': 'Nombre, duración y precio son obligatorios'}), 400
        
    try:
        duracion = int(duracion)
        precio = float(precio)
        if duracion <= 0 or precio < 0:
            raise ValueError()
    except ValueError:
        return jsonify({'error': 'Duración debe ser mayor a 0 y precio mayor o igual a 0'}), 400
        
    db = get_db()
    cursor = db.execute(
        'INSERT INTO servicios (nombre, descripcion, duracion, precio) VALUES (?, ?, ?, ?)',
        (nombre, descripcion, duracion, precio)
    )
    db.commit()
    
    nuevo_id = cursor.lastrowid
    return jsonify({'success': True, 'id': nuevo_id, 'message': 'Servicio creado exitosamente'}), 217

@app.route('/api/servicios/<int:id>', methods=['PUT'])
@login_required
def api_update_servicio(id):
    data = request.get_json() or {}
    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')
    duracion = data.get('duracion')
    precio = data.get('precio')
    
    if not nombre or not duracion or precio is None:
        return jsonify({'error': 'Nombre, duración y precio son obligatorios'}), 400
        
    try:
        duracion = int(duracion)
        precio = float(precio)
        if duracion <= 0 or precio < 0:
            raise ValueError()
    except ValueError:
        return jsonify({'error': 'Duración debe ser mayor a 0 y precio mayor o igual a 0'}), 400
        
    db = get_db()
    db.execute(
        'UPDATE servicios SET nombre = ?, descripcion = ?, duracion = ?, precio = ? WHERE id = ?',
        (nombre, descripcion, duracion, precio, id)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': 'Servicio actualizado exitosamente'})

@app.route('/api/servicios/<int:id>', methods=['DELETE'])
@login_required
def api_delete_servicio(id):
    db = get_db()
    # Verificar si el servicio está siendo usado por algún turno activo
    usado = db.execute('SELECT COUNT(*) as count FROM turnos WHERE servicio_id = ? AND estado != ?', (id, 'cancelado')).fetchone()
    if usado['count'] > 0:
        return jsonify({'error': 'No se puede eliminar el servicio porque tiene turnos activos agendados'}), 400
        
    db.execute('DELETE FROM servicios WHERE id = ?', (id,))
    db.commit()
    return jsonify({'success': True, 'message': 'Servicio eliminado exitosamente'})

# ==========================================
# API REST: HORARIOS DISPONIBLES (CLIENTE / ADMIN)
# ==========================================

@app.route('/api/horarios-disponibles', methods=['GET'])
def api_horarios_disponibles():
    fecha_str = request.args.get('fecha') # YYYY-MM-DD
    servicio_id = request.args.get('servicio_id')
    
    if not fecha_str or not servicio_id:
        return jsonify({'error': 'Faltan parámetros requeridos (fecha, servicio_id)'}), 400
        
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD'}), 400
        
    # El salón abre de Lunes a Sábado. Domingos cerrado (0 = Lunes, 6 = Domingo).
    if fecha_obj.weekday() == 6:
        return jsonify([]) # Domingo cerrado
        
    db = get_db()
    servicio = db.execute('SELECT * FROM servicios WHERE id = ?', (servicio_id,)).fetchone()
    if not servicio:
        return jsonify({'error': 'Servicio no encontrado'}), 404
        
    duracion_propuesta = servicio['duracion']
    
    # Horario de atención: 09:00 a 20:00.
    hora_inicio_salon = 9
    hora_fin_salon = 20
    
    # Obtener turnos existentes activos para ese día
    turnos_existentes = db.execute(
        """
        SELECT t.fecha_hora, s.duracion 
        FROM turnos t 
        JOIN servicios s ON t.servicio_id = s.id 
        WHERE DATE(t.fecha_hora) = DATE(?) AND t.estado != 'cancelado'
        """,
        (fecha_str,)
    ).fetchall()
    
    # Convertir turnos existentes a intervalos de datetime
    intervalos_ocupados = []
    for t in turnos_existentes:
        t_inicio = datetime.strptime(t['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        t_fin = t_inicio + timedelta(minutes=t['duracion'])
        intervalos_ocupados.append((t_inicio, t_fin))
        
    # Generar slots potenciales cada 30 minutos
    slots_disponibles = []
    current_time = fecha_obj.replace(hour=hora_inicio_salon, minute=0, second=0, microsecond=0)
    end_limit = fecha_obj.replace(hour=hora_fin_salon, minute=0, second=0, microsecond=0)
    
    # No permitir turnos en el pasado si la fecha consultada es HOY
    now = datetime.now()
    
    while current_time + timedelta(minutes=duracion_propuesta) <= end_limit:
        slot_inicio = current_time
        slot_fin = current_time + timedelta(minutes=duracion_propuesta)
        
        # Validar que el slot no esté en el pasado
        if slot_inicio > now:
            # Comprobar superposición con reservas existentes
            overlap = False
            for ocupado_inicio, ocupado_fin in intervalos_ocupados:
                # Dos intervalos [s1, e1] y [s2, e2] se superponen si: s1 < e2 y e1 > s2
                if slot_inicio < ocupado_fin and slot_fin > ocupado_inicio:
                    overlap = True
                    break
            
            if not overlap:
                slots_disponibles.append(slot_inicio.strftime('%H:%M'))
                
        current_time += timedelta(minutes=30)
        
    return jsonify(slots_disponibles)

# ==========================================
# API REST: RESERVAS (CLIENTE)
# ==========================================

@app.route('/api/reservar', methods=['POST'])
def api_reservar():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    telefono = data.get('telefono')
    email = data.get('email', '')
    servicio_id = data.get('servicio_id')
    fecha = data.get('fecha')     # YYYY-MM-DD
    horario = data.get('horario') # HH:MM
    
    if not nombre or not apellido or not telefono or not servicio_id or not fecha or not horario:
        return jsonify({'error': 'Todos los campos excepto el email son obligatorios'}), 400
        
    db = get_db()
    servicio = db.execute('SELECT * FROM servicios WHERE id = ?', (servicio_id,)).fetchone()
    if not servicio:
        return jsonify({'error': 'Servicio no encontrado'}), 404
        
    duracion = servicio['duracion']
    
    # Armar datetime propuesto
    try:
        fecha_hora_str = f"{fecha} {horario}:00"
        fecha_hora_propuesta = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Formato de fecha u horario inválido'}), 400
        
    # Validar que no sea en el pasado
    if fecha_hora_propuesta <= datetime.now():
        return jsonify({'error': 'No se puede reservar en un horario pasado'}), 400
        
    # Validar superposición (Prevención estricta de doble reserva)
    fecha_hora_fin_propuesta = fecha_hora_propuesta + timedelta(minutes=duracion)
    
    turnos_existentes = db.execute(
        """
        SELECT t.fecha_hora, s.duracion 
        FROM turnos t 
        JOIN servicios s ON t.servicio_id = s.id 
        WHERE DATE(t.fecha_hora) = DATE(?) AND t.estado != 'cancelado'
        """,
        (fecha,)
    ).fetchall()
    
    for t in turnos_existentes:
        ocupado_inicio = datetime.strptime(t['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        ocupado_fin = ocupado_inicio + timedelta(minutes=t['duracion'])
        if fecha_hora_propuesta < ocupado_fin and fecha_hora_fin_propuesta > ocupado_inicio:
            return jsonify({'error': 'El horario seleccionado ya no está disponible'}), 400
            
    # Registrar/Obtener cliente
    cliente = db.execute('SELECT * FROM clientes WHERE telefono = ?', (telefono,)).fetchone()
    if cliente:
        cliente_id = cliente['id']
        # Actualizar email/nombre por si cambiaron
        db.execute(
            'UPDATE clientes SET nombre = ?, apellido = ?, email = ? WHERE id = ?',
            (nombre, apellido, email, cliente_id)
        )
    else:
        cursor = db.execute(
            'INSERT INTO clientes (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)',
            (nombre, apellido, telefono, email)
        )
        cliente_id = cursor.lastrowid
        
    # Crear turno
    db.execute(
        'INSERT INTO turnos (cliente_id, servicio_id, fecha_hora, estado) VALUES (?, ?, ?, ?)',
        (cliente_id, servicio_id, fecha_hora_str, 'pendiente')
    )
    db.commit()
    
    return jsonify({
        'success': True,
        'message': '¡Reserva realizada con éxito! Tu turno quedó en estado pendiente de confirmación.'
    })

# ==========================================
# API REST: TURNOS (ADMINISTRACIÓN)
# ==========================================

@app.route('/api/turnos', methods=['GET'])
@login_required
def api_get_turnos():
    fecha_str = request.args.get('fecha') # YYYY-MM-DD
    
    db = get_db()
    if fecha_str:
        query = """
            SELECT t.id, t.fecha_hora, t.estado, t.cliente_id, t.servicio_id,
                   c.nombre as cliente_nombre, c.apellido as cliente_apellido, c.telefono as cliente_telefono, c.email as cliente_email,
                   s.nombre as servicio_nombre, s.duracion as servicio_duracion, s.precio as servicio_precio
            FROM turnos t
            JOIN clientes c ON t.cliente_id = c.id
            JOIN servicios s ON t.servicio_id = s.id
            WHERE DATE(t.fecha_hora) = DATE(?)
            ORDER BY t.fecha_hora ASC
        """
        turnos_rows = db.execute(query, (fecha_str,)).fetchall()
    else:
        query = """
            SELECT t.id, t.fecha_hora, t.estado, t.cliente_id, t.servicio_id,
                   c.nombre as cliente_nombre, c.apellido as cliente_apellido, c.telefono as cliente_telefono, c.email as cliente_email,
                   s.nombre as servicio_nombre, s.duracion as servicio_duracion, s.precio as servicio_precio
            FROM turnos t
            JOIN clientes c ON t.cliente_id = c.id
            JOIN servicios s ON t.servicio_id = s.id
            ORDER BY t.fecha_hora ASC
        """
        turnos_rows = db.execute(query).fetchall()
        
    result = []
    for row in turnos_rows:
        d = dict(row)
        # Formatear fecha y hora para facilitar su lectura en JS
        dt = datetime.strptime(d['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        d['hora'] = dt.strftime('%H:%M')
        d['fecha'] = dt.strftime('%Y-%m-%d')
        result.append(d)
        
    return jsonify(result)

@app.route('/api/turnos', methods=['POST'])
@login_required
def api_create_turno_admin():
    # El admin puede agendar un turno directamente para un cliente (buscándolo por teléfono o creándolo)
    data = request.get_json() or {}
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    telefono = data.get('telefono')
    email = data.get('email', '')
    servicio_id = data.get('servicio_id')
    fecha = data.get('fecha')
    horario = data.get('horario')
    estado = data.get('estado', 'confirmado') # Por defecto confirmado si lo hace el admin
    
    if not nombre or not apellido or not telefono or not servicio_id or not fecha or not horario:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
        
    db = get_db()
    servicio = db.execute('SELECT * FROM servicios WHERE id = ?', (servicio_id,)).fetchone()
    if not servicio:
        return jsonify({'error': 'Servicio no encontrado'}), 404
        
    duracion = servicio['duracion']
    
    # Armar datetime propuesto
    try:
        fecha_hora_str = f"{fecha} {horario}:00"
        fecha_hora_propuesta = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Formato de fecha u horario inválido'}), 400

    # Validar superposición (incluso para administradores)
    fecha_hora_fin_propuesta = fecha_hora_propuesta + timedelta(minutes=duracion)
    
    turnos_existentes = db.execute(
        """
        SELECT t.fecha_hora, s.duracion, (c.nombre || ' ' || c.apellido) as cliente_nombre
        FROM turnos t 
        JOIN servicios s ON t.servicio_id = s.id 
        JOIN clientes c ON t.cliente_id = c.id
        WHERE DATE(t.fecha_hora) = DATE(?) AND t.estado != 'cancelado'
        """,
        (fecha,)
    ).fetchall()
    
    for t in turnos_existentes:
        ocupado_inicio = datetime.strptime(t['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        ocupado_fin = ocupado_inicio + timedelta(minutes=t['duracion'])
        if fecha_hora_propuesta < ocupado_fin and fecha_hora_fin_propuesta > ocupado_inicio:
            return jsonify({
                'error': f'El horario se superpone con el turno de {t["cliente_nombre"]} ({t["duracion"]} min)'
            }), 400
            
    # Registrar/Obtener cliente
    cliente = db.execute('SELECT * FROM clientes WHERE telefono = ?', (telefono,)).fetchone()
    if cliente:
        cliente_id = cliente['id']
        db.execute(
            'UPDATE clientes SET nombre = ?, apellido = ?, email = ? WHERE id = ?',
            (nombre, apellido, email, cliente_id)
        )
    else:
        cursor = db.execute(
            'INSERT INTO clientes (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)',
            (nombre, apellido, telefono, email)
        )
        cliente_id = cursor.lastrowid
        
    # Crear turno
    db.execute(
        'INSERT INTO turnos (cliente_id, servicio_id, fecha_hora, estado) VALUES (?, ?, ?, ?)',
        (cliente_id, servicio_id, fecha_hora_str, estado)
    )
    db.commit()
    
    return jsonify({'success': True, 'message': 'Turno agendado exitosamente por administración'})

@app.route('/api/turnos/<int:id>/estado', methods=['PUT'])
@login_required
def api_update_turno_estado(id):
    data = request.get_json() or {}
    nuevo_estado = data.get('estado')
    
    if nuevo_estado not in ['pendiente', 'confirmado', 'cancelado']:
        return jsonify({'error': 'Estado inválido'}), 400
        
    db = get_db()
    # Validar que exista el turno
    turno = db.execute('SELECT * FROM turnos WHERE id = ?', (id,)).fetchone()
    if not turno:
        return jsonify({'error': 'Turno no encontrado'}), 404
        
    db.execute('UPDATE turnos SET estado = ? WHERE id = ?', (nuevo_estado, id))
    db.commit()
    
    return jsonify({'success': True, 'message': f'Estado del turno actualizado a {nuevo_estado}'})

@app.route('/api/turnos/<int:id>', methods=['DELETE'])
@login_required
def api_delete_turno(id):
    db = get_db()
    # Validar que exista el turno
    turno = db.execute('SELECT * FROM turnos WHERE id = ?', (id,)).fetchone()
    if not turno:
        return jsonify({'error': 'Turno no encontrado'}), 404
        
    db.execute('DELETE FROM turnos WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'success': True, 'message': 'Turno eliminado de la agenda'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
