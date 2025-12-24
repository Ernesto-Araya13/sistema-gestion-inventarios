"""
Utilidades de validación
Funciones reutilizables para validar datos de entrada
"""

import re
from datetime import datetime


def validate_email(email):
    """
    Valida formato de email
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password, min_length=6):
    """
    Valida que la contraseña tenga longitud mínima
    
    Args:
        password (str): Contraseña a validar
        min_length (int): Longitud mínima requerida
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    return len(password) >= min_length


def validate_required(value, field_name="Campo"):
    """
    Valida que un campo no esté vacío
    
    Args:
        value: Valor a validar
        field_name (str): Nombre del campo para mensaje de error
        
    Returns:
        tuple: (bool, str) - (True, "") si es válido, (False, mensaje) si no
    """
    if not value or (isinstance(value, str) and value.strip() == ""):
        return False, f"{field_name} es requerido"
    return True, ""


def validate_number(value, field_name="Campo", min_value=None, max_value=None):
    """
    Valida que un valor sea numérico y esté en rango
    
    Args:
        value: Valor a validar
        field_name (str): Nombre del campo
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
        
    Returns:
        tuple: (bool, str) - (True, "") si es válido, (False, mensaje) si no
    """
    try:
        num_value = float(value)
        if min_value is not None and num_value < min_value:
            return False, f"{field_name} debe ser mayor o igual a {min_value}"
        if max_value is not None and num_value > max_value:
            return False, f"{field_name} debe ser menor o igual a {max_value}"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} debe ser un número válido"


def validate_integer(value, field_name="Campo", min_value=None, max_value=None):
    """
    Valida que un valor sea entero y esté en rango
    
    Args:
        value: Valor a validar
        field_name (str): Nombre del campo
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
        
    Returns:
        tuple: (bool, str) - (True, "") si es válido, (False, mensaje) si no
    """
    try:
        int_value = int(value)
        if min_value is not None and int_value < min_value:
            return False, f"{field_name} debe ser mayor o igual a {min_value}"
        if max_value is not None and int_value > max_value:
            return False, f"{field_name} debe ser menor o igual a {max_value}"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} debe ser un número entero válido"


def validate_date(date_string, field_name="Fecha"):
    """
    Valida formato de fecha
    
    Args:
        date_string (str): Fecha en formato string
        field_name (str): Nombre del campo
        
    Returns:
        tuple: (bool, str) - (True, "") si es válido, (False, mensaje) si no
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} debe tener formato YYYY-MM-DD"

