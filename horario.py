import flet as ft

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
BLOQUES = [
    "7:00 - 7:40", "7:40 - 8:20", "8:30 - 9:10", "9:10 - 9:50",
    "9:50 - 10:30", "10:30 - 11:10", "11:10 - 11:50",
    "12:10 - 12:50", "12:50 - 1:30", "1:30 - 2:10"
]
RECESO = "11:50 - 12:10"

CURSOS_DEMO = [
    "4to - EO - A", "4to - EO - B", "4to - EL - A",
    "4to - MM - A", "4to - MT - A", "5to - EO - A", "5to - EL - A"
]

HORARIO_DEMO = {
    "4to - EO - A": {
        "Lunes":     ["Matemáticas / Prof. Navarro / Aula 3", "Matemáticas / Prof. Navarro / Aula 3", "Física / Prof. Isea / Aula 5",
                      "Física / Prof. Isea / Aula 5", "", "Circ. Eléctricos / Prof. Peraza / Taller 2", "Circ. Eléctricos / Prof. Peraza / Taller 2",
                      "Ed. Física / - / Cancha", "Ed. Física / - / Cancha", ""],
        "Martes":    ["Lenguaje / Prof. López / Aula 1", "Lenguaje / Prof. López / Aula 1", "", "",
                      "Sist. Digitales / Prof. Isea / Lab 1", "Sist. Digitales / Prof. Isea / Lab 1", "",
                      "Matemáticas / Prof. Navarro / Aula 3", "Matemáticas / Prof. Navarro / Aula 3", ""],
        "Miércoles": ["Física / Prof. Isea / Aula 5", "Física / Prof. Isea / Aula 5", "", "Circ. Eléctricos / Prof. Peraza / Taller 2",
                      "Circ. Eléctricos / Prof. Peraza / Taller 2", "", "Lenguaje / Prof. López / Aula 1",
                      "", "", ""],
        "Jueves":    ["Sist. Digitales / Prof. Isea / Lab 1", "Sist. Digitales / Prof. Isea / Lab 1", "",
                      "Matemáticas / Prof. Navarro / Aula 3", "Matemáticas / Prof. Navarro / Aula 3",
                      "Ed. Física / - / Cancha", "Ed. Física / - / Cancha", "", "", ""],
        "Viernes":   ["Circ. Eléctricos / Prof. Peraza / Taller 2", "Circ. Eléctricos / Prof. Peraza / Taller 2",
                      "Lenguaje / Prof. López / Aula 1", "", "Física / Prof. Isea / Aula 5", "Física / Prof. Isea / Aula 5",
                      "", "Sist. Digitales / Prof. Isea / Lab 1", "Sist. Digitales / Prof. Isea / Lab 1", ""],
    }
}

COLORES_MATERIAS = {}
PALETA = ["#1A3A5C", "#1A2A20", "#332415", "#1A3A38", "#2A2D3E", "#3A1A2A", "#1C2A40"]

def color_materia(nombre):
    if not nombre:
        return None
    key = nombre.split("/")[0].strip()
    if key not in COLORES_MATERIAS:
        COLORES_MATERIAS[key] = PALETA[len(COLORES_MATERIAS) % len(PALETA)]
    return COLORES_MATERIAS[key]

def color_texto_materia(nombre):
    if not nombre:
        return None
    key = nombre.split("/")[0].strip()
    paleta_texto = ["#5B9BD5", "#439A5D", "#E69138", "#76C7C0", "#C0C0C0", "#E091C0", "#8FBBDE"]
    idx = list(COLORES_MATERIAS.keys()).index(key) if key in COLORES_MATERIAS else 0
    return paleta_texto[idx % len(paleta_texto)]


