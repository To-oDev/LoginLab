# 🧪 Login Lab

**Login Lab** es un entorno de práctica para explorar cómo funcionan los sistemas de inicio de sesión en aplicaciones web.  
No es un producto final, sino un **playground de autenticación**: un espacio seguro para aprender, probar y romper sin consecuencias...

## 🎯 Objetivo
- Comprender los conceptos básicos de **login y autenticación**.  
- Practicar el manejo de sesiones, cookies y tokens.  
- Experimentar con opciones como **“Remember me”** y **aceptación de términos**.  
- Servir como base para integrar funciones más avanzadas (registro, roles, OAuth, etc.).  

## 🧩 Qué incluye
- Un **formulario de login y registro simple** con email y contraseña.
- Checkbox de **“Remember me”** para sesiones extendidas .
- Endpoint de **registro** con aceptación de términos y condiciones.
- API backend con rutas `/login` y `/register`.

## 🧰 Tecnologías

**Frontend**
- React 19.1.1  

**Backend**
- Python + FastAPI  
- Passlib + JWT  

**Base de datos**
- PostgreSQL + asyncpg  

## 🚀 Instalación

1. Instalación de PostgreSQL

    Para que Login Lab pueda almacenar usuarios y sesiones, necesitas tener instalado **PostgreSQL** en tu sistema.

    #### Windows
    1. Descarga el instalador desde [postgresql.org/download](https://www.postgresql.org/download/windows/).
    2. Durante la instalación, asegúrate de recordar:
        - El **usuario administrador** (por defecto `postgres`).
        - La **contraseña** que definas (por defecto el proyecto se conecta con 1234).
        - El **puerto** (5432 por defecto).
        
2. Crea la base de datos y tablas necesarias.

Abre una terminal y conectate con tu usuario a PostgreSQL:

````cmd
# -U, --username=USUARIO  nombre usuario de la base de datos
C:\> psql -U postgres
````

````sql
-- -------------------------
-- 2.1. Crear base de datos
-- -------------------------
CREATE DATABASE login_lab;

-- -------------------------
-- 2.2. Conectarse a la base de datos
-- -------------------------
\c login_lab;

-- -------------------------
-- 2.3. Crear tabla de usuarios
-- -------------------------
-- Activa la extensión uuid-ossp para utilizar UUID como tipo de dato automatico del atributo id. (solo una vez por base de datos)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla con atributo id como uuid automatico
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
-- 💡 UUID: Universally Unique Identifier. Es una cadena (normalmente de 36 caracteres, incluyendo guiones) que sirve para identificar algo de manera prácticamente única en todo el mundo, sin necesidad de un servidor central que las asigne.

--------------------------------------------------------------------------
-- OPCIONAL/NO NECESARIO
-- crear tabla con tipo de id estandar (requiere configuración de tipos en server para su tratamiento)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
--------------------------------------------------------------------------

-- -------------------------
-- 2.4. Crear índices (mejora búsqueda)
-- -------------------------
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- -------------------------
-- 2.5. Tabla para tokens (para su gestión)
-- -------------------------
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- -------------------------
-- 2.6. Consultas de prueba
-- -------------------------
-- Insertar usuario de prueba
INSERT INTO users (username, email, hashed_password)
VALUES ('testuser', 'test@example.com', 'hashed_password_demo');

-- Ver usuarios
SELECT * FROM users;
````

3. Clona este repositorio:
```bash
git clone git@github.com:To-oDev/LoginLab.git
# git clone https://github.com/To-oDev/LoginLab.git
```

4. Instala dependencias

```bash
# client
cd client
npm install

# server
cd server
# crea y carga un entorno virtual
python -m venv venv
venv/Scripts/activate
# instala dependencias listadas en requirements.txt
pip install -r requirements.txt
```

5. Inicia servidores de desarrollo

```bash
# (venv) LOGINLAB/server>
uvicorn app.main:app --reload

# client>
npm start
```
## 🧪 Prueba de autenticación

- Abre el frontend en tu navegador.

- Intenta iniciar sesión (no uses cuentas de Google).

- Si no estás registrado, el servidor negará el acceso.

- Regístrate con un correo y contraseña ficticios, y acepta los términos.

- Vuelve a iniciar sesión. El servidor devolverá un token JWT que se guardará en el LocalStorage.

## ⚠️ Importante

Este proyecto es con fines autodidactas. No usar directamente en producción.

Las contraseñas se encriptan con passlib.hash (pbkdf2_sha256).

Actualmente, no existe redirección tras iniciar sesión; la sesión puede validarse revisando el token en el LocalStorage (TODO: implementar redirección o pantalla de usuario autenticado).

## 💬 Próximos pasos

- Implementar refresh tokens.
- Añadir roles y permisos.
- Conectar OAuth (Google, GitHub, etc.).
- Crear interfaz de usuario autenticada.