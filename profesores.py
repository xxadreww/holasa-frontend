import flet as ft

db_profesores=[
    {"id": 1, "nombre": "Maria", "apellido": "Navarro", "telefono": "04141234567", "correo": "maria.navarro@email.com", "estado": "Activo", "asignaturas": ["Matemática - 1er Año", "Física - 2do Año"], "disponibilidad": {"Lunes": {"inicio": "07:00", "fin": "11:50"}, "Martes": {"inicio": "08:30", "fin": "12:50"}}},
    {"id": 2, "nombre": "Francisco", "apellido": "Isea", "telefono": "", "correo": "francisco.isea@email.com", "estado": "Activo", "asignaturas": ["Telecomunicaciones - 4to Año"], "disponibilidad": {"Miércoles": {"inicio": "07:00", "fin": "09:50"}}},
]

opciones_estado=["Activo", "Inactivo"]
opciones_dias=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
opciones_horas=["07:00", "07:40", "08:30", "09:10", "09:50", "10:30", "11:10", "11:50", "12:10", "12:50", "13:30", "14:10"]
opciones_materias=["Matemática - 1er Año", "Física - 2do Año", "Química - 3er Año", "Castellano - 4to Año", "Telecomunicaciones - 4to Año", "Dibujo Técnico - 5to Año"]

