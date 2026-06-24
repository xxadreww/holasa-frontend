import flet as ft

db_cursos = [
    {
        "id": 1, "year": "4to", "seccion": "A", "mencion": "Electrónica", "codigo_mencion": "EO",
        "asignaturas": [
            {"nombre": "Matemáticas", "tipo": "Teórica", "horas": 4},
            {"nombre": "Sistemas Digitales", "tipo": "Técnica", "horas": 3},
            {"nombre": "Física", "tipo": "Teórica", "horas": 3},
        ]
    },
    {
        "id": 2, "year": "4to", "seccion": "B", "mencion": "Electrónica", "codigo_mencion": "EO",
        "asignaturas": [
            {"nombre": "Matemáticas", "tipo": "Teórica", "horas": 4},
            {"nombre": "Circuitos Eléctricos", "tipo": "Técnica", "horas": 4},
        ]
    },
    {
        "id": 3, "year": "4to", "seccion": "A", "mencion": "Electricidad", "codigo_mencion": "EL",
        "asignaturas": [
            {"nombre": "Circuitos Eléctricos", "tipo": "Técnica", "horas": 4},
            {"nombre": "Lenguaje y Literatura", "tipo": "Teórica", "horas": 3},
        ]
    },
]

db_menciones_disp = [
    {"nombre": "Electrónica", "codigo": "EO"},
    {"nombre": "Electricidad", "codigo": "EL"},
    {"nombre": "Máquinas y Herramientas", "codigo": "MM"},
    {"nombre": "Refrigeración", "codigo": "MT"},
    {"nombre": "Metalmecánica", "codigo": "ME"},
]

db_asignaturas_disp = [
    {"nombre": "Matemáticas", "tipo": "Teórica"},
    {"nombre": "Física", "tipo": "Teórica"},
    {"nombre": "Lenguaje y Literatura", "tipo": "Teórica"},
    {"nombre": "Circuitos Eléctricos", "tipo": "Técnica"},
    {"nombre": "Sistemas Digitales", "tipo": "Técnica"},
    {"nombre": "Laboratorio de Electrónica", "tipo": "Práctica"},
    {"nombre": "Taller de Maquinaria", "tipo": "Técnica"},
    {"nombre": "Educación Física", "tipo": "Práctica"},
]

OPCIONES_YEARS = ["4to", "5to"]
OPCIONES_SECCIONES = ["A", "B", "C", "D"]
TIPOS_ASIGNATURA = ["Teórica", "Práctica", "Técnica"]

COLOR_TIPO = {
    "Teórica":  ("#1A3A5C", "#5B9BD5"),
    "Práctica": ("#1A2A20", "#439A5D"),
    "Técnica":  ("#332415", "#E69138"),
}

