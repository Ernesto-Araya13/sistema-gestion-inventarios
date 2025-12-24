# Sistema de Gestión de Inventarios

Aplicación de escritorio para la gestión de inventarios de bodegas, orientada a pequeñas y medianas empresas.

## Stack Tecnológico

- **Lenguaje**: Python 3
- **Framework UI**: Flet
- **Base de Datos**: MySQL
- **Arquitectura**: 3 capas (Presentación, Lógica de Negocio, Datos)

## Estructura del Proyecto

```
Proyecto_Final/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── test_connection.py      # Script de prueba de conexión
├── config/                # Configuración
│   └── database.py        # Configuración de conexión a BD
├── data/                  # Capa de Datos
│   └── database.py        # Operaciones CRUD con MySQL
├── business/              # Capa de Lógica de Negocio
│   ├── auth_logic.py      # Lógica de autenticación
│   └── product_logic.py   # Lógica de productos
├── presentation/          # Capa de Presentación (Flet)
│   ├── login_page.py      # Pantalla de login
│   └── product_page.py    # Pantalla de gestión de productos
└── utils/                 # Utilidades
    └── validators.py      # Validaciones reutilizables
```

## Instalación Rápida

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar conexión a la base de datos:**
   - Editar `config/database.py` con tus credenciales de MySQL
   - Asegúrate de que la base de datos `dbappescritorio` exista
   - Verifica que las tablas tengan la estructura correcta (ver INSTALACION.md)

3. **Probar la conexión:**
```bash
python test_connection.py
```

4. **Ejecutar la aplicación:**
```bash
python main.py
```

Para instrucciones detalladas, consulta [INSTALACION.md](INSTALACION.md)

## Requisitos de Base de Datos

La aplicación requiere una base de datos MySQL con las siguientes tablas:

- `rol` - Roles de usuario
- `usuario` - Usuarios del sistema
- `categoria` - Categorías de productos
- `producto` - Productos del inventario
- `movimiento` - Registro de entradas y salidas

**Importante:** Las tablas deben usar nomenclatura **snake_case** para los nombres de columnas.

Ver [INSTALACION.md](INSTALACION.md) para la estructura completa de las tablas.

## Configuración

### Base de Datos

Editar `config/database.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'dbappescritorio',
    'user': 'root',
    'password': 'tu_password',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### Usuario por Defecto

Para iniciar sesión, necesitas crear un usuario administrador en la base de datos:

```sql
INSERT INTO usuario (nombre_usuario, email, password, id_rol) 
VALUES ('Administrador', 'admin@inventario.com', 'admin123', 1);
```

- **Email:** admin@inventario.com
- **Contraseña:** admin123

## Funcionalidades MVP

- ✅ Autenticación de usuarios (login)
- ✅ Gestión de productos (CRUD)
  - Crear productos
  - Listar productos
  - Actualizar productos
  - Eliminar (desactivar) productos
- ✅ Validaciones de datos
- ✅ Control básico de inventario

## Próximos Sprints

- Control de inventario (entradas y salidas)
- Actualización automática de stock
- Generación de reportes
  - Stock actual
  - Movimientos por fecha
  - Alertas de stock mínimo
- Gestión de roles y permisos
- Dashboard con estadísticas

## Arquitectura

El proyecto sigue una arquitectura de 3 capas:

1. **Capa de Presentación** (`presentation/`)
   - Interfaz de usuario con Flet
   - Formularios y tablas

2. **Capa de Lógica de Negocio** (`business/`)
   - Validaciones
   - Reglas de negocio
   - Control de flujo

3. **Capa de Datos** (`data/`)
   - Operaciones CRUD con MySQL
   - Data Access Objects (DAOs)

## Solución de Problemas

### Error de conexión a MySQL
- Verificar que MySQL esté ejecutándose
- Verificar credenciales en `config/database.py`
- Verificar que la base de datos exista

### Error de columnas desconocidas
- Verificar que las tablas usen snake_case
- Ver estructura esperada en INSTALACION.md

Para más detalles, consulta [INSTALACION.md](INSTALACION.md)

## Desarrollo

Este proyecto sigue metodología Ágil Scrum con desarrollo incremental por sprints.

### Tecnologías Utilizadas

- **Python 3.8+**
- **Flet** - Framework de interfaz gráfica
- **MySQL** - Base de datos relacional
- **mysql-connector-python** - Conector MySQL para Python

## Licencia

Proyecto académico - Sistema de Gestión de Inventarios
