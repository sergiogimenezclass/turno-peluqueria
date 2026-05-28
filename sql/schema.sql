-- Esquema de base de datos para Lumière Salon

DROP TABLE IF EXISTS turnos;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS usuarios;

-- Tabla de administradores
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Tabla de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT UNIQUE NOT NULL,
    email TEXT
);

-- Tabla de servicios
CREATE TABLE servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    duracion INTEGER NOT NULL, -- Duración en minutos
    precio REAL NOT NULL -- Precio del servicio
);

-- Tabla de turnos/reservas
CREATE TABLE turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente', -- 'pendiente', 'confirmado', 'cancelado'
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE RESTRICT
);
