import flet as ft

DIAS_SEMANA=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS_DISPONIBLES=[
    "7:00", "7:40", "8:20", "8:30", "9:10", "9:50",
    "10:30", "11:10", "11:50", "12:10", "12:50", "13:30", "14:10"
]

db_sesiones=[
    {"id": 1, "dia": "Lunes", "hora_inicio": "7:00", "hora_fin": "7:40"},
    {"id": 2, "dia": "Lunes", "hora_inicio": "7:40", "hora_fin": "8:20"},
    {"id": 3, "dia": "Martes", "hora_inicio": "8:30", "hora_fin": "9:10"},
    {"id": 4, "dia": "Miércoles", "hora_inicio": "9:50", "hora_fin": "10:30"},
    {"id": 5, "dia": "Jueves", "hora_inicio": "10:30", "hora_fin": "11:10"},
    {"id": 6, "dia": "Viernes", "hora_inicio": "12:10", "hora_fin": "12:50"},
]

COLOR_DIA={
    "Lunes": ("#1A3A5C", "#5B9BD5"),
    "Martes": ("#1A2A20", "#439A5D"),
    "Miércoles": ("#332415", "#E69138"),
    "Jueves": ("#1A3A38", "#76C7C0"),
    "Viernes": ("#3A1A30", "#D988B9"),
}

