import flet as ft

def vista_dashboard(on_navigate=None):
    estilo_tarjeta_oscura = {
        "bgcolor": "#1E202D",
        "border_radius": 15,
        "padding": 20,
        "border": ft.border.all(1, "#303346")
    }

    def navegar(destino, e):
        if on_navigate:
            on_navigate(destino)

    def fila_info(etiqueta, valor, color_valor="#A0A0B0"):
        return ft.Row([
            ft.Text(etiqueta, color="#A0A0B0", size=13),
            ft.Text(valor, color=color_valor, size=13, weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    tarjeta_institucion = ft.Container(
        bgcolor="#1B4D2E",
        border_radius=15, 
        padding=20,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.SCHOOL, color="#FFFFFF", size=22),
                ft.Text("E.T.I Fundación la Salle de Ciencias Naturales",
                        size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF", expand=True)
            ], spacing=10),
            ft.Container(height=4),
            fila_info("Sede:", "Ciudad Guayana, San Félix", "#FFFFFF"),
            fila_info("Año Académico:", "2024-2", "#FFFFFF"),
            fila_info("Estado del Sistema:", "Operativo", "#FFFFFF"),
        ], spacing=8)
    )

    def tarjeta_accion(icono, titulo, descripcion, color_icono, color_bg, color_borde, on_click):
        return ft.Container(
            bgcolor=color_bg, 
            border_radius=12, 
            padding=18,
            border=ft.border.all(1, color_borde), 
            expand=True,
            on_click=on_click, 
            ink=True,
            content=ft.Column([
                ft.Icon(icono, color=color_icono, size=28),
                ft.Container(height=6),
                ft.Text(titulo, color=ft.colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                ft.Text(descripcion, color="#A0A0B0", size=11),
            ], spacing=4)
        )

    tarjeta_generar = ft.Container(
        bgcolor="#1E202D", 
        border_radius=15, 
        padding=20,
        border=ft.border.all(1, "#439A5D"),
        content=ft.Column([
            ft.Row([
                ft.Text("Generar Horarios", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
            ], spacing=10),
            ft.Container(height=4),
            ft.Text(
                "Inicia el proceso de generación automática del horario académico para el período activo.",
                color="#A0A0B0", size=13
            ),
            ft.Container(height=10),
            ft.ElevatedButton(
                "Iniciar Generación",
                icon=ft.icons.PLAY_ARROW,
                bgcolor="#439A5D", 
                color=ft.colors.WHITE, 
                height=46, 
                expand=False,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda e: navegar("generacion", e)
            )
        ], spacing=4)
    )

    tarjeta_db = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.STORAGE, color="#5B9BD5", size=22),
                ft.Text("Administrar Base de Datos", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
            ], spacing=10),
            ft.Container(height=4),
            ft.Text(
                "Gestiona los registros de profesores, cursos, menciones, asignaturas, salones y sesiones.",
                color="#A0A0B0", size=13
            ),
            ft.Container(height=12),
            ft.Row([
                tarjeta_accion(
                    ft.icons.PEOPLE, "Profesores", "Gestiona el plantel docente",
                    "#439A5D", "#1A2A20", "#439A5D",
                    lambda e: navegar("profesores", e)
                ),
                tarjeta_accion(
                    ft.icons.CLASS_, "Cursos", "Años, secciones y menciones",
                    "#5B9BD5", "#1A3A5C", "#5B9BD5",
                    lambda e: navegar("cursos", e)
                ),
            ], spacing=12),
            ft.Row([
                tarjeta_accion(
                    ft.icons.LABEL, "Menciones", "Menciones técnicas disponibles",
                    "#76C7C0", "#1A3A38", "#76C7C0",
                    lambda e: navegar("menciones", e)
                ),
                tarjeta_accion(
                    ft.icons.BOOK, "Asignaturas", "Materias y clasificaciones",
                    "#E69138", "#332415", "#E69138",
                    lambda e: navegar("materias", e)
                ),
            ], spacing=12),
            ft.Row([
                tarjeta_accion(
                    ft.icons.MEETING_ROOM, "Salones", "Espacios físicos disponibles",
                    "#C0C0C0", "#2A2D3E", "#C0C0C0",
                    lambda e: navegar("salones", e)
                ),
                tarjeta_accion(
                    ft.icons.ACCESS_TIME, "Sesiones", "Bloques horarios por día",
                    "#E091C0", "#3A1A2A", "#E091C0",
                    lambda e: navegar("sesiones", e)
                ),
            ], spacing=12),
        ], spacing=12)
    )

    tarjeta_stats = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            ft.Text("Resumen del Sistema", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Divider(color="#303346", height=8),
            ft.Row([
                ft.Container(
                    bgcolor="#1A2A20", border_radius=10, padding=12, expand=True,
                    content=ft.Column([
                        ft.Text("42", size=26, weight=ft.FontWeight.BOLD, color="#439A5D"),
                        ft.Text("Profesores", size=11, color="#439A5D")
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
                ft.Container(
                    bgcolor="#1A3A5C", border_radius=10, padding=12, expand=True,
                    content=ft.Column([
                        ft.Text("7", size=26, weight=ft.FontWeight.BOLD, color="#5B9BD5"),
                        ft.Text("Cursos", size=11, color="#5B9BD5")
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
            ], spacing=10),
            ft.Row([
                ft.Container(
                    bgcolor="#332415", border_radius=10, padding=12, expand=True,
                    content=ft.Column([
                        ft.Text("8", size=26, weight=ft.FontWeight.BOLD, color="#E69138"),
                        ft.Text("Asignaturas", size=11, color="#E69138")
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
                ft.Container(
                    bgcolor="#2A2D3E", border_radius=10, padding=12, expand=True,
                    content=ft.Column([
                        ft.Text("7", size=26, weight=ft.FontWeight.BOLD, color="#C0C0C0"),
                        ft.Text("Salones", size=11, color="#C0C0C0")
                    ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ),
            ], spacing=10),
            ft.Divider(color="#303346", height=8),
            ft.Row([
                ft.Container(content=ft.Text("2 Docentes con Prioridad", color="#E69138", size=11),
                             bgcolor="#332415", padding=8, border_radius=8),
                ft.Container(content=ft.Text("5 Menciones activas", color="#76C7C0", size=11),
                             bgcolor="#1A3A38", padding=8, border_radius=8)
            ], spacing=8, wrap=True),
        ], spacing=10)
    )

    tarjeta_horario_actual = ft.Container(
        **estilo_tarjeta_oscura,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.CALENDAR_TODAY, color="#5B9BD5", size=18),
                ft.Text("Último Horario", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text("Generado", color="#439A5D", size=11, weight=ft.FontWeight.BOLD),
                    bgcolor="#1A2A20", padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=8, border=ft.border.all(1, "#439A5D")
                )
            ]),
            ft.Divider(color="#303346", height=8),
            fila_info("Período:", "2024-2"),
            fila_info("Generado el:", "15/06/2024"),
            fila_info("Cursos cubiertos:", "7 de 7"),
            fila_info("Conflictos:", "0"),
            ft.Container(height=6),
            ft.TextButton(
                "Ver Horario Completo",
                icon=ft.icons.ARROW_FORWARD,
                style=ft.ButtonStyle(color="#5B9BD5"),
                on_click=lambda e: navegar("horario", e)
            )
        ], spacing=8)
    )

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column([
                            ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text("Sistema de Gestión de Horarios Académicos", size=14, color="#A0A0B0")
                        ], spacing=2),
                    ]
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.ListView(
                    expand=True,
                    spacing=20,
                    padding=ft.padding.only(bottom=20),
                    controls=[
                        ft.Row(
                            expand=True,
                            spacing=20,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Column(expand=5, spacing=20, controls=[
                                    tarjeta_institucion,
                                    tarjeta_generar,
                                ]),
                                ft.Column(expand=7, spacing=20, controls=[
                                    tarjeta_horario_actual,
                                ])
                            ]
                        ),
                        ft.Container(
                            content=tarjeta_db,
                        ),
                        ft.Container(
                            content=tarjeta_stats,
                        ),
                    ]
                )
            ],
            expand=True
        )
    )