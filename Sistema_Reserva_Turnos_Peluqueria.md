# Sistema de Reserva de Turnos para Peluquería

## 1. Descripción General del Proyecto

Desarrollar una aplicación web para la gestión de turnos de una peluquería. El sistema permitirá a los clientes reservar turnos online y a los administradores gestionar clientes, servicios y turnos desde un panel privado.

---

# 2. Objetivos del Sistema

## Objetivo General

Digitalizar la gestión de turnos de una peluquería mediante una aplicación web simple, segura y fácil de utilizar.

## Objetivos Específicos

- Permitir reservas online.
- Gestionar clientes.
- Gestionar servicios.
- Gestionar turnos.
- Evitar superposición de reservas.
- Implementar autenticación para administradores.
- Persistir datos en SQLite.

---

# 3. Alcance del MVP

Incluye:

- Login de administrador.
- CRUD de clientes.
- CRUD de servicios.
- CRUD de turnos.
- Reserva pública.
- Base de datos SQLite.
- Validaciones básicas.

No incluye:

- WhatsApp.
- Correos electrónicos.
- Pagos online.
- Gestión de empleados.

---

# 4. Stack Tecnológico

## Frontend

- HTML5
- CSS3
- JavaScript Vanilla
- Fetch API

## Backend

- Python 3
- Flask

## Base de Datos

- SQLite

---

# 5. Roles del Sistema

## Cliente

- Reservar turnos.
- Consultar servicios.

## Administrador

- Iniciar sesión.
- Gestionar clientes.
- Gestionar servicios.
- Gestionar turnos.
- Consultar agenda.

---

# 6. Requerimientos Funcionales

- Login de administrador.
- CRUD de clientes.
- CRUD de servicios.
- CRUD de turnos.
- Reserva pública.
- Consulta de agenda.
- Evitar reservas duplicadas.

---

# 7. Requerimientos No Funcionales

- Aplicación responsive.
- Contraseñas almacenadas con hash.
- Uso de SQLite.
- Uso de sesiones Flask.
- Interfaz intuitiva.

---

# 8. Casos de Uso Principales

## Cliente

### Reservar Turno

1. Selecciona servicio.
2. Selecciona fecha.
3. Selecciona horario.
4. Completa datos.
5. Confirma reserva.

## Administrador

### Gestionar Clientes

Crear, editar, eliminar y listar clientes.

### Gestionar Servicios

Crear, editar, eliminar y listar servicios.

### Gestionar Turnos

Crear, editar, cancelar y listar turnos.

---

# 9. Módulos del Sistema

## Login

- Iniciar sesión.
- Cerrar sesión.

## Clientes

- Alta.
- Baja.
- Modificación.
- Consulta.

## Servicios

- Alta.
- Baja.
- Modificación.
- Consulta.

## Turnos

- Alta.
- Baja.
- Modificación.
- Consulta.

## Reserva Pública

- Selección de servicio.
- Selección de horario.
- Confirmación.

---

# 10. Modelo de Datos

Entidades:

- Usuarios
- Clientes
- Servicios
- Turnos

---

# 11. Diagrama Entidad Relación

```text
CLIENTES
    |
    | 1:N
    |
TURNOS
    |
    | N:1
    |
SERVICIOS

USUARIOS
(Administra el sistema)
```

---

# 12. Estructura de la Base de Datos

## usuarios

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| usuario | TEXT |
| password_hash | TEXT |

## clientes

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| nombre | TEXT |
| apellido | TEXT |
| telefono | TEXT |
| email | TEXT |

## servicios

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| nombre | TEXT |
| descripcion | TEXT |
| duracion | INTEGER |
| precio | REAL |

## turnos

| Campo | Tipo |
|---------|---------|
| id | INTEGER |
| cliente_id | INTEGER |
| servicio_id | INTEGER |
| fecha_hora | DATETIME |
| estado | TEXT |

---

# 13. API REST

## Login

```http
POST /login
POST /logout
```

## Clientes

```http
GET /api/clientes
GET /api/clientes/<id>
POST /api/clientes
PUT /api/clientes/<id>
DELETE /api/clientes/<id>
```

## Servicios

```http
GET /api/servicios
GET /api/servicios/<id>
POST /api/servicios
PUT /api/servicios/<id>
DELETE /api/servicios/<id>
```

## Turnos

```http
GET /api/turnos
GET /api/turnos/<id>
POST /api/turnos
PUT /api/turnos/<id>
DELETE /api/turnos/<id>
```

## Reserva Pública

```http
GET /api/horarios-disponibles
POST /api/reservar
```

---

# 14. Pantallas

## Públicas

- Inicio
- Reserva
- Confirmación

## Administración

- Login
- Dashboard
- Clientes
- Servicios
- Turnos

---

# 15. Flujo de Navegación

## Cliente

```text
Inicio
 ↓
Reserva
 ↓
Confirmación
```

## Administrador

```text
Login
 ↓
Dashboard
 ├─ Clientes
 ├─ Servicios
 └─ Turnos
```

---

# 16. Estructura de Carpetas

```text
peluqueria/
│
├── app.py
├── database/
│   └── peluqueria.db
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── login.js
│       ├── clientes.js
│       ├── servicios.js
│       ├── turnos.js
│       └── reserva.js
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── clientes.html
│   ├── servicios.html
│   ├── turnos.html
│   └── reserva.html
├── sql/
│   └── schema.sql
└── requirements.txt
```

---

# 17. Estrategia de Autenticación

Se utilizarán sesiones de Flask.

- Login mediante usuario y contraseña.
- Contraseñas hasheadas con Werkzeug.
- Rutas protegidas mediante sesión.

```python
generate_password_hash()
check_password_hash()
```

---

# 18. Validaciones

## Clientes

- Nombre obligatorio.
- Teléfono obligatorio.

## Servicios

- Nombre obligatorio.
- Duración mayor a 0.
- Precio mayor o igual a 0.

## Turnos

- Cliente obligatorio.
- Servicio obligatorio.
- Fecha obligatoria.
- Horario obligatorio.
- Sin duplicados.

---

# 19. Mejoras Futuras

- Recordatorios por WhatsApp.
- Correo electrónico.
- Integración con Google Calendar.
- Gestión de empleados.
- Estadísticas.
- Múltiples sucursales.

---

# 20. Distribución de Tareas

## Alumno 1

- Base de datos.
- Modelo relacional.

## Alumno 2

- Backend Flask.
- API REST.

## Alumno 3

- Login.
- Sesiones.

## Alumno 4

- CRUD Clientes.
- CRUD Servicios.

## Alumno 5

- CRUD Turnos.
- Reserva pública.

---

# Criterios de Aprobación

- CRUD funcionales.
- Login operativo.
- Persistencia SQLite.
- Reserva pública funcional.
- Validaciones implementadas.
- Código organizado y documentado.
