"""
Capa de Lógica de Negocio - Productos
Maneja la lógica de negocio para gestión de productos
"""

from data.database import ProductoDAO, CategoriaDAO
from utils.validators import (
    validate_required, validate_number, validate_integer
)


class ProductService:
    """Servicio de gestión de productos"""
    
    @staticmethod
    def create_product(codigo: str, nombre: str, descripcion: str, 
                      id_categoria: int, precio: float, stock_minimo: int,
                      unidad_medida: str) -> tuple:
        """
        Crea un nuevo producto con validaciones
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validaciones
        is_valid, msg = validate_required(codigo, "Código")
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_required(nombre, "Nombre")
        if not is_valid:
            return False, msg
        
        # Verificar que el código no exista
        producto_existente = ProductoDAO.get_by_codigo(codigo)
        if producto_existente:
            return False, f"Ya existe un producto con el código {codigo}"
        
        # Validar precio
        is_valid, msg = validate_number(precio, "Precio", min_value=0)
        if not is_valid:
            return False, msg
        
        # Validar stock mínimo
        is_valid, msg = validate_integer(stock_minimo, "Stock mínimo", min_value=0)
        if not is_valid:
            return False, msg
        
        # Validar unidad de medida
        if not unidad_medida or unidad_medida.strip() == "":
            unidad_medida = "UNIDAD"
        
        # Si no hay categoría, usar la categoría por defecto (id=1)
        if not id_categoria or id_categoria <= 0:
            id_categoria = 1
        
        # Crear producto
        success = ProductoDAO.create(
            codigo, nombre, descripcion, id_categoria,
            precio, stock_minimo, unidad_medida
        )
        
        if success:
            return True, "Producto creado exitosamente"
        else:
            return False, "Error al crear el producto"
    
    @staticmethod
    def get_all_products(activo: bool = True) -> list:
        """
        Obtiene todos los productos
        
        Args:
            activo (bool): Si True, solo productos activos
            
        Returns:
            list: Lista de productos
        """
        return ProductoDAO.get_all(activo)
    
    @staticmethod
    def get_product_by_id(id_producto: int) -> dict:
        """
        Obtiene un producto por ID
        
        Args:
            id_producto (int): ID del producto
            
        Returns:
            dict: Datos del producto o None
        """
        return ProductoDAO.get_by_id(id_producto)
    
    @staticmethod
    def update_product(id_producto: int, nombre: str, descripcion: str,
                      id_categoria: int, precio: float, stock_minimo: int,
                      unidad_medida: str) -> tuple:
        """
        Actualiza un producto existente
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validaciones similares a create
        is_valid, msg = validate_required(nombre, "Nombre")
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_number(precio, "Precio", min_value=0)
        if not is_valid:
            return False, msg
        
        is_valid, msg = validate_integer(stock_minimo, "Stock mínimo", min_value=0)
        if not is_valid:
            return False, msg
        
        if not unidad_medida or unidad_medida.strip() == "":
            unidad_medida = "UNIDAD"
        
        if not id_categoria or id_categoria <= 0:
            id_categoria = 1
        
        success = ProductoDAO.update(
            id_producto, nombre, descripcion, id_categoria,
            precio, stock_minimo, unidad_medida
        )
        
        if success:
            return True, "Producto actualizado exitosamente"
        else:
            return False, "Error al actualizar el producto"
    
    @staticmethod
    def delete_product(id_producto: int) -> tuple:
        """
        Elimina (desactiva) un producto
        
        Returns:
            tuple: (success: bool, message: str)
        """
        success = ProductoDAO.delete(id_producto)
        
        if success:
            return True, "Producto eliminado exitosamente"
        else:
            return False, "Error al eliminar el producto"
    
    @staticmethod
    def get_categories() -> list:
        """
        Obtiene todas las categorías
        
        Returns:
            list: Lista de categorías
        """
        return CategoriaDAO.get_all()