def vista_horario():
    estilo_tarjeta_oscura = {
        "bgcolor": "#1E202D",
        "border_radius": 15,
        "padding": 20,
        "border": ft.border.all(1, "#303346")
    }

    curso_actual = ft.Ref[ft.Dropdown]()
    grilla_ref = ft.Column(spacing=0)

    dd_curso = ft.Dropdown(
        ref=curso_actual,
        label="Seleccionar Curso",
        options=[ft.dropdown.Option(c) for c in CURSOS_DEMO],
        value=CURSOS_DEMO[0],
        border_color="#303346", focused_border_color="#439A5D", border_radius=10,
        bgcolor="#13141C", color=ft.colors.WHITE, width=260
    )

    def celda_clase(contenido, is_receso=False):
        if is_receso:
            return ft.Container(
                height=38, bgcolor="#0F1018",
                border=ft.border.all(1, "#303346"),
                content=ft.Text("RECESO", color="#5A5D70", size=11, italic=True,
                                 text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center
            )
        if not contenido:
            return ft.Container(
                height=50,
                bgcolor="#13141C",
                border=ft.border.all(1, "#222435"),
            )
        partes = contenido.split(" / ")
        materia = partes[0] if len(partes) > 0 else ""
        profesor = partes[1] if len(partes) > 1 else ""
        aula = partes[2] if len(partes) > 2 else ""
        bg = color_materia(materia) or "#1E202D"
        col = color_texto_materia(materia) or "#A0A0B0"
        return ft.Container(
            height=50,
            bgcolor=bg,
            border=ft.border.all(1, "#303346"),
            padding=ft.padding.symmetric(horizontal=6, vertical=4),
            content=ft.Column([
                ft.Text(materia, color=col, size=11, weight=ft.FontWeight.BOLD,
                        overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
                ft.Text(f"{profesor}", color="#A0A0B0", size=10, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Text(aula, color="#5A5D70", size=9),
            ], spacing=1)
        )

    def celda_hora(hora, is_receso=False):
        return ft.Container(
            width=100, height=50 if not is_receso else 38,
            bgcolor="#1A1C28" if not is_receso else "#0F1018",
            border=ft.border.all(1, "#303346"),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            content=ft.Text(hora, color="#A0A0B0" if not is_receso else "#5A5D70",
                            size=10, text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center
        )

    def celda_cabecera(texto, ancho=None):
        return ft.Container(
            width=ancho, expand=True if not ancho else False,
            height=40, bgcolor="#1A1C28",
            border=ft.border.all(1, "#303346"),
            content=ft.Text(texto, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                            size=12, text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center
        )

    def construir_grilla(curso):
        grilla_ref.controls.clear()
        horario = HORARIO_DEMO.get(curso, {d: [""] * len(BLOQUES) for d in DIAS})
        fila_header = ft.Row([celda_hora("Hora", is_receso=False)] +
                              [celda_cabecera(d) for d in DIAS], spacing=0)
        grilla_ref.controls.append(fila_header)
        for i, bloque in enumerate(BLOQUES):
            fila = [celda_hora(bloque)]
            for dia in DIAS:
                celdas_dia = horario.get(dia, [""] * len(BLOQUES))
                contenido = celdas_dia[i] if i < len(celdas_dia) else ""
                fila.append(ft.Container(expand=True, content=celda_clase(contenido)))
            grilla_ref.controls.append(ft.Row(fila, spacing=0))
            if i == 6:
                fila_receso = [celda_hora(RECESO, is_receso=True)] + [
                    ft.Container(expand=True, content=celda_clase("", is_receso=True)) for _ in DIAS
                ]
                grilla_ref.controls.append(ft.Row(fila_receso, spacing=0))
    def cambiar_curso(e):
        construir_grilla(dd_curso.value)
        e.page.update()

    dd_curso.on_change = cambiar_curso
    construir_grilla(CURSOS_DEMO[0])

    def stat_chip(icono, texto, color, bgcolor):
        return ft.Container(
            bgcolor=bgcolor, border_radius=10, padding=ft.padding.symmetric(horizontal=12, vertical=8),
            content=ft.Row([ft.Icon(icono, color=color, size=16), ft.Text(texto, color=color, size=12, weight=ft.FontWeight.BOLD)])
        )

    # --- NUEVOS BOTONES DE ACCIÓN ---
    btn_ver = ft.IconButton(
        icon=ft.icons.VISIBILITY,
        icon_color="#439A5D",
        tooltip="Vista Previa",
        bgcolor="#1A2A20",
        on_click=lambda _: print("Ver horario")
    )
    
    btn_descargar = ft.IconButton(
        icon=ft.icons.FILE_DOWNLOAD_ROUNDED,
        icon_color="#5B9BD5",
        tooltip="Descargar Horario",
        bgcolor="#1A3A5C",
        on_click=lambda _: print("Descargar horario")
    )

    barra_superior = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Row([
            ft.Column([
                ft.Text("Vista de Horario", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Horario generado", size=12, color="#A0A0B0")
            ], spacing=2, expand=True),
            dd_curso,
            stat_chip(ft.icons.CHECK_CIRCLE, "Generado", "#439A5D", "#1A2A20"),
            stat_chip(ft.icons.CALENDAR_TODAY, "2024-2", "#5B9BD5", "#1A3A5C"),
            btn_ver,
            btn_descargar,
        ], spacing=15, alignment=ft.CrossAxisAlignment.CENTER)
    )

    tarjeta_grilla = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.GRID_ON, color="#439A5D"),
                ft.Text("Horario Semanal", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.TextButton("Exportar PDF", icon=ft.icons.PICTURE_AS_PDF, style=ft.ButtonStyle(color="#5B9BD5")),
            ]),
            ft.Container(
                content=ft.Column([grilla_ref], scroll=ft.ScrollMode.AUTO),
                expand=True
            )
        ], spacing=15, expand=True)
    )

    return ft.Container(
        padding=20, expand=True,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column([
                            ft.Text("Horario Generado", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text("Visualización del horario por curso y sección", size=14, color="#A0A0B0")
                        ], spacing=2),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                barra_superior,
                ft.Container(height=5),
                ft.Column([tarjeta_grilla], expand=True, scroll=ft.ScrollMode.AUTO),
            ],
            expand=True
        )
    )