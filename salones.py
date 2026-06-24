import flet as ft

db_salones=[
    {"id": 1, "nombre": "Aula 1", "tipo": "Teórica"},
    {"id": 2, "nombre": "Aula 2", "tipo": "Teórica"},
    {"id": 3, "nombre": "Aula 3", "tipo": "Teórica"},
    {"id": 4, "nombre": "Lab 1", "tipo": "Laboratorio"},
    {"id": 5, "nombre": "Taller 1", "tipo": "Taller"},
    {"id": 6, "nombre": "Taller 2", "tipo": "Taller"},
    {"id": 7, "nombre": "Cancha", "tipo": "Deportivo"},
]

TIPOS_SALON=["Teórica", "Laboratorio", "Taller", "Deportivo", "Otro"]

COLOR_TIPO={
    "Teórica": ("#1A3A5C", "#5B9BD5"),
    "Laboratorio": ("#1A2A20", "#439A5D"),
    "Taller": ("#332415", "#E69138"),
    "Deportivo": ("#1A3A38", "#76C7C0"),
    "Otro": ("#2A2D3E", "#C0C0C0"),
}

ICONO_TIPO={
    "Teórica": ft.icons.MEETING_ROOM,
    "Laboratorio": ft.icons.BIOTECH,
    "Taller": ft.icons.BUILD,
    "Deportivo": ft.icons.SPORTS_SOCCER,
    "Otro": ft.icons.ROOM,
}

