"""
Capa de Presentación - Gestión de Productos
Interfaz de usuario para CRUD de productos usando Flet
"""

import flet as ft
from business.product_logic import ProductService


class ProductPage:
    """Página de gestión de productos"""
    
    def __init__(self, page: ft.Page, user_data: dict, on_logout=None):
        """
        Inicializa la página de productos
        
        Args:
            page: Objeto Page de Flet
            user_data: Datos del usuario autenticado
            on_logout: Callback para cerrar sesión
        """
        self.page = page
        self.user_data = user_data
        self.on_logout = on_logout
        self.product_service = ProductService()
        self.products_table = None
        self.products_data = []
        self.selected_product_id = None
        
        # Campos del formulario
        self.codigo_field = None
        self.nombre_field = None
        self.descripcion_field = None
        self.precio_field = None
        self.stock_minimo_field = None
        self.unidad_field = None
        self.message_text = None
        
        # Referencias a botones
        self.update_button = None
        self.delete_button = None
    
    def build(self) -> ft.Container:
        """Construye la interfaz de gestión de productos"""
        
        # Título y botón de logout
        header = ft.Row(
            controls=[
                ft.Text(
                    value=f"Gestión de Productos - {self.user_data.get('nombre_usuario', 'Usuario')}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    expand=True
                ),
                ft.ElevatedButton(
                    text="Cerrar Sesión",
                    on_click=lambda e: self._handle_logout(),
                    color=ft.Colors.RED
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        # Formulario de productos
        form_container = self._build_form()
        
        # Tabla de productos
        table_container = self._build_table()
        
        # Contenedor principal
        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Divider(),
                    form_container,
                    ft.Divider(),
                    table_container
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )
        
        # Cargar productos al inicializar
        self._load_products()
        
        return main_container
    
    def _build_form(self) -> ft.Container:
        """Construye el formulario de productos"""
        
        self.codigo_field = ft.TextField(
            label="Código del Producto",
            hint_text="Ej: PROD-001",
            width=200
        )
        
        self.nombre_field = ft.TextField(
            label="Nombre del Producto",
            hint_text="Nombre descriptivo",
            width=300,
            expand=True
        )
        
        self.descripcion_field = ft.TextField(
            label="Descripción",
            hint_text="Descripción del producto",
            multiline=True,
            min_lines=2,
            max_lines=3,
            width=300,
            expand=True
        )
        
        self.precio_field = ft.TextField(
            label="Precio Unitario",
            hint_text="0.00",
            width=150,
            value="0.00"
        )
        
        self.stock_minimo_field = ft.TextField(
            label="Stock Mínimo",
            hint_text="0",
            width=150,
            value="0"
        )
        
        self.unidad_field = ft.TextField(
            label="Unidad de Medida",
            hint_text="UNIDAD, KG, L, etc.",
            width=150,
            value="UNIDAD"
        )
        
        self.message_text = ft.Text(
            value="",
            size=12,
            visible=False
        )
        
        # Crear botones con referencias
        self.update_button = ft.ElevatedButton(
            text="Actualizar",
            on_click=lambda e: self._update_product(),
            color=ft.Colors.ORANGE,
            disabled=True
        )
        
        self.delete_button = ft.ElevatedButton(
            text="Eliminar",
            on_click=lambda e: self._delete_product(),
            color=ft.Colors.RED,
            disabled=True
        )
        
        form_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Nuevo Producto",
                    on_click=lambda e: self._clear_form(),
                    color=ft.Colors.BLUE
                ),
                ft.ElevatedButton(
                    text="Guardar",
                    on_click=lambda e: self._save_product(),
                    color=ft.Colors.GREEN
                ),
                self.update_button,
                self.delete_button
            ],
            spacing=10
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Formulario de Producto", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[self.codigo_field, self.nombre_field],
                        spacing=10
                    ),
                    self.descripcion_field,
                    ft.Row(
                        controls=[self.precio_field, self.stock_minimo_field, self.unidad_field],
                        spacing=10
                    ),
                    self.message_text,
                    form_buttons
                ],
                spacing=10
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=5
        )
    
    def _build_table(self) -> ft.Container:
        """Construye la tabla de productos"""
        
        self.products_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Stock")),
                ft.DataColumn(ft.Text("Stock Mín.")),
                ft.DataColumn(ft.Text("Unidad"))
            ],
            rows=[],
            heading_row_color=ft.Colors.BLUE_GREY_100,
            data_row_min_height=40,
            data_row_max_height=40
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Lista de Productos", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.products_table,
                        height=400,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5
                    )
                ],
                spacing=10
            ),
            padding=10
        )
    
    def _load_products(self):
        """Carga los productos desde la base de datos"""
        self.products_data = self.product_service.get_all_products()
        self._refresh_table()
    
    def _refresh_table(self):
        """Actualiza la tabla de productos"""
        rows = []
        for product in self.products_data:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(product.get('id_producto', '')))),
                    ft.DataCell(ft.Text(product.get('codigo_producto', ''))),
                    ft.DataCell(ft.Text(product.get('nombre_producto', ''))),
                    ft.DataCell(ft.Text(product.get('nombre_categoria', 'General'))),
                    ft.DataCell(ft.Text(f"${product.get('precio_unitario', 0):.2f}")),
                    ft.DataCell(ft.Text(str(product.get('stock_actual', 0)))),
                    ft.DataCell(ft.Text(str(product.get('stock_minimo', 0)))),
                    ft.DataCell(ft.Text(product.get('unidad_medida', 'UNIDAD')))
                ],
                on_select_changed=lambda e, p=product: self._select_product(p)
            )
            rows.append(row)
        
        self.products_table.rows = rows
        self.page.update()
    
    def _select_product(self, product: dict):
        """Selecciona un producto de la tabla y carga sus datos en el formulario"""
        self.selected_product_id = product.get('id_producto')
        
        self.codigo_field.value = product.get('codigo_producto', '')
        self.codigo_field.disabled = True  # No se puede cambiar el código
        
        self.nombre_field.value = product.get('nombre_producto', '')
        self.descripcion_field.value = product.get('descripcion', '')
        self.precio_field.value = str(product.get('precio_unitario', 0))
        self.stock_minimo_field.value = str(product.get('stock_minimo', 0))
        self.unidad_field.value = product.get('unidad_medida', 'UNIDAD')
        
        # Habilitar botones de actualizar y eliminar
        if self.update_button:
            self.update_button.disabled = False
        if self.delete_button:
            self.delete_button.disabled = False
        
        self._show_message("Producto seleccionado. Puede actualizar o eliminar.", ft.Colors.BLUE)
        self.page.update()
    
    def _clear_form(self):
        """Limpia el formulario"""
        self.selected_product_id = None
        self.codigo_field.value = ""
        self.codigo_field.disabled = False
        self.nombre_field.value = ""
        self.descripcion_field.value = ""
        self.precio_field.value = "0.00"
        self.stock_minimo_field.value = "0"
        self.unidad_field.value = "UNIDAD"
        
        # Deshabilitar botones de actualizar y eliminar
        if self.update_button:
            self.update_button.disabled = True
        if self.delete_button:
            self.delete_button.disabled = True
        
        self._show_message("Formulario limpiado. Listo para nuevo producto.", ft.Colors.BLUE)
        self.page.update()
    
    def _save_product(self):
        """Guarda un nuevo producto"""
        codigo = self.codigo_field.value
        nombre = self.nombre_field.value
        descripcion = self.descripcion_field.value or ""
        precio = float(self.precio_field.value or "0")
        stock_minimo = int(self.stock_minimo_field.value or "0")
        unidad = self.unidad_field.value or "UNIDAD"
        
        success, message = self.product_service.create_product(
            codigo, nombre, descripcion, 1, precio, stock_minimo, unidad
        )
        
        if success:
            self._show_message(message, ft.Colors.GREEN)
            self._clear_form()
            self._load_products()
        else:
            self._show_message(message, ft.Colors.RED)
    
    def _update_product(self):
        """Actualiza un producto existente"""
        if not self.selected_product_id:
            self._show_message("Seleccione un producto para actualizar", ft.Colors.RED)
            return
        
        nombre = self.nombre_field.value
        descripcion = self.descripcion_field.value or ""
        precio = float(self.precio_field.value or "0")
        stock_minimo = int(self.stock_minimo_field.value or "0")
        unidad = self.unidad_field.value or "UNIDAD"
        
        success, message = self.product_service.update_product(
            self.selected_product_id, nombre, descripcion, 1, precio, stock_minimo, unidad
        )
        
        if success:
            self._show_message(message, ft.Colors.GREEN)
            self._clear_form()
            self._load_products()
        else:
            self._show_message(message, ft.Colors.RED)
    
    def _delete_product(self):
        """Elimina un producto"""
        if not self.selected_product_id:
            self._show_message("Seleccione un producto para eliminar", ft.Colors.RED)
            return
        
        # Confirmación (simplificada)
        success, message = self.product_service.delete_product(self.selected_product_id)
        
        if success:
            self._show_message(message, ft.Colors.GREEN)
            self._clear_form()
            self._load_products()
        else:
            self._show_message(message, ft.Colors.RED)
    
    def _show_message(self, message: str, color):
        """Muestra un mensaje en el formulario"""
        self.message_text.value = message
        self.message_text.color = color
        self.message_text.visible = True
        self.page.update()
    
    def _handle_logout(self):
        """Maneja el cierre de sesión"""
        if self.on_logout:
            self.on_logout()