def vista_profesores(on_volver_menu=None):
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
        "data_row_max_height": 70,
    }

    tabla_profesores=ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("Profesor", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Contacto", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Asignaturas / Horarios", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        **estilo_tabla
    )

    txt_total=ft.Text("Profesores registrados: 0", color="#A0A0B0", size=14, weight=ft.FontWeight.W_500)
    
    id_actual=ft.Text(visible=False)
    txt_nombre=ft.TextField(label="Nombre", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE)
    txt_apellido=ft.TextField(label="Apellido", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE)
    txt_telefono=ft.TextField(label="Teléfono (Opcional)", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE)
    txt_correo=ft.TextField(label="Correo Electrónico (Opcional)", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE)
    dd_estado=ft.Dropdown(label="Estado", options=[ft.dropdown.Option(x) for x in opciones_estado], value="Activo", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE)

    asignaturas_seleccionadas=[]
    disponibilidad_configurada={}

    # Lista de elementos en Row con Wrap para que se expandan dinámicamente hacia abajo con scroll
    lista_chips_asignaturas=ft.Row(wrap=True, spacing=5)
    dd_materia_agregar=ft.Dropdown(label="Selecciona asignatura y curso", options=[ft.dropdown.Option(m) for m in opciones_materias], border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE, expand=True)
    
    lista_chips_disponibilidad=ft.Row(wrap=True, spacing=5)
    dd_disp_dia=ft.Dropdown(label="Día", options=[ft.dropdown.Option(d) for d in opciones_dias], value="Lunes", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE, width=110)
    dd_disp_inicio=ft.Dropdown(label="Hora Inicio", options=[ft.dropdown.Option(h) for h in opciones_horas], value="07:00", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE, expand=True)
    dd_disp_fin=ft.Dropdown(label="Hora Final", options=[ft.dropdown.Option(h) for h in opciones_horas], value="11:50", border_radius=10, border_color="#303346", focused_border_color="#439A5D", color=ft.colors.WHITE, expand=True)

    def refrescar_ui_ciclos():
        lista_chips_asignaturas.controls.clear()
        for asig in asignaturas_seleccionadas:
            lista_chips_asignaturas.controls.append(
                ft.Container(
                    bgcolor="#1A2A20", border=ft.border.all(1, "#439A5D"), border_radius=15, padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    content=ft.Row([
                        ft.Text(asig, color="#439A5D", size=12),
                        ft.IconButton(ft.icons.CLOSE, icon_color="#439A5D", icon_size=14, on_click=lambda e, a=asig: remover_materia_ciclo(a, e), width=20, height=20)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER, tight=True)
                )
            )
        
        lista_chips_disponibilidad.controls.clear()
        for d, horas in disponibilidad_configurada.items():
            lista_chips_disponibilidad.controls.append(
                ft.Container(
                    bgcolor="#332415", border=ft.border.all(1, "#E69138"), border_radius=15, padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    content=ft.Row([
                        ft.Text(f"{d}: {horas['inicio']} a {horas['fin']}", color="#E69138", size=12),
                        ft.IconButton(ft.icons.CLOSE, icon_color="#E69138", icon_size=14, on_click=lambda e, dia=d: remover_disponibilidad_ciclo(dia, e), width=20, height=20)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER, tight=True)
                )
            )

    def agregar_materia_ciclo(e):
        if dd_materia_agregar.value and dd_materia_agregar.value not in asignaturas_seleccionadas:
            asignaturas_seleccionadas.append(dd_materia_agregar.value)
            dd_materia_agregar.value=None
            refrescar_ui_ciclos()
            e.page.update()

    def remover_materia_ciclo(asig, e):
        if asig in asignaturas_seleccionadas:
            asignaturas_seleccionadas.remove(asig)
            refrescar_ui_ciclos()
            e.page.update()

    def agregar_disponibilidad_ciclo(e):
        idx_in=opciones_horas.index(dd_disp_inicio.value)
        idx_fi=opciones_horas.index(dd_disp_fin.value)
        if idx_in>=idx_fi:
            e.page.snack_bar=ft.SnackBar(ft.Text("La hora de inicio debe ser menor a la hora final"), bgcolor="#E57373")
            e.page.snack_bar.open=True
            e.page.update()
            return
        
        disponibilidad_configurada[dd_disp_dia.value]={"inicio": dd_disp_inicio.value, "fin": dd_disp_fin.value}
        refrescar_ui_ciclos()
        e.page.update()

    def remover_disponibilidad_ciclo(dia, e):
        if dia in disponibilidad_configurada:
            del disponibilidad_configurada[dia]
            refrescar_ui_ciclos()
            e.page.update()

    def cerrar_modal(e):
        modal_profesor.open=False
        e.page.update()

    def cerrar_modal_info(e):
        modal_info.open=False
        e.page.update()

    def cerrar_modal_confirmacion(e):
        modal_confirmacion.open=False
        e.page.update()

    def cerrar_modal_credenciales(e):
        modal_credenciales.open=False
        e.page.update()

    def pre_guardar_profesor(e):
        nombre=txt_nombre.value.strip()
        apellido=txt_apellido.value.strip()
        tel=txt_telefono.value.strip()
        corr=txt_correo.value.strip()

        if not nombre or not apellido:
            e.page.snack_bar=ft.SnackBar(ft.Text("El nombre y apellido son campos requeridos"), bgcolor="#E57373")
            e.page.snack_bar.open=True
            e.page.update()
            return

        for p in db_profesores:
            if str(p["id"])!=id_actual.value:
                coincide_tel=(tel and p["telefono"]==tel)
                coincide_corr=(corr and p["correo"].lower()==corr.lower())
                if coincide_tel or coincide_corr:
                    # Formatear el aviso de duplicado de forma estética y legible
                    dup_nombre.value=f"{p['nombre']} {p['apellido']}"
                    dup_contacto.value=f"Tel: {p['telefono'] or 'N/P'} | Correo: {p['correo'] or 'N/P'}"
                    e.page.dialog=modal_credenciales
                    modal_credenciales.open=True
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
        apellido=txt_apellido.value.strip()
        tel=txt_telefono.value.strip()
        corr=txt_correo.value.strip()
        es_nuevo=id_actual.value==""

        if es_nuevo:
            nuevo_id=max([p["id"] for p in db_profesores], default=0)+1
            db_profesores.append({
                "id": nuevo_id, "nombre": nombre, "apellido": apellido, "telefono": tel, "correo": corr,
                "estado": dd_estado.value, "asignaturas": list(asignaturas_seleccionadas), "disponibilidad": dict(disponibilidad_configurada)
            })
        else:
            for p in db_profesores:
                if str(p["id"])==id_actual.value:
                    p["nombre"]=nombre
                    p["apellido"]=apellido
                    p["telefono"]=tel
                    p["correo"]=corr
                    p["estado"]=dd_estado.value
                    p["asignaturas"]=list(asignaturas_seleccionadas)
                    p["disponibilidad"]=dict(disponibilidad_configurada)
            cerrar_modal_confirmacion(e)

        if modal_credenciales.open:
            cerrar_modal_credenciales(e)

        cerrar_modal(e)
        cargar_datos()
        txt_buscar.value=""
        
        if es_nuevo:
            e.page.dialog=modal_info
            modal_info.open=True
        e.page.update()

    modal_info=ft.AlertDialog(
        content=ft.Column([
            ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED,color="#439A5D",size=50),
            ft.Text("Éxito",weight=ft.FontWeight.BOLD,color=ft.colors.WHITE,size=16,text_align=ft.TextAlign.CENTER),
            ft.Text("Profesor añadido exitosamente.",color="#A0A0B0",size=13,text_align=ft.TextAlign.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=10,tight=True,width=300),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.ElevatedButton("OK",on_click=cerrar_modal_info,bgcolor="#439A5D",color=ft.colors.WHITE,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    modal_profesor=ft.AlertDialog(
        title=ft.Text("Formulario de Profesor", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=560,
            content=ft.Column([
                id_actual,
                ft.Row([txt_nombre, txt_apellido], spacing=10),
                ft.Row([txt_telefono, txt_correo], spacing=10),
                dd_estado,
                ft.Divider(color="#303346", height=10),
                
                ft.Text("Asignaturas y Cursos", size=14, weight=ft.FontWeight.BOLD, color="#5B9BD5"),
                ft.Row([dd_materia_agregar, ft.IconButton(ft.icons.ADD_CIRCLE, icon_color="#439A5D", icon_size=32, on_click=agregar_materia_ciclo)], spacing=5),
                lista_chips_asignaturas,
                ft.Divider(color="#303346", height=10),

                ft.Text("Disponibilidad Horaria Diaria", size=14, weight=ft.FontWeight.BOLD, color="#E69138"),
                ft.Row([dd_disp_dia, dd_disp_inicio, dd_disp_fin, ft.IconButton(ft.icons.ADD_CIRCLE, icon_color="#E69138", icon_size=32, on_click=agregar_disponibilidad_ciclo)], spacing=5),
                lista_chips_disponibilidad,
                
            ], spacing=15, scroll=ft.ScrollMode.AUTO, tight=True, height=500) # Pasamos el control de altura aquí para activar el scroll dinámico
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_modal, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Guardar Registro", on_click=pre_guardar_profesor, bgcolor="#439A5D", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_padding=20
    )

    # Variables estéticas para el modal de duplicados, asemejándose a "Ver Información"
    dup_nombre=ft.Text(size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    dup_contacto=ft.Text(color="#A0A0B0", size=13)
    modal_credenciales=ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.icons.WARNING_ROUNDED, color="#E69138", size=28),
            ft.Text("Credenciales Duplicadas", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        ], spacing=10),
        content=ft.Container(
            width=480,
            content=ft.Column([
                ft.Text("Ya existe un docente con estos datos de contacto en el sistema:", color="#A0A0B0", size=13),
                ft.Container(
                    bgcolor="#13141C", padding=15, border_radius=10, border=ft.border.all(1, "#303346"),
                    content=ft.Row([
                        ft.Icon(ft.icons.ACCOUNT_BOX, size=40, color="#E69138"),
                        ft.Column([dup_nombre, dup_contacto], spacing=2)
                    ], spacing=10)
                ),
                ft.Text("¿Está completamente seguro de que desea registrar este duplicado?", color="#A0A0B0", size=13)
            ], spacing=15, tight=True)
        ),
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions=[
            ft.TextButton("No, Cancelar", on_click=cerrar_modal_credenciales, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Forzar Registro", on_click=ejecutar_guardado, bgcolor="#E69138", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_padding=20
    )

    modal_confirmacion=ft.AlertDialog(
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        actions_padding=20,
        actions_alignment=ft.MainAxisAlignment.END
    )

    # Componentes para la funcionalidad de Visualización (Ver Info) recuperada
    info_nombre=ft.Text(size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    info_contacto=ft.Text(color="#A0A0B0", size=13)
    info_estado_badge=ft.Container(padding=ft.padding.symmetric(horizontal=10, vertical=5), border_radius=15)
    info_asignaturas=ft.Row(wrap=True, spacing=5)
    seccion_info_disp=ft.Column(spacing=10)

    def cerrar_modal_ver(e):
        modal_ver.open=False
        e.page.update()

    modal_ver=ft.AlertDialog(
        bgcolor="#1E202D",
        shape=ft.RoundedRectangleBorder(radius=15),
        content=ft.Container(
            width=480,
            padding=10,
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=50, color="#439A5D"),
                    ft.Column([
                        info_nombre,
                        ft.Row([info_estado_badge, info_contacto], alignment=ft.MainAxisAlignment.START, spacing=10)
                    ], spacing=2)
                ]),
                ft.Divider(color="#5A5D70", height=20, thickness=1.5),
                ft.Text("Asignaturas y Cursos Asignados", color="#A0A0B0", size=13, weight=ft.FontWeight.BOLD),
                info_asignaturas,
                ft.Divider(color="#5A5D70", height=20, thickness=1.5),
                ft.Text("Horario de Disponibilidad Semanal", color="#E69138", size=13, weight=ft.FontWeight.BOLD),
                seccion_info_disp
            ], tight=True, scroll=ft.ScrollMode.AUTO)
        ),
        actions=[
            ft.ElevatedButton("Cerrar", on_click=cerrar_modal_ver, bgcolor="#439A5D", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions_padding=20
    )

    def abrir_modal_ver(prof, e):
        info_nombre.value=f"{prof['nombre']} {prof['apellido']}"
        tel=prof['telefono'] if prof['telefono'] else "Sin teléfono"
        corr=prof['correo'] if prof['correo'] else "Sin correo"
        info_contacto.value=f"{tel} | {corr}"
        
        info_estado_badge.content=ft.Text(prof["estado"], size=11, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
        info_estado_badge.bgcolor="#2D6B3F" if prof["estado"] == "Activo" else "#E57373"
        
        info_asignaturas.controls.clear()
        for asig in prof["asignaturas"]:
            info_asignaturas.controls.append(ft.Container(content=ft.Text(asig, size=12, color=ft.colors.WHITE), bgcolor="#2A2D3E", padding=ft.padding.symmetric(horizontal=10, vertical=5), border_radius=15))

        seccion_info_disp.controls.clear()
        if prof["disponibilidad"]:
            for dia, horas in prof["disponibilidad"].items():
                seccion_info_disp.controls.append(
                    ft.Container(
                        bgcolor="#332415", padding=10, border_radius=10, border=ft.border.all(1, "#E69138"),
                        content=ft.Row([
                            ft.Text(dia, color="#E69138", weight=ft.FontWeight.BOLD, size=13, width=80),
                            ft.Icon(ft.icons.ARROW_FORWARD, size=14, color="#A0A0B0"),
                            ft.Text(f"{horas['inicio']} a {horas['fin']}", color=ft.colors.WHITE, size=13)
                        ], alignment=ft.MainAxisAlignment.START)
                    )
                )
        else:
            seccion_info_disp.controls.append(ft.Text("No se ha configurado disponibilidad horaria.", color="#A0A0B0", size=13))

        e.page.dialog=modal_ver
        modal_ver.open=True
        e.page.update()

    def pedir_confirmacion_eliminar(prof, e):
        modal_confirmacion.title=ft.Text("¿Confirmar Eliminación?", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        modal_confirmacion.content=ft.Text(f"¿Está seguro de que desea eliminar al docente '{prof['nombre']} {prof['apellido']}' del plantel?", color="#A0A0B0")
        modal_confirmacion.actions=[
            ft.TextButton("No, Cancelar", on_click=cerrar_modal_confirmacion, style=ft.ButtonStyle(color="#A0A0B0")),
            ft.ElevatedButton("Sí, Confirmar", on_click=lambda ex: ejecutar_eliminacion(prof["id"], ex), bgcolor="#E57373", color=ft.colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ]
        e.page.dialog=modal_confirmacion
        modal_confirmacion.open=True
        e.page.update()

    def ejecutar_eliminacion(prof_id, e):
        global db_profesores
        db_profesores=[p for p in db_profesores if p["id"]!=prof_id]
        cerrar_modal_confirmacion(e)
        cargar_datos()
        txt_buscar.value=""
        e.page.update()

    def abrir_modal_crear(e):
        id_actual.value=""
        txt_nombre.value=""
        txt_apellido.value=""
        txt_telefono.value=""
        txt_correo.value=""
        dd_estado.value="Activo"
        
        asignaturas_seleccionadas.clear()
        disponibilidad_configurada.clear()
        dd_materia_agregar.value=None
        refrescar_ui_ciclos()
        
        e.page.dialog=modal_profesor
        modal_profesor.open=True
        e.page.update()

    def abrir_modal_editar(prof, e):
        id_actual.value=str(prof["id"])
        txt_nombre.value=prof["nombre"]
        txt_apellido.value=prof["apellido"]
        txt_telefono.value=prof.get("telefono", "")
        txt_correo.value=prof.get("correo", "")
        dd_estado.value=prof.get("estado", "Activo")
        
        asignaturas_seleccionadas.clear()
        asignaturas_seleccionadas.extend(prof.get("asignaturas", []))
        
        disponibilidad_configurada.clear()
        disponibilidad_configurada.update(prof.get("disponibilidad", {}))
        
        dd_materia_agregar.value=None
        refrescar_ui_ciclos()
        
        e.page.dialog=modal_profesor
        modal_profesor.open=True
        e.page.update()

    def filtrar_profesores(e):
        term=txt_buscar.value.lower()
        cargar_datos(term)
        e.page.update()

    txt_buscar=ft.TextField(
        hint_text="Buscar profesor por nombre, apellido o contacto",
        width=320,
        height=40,
        content_padding=ft.padding.only(left=15, right=10),
        border_radius=10,
        border_color="#303346",
        focused_border_color="#439A5D",
        prefix=ft.Icon(ft.icons.SEARCH, color="#A0A0B0", size=20),
        hint_style=ft.TextStyle(color="#5A5D70", size=13),
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=13),
        on_change=filtrar_profesores
    )

    def cargar_datos(filtro=""):
        tabla_profesores.rows.clear()
        for p in db_profesores:
            nom=p["nombre"].lower()
            ape=p["apellido"].lower()
            tel=p.get("telefono", "").lower()
            cor=p.get("correo", "").lower()
            
            if filtro and (filtro not in nom and filtro not in ape and filtro not in tel and filtro not in cor):
                continue

            estado_activo=p.get("estado", "Activo")=="Activo"
            bg_est, col_est=("#1A2A20", "#439A5D") if estado_activo else ("#3E2A2A", "#E57373")

            mats=", ".join(p.get("asignaturas", [])) if p.get("asignaturas") else "Ninguna"
            
            disps=[]
            for d, h in p.get("disponibilidad", {}).items():
                disps.append(f"{d[0:2]}: {h['inicio']}-{h['fin']}")
            disp_str=" | ".join(disps) if disps else "Sin horario"

            tabla_profesores.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Row([
                    ft.Icon(ft.icons.PERSON, color="#5B9BD5" if estado_activo else "#A0A0B0", size=18),
                    ft.Text(f"{p['nombre']} {p['apellido']}", color=ft.colors.WHITE, weight=ft.FontWeight.W_500)
                ])),
                ft.DataCell(ft.Column([
                    ft.Text(p.get("correo", "Sin correo"), color="#A0A0B0", size=12, weight=ft.FontWeight.W_400),
                    ft.Text(p.get("telefono", "Sin telf"), color="#6C7A89", size=11)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=1)),
                ft.DataCell(ft.Container(
                    content=ft.Text(p.get("estado", "Activo"), size=11, color=col_est, weight=ft.FontWeight.BOLD),
                    bgcolor=bg_est, padding=ft.padding.symmetric(horizontal=10, vertical=4), border_radius=10
                )),
                ft.DataCell(ft.Column([
                    ft.Container(width=240, content=ft.Text(f"Asig: {mats}", color="#A0A0B0", size=11, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS)),
                    ft.Container(width=240, content=ft.Text(f"Disp: {disp_str}", color="#E69138", size=11, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=2)),
                ft.DataCell(ft.Row([
                    ft.Container(content=ft.IconButton(ft.icons.VISIBILITY, icon_color="#439A5D", icon_size=16, on_click=lambda e, pr=p: abrir_modal_ver(pr, e)), bgcolor="#1A2A20", border_radius=8, width=32, height=32),
                    ft.Container(content=ft.IconButton(ft.icons.EDIT, icon_color="#A0A0B0", icon_size=16, on_click=lambda e, pr=p: abrir_modal_editar(pr, e)), bgcolor="#2A2D3E", border_radius=8, width=32, height=32),
                    ft.Container(content=ft.IconButton(ft.icons.DELETE, icon_color="#E57373", icon_size=16, on_click=lambda e, pr=p: pedir_confirmacion_eliminar(pr, e)), bgcolor="#3E2A2A", border_radius=8, width=32, height=32),
                ], spacing=10))
            ]))
        txt_total.value=f"Profesores registrados: {len(db_profesores)}"

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
                                ft.Text("Gestión de Profesores", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Administra el plantel docente y sus asignaciones correspondientes", size=14, color="#A0A0B0")
                            ], spacing=2)
                        ]),
                        ft.ElevatedButton(
                            "Añadir Profesor",
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
                                ft.Icon(ft.icons.PEOPLE, color="#439A5D"),
                                ft.Text("Plantel Docente Registrado", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
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
                                            content=tabla_profesores
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