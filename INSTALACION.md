# Guía de Instalación - Sistema de Gestión de Inventarios

## Requisitos Previos

1. **Python 3.8 o superior**
   - Verificar instalación: `python --version`
   - Descargar desde: https://www.python.org/downloads/

2. **Conexión a Internet**
   - La base de datos está alojada en la nube (Aiven Cloud)
   - Se requiere conexión a Internet para acceder a la base de datos

3. **MySQL Workbench (Opcional pero recomendado)**
   - Para gestionar la base de datos visualmente
   - Descargar desde: https://dev.mysql.com/downloads/workbench/
   - Permite conectarse a la base de datos en la nube

## Pasos de Instalación

### 1. Clonar o descargar el proyecto

```bash
cd Proyecto_Final
```

### 2. Crear entorno virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar conexión a la base de datos

La base de datos está configurada para conectarse a **Aiven Cloud**. El archivo `config/database.py` contiene la configuración actual:

```python
DB_CONFIG = {
    'host': 'mysql-5f02b23-ernestoaraya908-e622.i.aivencloud.com',
    'database': 'db_escritorio',
    'user': 'avnadmin',
    'password': '',  # Privada. Pedir a Ernesto.
    'port': 20259,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

**Configuración actual:**
- **Host:** Servidor MySQL en Aiven Cloud
- **Base de datos:** `db_escritorio`
- **Usuario:** `avnadmin`
- **Puerto:** `20259` (puerto personalizado de Aiven)
- **Contraseña:** Contactar a Ernesto para obtener la contraseña

**Nota importante:** 
- La base de datos `db_escritorio` ya está creada y configurada en la nube
- Si necesitas la contraseña, contacta a Ernesto
- La conexión es remota, no requiere MySQL instalado localmente

### 5. Verificar estructura de la base de datos

La aplicación requiere las siguientes tablas con la estructura correcta (ya configuradas en la nube):

- **rol**: Roles de usuario (Administrador, Operador, Consulta)
  - Columnas: `id_rol`, `nombre_rol`, `descripcion`, `fecha_creacion`
  
- **usuario**: Usuarios del sistema
  - Columnas: `id_usuario`, `nombre_usuario`, `email`, `password`, `id_rol`, `activo`, `fecha_creacion`, `fecha_ultimo_acceso`
  
- **categoria**: Categorías de productos
  - Columnas: `id_categoria`, `nombre_categoria`, `descripcion`, `fecha_creacion`
  
- **producto**: Productos del inventario
  - Columnas: `id_producto`, `codigo_producto`, `nombre_producto`, `descripcion`, `id_categoria`, `precio_unitario`, `stock_actual`, `stock_minimo`, `unidad_medida`, `activo`, `fecha_creacion`, `fecha_actualizacion`
  
- **movimiento**: Registro de entradas y salidas
  - Columnas: `id_movimiento`, `id_producto`, `tipo_movimiento`, `cantidad`, `precio_unitario`, `motivo`, `id_usuario`, `fecha_movimiento`, `observaciones`

**Importante:** Las tablas deben usar nomenclatura **snake_case** (guiones bajos) para los nombres de columnas.

### 6. Verificar datos iniciales

Asegúrate de tener al menos:

- **Roles:** Administrador, Operador, Consulta
- **Categoría por defecto:** General
- **Usuario administrador:**
  - Email: `admin@empresa.com`
  - Contraseña: `admin123`
  - Rol: Administrador

Si no tienes estos datos, puedes crearlos manualmente conectándote a la base de datos en la nube.

### 7. Probar la conexión

Ejecutar el script de prueba:

```bash
python test_connection.py
```

O desde Python:

```python
from config.database import test_connection
test_connection()
```

**Si la conexión es exitosa**, verás el mensaje: "Conexión a MySQL exitosa"

### 8. Ejecutar la aplicación

```bash
python main.py
```

## Solución de Problemas

### Error: "No se pudo conectar a MySQL"

1. **Verificar conexión a Internet:**
   - La base de datos está en la nube, requiere conexión a Internet
   - Verificar que no haya firewall bloqueando el puerto 20259

2. **Verificar credenciales en `config/database.py`:**
   - Host correcto: `mysql-5f02b23-ernestoaraya908-e622.i.aivencloud.com`
   - Usuario correcto: `avnadmin`
   - Contraseña correcta (contactar a Ernesto si no la tienes)
   - Puerto correcto: `20259`

3. **Verificar que la base de datos exista en la nube:**
   - La base de datos `db_escritorio` debe estar activa en Aiven Cloud
   - Contactar al administrador si hay problemas de acceso

4. **Verificar que las tablas se hayan creado:**
   - Conectarse a la base de datos usando MySQL Workbench o cliente similar
   - Ejecutar: `SHOW TABLES;`
   - Deben aparecer: `rol`, `usuario`, `categoria`, `producto`, `movimiento`

5. **Verificar estructura de columnas:**
   ```sql
   DESCRIBE usuario;
   ```
   Las columnas deben usar snake_case (ej: `id_usuario`, `nombre_usuario`, `email`, `password`)

### Error: "Unknown column 'u.id_usuario' in 'field list'"

Este error indica que las tablas tienen una estructura diferente (probablemente camelCase). 

**Solución:**
- Verifica que las columnas usen snake_case
- Si las tablas tienen estructura camelCase (`idusuario`, `nombreUsuario`, etc.), necesitarás:
  1. Modificar la estructura de las tablas para usar snake_case, o
  2. Actualizar el código en `data/database.py` para usar los nombres de columnas correctos

### Error: "ModuleNotFoundError"

Asegurarse de que todas las dependencias estén instaladas:
```bash
pip install -r requirements.txt
```

### Error: "Access denied for user" o "Connection timeout"

1. **Verificar credenciales:**
   - Usuario y contraseña correctos
   - La contraseña puede haber cambiado, contactar a Ernesto

2. **Verificar conectividad de red:**
   - Firewall corporativo puede estar bloqueando el puerto
   - Verificar que el puerto 20259 esté abierto

3. **Verificar estado del servicio en Aiven:**
   - El servicio puede estar temporalmente no disponible
   - Contactar al administrador de Aiven Cloud

### Error: "Can't connect to MySQL server"

1. **Verificar que el host sea correcto:**
   - Host: `mysql-5f02b23-ernestoaraya908-e622.i.aivencloud.com`
   - No debe tener espacios o caracteres extra

2. **Verificar el puerto:**
   - Puerto: `20259` (no el puerto estándar 3306)
   - Aiven Cloud usa puertos personalizados

3. **Verificar DNS:**
   - El hostname debe resolverse correctamente
   - Probar hacer ping al hostname

## Estructura de la Base de Datos

La aplicación espera las siguientes tablas con estructura específica (ya configuradas en la nube):

### Tabla: rol
- `id_rol` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `nombre_rol` (VARCHAR(50), UNIQUE)
- `descripcion` (TEXT)
- `fecha_creacion` (TIMESTAMP)

### Tabla: usuario
- `id_usuario` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `nombre_usuario` (VARCHAR(100))
- `email` (VARCHAR(100), UNIQUE)
- `password` (VARCHAR(255))
- `id_rol` (INT, FOREIGN KEY → rol.id_rol)
- `activo` (BOOLEAN, DEFAULT TRUE)
- `fecha_creacion` (TIMESTAMP)
- `fecha_ultimo_acceso` (TIMESTAMP, NULL)

### Tabla: categoria
- `id_categoria` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `nombre_categoria` (VARCHAR(100), UNIQUE)
- `descripcion` (TEXT)
- `fecha_creacion` (TIMESTAMP)

### Tabla: producto
- `id_producto` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `codigo_producto` (VARCHAR(50), UNIQUE)
- `nombre_producto` (VARCHAR(200))
- `descripcion` (TEXT)
- `id_categoria` (INT, FOREIGN KEY → categoria.id_categoria)
- `precio_unitario` (DECIMAL(10,2))
- `stock_actual` (INT, DEFAULT 0)
- `stock_minimo` (INT, DEFAULT 0)
- `unidad_medida` (VARCHAR(20), DEFAULT 'UNIDAD')
- `activo` (BOOLEAN, DEFAULT TRUE)
- `fecha_creacion` (TIMESTAMP)
- `fecha_actualizacion` (TIMESTAMP)

### Tabla: movimiento
- `id_movimiento` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `id_producto` (INT, FOREIGN KEY → producto.id_producto)
- `tipo_movimiento` (ENUM('ENTRADA', 'SALIDA'))
- `cantidad` (INT)
- `precio_unitario` (DECIMAL(10,2))
- `motivo` (VARCHAR(200))
- `id_usuario` (INT, FOREIGN KEY → usuario.id_usuario)
- `fecha_movimiento` (TIMESTAMP)
- `observaciones` (TEXT)

## Usuario por Defecto

Para poder iniciar sesión, necesitas crear un usuario administrador en la base de datos:

```sql
INSERT INTO usuario (nombre_usuario, email, password, id_rol) 
VALUES ('Administrador', 'admin@empresa.com', 'admin123', 1);
```

- **Email:** admin@empresa.com
- **Contraseña:** admin123
- **Rol:** Administrador (id_rol = 1)

⚠️ **IMPORTANTE:** Cambiar la contraseña del administrador en producción. En producción, usar hash seguro (bcrypt, argon2, etc.) para las contraseñas.

## Conectarse a la Base de Datos desde MySQL Workbench

Para gestionar la base de datos visualmente:

1. Abrir MySQL Workbench
2. Crear nueva conexión:
   - **Connection Name:** Aiven Cloud - db_escritorio
   - **Hostname:** `mysql-5f02b23-ernestoaraya908-e622.i.aivencloud.com`
   - **Port:** `20259`
   - **Username:** `avnadmin`
   - **Password:** (solicitar a Ernesto)
3. Hacer clic en "Test Connection" para verificar
4. Si es exitoso, hacer clic en "OK" y conectar

## Próximos Pasos

Una vez instalado y funcionando:

1. Iniciar sesión con el usuario administrador
2. Crear productos de prueba
3. Explorar las funcionalidades del MVP
4. Preparar para los siguientes sprints (inventario, reportes, etc.)

## Notas Adicionales

- **Base de datos en la nube:** La base de datos está alojada en Aiven Cloud, no requiere MySQL local
- **Conexión remota:** Se requiere conexión a Internet para acceder a la base de datos
- **Seguridad:** La contraseña de la base de datos es privada, contactar a Ernesto para obtenerla
- **Estructura:** La aplicación está diseñada para trabajar con estructura snake_case
- **Backup:** Se recomienda hacer respaldo regular de la base de datos en la nube
- **Disponibilidad:** La base de datos está disponible 24/7 desde cualquier ubicación con Internet

## Información de Contacto

Para obtener la contraseña de la base de datos o resolver problemas de acceso:
- **Contactar a:** Ernesto
- **Base de datos:** db_escritorio en Aiven Cloud
