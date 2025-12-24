"""
Capa de Presentación - Pantalla de Login
Interfaz de usuario para autenticación usando Flet
"""

import flet as ft
from business.auth_logic import AuthService


class LoginPage:
    """Página de inicio de sesión"""
    
    def __init__(self, page: ft.Page, on_login_success):
        """
        Inicializa la página de login
        
        Args:
            page: Objeto Page de Flet
            on_login_success: Callback cuando el login es exitoso
        """
        self.page = page
        self.on_login_success = on_login_success
        self.email_field = None
        self.password_field = None
        self.error_message = None
    
    def build(self) -> ft.Container:
        """Construye la interfaz de login"""
        
        # Campo de email
        self.email_field = ft.TextField(
            label="Email",
            hint_text="usuario@ejemplo.com",
            width=300,
            autofocus=True,
            on_submit=lambda e: self._handle_login()
        )
        
        # Campo de contraseña
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="Ingrese su contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            on_submit=lambda e: self._handle_login()
        )
        
        # Mensaje de error
        self.error_message = ft.Text(
            value="",
            color=ft.Colors.RED,
            size=12,
            visible=False
        )
        
        # Botón de login
        login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            on_click=lambda e: self._handle_login(),
            width=300,
            height=40
        )
        
        # Contenedor principal
        login_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Sistema de Gestión de Inventarios",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.email_field,
                    self.password_field,
                    self.error_message,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    login_button,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        value="Usuario: admin@inventario.com\nContraseña: admin123",
                        size=10,
                        color=ft.Colors.GREY,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,
            width=self.page.width,
            height=self.page.height,
            padding=20
        )
        
        return login_container
    
    def _handle_login(self):
        """Maneja el evento de login"""
        email = self.email_field.value
        password = self.password_field.value
        
        # Limpiar mensaje de error anterior
        self.error_message.visible = False
        self.error_message.value = ""
        self.page.update()
        
        # Intentar autenticación
        success, message, user_data = AuthService.login(email, password)
        
        if success:
            # Login exitoso, llamar callback
            self.on_login_success(user_data)
        else:
            # Mostrar error
            self.error_message.value = message
            self.error_message.visible = True
            self.page.update()

