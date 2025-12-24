"""
Capa de Lógica de Negocio - Autenticación
Maneja la lógica de autenticación y validación de usuarios
"""

from data.database import UsuarioDAO
from utils.validators import validate_email, validate_password, validate_required


class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def login(email: str, password: str) -> tuple:
        """
        Autentica un usuario
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña
            
        Returns:
            tuple: (success: bool, message: str, user_data: dict or None)
        """
        # Validaciones
        is_valid, msg = validate_required(email, "Email")
        if not is_valid:
            return False, msg, None
        
        is_valid, msg = validate_required(password, "Contraseña")
        if not is_valid:
            return False, msg, None
        
        if not validate_email(email):
            return False, "El formato del email no es válido", None
        
        # Intentar autenticación
        usuario = UsuarioDAO.login(email, password)
        
        if usuario:
            return True, "Login exitoso", usuario
        else:
            return False, "Email o contraseña incorrectos", None
    
    @staticmethod
    def get_user_info(user_id: int) -> dict:
        """
        Obtiene información de un usuario
        
        Args:
            user_id (int): ID del usuario
            
        Returns:
            dict: Información del usuario o None
        """
        return UsuarioDAO.get_by_id(user_id)

