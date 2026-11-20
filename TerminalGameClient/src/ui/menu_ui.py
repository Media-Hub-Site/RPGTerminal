from utils.common import time, os
from utils.console import console, Panel
from core import UI_MAP


def bienvenida():
    try:
        os.system("cls")
        UI_MAP['intro']()
        from ui.animations import play_intro_animation
        play_intro_animation()
    except Exception:
        pass

def volver_a_jugar_UI():
    console.print("[yellow]Gracias por jugar[/yellow]") # estos textos son amarillos
    console.rule()
    console.print("[yellow]Juego terminado[/yellow]")
    time.sleep(2.5)
    console.print("\n¿Deseas volver a jugar?")
    console.print("1 = SI\n2 = NON")

    
def eleccion_UI():
    from ui.sprites import render_sprite_rich
    from rich.table import Table
    os.system("cls")

    # Matriz con los 10 personajes en 2 filas de 5 columnas
    personajes_fila1 = [
        ("1", "Naruto", "Viento"),
        ("2", "Sasuke", "Fuego"),
        ("3", "Goku", "Ki"),
        ("4", "Vegeta", "Ki"),
        ("5", "Ichigo", "Espíritu"),
    ]
    personajes_fila2 = [
        ("6", "Aizen", "Kido"),
        ("7", "Kyo", "Fuego"),
        ("8", "Iori", "Llama"),
        ("9", "Kazuha", "Anemo"),
        ("10", "Alhacen", "Dendro"),
    ]

    grid = Table.grid(padding=(0, 2), expand=True)
    for _ in range(5):
        grid.add_column(justify="center", ratio=1)

    # Fila 1: Sprites, nombres y elementos
    sprites_f1 = [render_sprite_rich(name, facing="right", pose="idle") for _, name, _ in personajes_fila1]
    labels_f1 = [f"[bold yellow]{num}.[/bold yellow] [bold white]{name}[/bold white]\n[cyan]<{elem}>[/cyan]" for num, name, elem in personajes_fila1]
    grid.add_row(*sprites_f1)
    grid.add_row(*labels_f1)
    grid.add_row("", "", "", "", "")  # Espaciado

    # Fila 2: Sprites, nombres y elementos
    sprites_f2 = [render_sprite_rich(name, facing="right", pose="idle") for _, name, _ in personajes_fila2]
    labels_f2 = [f"[bold yellow]{num}.[/bold yellow] [bold white]{name}[/bold white]\n[cyan]<{elem}>[/cyan]" for num, name, elem in personajes_fila2]
    grid.add_row(*sprites_f2)
    grid.add_row(*labels_f2)

    console.print(Panel(grid, title="[bold yellow]⚔️ ELIGE TU LUCHADOR ⚔️[/bold yellow]", border_style="bright_blue"))
    console.print("[green]0. 🎲 Elegir aleatoriamente[/green]".center(75))


def menu_UI(jugador, oponente, vida_maxima_j, vida_maxima_o):
    from characters.Models.BaseModel import Personaje

    if not jugador:
        console.print("[bold red]⚠ No se ha elegido ningún personaje.[/bold red]")
        jugador = Personaje.elegir_Personaje()

    Personaje.mostrar_estado(jugador, oponente, vida_maxima_j, vida_maxima_o)
    ancho_total = 70
    console.rule()
    console.print(f"🆚  Enfrentamiento contra: [cyan]{oponente.nombre}[/cyan]".center(ancho_total))
    console.rule()


def opciones_UI():
    from ui.animations import CONFIG_ANIMACIONES, set_efectos_extra, set_animaciones_activas
    from ui.button_nav import select_menu_option

    while True:
        estado_anim = "ACTIVADAS" if CONFIG_ANIMACIONES['animaciones_activas'] else "DESACTIVADAS"
        estado_extra = "ACTIVADOS" if CONFIG_ANIMACIONES['efectos_extra'] else "DESACTIVADOS"

        opciones = [
            (1, f"Animaciones ({estado_anim})", "Alternar animaciones completas asciimatics"),
            (2, f"Efectos extra ({estado_extra})", "Alternar estrellas y partículas"),
            (0, "Volver al combate", "Regresar a la batalla"),
        ]

        opc = select_menu_option(
            "⚙️ CONFIGURACIÓN DE EFECTOS Y GRÁFICOS",
            opciones,
            columnas=1
        )

        if opc in (0, None):
            break
        elif opc == 1:
            set_animaciones_activas(not CONFIG_ANIMACIONES['animaciones_activas'])
        elif opc == 2:
            set_efectos_extra(not CONFIG_ANIMACIONES['efectos_extra'])

        