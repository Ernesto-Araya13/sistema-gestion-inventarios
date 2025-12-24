"""
Archivo principal de la aplicación
Sistema de Gestión de Inventarios - Aplicación de escritorio con Flet
"""

import flet as ft
from presentation.login_page import LoginPage
from presentation.product_page import ProductPage
from config.database import test_connection


def main(page: ft.Page):
    """
    Función principal de la aplicación Flet
    
    Args:
        page: Objeto Page de Flet
    """
    # Configuración de la página
    page.title = "Sistema de Gestión de Inventarios"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Variable para almacenar datos del usuario autenticado
    current_user = None
    
    def show_login():
        """Muestra la pantalla de login"""
        login_page = LoginPage(page, on_login_success=handle_login_success)
        page.clean()
        page.add(login_page.build())
        page.update()
    
    def show_products(user_data: dict):
        """Muestra la pantalla de gestión de productos"""
        product_page = ProductPage(page, user_data, on_logout=handle_logout)
        page.clean()
        page.add(product_page.build())
        page.update()
    
    def handle_login_success(user_data: dict):
        """
        Callback cuando el login es exitoso
        
        Args:
            user_data: Diccionario con datos del usuario autenticado
        """
        nonlocal current_user
        current_user = user_data
        show_products(user_data)
    
    def handle_logout():
        """Maneja el cierre de sesión"""
        nonlocal current_user
        current_user = None
        show_login()
    
    # Verificar conexión a base de datos
    if not test_connection():
        # Mostrar diálogo de error
        def close_dialog(e):
            dialog.open = False
            page.update()
            page.window.close()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error de Conexión"),
            content=ft.Text(
                "No se pudo conectar a la base de datos MySQL.\n\n"
                "Por favor verifique:\n"
                "1. Que MySQL esté ejecutándose\n"
                "2. Que la base de datos 'dbappescritorio' exista\n"
                "3. Que las credenciales en config/database.py sean correctas\n"
                "4. Que las tablas necesarias estén creadas en la base de datos"
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
        return
    
    # Mostrar pantalla de login inicial
    show_login()


if __name__ == "__main__":
    # Ejecutar la aplicación Flet
    ft.app(target=main)

