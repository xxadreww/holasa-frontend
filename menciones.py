import flet as ft

db_menciones=[
    {"id": 1, "nombre": "Electrónica", "codigo": "EO"},
    {"id": 2, "nombre": "Electricidad", "codigo": "EL"},
    {"id": 3, "nombre": "Máquinas y Herramientas", "codigo": "MM"},
    {"id": 4, "nombre": "Refrigeración", "codigo": "MT"},
    {"id": 5, "nombre": "Metalmecánica", "codigo": "ME"},
]

def vista_menciones(on_volver_menu=None):
    estilo_tarjeta_oscura={
        "bgcolor": "#1E202D",
        "border_radius": 15,
        "padding": 20,
        "border": ft.border.all(1, "#303346")
    }

    estilo_tabla={
        "bgcolor": "#13141C",
        "border_radius": 15,
        "border": ft.border.all(1, "#303346"),
        "horizontal_lines": ft.border.BorderSide(1, "#303346"),
        "vertical_lines": ft.border.BorderSide(0, ft.colors.TRANSPARENT),
        "heading_row_color": "#1A1C28",
        "data_row_max_height": 64,
    }

    tabla_menciones=ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("Mención", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Código", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        **estilo_tabla
    )

    txt_total=ft.Text("Menciones registradas: 0", color="#A0A0B0", size=14, weight=ft.FontWeight.W_500)
    id_actual=ft.Text(visible=False)
    
    txt_nombre=ft.TextField(
        label="Nombre de la Mención",
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color="#A0A0B0")
    )
    
    txt_codigo=ft.TextField(
        label="Código (ej: EO, EL)",
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        max_length=3,
        width=180,
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color="#A0A0B0")
    )

    def cerrar_modal(e):
        modal_mencion.open=False
        e.page.update()

    def cerrar_modal_exito(e):
        modal_exito.open=False
        e.page.update()

    def cerrar_modal_duplicado(e):
        modal_duplicado.open=False
        e.page.update()

    def confirmar_guardar_mencion(e):
        nombre=txt_nombre.value.strip()
        codigo=txt_codigo.value.strip().upper()
        
        if not nombre:
            e.page.snack_bar=ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#E57373")
            e.page.snack_bar.open=True
            e.page.update()
            return
        
        for m in db_menciones:
            if str(m["id"])!=id_actual.value:
                if m["nombre"].lower()==nombre.lower():
                    dup_tipo.value="El nombre de la mención ya existe"
                    dup_detalle.value=f"Nombre: {m['nombre']} | Código: {m['codigo']}"
                    e.page.dialog=modal_duplicado
                    modal_duplicado.open=True
                    e.page.update()
                    return
                if codigo and m["codigo"].upper()==codigo:
                    dup_tipo.value="El código de la mención ya existe"
                    dup_detalle.value=f"Nombre: {m['nombre']} | Código: {m['codigo']}"
                    e.page.dialog=modal_duplicado
                    modal_duplicado.open=True
                    e.page.update()
                    return

        modal_mencion.open=False
        if id_actual.value!="":
            abrir_modal_confirmar_accion(
                "¿Confirmar Edición?",
                "¿Está seguro de que desea guardar los cambios realizados en esta mención?",
                "#439A5D",
                ejecutar_guardado,
                e
            )
        else:
            ejecutar_guardado(e)

    def ejecutar_guardado(e):
        nombre=txt_nombre.value.strip()
        codigo=txt_codigo.value.strip().upper()
        es_nuevo=id_actual.value==""
        
        if es_nuevo:
            nuevo_id=max([m["id"] for m in db_menciones], default=0)+1
            db_menciones.append({"id": nuevo_id, "nombre": nombre, "codigo": codigo})
        else:
            for m in db_menciones:
                if str(m["id"])==id_actual.value:
                    m["nombre"]=nombre
                    m["codigo"]=codigo
        
        cargar_datos()
        txt_buscar.value=""
        
        if es_nuevo:
            e.page.dialog=modal_exito
            modal_exito.open=True
        
        e.page.update()

    modal_mencion=ft.AlertDialog(
        title=ft.Text("Formulario de Mención", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=480,
            content=ft.Column([
                id_actual,
                txt_nombre,
                txt_codigo,
            ], spacing=15, scroll=ft.ScrollMode.AUTO)
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton(
                "Guardar Registro",
                on_click=confirmar_guardar_mencion,
                bgcolor="#439A5D",
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            )
        ],
        actions_padding=20
    )

    modal_confirmacion=ft.AlertDialog(
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions_padding=20,
        actions_alignment=ft.MainAxisAlignment.END
    )

    dup_tipo=ft.Text(size=14,weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,text_align=ft.TextAlign.CENTER)
    dup_detalle=ft.Text(color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)

    modal_duplicado=ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.WARNING_ROUNDED,color="#E69138",size=50),
            ft.Text("Registro Duplicado",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Container(
                bgcolor="#13141C",padding=12,border_radius=10,border=ft.border.all(1,"#303346"),width=280,
                content=ft.Column([dup_tipo,dup_detalle],spacing=4,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ),
            ft.Text("Por favor, verifique los datos antes de continuar.",color="#A0A0B0",size=12,text_align=ft.TextAlign.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=12,tight=True,width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("Entendido",on_click=cerrar_modal_duplicado,bgcolor="#E69138",color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    modal_exito=ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED,color="#439A5D",size=50),
            ft.Text("Éxito",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Text("Sección agregada con éxito.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=10,tight=True,width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK",on_click=cerrar_modal_exito,bgcolor="#439A5D",color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    def abrir_modal_confirmar_accion(titulo, mensaje, color_btn, accion_si, e):
        modal_confirmacion.title=ft.Text(titulo, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        modal_confirmacion.content=ft.Text(mensaje, color="#A0A0B0")
        modal_confirmacion.actions=[
            ft.TextButton("No, Cancelar", on_click=lambda ex: cerrar_modal_confirmacion(ex), style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Confirmar", on_click=lambda ex: [cerrar_modal_confirmacion(ex), accion_si(e)], bgcolor=color_btn, color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ]
        e.page.dialog=modal_confirmacion
        modal_confirmacion.open=True
        e.page.update()

    def cerrar_modal_confirmacion(e):
        modal_confirmacion.open=False
        e.page.update()

    def abrir_modal_crear(e):
        id_actual.value=""
        txt_nombre.value=""
        txt_codigo.value=""
        e.page.dialog=modal_mencion
        modal_mencion.open=True
        e.page.update()

    def abrir_modal_editar(men, e):
        id_actual.value=str(men["id"])
        txt_nombre.value=men["nombre"]
        txt_codigo.value=men.get("codigo", "")
        e.page.dialog=modal_mencion
        modal_mencion.open=True
        e.page.update()

    def pedir_confirmacion_eliminar(men, e):
        abrir_modal_confirmar_accion(
            "¿Confirmar Eliminación?",
            f"¿Está completamente seguro de que desea eliminar la mención {men['nombre']} del sistema?",
            "#E57373",
            lambda ex: ejecutar_eliminacion(men["id"], ex),
            e
        )

    def ejecutar_eliminacion(men_id, e):
        db_menciones[:]=[m for m in db_menciones if m["id"]!=men_id]
        cargar_datos()
        txt_buscar.value=""
        e.page.update()

    def filtrar_menciones(e):
        term=txt_buscar.value.lower()
        cargar_datos(term)
        e.page.update()

    txt_buscar=ft.TextField(
        hint_text="Búsqueda",
        width=320,
        height=40,
        content_padding=ft.padding.only(left=15, right=10),
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        prefix=ft.Icon(ft.icons.SEARCH, color="#A0A0B0", size=20),
        hint_style=ft.TextStyle(color="#5A5D70", size=13),
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=13),
        on_change=filtrar_menciones
    )

    def cargar_datos(filtro=""):
        tabla_menciones.rows.clear()
        for men in db_menciones:
            nombre=men["nombre"].lower()
            codigo=men.get("codigo", "").lower()
            
            if filtro and (filtro not in nombre and filtro not in codigo):
                continue

            tabla_menciones.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(men["nombre"][0], weight=ft.FontWeight.BOLD, size=13),
                        bgcolor="#2A2D3E", color=ft.colors.WHITE, radius=14
                    ),
                    ft.Text(men["nombre"], color=ft.colors.WHITE, weight=ft.FontWeight.W_500, expand=True)
                ], expand=True)),
                ft.DataCell(ft.Container(
                    content=ft.Text(men.get("codigo", "—"), size=12, color="#5B9BD5", weight=ft.FontWeight.BOLD),
                    bgcolor="#1A3A5C",
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                    border_radius=10
                )),
                ft.DataCell(ft.Row([
                    ft.Container(
                        content=ft.IconButton(ft.icons.EDIT, icon_color="#A0A0B0", icon_size=16,
                                              on_click=lambda e, m=men: abrir_modal_editar(m, e)),
                        bgcolor="#2A2D3E", border_radius=8, width=32, height=32
                    ),
                    ft.Container(
                        content=ft.IconButton(ft.icons.DELETE, icon_color="#E57373", icon_size=16,
                                              on_click=lambda e, m=men: pedir_confirmacion_eliminar(m, e)),
                        bgcolor="#3E2A2A", border_radius=8, width=32, height=32
                    ),
                ], spacing=10))
            ]))
        txt_total.value=f"Menciones registradas: {len(db_menciones)}"

    cargar_datos()

    return ft.Container(
        padding=20, expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row([
                            ft.IconButton(ft.icons.ARROW_BACK, icon_color="#A0A0B0", on_click=on_volver_menu if on_volver_menu else lambda e: None) if on_volver_menu else ft.Container(),
                            ft.Column([
                                ft.Text("Gestión de Menciones", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Administra las menciones técnicas disponibles", size=14, color="#A0A0B0")
                            ], spacing=2)
                        ]),
                        ft.ElevatedButton(
                            "Añadir Mención",
                            icon=ft.icons.ADD,
                            on_click=abrir_modal_crear,
                            bgcolor="#439A5D",
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=20)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Container(
                    **estilo_tarjeta_oscura,
                    expand=True,
                    content=ft.Column([
                        ft.Row([
                            ft.Row([
                                ft.Icon(ft.icons.LABEL, color="#439A5D"),
                                ft.Text("Menciones Registradas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT),
                                txt_total
                            ]),
                            txt_buscar
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                        ft.Column(
                            [
                                ft.Row([
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.alignment.center,
                                        content=ft.Container(
                                            width=1280,
                                            content=tabla_menciones
                                        )
                                    )
                                ])
                            ],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO
                        )
                    ], spacing=15, expand=True)
                )
            ],
            expand=True
        )
    )