def vista_cursos():
    estilo_tarjeta_oscura = {
        "bgcolor": "#1E202D",
        "border_radius": 10,
        "padding": ft.padding.symmetric(horizontal=15, vertical=6),
        "border": ft.border.all(1, "#303346"),
        "height": 45
    }

    grilla_cursos = ft.Row(wrap=True, spacing=20, run_spacing=20)
    txt_total = ft.Text("0", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    txt_total_asig = ft.Text("0", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    id_actual = ft.Text(visible=False)
    dd_year = ft.Dropdown(
        label="Año",
        options=[ft.dropdown.Option(y) for y in OPCIONES_YEARS],
        value="4to",
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE, expand=True
    )
    dd_seccion = ft.Dropdown(
        label="Sección",
        options=[ft.dropdown.Option(s) for s in OPCIONES_SECCIONES],
        value="A",
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE, width=130
    )

    dd_mencion = ft.Dropdown(
        label="Mención",
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE, expand=True
    )
    txt_nueva_mencion = ft.TextField(
        label="Nombre de nueva mención",
        border_radius=10, border_color="#303346", focused_border_color="#439A5D",
        color=ft.colors.WHITE, label_style=ft.TextStyle(color="#A0A0B0"), expand=True
    )
    txt_codigo_mencion = ft.TextField(
        label="Código", max_length=3, width=120,
        border_radius=10, border_color="#303346", focused_border_color="#439A5D",
        color=ft.colors.WHITE, label_style=ft.TextStyle(color="#A0A0B0")
    )
    panel_nueva_mencion = ft.Column(visible=False, controls=[
        ft.Text("Nueva mención:", color="#A0A0B0", size=12),
        ft.Row([txt_nueva_mencion, txt_codigo_mencion], spacing=10)
    ], spacing=8)

    asignaturas_temp = []
    lista_chips_asig = ft.Column(spacing=8)

    dd_asignatura = ft.Dropdown(
        label="Asignatura",
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE, expand=True
    )
    dd_horas_asig = ft.Dropdown(
        label="Horas semanales",
        options=[ft.dropdown.Option(str(h)) for h in range(1, 9)],
        value="3", width=160,
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE
    )

    def cerrar_modal_advertencia(e):
        modal_advertencia.open = False
        e.page.update()

    def cerrar_modal_exito(e):
        modal_exito.open = False
        e.page.update()

    modal_advertencia = ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.WARNING_ROUNDED, color="#E69138", size=50),
            ft.Text("Curso Duplicado", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16, text_align=ft.TextAlign.CENTER),
            ft.Text("Estás intentando agregar o modificar un curso que ya existe, por favor verifícalo.", color="#A0A0B0", size=13, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12, tight=True, width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK", on_click=cerrar_modal_advertencia, bgcolor="#E69138", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    modal_exito = ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED, color="#439A5D", size=50),
            ft.Text("Éxito", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16, text_align=ft.TextAlign.CENTER),
            ft.Text("Curso procesado de manera exitosa.", color="#A0A0B0", size=13, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, tight=True, width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK", on_click=cerrar_modal_exito, bgcolor="#439A5D", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    def actualizar_dd_menciones():
        opciones = [ft.dropdown.Option(m["nombre"]) for m in db_menciones_disp]
        opciones.append(ft.dropdown.Option(key="__nueva__", text="[+] Nueva Mención"))
        dd_mencion.options = opciones

    def actualizar_dd_asignaturas():
        dd_asignatura.options = [ft.dropdown.Option(a["nombre"]) for a in db_asignaturas_disp]

    def on_mencion_change(e):
        panel_nueva_mencion.visible = (dd_mencion.value == "__nueva__")
        e.page.update()

    dd_mencion.on_change = on_mencion_change

    def refrescar_chips_asig():
        lista_chips_asig.controls.clear()
        for asig in asignaturas_temp:
            bg, col = COLOR_TIPO.get(asig["tipo"], ("#2A2D3E", "#A0A0B0"))
            lista_chips_asig.controls.append(
                ft.Container(
                    bgcolor=bg, border=ft.border.all(1, col), border_radius=10,
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    content=ft.Row([
                        ft.Column([
                            ft.Text(asig["nombre"], color=col, size=13, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{asig['tipo']} · {asig['horas']}h/sem", color="#A0A0B0", size=11)
                        ], spacing=1, expand=True),
                        ft.IconButton(ft.icons.CLOSE, icon_color=col, icon_size=14,
                                      on_click=lambda e, a=asig: quitar_asig(e, a), width=20, height=20)
                    ])
                )
            )

    def quitar_asig(e, asig):
        if asig in asignaturas_temp:
            asignaturas_temp.remove(asig)
            refrescar_chips_asig()
            e.page.update()

    def agregar_asignatura(e):
        nombre = dd_asignatura.value
        if not nombre:
            return
        encontrado = next((a for a in db_asignaturas_disp if a["nombre"] == nombre), None)
        if not encontrado:
            return
        tipo = encontrado["tipo"]
        if any(a["nombre"] == nombre for a in asignaturas_temp):
            return
        horas = int(dd_horas_asig.value or 3)
        asignaturas_temp.append({"nombre": nombre, "tipo": tipo, "horas": horas})
        refrescar_chips_asig()
        dd_asignatura.value = None
        e.page.update()

    def cerrar_modal(e):
        modal_curso.open = False
        e.page.update()

    def confirmar_guardar_curso(e):
        es_duplicado=False
        id_form=str(id_actual.value).strip()
        year_form=str(dd_year.value).strip()
        seccion_form=str(dd_seccion.value).strip()
        mencion_form=str(dd_mencion.value).strip()
        
        if mencion_form=="__nueva__":
            mencion_form=str(txt_nueva_mencion.value).strip()
        
        for c in db_cursos:
            if str(c["year"]).strip()==year_form and str(c["seccion"]).strip()==seccion_form and str(c["mencion"]).strip()==mencion_form:
                if id_form=="":
                    es_duplicado=True
                    break
                elif str(c["id"]).strip()!=id_form:
                    es_duplicado=True
                    break
        
        if es_duplicado:
            e.page.dialog=modal_advertencia
            modal_advertencia.open=True
            e.page.update()
            return

        modal_curso.open=False
        if id_form!="":
            abrir_modal_confirmar_accion(
                "¿Confirmar Edición?",
                "¿Está seguro de que desea guardar los cambios realizados en este curso?",
                "#439A5D",
                ejecutar_guardado,
                e
            )
        else:
            ejecutar_guardado(e)

    def ejecutar_guardado(e):
        mencion_nombre=None
        if dd_mencion.value=="__nueva__":
            mencion_nombre=txt_nueva_mencion.value.strip()
            codigo=txt_codigo_mencion.value.strip().upper()
            if not mencion_nombre:
                return
            db_menciones_disp.append({"nombre":mencion_nombre,"codigo":codigo})
            actualizar_dd_menciones()
        else:
            mencion_nombre=dd_mencion.value
        mencion_obj=next((m for m in db_menciones_disp if m["nombre"]==mencion_nombre),{})
        codigo_mencion=mencion_obj.get("codigo","")
        if id_actual.value=="":
            nuevo_id=max([c["id"] for c in db_cursos],default=0)+1
            db_cursos.append({
                "id":nuevo_id,
                "year":dd_year.value,
                "seccion":dd_seccion.value,
                "mencion":mencion_nombre,
                "codigo_mencion":codigo_mencion,
                "asignaturas":asignaturas_temp.copy()
            })
        else:
            for c in db_cursos:
                if str(c["id"])==str(id_actual.value):
                    c["year"]=dd_year.value
                    c["seccion"]=dd_seccion.value
                    c["mencion"]=mencion_nombre
                    c["codigo_mencion"]=codigo_mencion
                    c["asignaturas"]=asignaturas_temp.copy()
        
        cargar_grilla(txt_buscar.value.lower())
        e.page.dialog=modal_exito
        modal_exito.open=True
        e.page.update()

    modal_curso = ft.AlertDialog(
        title=ft.Text("Formulario de Curso", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=580,
            content=ft.Column([
                id_actual,
                ft.Row([dd_year, dd_seccion], spacing=15),
                ft.Text("-------------------------------------------------------------------------", color="#303346", size=12),
                ft.Text("Mención Técnica", color="#A0A0B0", weight=ft.FontWeight.BOLD),
                ft.Row([
                    dd_mencion,
                    ft.IconButton(
                        ft.icons.ADD_CIRCLE_OUTLINE, icon_color="#439A5D", tooltip="Crear nueva mención",
                        on_click=lambda e: (setattr(dd_mencion, 'value', '__nueva__'), setattr(panel_nueva_mencion, 'visible', True), e.page.update())
                    )
                ]),
                panel_nueva_mencion,
                ft.Text("-------------------------------------------------------------------------", color="#303346", size=12),
                ft.Text("Asignaturas del Curso", color="#A0A0B0", weight=ft.FontWeight.BOLD),
                ft.Row([
                    dd_asignatura,
                    dd_horas_asig,
                    ft.ElevatedButton("Agregar", icon=ft.icons.ADD, bgcolor="#439A5D", color=ft.colors.WHITE,
                                      on_click=agregar_asignatura,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                ], spacing=10),
                lista_chips_asig,
            ], spacing=12, scroll=ft.ScrollMode.AUTO)
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton(
                "Guardar Registro", on_click=confirmar_guardar_curso,
                bgcolor="#439A5D", color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            )
        ],
        actions_padding=20
    )

    modal_confirmacion = ft.AlertDialog(
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions_padding=20,
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_modal_confirmar_accion(titulo, mensaje, color_btn, accion_si, e):
        modal_confirmacion.title=ft.Text(titulo,weight=ft.FontWeight.BOLD,color=ft.colors.WHITE)
        modal_confirmacion.content=ft.Text(mensaje,color="#A0A0B0")
        def click_si(ex):
            modal_confirmacion.open=False
            ex.page.update()
            accion_si(ex)

        modal_confirmacion.actions=[
            ft.TextButton("No, Cancelar",on_click=lambda ex: cerrar_modal_confirmacion(ex),style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Confirmar",on_click=click_si,bgcolor=color_btn,color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ]
        e.page.dialog=modal_confirmacion
        modal_confirmacion.open=True
        e.page.update()

    def cerrar_modal_confirmacion(e):
        modal_confirmacion.open = False
        e.page.update()

    def pedir_confirmacion_eliminar(cur, e):
        abrir_modal_confirmar_accion(
            "¿Confirmar Eliminación?",
            f"¿Está completamente seguro de que desea eliminar este curso del sistema?",
            "#E57373",
            lambda ex: ejecutar_eliminacion(cur["id"], ex),
            e
        )

    def ejecutar_eliminacion(cur_id, e):
        global db_cursos
        db_cursos = [c for c in db_cursos if c["id"] != cur_id]
        cargar_grilla(txt_buscar.value.lower())
        e.page.update()

    def abrir_modal_crear(e):
        id_actual.value = ""
        dd_year.value = "4to"
        dd_seccion.value = "A"
        dd_mencion.value = None
        dd_asignatura.value = None
        dd_horas_asig.value = "3"
        txt_nueva_mencion.value = ""
        txt_codigo_mencion.value = ""
        panel_nueva_mencion.visible = False
        asignaturas_temp.clear()
        actualizar_dd_menciones()
        actualizar_dd_asignaturas()
        refrescar_chips_asig()
        e.page.dialog = modal_curso
        modal_curso.open = True
        e.page.update()

    def abrir_modal_editar(cur, e):
        id_actual.value = str(cur["id"])
        dd_year.value = cur["year"]
        dd_seccion.value = cur["seccion"]
        actualizar_dd_menciones()
        actualizar_dd_asignaturas()
        dd_mencion.value = cur["mencion"]
        dd_asignatura.value = None
        dd_horas_asig.value = "3"
        txt_nueva_mencion.value = ""
        txt_codigo_mencion.value = ""
        panel_nueva_mencion.visible = (cur["mencion"] == "__nueva__")
        asignaturas_temp.clear()
        asignaturas_temp.extend([a.copy() for a in cur.get("asignaturas", [])])
        refrescar_chips_asig()
        e.page.dialog = modal_curso
        modal_curso.open = True
        e.page.update()

    def filtrar_cursos(e):
        term = txt_buscar.value.lower()
        cargar_grilla(term)
        e.page.update()

    txt_buscar = ft.TextField(
        hint_text="Busqueda",
        width=320,
        height=40,
        content_padding=ft.padding.only(left=15, right=10),
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        prefix=ft.Icon(ft.icons.SEARCH, color="#A0A0B0", size=20),
        hint_style=ft.TextStyle(color="#5A5D70", size=13),
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=13),
        on_change=filtrar_cursos
    )

    def cargar_grilla(filtro=""):
        grilla_cursos.controls.clear()
        total_asig = 0
        cursos_visibles = 0
        for cur in db_cursos:
            year_str = cur["year"].lower()
            seccion_str = cur["seccion"].lower()
            
            if filtro and (filtro not in year_str and filtro not in seccion_str):
                continue
                
            cursos_visibles += 1
            total_asig += len(cur.get("asignaturas", []))
            chips_asig = ft.Row(wrap=True, spacing=5)
            for asig in cur.get("asignaturas", []):
                bg, col = COLOR_TIPO.get(asig["tipo"], ("#2A2D3E", "#A0A0B0"))
                chips_asig.controls.append(
                    ft.Container(
                        content=ft.Text(f"{asig['nombre']} ({asig['horas']}h)", size=10, color=col),
                        bgcolor=bg, padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        border_radius=8
                    )
                )

            tarjeta = ft.Container(
                width=300, bgcolor="#1E202D", border_radius=15,
                border=ft.border.all(1, "#303346"), padding=0,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column([
                    ft.Container(
                        bgcolor="#2A2D3E", padding=16,
                        border_radius=ft.border_radius.only(top_left=15, top_right=15),
                        content=ft.Row([
                            ft.Icon(ft.icons.CLASS_, color="#5B9BD5", size=24),
                            ft.Column([
                                ft.Text(f"{cur['year']} año — Sección {cur['seccion']}",
                                        color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=15),
                                ft.Text(f"{cur['mencion']} ({cur.get('codigo_mencion', '')})",
                                        color="#5B9BD5", size=12)
                            ], spacing=1, expand=True),
                            ft.Container(
                                content=ft.Text(str(len(cur.get("asignaturas", []))),
                                                size=18, weight=ft.FontWeight.BOLD, color="#5B9BD5"),
                                bgcolor="#13141C", width=36, height=36, border_radius=8,
                                alignment=ft.alignment.center
                            )
                        ], spacing=10)
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=14, vertical=12),
                        content=ft.Column([
                            ft.Text("Asignaturas:", color="#A0A0B0", size=11, weight=ft.FontWeight.BOLD),
                            chips_asig if chips_asig.controls else ft.Text("Sin asignaturas", color="#5A5D70", size=11),
                            ft.Container(height=6),
                            ft.Row([
                                ft.Container(
                                    content=ft.IconButton(ft.icons.EDIT, icon_color="#A0A0B0", icon_size=16,
                                                          on_click=lambda e, c=cur: abrir_modal_editar(c, e)),
                                    bgcolor="#2A2D3E", border_radius=8, width=32, height=32
                                ),
                                ft.Container(
                                    content=ft.IconButton(ft.icons.DELETE, icon_color="#E57373", icon_size=16,
                                                          on_click=lambda e, c=cur: pedir_confirmacion_eliminar(c, e)),
                                    bgcolor="#3E2A2A", border_radius=8, width=32, height=32
                                ),
                            ], spacing=8)
                        ], spacing=4)
                    )
                ], spacing=0)
            )
            grilla_cursos.controls.append(tarjeta)

        txt_total.value = str(cursos_visibles)
        txt_total_asig.value = str(total_asig)

    cargar_grilla()

    tarjeta_stats = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Row([
            ft.Row([
                txt_total,
                ft.Text("Cursos registrados", color="#A0A0B0", size=13)
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.VerticalDivider(color="#303346", width=1),
            ft.Row([
                txt_total_asig,
                ft.Text("Asignaturas asignadas", color="#A0A0B0", size=13)
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    )

    return ft.Container(
        padding=20, expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column([
                            ft.Text("Gestión de Cursos", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text("Administra los cursos, sus menciones y asignaturas", size=14, color="#A0A0B0")
                        ], spacing=2),
                        ft.Row([
                            txt_buscar,
                            ft.ElevatedButton(
                                "Añadir Curso", icon=ft.icons.ADD, on_click=abrir_modal_crear,
                                bgcolor="#439A5D", color=ft.colors.WHITE,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=20)
                            )
                        ], spacing=10)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                tarjeta_stats,
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [ft.Container(content=grilla_cursos, expand=True)],
                        scroll=ft.ScrollMode.AUTO, expand=True
                    )
                )
            ],
            expand=True
        )
    )