def vista_sesiones(on_volver_menu=None):
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

    tabla_sesiones=ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("Día", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Hora Inicio", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Hora Fin", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        **estilo_tabla
    )

    txt_total=ft.Text("Sesiones registradas: 0", color="#A0A0B0", size=14, weight=ft.FontWeight.W_500)
    contadores_dia={d: ft.Text("0", size=16, weight=ft.FontWeight.BOLD, color=COLOR_DIA[d][1]) for d in DIAS_SEMANA}

    id_actual=ft.Text(visible=False)
    dd_dia=ft.Dropdown(
        label="Día de la Sesión",
        options=[ft.dropdown.Option(d) for d in DIAS_SEMANA],
        value="Lunes",
        border_color="#303346",
        focused_border_color="#439A5D",
        border_radius=10,
        bgcolor="#13141C",
        color=ft.colors.WHITE,
    )
    dd_inicio=ft.Dropdown(
        label="Hora de Inicio",
        options=[ft.dropdown.Option(h) for h in HORAS_DISPONIBLES],
        value="7:00",
        border_color="#303346",
        focused_border_color="#439A5D",
        border_radius=10,
        bgcolor="#13141C",
        color=ft.colors.WHITE,
    )
    dd_fin=ft.Dropdown(
        label="Hora Final",
        options=[ft.dropdown.Option(h) for h in HORAS_DISPONIBLES],
        value="7:40",
        border_color="#303346",
        focused_border_color="#439A5D",
        border_radius=10,
        bgcolor="#13141C",
        color=ft.colors.WHITE,
    )

    def cerrar_modal(e):
        modal_sesion.open=False
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

    def pre_guardar_sesion(e):
        idx_inicio=HORAS_DISPONIBLES.index(dd_inicio.value)
        idx_fin=HORAS_DISPONIBLES.index(dd_fin.value)
        if idx_inicio>=idx_fin:
            e.page.snack_bar=ft.SnackBar(ft.Text("La hora de inicio debe ser menor a la hora final"), bgcolor="#E57373")
            e.page.snack_bar.open=True
            e.page.update()
            return

        for s in db_sesiones:
            if str(s["id"])!=id_actual.value:
                if s["dia"]==dd_dia.value and s["hora_inicio"]==dd_inicio.value and s["hora_fin"]==dd_fin.value:
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
        es_nuevo=id_actual.value==""
        if es_nuevo:
            nuevo_id=max([s["id"] for s in db_sesiones], default=0)+1
            db_sesiones.append({"id": nuevo_id, "dia": dd_dia.value, "hora_inicio": dd_inicio.value, "hora_fin": dd_fin.value})
        else:
            for s in db_sesiones:
                if str(s["id"])==id_actual.value:
                    s["dia"]=dd_dia.value
                    s["hora_inicio"]=dd_inicio.value
                    s["hora_fin"]=dd_fin.value
            cerrar_modal_confirmacion(e)
        
        cerrar_modal(e)
        cargar_datos()
        txt_buscar.value=""
        
        if es_nuevo:
            e.page.dialog=modal_info
            modal_info.open=True
        e.page.update()

    modal_sesion=ft.AlertDialog(
        title=ft.Text("Formulario de Sesión", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=460,
            content=ft.Column([
                id_actual,
                dd_dia,
                dd_inicio,
                dd_fin,
            ], spacing=15, tight=True)
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton(
                "Guardar Registro",
                on_click=pre_guardar_sesion,
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
            ft.Text("Sesión añadida exitosamente.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
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
            ft.Text("Sesión Duplicada",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Text("Estás intentando agregar o modificar una sesión que ya existe, por favor verifícalo.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
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

    def pedir_confirmacion_eliminar(ses, e):
        modal_confirmacion.title=ft.Text("¿Confirmar Eliminación?", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        modal_confirmacion.content=ft.Text(f"¿Está seguro de que desea eliminar el bloque del {ses['dia']} ({ses['hora_inicio']} - {ses['hora_fin']})?", color="#A0A0B0")
        modal_confirmacion.actions=[
            ft.TextButton("No, Cancelar", on_click=cerrar_modal_confirmacion, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Confirmar", on_click=lambda ex: ejecutar_eliminacion(ses["id"], ex), bgcolor="#E57373", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ]
        e.page.dialog=modal_confirmacion
        modal_confirmacion.open=True
        e.page.update()

    def ejecutar_eliminacion(ses_id, e):
        global db_sesiones
        db_sesiones=[s for s in db_sesiones if s["id"]!=ses_id]
        cerrar_modal_confirmacion(e)
        cargar_datos()
        txt_buscar.value=""
        e.page.update()

    def abrir_modal_crear(e):
        id_actual.value=""
        dd_dia.value="Lunes"
        dd_inicio.value="7:00"
        dd_fin.value="7:40"
        e.page.dialog=modal_sesion
        modal_sesion.open=True
        e.page.update()

    def abrir_modal_editar(ses, e):
        id_actual.value=str(ses["id"])
        dd_dia.value=ses["dia"]
        dd_inicio.value=ses["hora_inicio"]
        dd_fin.value=ses["hora_fin"]
        e.page.dialog=modal_sesion
        modal_sesion.open=True
        e.page.update()

    def filtrar_sesiones(e):
        term=txt_buscar.value.lower()
        cargar_datos(term)
        e.page.update()

    txt_buscar=ft.TextField(
        hint_text="Búsqueda por día",
        width=320,
        height=40,
        content_padding=ft.padding.only(left=15, right=10),
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        prefix=ft.Icon(ft.icons.SEARCH, color="#A0A0B0", size=20),
        hint_style=ft.TextStyle(color="#5A5D70", size=13),
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=13),
        on_change=filtrar_sesiones
    )

    def cargar_datos(filtro=""):
        tabla_sesiones.rows.clear()
        conteo={d: 0 for d in DIAS_SEMANA}

        for ses in db_sesiones:
            dia=ses.get("dia", "Lunes")
            if dia in conteo:
                conteo[dia]+=1
                
            if filtro and filtro not in dia.lower():
                continue

            bg, col=COLOR_DIA.get(dia, ("#2A2D3E", "#A0A0B0"))

            tabla_sesiones.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Container(
                    content=ft.Text(dia, size=12, color=col, weight=ft.FontWeight.BOLD),
                    bgcolor=bg,
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                    border_radius=10
                )),
                ft.DataCell(ft.Text(ses["hora_inicio"], color=ft.colors.WHITE, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(ses["hora_fin"], color=ft.colors.WHITE, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Row([
                    ft.Container(
                        content=ft.IconButton(ft.icons.EDIT, icon_color="#A0A0B0", icon_size=16,
                                              on_click=lambda e, s=ses: abrir_modal_editar(s, e)),
                        bgcolor="#2A2D3E", border_radius=8, width=32, height=32
                    ),
                    ft.Container(
                        content=ft.IconButton(ft.icons.DELETE, icon_color="#E57373", icon_size=16,
                                              on_click=lambda e, s=ses: pedir_confirmacion_eliminar(s, e)),
                        bgcolor="#3E2A2A", border_radius=8, width=32, height=32
                    ),
                ], spacing=10))
            ]))

        txt_total.value=f"Sesiones registradas: {len(db_sesiones)}"
        for d in DIAS_SEMANA:
            contadores_dia[d].value=str(conteo[d])

    cargar_datos()

    chips_dias=ft.Row([
        ft.Container(
            bgcolor=COLOR_DIA[d][0],
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            expand=True,
            content=ft.Row([
                ft.Icon(ft.icons.ACCESS_TIME, color=COLOR_DIA[d][1], size=16),
                ft.Text(d, color=COLOR_DIA[d][1], size=11, weight=ft.FontWeight.W_500),
                ft.VerticalDivider(width=5, color=ft.colors.TRANSPARENT),
                contadores_dia[d]
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
        ) for d in DIAS_SEMANA
    ], spacing=10)

    tarjeta_stats=ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            chips_dias
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
                                ft.Text("Gestión de Sesiones", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Define los bloques de horas académicas y días hábiles", size=14, color="#A0A0B0")
                            ], spacing=2)
                        ]),
                        ft.ElevatedButton(
                            "Añadir Sesión",
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
                                ft.Icon(ft.icons.ACCESS_TIME, color="#439A5D"),
                                ft.Text("Sesiones Registradas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
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
                                            content=tabla_sesiones
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