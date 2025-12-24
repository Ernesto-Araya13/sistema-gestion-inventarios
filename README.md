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
   - Copiar `config/database.py.example` a `config/database.py`
   - Editar `config/database.py` con tus credenciales de MySQL
   - La base de datos está alojada en **Aiven Cloud** (requiere conexión a Internet)
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

La aplicación requiere una base de datos MySQL con las siguientes tablas (ya configuradas en la nube):

- `rol` - Roles de usuario
- `usuario` - Usuarios del sistema
- `categoria` - Categorías de productos
- `producto` - Productos del inventario
- `movimiento` - Registro de entradas y salidas

**Importante:** 
- Las tablas deben usar nomenclatura **snake_case** para los nombres de columnas
- La base de datos está alojada en **Aiven Cloud** (requiere conexión a Internet)
- No se requiere MySQL instalado localmente

Ver [INSTALACION.md](INSTALACION.md) para la estructura completa de las tablas y detalles de conexión.

## Configuración

### Base de Datos

La base de datos está alojada en **Aiven Cloud**. Para configurar la conexión:

1. Copiar el archivo de ejemplo:
   ```bash
   cp config/database.py.example config/database.py
   ```

2. Editar `config/database.py` con tus credenciales:

```python
DB_CONFIG = {
    'host': 'mysql-xxx.i.aivencloud.com',  # Host de Aiven Cloud
    'database': 'db_escritorio',
    'user': 'avnadmin',  # Usuario de Aiven
    'password': 'tu_password',  # Contraseña (contactar a Ernesto)
    'port': 20259,  # Puerto personalizado de Aiven
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

**Nota:** Para obtener las credenciales de acceso, contactar a Ernesto.

### Usuario por Defecto

Para iniciar sesión, necesitas crear un usuario administrador en la base de datos:

```sql
INSERT INTO usuario (nombre_usuario, email, password, id_rol) 
VALUES ('Administrador', 'admin@empresa.com', 'admin123', 1);
```

- **Email:** admin@empresa.com
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
- Verificar conexión a Internet (la BD está en la nube)
- Verificar credenciales en `config/database.py`
- Verificar que el host y puerto sean correctos
- Verificar firewall (puerto 20259 debe estar abierto)

### Error de columnas desconocidas
- Verificar que las tablas usen snake_case
- Ver estructura esperada en INSTALACION.md

### Error de timeout o acceso denegado
- Verificar que las credenciales sean correctas
- Contactar a Ernesto para obtener/verificar credenciales
- Verificar estado del servicio en Aiven Cloud

Para más detalles, consulta [INSTALACION.md](INSTALACION.md)

## Desarrollo

Este proyecto sigue metodología Ágil Scrum con desarrollo incremental por sprints.

### Tecnologías Utilizadas

- **Python 3.8+**
- **Flet** - Framework de interfaz gráfica
- **MySQL** - Base de datos relacional (alojada en Aiven Cloud)
- **mysql-connector-python** - Conector MySQL para Python

### Infraestructura

- **Base de datos:** Aiven Cloud (MySQL en la nube)
- **Hosting:** Base de datos remota, disponible 24/7
- **Conexión:** Requiere conexión a Internet

## Licencia

Proyecto académico - Sistema de Gestión de Inventarios
