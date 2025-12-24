"""
Script de prueba de conexión a la base de datos
Ayuda a diagnosticar problemas de conexión
"""

from config.database import get_connection, DB_CONFIG
import mysql.connector
from mysql.connector import Error

def test_detailed_connection():
    """Prueba la conexión con información detallada"""
    print("=" * 50)
    print("PRUEBA DE CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    print(f"\nConfiguración actual:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Puerto: {DB_CONFIG['port']}")
    print(f"  Base de datos: {DB_CONFIG['database']}")
    print(f"  Usuario: {DB_CONFIG['user']}")
    print(f"  Contraseña: {'***' if DB_CONFIG['password'] else '(vacía)'}")
    print("\n" + "-" * 50)
    
    # Intentar conexión sin especificar base de datos primero
    print("\n1. Probando conexión al servidor MySQL...")
    try:
        config_test = DB_CONFIG.copy()
        config_test.pop('database')  # Quitar base de datos para probar servidor
        connection = mysql.connector.connect(**config_test)
        if connection.is_connected():
            print("   ✓ Conexión al servidor MySQL exitosa")
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            print(f"   Bases de datos disponibles: {', '.join(databases)}")
            
            if DB_CONFIG['database'] in databases:
                print(f"   ✓ La base de datos '{DB_CONFIG['database']}' existe")
            else:
                print(f"   ✗ La base de datos '{DB_CONFIG['database']}' NO existe")
                print(f"   Bases de datos encontradas: {', '.join(databases)}")
            
            cursor.close()
            connection.close()
        else:
            print("   ✗ No se pudo conectar al servidor")
    except Error as e:
        print(f"   ✗ Error: {e}")
        print("\n   Posibles soluciones:")
        print("   - Verificar que MySQL esté ejecutándose")
        print("   - Verificar el puerto (por defecto 3306)")
        print("   - Verificar usuario y contraseña en config/database.py")
        return False
    
    # Intentar conexión con la base de datos
    print("\n2. Probando conexión a la base de datos específica...")
    connection = get_connection()
    if connection:
        print(f"   ✓ Conexión a '{DB_CONFIG['database']}' exitosa")
        
        # Verificar tablas
        print("\n3. Verificando tablas en la base de datos...")
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            if tables:
                print(f"   ✓ Tablas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"     - {table}")
            else:
                print("   ⚠ No se encontraron tablas en la base de datos")
                print("   Debe ejecutar el script database/schema.sql")
            cursor.close()
        except Error as e:
            print(f"   ✗ Error al verificar tablas: {e}")
        
        connection.close()
        print("\n" + "=" * 50)
        print("✓ CONEXIÓN EXITOSA - La aplicación debería funcionar")
        print("=" * 50)
        return True
    else:
        print(f"   ✗ No se pudo conectar a '{DB_CONFIG['database']}'")
        print("\n" + "=" * 50)
        print("✗ CONEXIÓN FALLIDA")
        print("=" * 50)
        return False

if __name__ == "__main__":
    test_detailed_connection()