def vista_salones(on_volver_menu=None):
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

    tabla_salones=ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("Salón", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        **estilo_tabla
    )

    txt_total=ft.Text("Salones registrados: 0", color="#A0A0B0", size=14, weight=ft.FontWeight.W_500)
    contadores_tipo={t: ft.Text("0", size=16, weight=ft.FontWeight.BOLD, color=COLOR_TIPO[t][1]) for t in TIPOS_SALON}

    id_actual=ft.Text(visible=False)
    txt_nombre=ft.TextField(
        label="Nombre del Salón",
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color="#A0A0B0")
    )
    dd_tipo=ft.Dropdown(
        label="Tipo de Espacio",
        options=[ft.dropdown.Option(t) for t in TIPOS_SALON],
        value="Teórica",
        border_color="#303346",
        focused_border_color="#439A5D",
        border_radius=10,
        bgcolor="#13141C",
        color=ft.colors.WHITE,
    )

    def cerrar_modal(e):
        modal_salon.open=False
        e.page.update()

    def cerrar_modal_info(e):
        modal_info.open=False
        e.page.update()

    def cerrar_modal_confirmacion(e):
        modal_confirmacion.open=False
        e.page.update()

    def cerrar_modal_advertencia(e):
        modal_advertencia.open=False
        e.page.update()

    def pre_guardar_salon(e):
        nombre=txt_nombre.value.strip()
        if not nombre:
            e.page.snack_bar=ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="#E57373")
            e.page.snack_bar.open=True
            e.page.update()
            return

        for s in db_salones:
            if str(s["id"])!=id_actual.value:
                if s["nombre"].lower()==nombre.lower():
                    e.page.dialog=modal_advertencia
                    modal_advertencia.open=True
                    e.page.update()
                    return

        es_nuevo=id_actual.value==""
        if not es_nuevo:
            modal_confirmacion.title=ft.Text("¿Confirmar Cambios?", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
            modal_confirmacion.content=ft.Text("¿Está seguro de que desea guardar las modificaciones realizadas?", color="#A0A0B0")
            modal_confirmacion.actions=[
                ft.TextButton("No, Cancelar", on_click=cerrar_modal_confirmacion, style=ft.ButtonStyle(color="#A0A0B0")),
                ft.ElevatedButton("Sí, Guardar", on_click=ejecutar_guardado, bgcolor="#439A5D", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
            ]
            e.page.dialog=modal_confirmacion
            modal_confirmacion.open=True
            e.page.update()
        else:
            ejecutar_guardado(e)

    def ejecutar_guardado(e):
        nombre=txt_nombre.value.strip()
        es_nuevo=id_actual.value==""
        
        if es_nuevo:
            nuevo_id=max([s["id"] for s in db_salones], default=0)+1
            db_salones.append({"id": nuevo_id, "nombre": nombre, "tipo": dd_tipo.value})
        else:
            for s in db_salones:
                if str(s["id"])==id_actual.value:
                    s["nombre"]=nombre
                    s["tipo"]=dd_tipo.value
            cerrar_modal_confirmacion(e)
        
        cerrar_modal(e)
        cargar_datos()
        txt_buscar.value=""
        
        if es_nuevo:
            e.page.dialog=modal_info
            modal_info.open=True
        e.page.update()

    modal_salon=ft.AlertDialog(
        title=ft.Text("Formulario de Salón", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=460,
            content=ft.Column([
                id_actual,
                txt_nombre,
                dd_tipo,
            ], spacing=15, tight=True)
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton(
                "Guardar Registro",
                on_click=pre_guardar_salon,
                bgcolor="#439A5D",
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            )
        ],
        actions_padding=20
    )

    modal_info=ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED,color="#439A5D",size=50),
            ft.Text("Éxito",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Text("Salón añadido exitosamente.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=10,tight=True,width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK",on_click=cerrar_modal_info,bgcolor="#439A5D",color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    modal_advertencia=ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.WARNING_ROUNDED,color="#E69138",size=50),
            ft.Text("Salón Duplicado",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Text("Estás intentando agregar o modificar un salón que ya existe, por favor verifícalo.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=12,tight=True,width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK",on_click=cerrar_modal_advertencia,bgcolor="#E69138",color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    modal_confirmacion=ft.AlertDialog(
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions_padding=20,
        actions_alignment=ft.MainAxisAlignment.END
    )

    def pedir_confirmacion_eliminar(sal, e):
        modal_confirmacion.title=ft.Text("¿Confirmar Eliminación?", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        modal_confirmacion.content=ft.Text(f"¿Está seguro de que desea eliminar el espacio '{sal['nombre']}'?", color="#A0A0B0")
        modal_confirmacion.actions=[
            ft.TextButton("No, Cancelar", on_click=cerrar_modal_confirmacion, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Confirmar", on_click=lambda ex: ejecutar_eliminacion(sal["id"], ex), bgcolor="#E57373", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ]
        e.page.dialog=modal_confirmacion
        modal_confirmacion.open=True
        e.page.update()

    def ejecutar_eliminacion(sal_id, e):
        global db_salones
        db_salones=[s for s in db_salones if s["id"]!=sal_id]
        cerrar_modal_confirmacion(e)
        cargar_datos()
        txt_buscar.value=""
        e.page.update()

    def abrir_modal_crear(e):
        id_actual.value=""
        txt_nombre.value=""
        dd_tipo.value="Teórica"
        e.page.dialog=modal_salon
        modal_salon.open=True
        e.page.update()

    def abrir_modal_editar(sal, e):
        id_actual.value=str(sal["id"])
        txt_nombre.value=sal["nombre"]
        dd_tipo.value=sal.get("tipo", "Teórica")
        e.page.dialog=modal_salon
        modal_salon.open=True
        e.page.update()

    def filtrar_salones(e):
        term=txt_buscar.value.lower()
        cargar_datos(term)
        e.page.update()

    txt_buscar=ft.TextField(
        hint_text="Búsqueda por nombre o tipo",
        width=320,
        height=40,
        content_padding=ft.padding.only(left=15, right=10),
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        prefix=ft.Icon(ft.icons.SEARCH, color="#A0A0B0", size=20),
        hint_style=ft.TextStyle(color="#5A5D70", size=13),
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=13),
        on_change=filtrar_salones
    )

    def cargar_datos(filtro=""):
        tabla_salones.rows.clear()
        conteo={t: 0 for t in TIPOS_SALON}

        for sal in db_salones:
            tipo=sal.get("tipo", "Otro")
            nombre=sal["nombre"].lower()
            
            if tipo in conteo:
                conteo[tipo]+=1
                
            if filtro and (filtro not in nombre and filtro not in tipo.lower()):
                continue

            bg, col=COLOR_TIPO.get(tipo, ("#2A2D3E", "#A0A0B0"))
            icono=ICONO_TIPO.get(tipo, ft.icons.ROOM)

            tabla_salones.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Row([
                    ft.Icon(icono, color=col, size=18),
                    ft.Text(sal["nombre"], color=ft.colors.WHITE, weight=ft.FontWeight.W_500, expand=True)
                ], expand=True)),
                ft.DataCell(ft.Container(
                    content=ft.Text(tipo, size=12, color=col, weight=ft.FontWeight.BOLD),
                    bgcolor=bg,
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                    border_radius=10
                )),
                ft.DataCell(ft.Row([
                    ft.Container(
                        content=ft.IconButton(ft.icons.EDIT, icon_color="#A0A0B0", icon_size=16,
                                              on_click=lambda e, s=sal: abrir_modal_editar(s, e)),
                        bgcolor="#2A2D3E", border_radius=8, width=32, height=32
                    ),
                    ft.Container(
                        content=ft.IconButton(ft.icons.DELETE, icon_color="#E57373", icon_size=16,
                                              on_click=lambda e, s=sal: pedir_confirmacion_eliminar(s, e)),
                        bgcolor="#3E2A2A", border_radius=8, width=32, height=32
                    ),
                ], spacing=10))
            ]))

        txt_total.value=f"Salones registrados: {len(db_salones)}"
        for t in TIPOS_SALON:
            contadores_tipo[t].value=str(conteo[t])

    cargar_datos()

    chips_tipos=ft.Row([
        ft.Container(
            bgcolor=COLOR_TIPO[t][0],
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            expand=True,
            content=ft.Row([
                ft.Icon(ICONO_TIPO[t], color=COLOR_TIPO[t][1], size=16),
                ft.Text(t, color=COLOR_TIPO[t][1], size=11, weight=ft.FontWeight.W_500),
                ft.VerticalDivider(width=5, color=ft.colors.TRANSPARENT),
                contadores_tipo[t]
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
        ) for t in TIPOS_SALON
    ], spacing=10)

    tarjeta_stats=ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            chips_tipos
        ], spacing=0)
    )

    return ft.Container(
        padding=20, expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row([
                            ft.IconButton(ft.icons.ARROW_BACK, icon_color="#A0A0B0", on_click=on_volver_menu if on_volver_menu else lambda e: None) if on_volver_menu else ft.Container(),
                            ft.Column([
                                ft.Text("Gestión de Salones", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Administra los espacios físicos disponibles para clases", size=14, color="#A0A0B0")
                            ], spacing=2)
                        ]),
                        ft.ElevatedButton(
                            "Añadir Salón",
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
                tarjeta_stats,
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                ft.Container(
                    **estilo_tarjeta_oscura,
                    expand=True,
                    content=ft.Column([
                        ft.Row([
                            ft.Row([
                                ft.Icon(ft.icons.MEETING_ROOM, color="#439A5D"),
                                ft.Text("Salones Registrados", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
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
                                            content=tabla_salones
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