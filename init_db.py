import os
import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    # Asegurar que existe el directorio database/
    db_dir = os.path.join(os.path.dirname(__file__), 'database')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Creado directorio: {db_dir}")

    db_path = os.path.join(db_dir, 'peluqueria.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'sql', 'schema.sql')

    print(f"Conectando a base de datos en: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar esquema
    print(f"Leyendo esquema desde: {schema_path}")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    print("Esquema creado exitosamente.")

    # Sembrar administrador por defecto
    admin_user = 'admin'
    admin_pass = 'admin123'
    pass_hash = generate_password_hash(admin_pass)
    
    cursor.execute(
        "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
        (admin_user, pass_hash)
    )
    print(f"Usuario administrador sembrado: '{admin_user}' con contraseña '{admin_pass}' (encriptada).")

    # Sembrar servicios base
    servicios = [
        ('Corte Premium', 'Desde clásicos atemporales hasta tendencias vanguardistas, diseñamos tu estilo.', 45, 4500.0),
        ('Color & Balayage', 'Balayage, reflejos y coloración experta para dar vida y brillo a tu cabello.', 120, 8500.0),
        ('Tratamiento Barba', 'Tratamiento completo de barbería, perfilado y cuidado facial masculino.', 30, 3000.0),
        ('Tratamiento Facial', 'Limpieza e hidratación facial para revitalizar tu piel.', 60, 4200.0)
    ]

    cursor.executemany(
        "INSERT INTO servicios (nombre, descripcion, duracion, precio) VALUES (?, ?, ?, ?)",
        servicios
    )
    print(f"Sembrados {len(servicios)} servicios base.")

    conn.commit()
    conn.close()
    print("Inicialización de base de datos completa.")

if __name__ == '__main__':
    init_db()
