import flet as ft
from dashboard import vista_dashboard
from profesores import vista_profesores
from materias import vista_materias
from menciones import vista_menciones
from sesiones import vista_sesiones
from salones import vista_salones
from cursos import vista_cursos
from generacion import vista_generacion
from horario import vista_horario

NAV_ITEMS = [
    {"id": "dashboard",  "label": "Dashboard",    "icono": ft.icons.DASHBOARD_OUTLINED,     "icono_sel": ft.icons.DASHBOARD},
    {"id": "generacion", "label": "Generar",      "icono": ft.icons.AUTO_FIX_HIGH,          "icono_sel": ft.icons.AUTO_FIX_HIGH},
    {"id": "horario",    "label": "Horario",       "icono": ft.icons.CALENDAR_TODAY_OUTLINED,"icono_sel": ft.icons.CALENDAR_TODAY},
    None,
    {"id": "profesores", "label": "Profesores",   "icono": ft.icons.PEOPLE_OUTLINE,         "icono_sel": ft.icons.PEOPLE},
    {"id": "cursos",     "label": "Cursos",        "icono": ft.icons.CLASS_,                 "icono_sel": ft.icons.CLASS_},
    {"id": "menciones",  "label": "Menciones",     "icono": ft.icons.LABEL_OUTLINE,          "icono_sel": ft.icons.LABEL},
    {"id": "materias",   "label": "Asignaturas",   "icono": ft.icons.BOOK_OUTLINED,          "icono_sel": ft.icons.BOOK},
    {"id": "salones",    "label": "Salones",        "icono": ft.icons.MEETING_ROOM_OUTLINED,  "icono_sel": ft.icons.MEETING_ROOM},
    {"id": "sesiones",   "label": "Sesiones",       "icono": ft.icons.ACCESS_TIME,            "icono_sel": ft.icons.ACCESS_TIME_FILLED},
]

def main(page: ft.Page):
    page.title = "E.T.I Fundación La Salle - HOLASA"
    page.bgcolor = "#13141C"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 1100
    page.window_min_height = 700

    vista_actual = ft.Ref[str]()
    vista_actual.current = "dashboard"

    contenido = ft.Container(expand=True)
    nav_controls = {}

    def construir_item_nav(item, seleccionado=False):
        if item is None:
            return ft.Divider(color="#303346", height=1, thickness=1)

        color_act = "#439A5D"
        color_inact = "#A0A0B0"
        color = color_act if seleccionado else color_inact
        icono = item["icono_sel"] if seleccionado else item["icono"]

        return ft.Container(
            key=item["id"],
            bgcolor="#2A2D3E" if seleccionado else ft.colors.TRANSPARENT,
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            margin=ft.margin.symmetric(horizontal=8, vertical=2),
            border=ft.border.all(1, "#439A5D") if seleccionado else ft.border.all(0, ft.colors.TRANSPARENT),
            on_click=lambda e, v=item["id"]: cambiar_vista(v, e),
            ink=True,
            content=ft.Row([
                ft.Icon(icono, color=color, size=19),
                ft.Text(item["label"], color=color, size=13,
                        weight=ft.FontWeight.BOLD if seleccionado else ft.FontWeight.NORMAL)
            ], spacing=10)
        )

    nav_column = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    def refrescar_nav(vista_sel):
        nav_column.controls.clear()
        for item in NAV_ITEMS:
            nav_column.controls.append(
                construir_item_nav(item, seleccionado=(item is not None and item["id"] == vista_sel))
            )

    def cargar_vista(vista_id):
        if vista_id == "dashboard":
            return vista_dashboard(on_navigate=lambda v, e=None: cambiar_vista_simple(v))
        elif vista_id == "profesores":
            return vista_profesores()
        elif vista_id == "materias":
            return vista_materias()
        elif vista_id == "menciones":
            return vista_menciones()
        elif vista_id == "sesiones":
            return vista_sesiones()
        elif vista_id == "salones":
            return vista_salones()
        elif vista_id == "cursos":
            return vista_cursos()
        elif vista_id == "generacion":
            return vista_generacion()
        elif vista_id == "horario":
            return vista_horario()
        return ft.Text("Vista no encontrada", color=ft.colors.WHITE)

    def cambiar_vista_simple(vista_id):
        vista_actual.current = vista_id
        contenido.content = cargar_vista(vista_id)
        refrescar_nav(vista_id)
        page.update()

    def cambiar_vista(vista_id, e=None):
        cambiar_vista_simple(vista_id)

    refrescar_nav("dashboard")
    contenido.content = cargar_vista("dashboard")

    sidebar = ft.Container(
        width=200,
        bgcolor="#1E202D",
        border=ft.border.only(right=ft.border.BorderSide(1, "#303346")),
        content=ft.Column([
            ft.Container(
                bgcolor="#13141C",
                padding=ft.padding.symmetric(horizontal=16, vertical=18),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.SCHEDULE, color="#439A5D", size=22),
                        ft.Text("HOLASA", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                    ], spacing=8),
                    ft.Text("Gestión Académica", size=10, color="#5A5D70")
                ], spacing=2)
            ),
            ft.Divider(color="#303346", height=1, thickness=1),
            ft.Container(
                padding=ft.padding.only(top=8, bottom=8),
                expand=True,
                content=nav_column
            ),
            ft.Divider(color="#303346", height=1, thickness=1),
            ft.Container(
                padding=16,
                content=ft.Column([
                    ft.Text("Realizado en: 2026", color="#5A5D70", size=10),
                    ft.Text("E.T.I Fundación La Salle", color="#5A5D70", size=10),
                ], spacing=2)
            )
        ], spacing=0, expand=True)
    )

    page.add(
        ft.Row([
            sidebar,
            ft.Container(expand=True, content=contenido, bgcolor="#13141C")
        ], spacing=0, expand=True)
    )

ft.app(target=main)
