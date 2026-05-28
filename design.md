# design.md

# Sistema de Reserva de Turnos para Peluquería

## Design Vision

Diseñar una aplicación web moderna para una peluquería pequeña con un único profesional.

La experiencia debe sentirse profesional, elegante y premium, inspirada visualmente en Apple y funcionalmente en Google Calendar.

El sistema debe priorizar la gestión rápida de turnos y minimizar la complejidad visual.

La aplicación debe sentirse más cercana a un producto SaaS moderno que a un sistema académico de CRUD tradicional.

---

# Design Principles

## 1. Mobile First

La interfaz debe diseñarse primero para dispositivos móviles.

Posteriormente debe adaptarse a tablet y desktop.

La experiencia móvil tiene prioridad.

## 2. Agenda First

El elemento más importante del sistema son los turnos.

La agenda debe ocupar el protagonismo visual del dashboard.

Los clientes no deben aparecer como módulo independiente.

## 3. Minimalismo Elegante

Evitar:
- Tablas complejas.
- Menús excesivos.
- Formularios sobrecargados.
- Demasiados colores.

Priorizar:
- Espacios en blanco.
- Tipografía clara.
- Fotografías profesionales.
- Jerarquía visual limpia.

## 4. Inspiración Visual

- Funcional: Google Calendar.
- Estética: Apple.
- UX: SaaS moderno.

---

# Color System

## Primary
#FF7A00

## Secondary
#FFFFFF

## Light Background
#F8F9FA

## Dark Background
#121212

## Text Light
#1F2937

## Text Dark
#F3F4F6

---

# Typography

SF Pro Display

Fallback:

-apple-system, BlinkMacSystemFont, sans-serif

---

# Navigation

## Mobile

Bottom Navigation

- Inicio
- Turnos
- Servicios
- Perfil

## Desktop

Top Navigation

- Dashboard
- Turnos
- Servicios

Sin sidebar.

---

# Landing Page

## Hero

- Fotografía profesional de peluquería.
- Título principal.
- Subtítulo.
- Botón Reservar Turno.

Ejemplo:

"Tu estilo comienza aquí"

"Reservá tu turno online en menos de un minuto."

---

# Reserva Pública

Formulario tradicional.

Campos:

- Nombre
- Apellido
- Teléfono
- Servicio
- Fecha
- Horario

Botón principal:

Confirmar Reserva

---

# Dashboard

Tarjetas superiores:

- Turnos Hoy
- Próximo Turno
- Servicios

Debajo:

Timeline de agenda.

---

# Agenda

Timeline vertical inspirado en Google Calendar.

Cada turno se representa mediante una tarjeta.

Información:

- Hora
- Cliente
- Servicio
- Teléfono

Acciones:

- Confirmar
- Cancelar

---

# Servicios

Vista mediante cards.

Cada card muestra:

- Nombre
- Duración
- Precio

Acciones:

- Editar
- Eliminar

---

# Clientes

No existe módulo principal de clientes.

Los clientes se administran desde los turnos.

La entidad sigue existiendo en la base de datos.

---

# Login

Estilo SaaS moderno.

Elementos:

- Logo
- Usuario
- Contraseña
- Botón Ingresar

Diseño centrado.

---

# Formularios

## Mobile

Una columna.

## Desktop

Dos columnas.

---

# Botones

Estilo outline.

Color principal naranja.

Hover con fondo naranja y texto blanco.

---

# Dark Mode

Debe existir soporte completo para:

- Light Mode
- Dark Mode

---

# Responsive

## Mobile
0-767px

## Tablet
768-1023px

## Desktop
1024px+

---

# UX Goals

- Reservar un turno en menos de 60 segundos.
- Encontrar el próximo turno en menos de 5 segundos.
- Gestionar la agenda diaria desde una única pantalla.
