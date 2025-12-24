"""
Capa de Datos - Operaciones CRUD con MySQL
Maneja todas las interacciones directas con la base de datos
"""

from config.database import get_connection
from mysql.connector import Error
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Gestor de operaciones de base de datos"""
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict]]:
        """
        Ejecuta una consulta SQL genérica
        
        Args:
            query (str): Consulta SQL
            params (tuple): Parámetros para la consulta
            fetch (bool): Si debe retornar resultados
            
        Returns:
            List[Dict] o None: Resultados de la consulta
        """
        connection = None
        try:
            connection = get_connection()
            if not connection:
                return None
                
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                results = cursor.fetchall()
                cursor.close()
                connection.close()
                return results
            else:
                connection.commit()
                cursor.close()
                connection.close()
                return []
                
        except Error as e:
            print(f"Error ejecutando consulta: {e}")
            if connection:
                connection.rollback()
                connection.close()
            return None


class UsuarioDAO:
    """Data Access Object para operaciones de Usuario"""
    
    @staticmethod
    def login(email: str, password: str) -> Optional[Dict]:
        """
        Autentica un usuario
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña
            
        Returns:
            Dict o None: Datos del usuario si la autenticación es exitosa
        """
        query = """
            SELECT u.id_usuario, u.nombre_usuario, u.email, u.id_rol, r.nombre_rol
            FROM usuario u
            INNER JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.email = %s AND u.password = %s AND u.activo = TRUE
        """
        results = DatabaseManager.execute_query(query, (email, password))
        return results[0] if results and len(results) > 0 else None
    
    @staticmethod
    def get_by_id(id_usuario: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        query = "SELECT * FROM usuario WHERE id_usuario = %s"
        results = DatabaseManager.execute_query(query, (id_usuario,))
        return results[0] if results and len(results) > 0 else None


class ProductoDAO:
    """Data Access Object para operaciones de Producto"""
    
    @staticmethod
    def create(codigo: str, nombre: str, descripcion: str, id_categoria: int,
               precio: float, stock_minimo: int, unidad_medida: str) -> bool:
        """
        Crea un nuevo producto
        
        Returns:
            bool: True si se creó exitosamente
        """
        query = """
            INSERT INTO producto (codigo_producto, nombre_producto, descripcion, 
                                id_categoria, precio_unitario, stock_minimo, unidad_medida)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        result = DatabaseManager.execute_query(
            query, 
            (codigo, nombre, descripcion, id_categoria, precio, stock_minimo, unidad_medida),
            fetch=False
        )
        return result is not None
    
    @staticmethod
    def get_all(activo: bool = True) -> List[Dict]:
        """
        Obtiene todos los productos
        
        Args:
            activo (bool): Si True, solo productos activos
            
        Returns:
            List[Dict]: Lista de productos
        """
        if activo:
            query = """
                SELECT p.*, c.nombre_categoria
                FROM producto p
                LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
                WHERE p.activo = TRUE
                ORDER BY p.nombre_producto
            """
        else:
            query = """
                SELECT p.*, c.nombre_categoria
                FROM producto p
                LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
                ORDER BY p.nombre_producto
            """
        results = DatabaseManager.execute_query(query)
        return results if results else []
    
    @staticmethod
    def get_by_id(id_producto: int) -> Optional[Dict]:
        """Obtiene un producto por ID"""
        query = """
            SELECT p.*, c.nombre_categoria
            FROM producto p
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            WHERE p.id_producto = %s
        """
        results = DatabaseManager.execute_query(query, (id_producto,))
        return results[0] if results and len(results) > 0 else None
    
    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Dict]:
        """Obtiene un producto por código"""
        query = """
            SELECT p.*, c.nombre_categoria
            FROM producto p
            LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
            WHERE p.codigo_producto = %s
        """
        results = DatabaseManager.execute_query(query, (codigo,))
        return results[0] if results and len(results) > 0 else None
    
    @staticmethod
    def update(id_producto: int, nombre: str, descripcion: str, id_categoria: int,
               precio: float, stock_minimo: int, unidad_medida: str) -> bool:
        """
        Actualiza un producto existente
        
        Returns:
            bool: True si se actualizó exitosamente
        """
        query = """
            UPDATE producto 
            SET nombre_producto = %s, descripcion = %s, id_categoria = %s,
                precio_unitario = %s, stock_minimo = %s, unidad_medida = %s
            WHERE id_producto = %s
        """
        result = DatabaseManager.execute_query(
            query,
            (nombre, descripcion, id_categoria, precio, stock_minimo, unidad_medida, id_producto),
            fetch=False
        )
        return result is not None
    
    @staticmethod
    def delete(id_producto: int) -> bool:
        """
        Elimina (desactiva) un producto
        
        Returns:
            bool: True si se eliminó exitosamente
        """
        query = "UPDATE producto SET activo = FALSE WHERE id_producto = %s"
        result = DatabaseManager.execute_query(query, (id_producto,), fetch=False)
        return result is not None
    
    @staticmethod
    def update_stock(id_producto: int, cantidad: int) -> bool:
        """
        Actualiza el stock de un producto
        
        Args:
            id_producto (int): ID del producto
            cantidad (int): Cantidad a sumar (puede ser negativa)
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        query = "UPDATE producto SET stock_actual = stock_actual + %s WHERE id_producto = %s"
        result = DatabaseManager.execute_query(query, (cantidad, id_producto), fetch=False)
        return result is not None


class CategoriaDAO:
    """Data Access Object para operaciones de Categoría"""
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Obtiene todas las categorías"""
        query = "SELECT * FROM categoria ORDER BY nombre_categoria"
        results = DatabaseManager.execute_query(query)
        return results if results else []
