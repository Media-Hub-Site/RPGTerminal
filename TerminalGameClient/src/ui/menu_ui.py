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
    MOVIMIENTOS = {
        "Naruto": {
            4: ("Rasengan", 60),
            7: ("Esquivar", 15),
            8: ("RasenShuriken", 150),
        },
        "Sasuke": {
            4: ("Chidori", 60),
            7: ("Esquivar", 15),
            8: ("Raikiri", 150),
        },
        "Ichigo": {
            4: ("Getsuga Tensho", 50),
            7: ("Esquivar", 15),
            8: ("Bankai", 160),
        },
        "Aizen": {
            4: ("Kido", 50),
            7: ("Esquivar", 15),
            8: ("Kyokasuigetsu", 130),
        },
        "Kazuha": {
            4: ("Elemental", 50),
            7: ("Esquivar", 15),
            8: ("Ulti", 130),
        },
        "Alhacen": {
            4: ("Elemental", 50),
            7: ("Esquivar", 15),
            8: ("Ulti", 130),
        },
        "Iori": {
            4: ("Combo", 50),
            7: ("Esquivar", 15),
            8: ("Especial", 130),
        },
        "Kyo": {
            4: ("Combo", 50),
            7: ("Esquivar", 15),
            8: ("Especial", 130),
        },
        "Goku": {
            4: ("Kamehameha", 50),
            7: ("Esquivar", 15),
            8: ("Super Saiyajin", 130),
        },
        "Vegeta": {
            4: ("Garlick Gun", 50),
            7: ("Esquivar", 15),
            8: ("Super Saiyajin", 130),
        },
    }

    os.system("cls")

    if not jugador:
        console.print("[bold red]⚠ No se ha elegido ningún personaje.[/bold red]")
        jugador = Personaje.elegir_Personaje()

    Personaje.mostrar_estado(jugador, oponente, vida_maxima_j, vida_maxima_o)
    time.sleep(1)

    ancho_total = 70
    console.rule()
    console.print(f"🆚  Enfrentamiento contra: [cyan]{oponente.nombre}[/cyan]".center(ancho_total))
    console.rule()

    from rich.table import Table

    opts = Table(show_header=False, box=None)
    opts.add_column("Key", justify="center", width=8)
    opts.add_column("Description")
    opts.add_row("1", "Atacar [-10 stamina]")
    opts.add_row("2", "Esperar [+15 stamina y +15 vida]")
    opts.add_row("T", "Tienda")
    opts.add_row("E", "Mochila")
    opts.add_row("O", "Opciones visuales / Efectos")

    console.print(Panel(opts, title="Opciones", border_style="green"))

    # Mostrar habilidades especiales
    if jugador.nombre in MOVIMIENTOS:
        console.print("[blue]╔═════════════ HABILIDADES ESPECIALES ═════════════╗[/blue]")
        for key, (nombre, costo) in MOVIMIENTOS[jugador.nombre].items():
            console.print(f"  {key}. {nombre:<25} [-{costo} stamina]")
        console.print("[blue]╚══════════════════════════════════════════════════╝[/blue]")
    else:
        console.print("[red]⚠ Este personaje no tiene habilidades definidas.[/red]")


def opciones_UI():
    from ui.animations import CONFIG_ANIMACIONES, set_efectos_extra, set_animaciones_activas
    os.system("cls")
    console.print(Panel("[bold yellow]CONFIGURACIÓN DE EFECTOS Y GRÁFICOS[/bold yellow]", border_style="yellow"))

    estado_anim = "ACTIVADAS (Asciimatics + Rich)" if CONFIG_ANIMACIONES['animaciones_activas'] else "DESACTIVADAS"
    estado_extra = "ACTIVADOS (Partículas y Estrellas)" if CONFIG_ANIMACIONES['efectos_extra'] else "DESACTIVADOS (Modo limpio)"

    console.print(f"\n1. Animaciones visuales: [cyan]{estado_anim}[/cyan]")
    console.print(f"2. Modo de efectos extra: [cyan]{estado_extra}[/cyan]")
    console.print("0. Volver al combate\n")

    opc = input("Elige una opción a alternar (1, 2 o 0): ").strip()
    if opc == "1":
        set_animaciones_activas(not CONFIG_ANIMACIONES['animaciones_activas'])
        console.print("[green]Ajuste de animaciones actualizado.[/green]")
        time.sleep(1)
    elif opc == "2":
        set_efectos_extra(not CONFIG_ANIMACIONES['efectos_extra'])
        console.print("[green]Ajuste de efectos extra actualizado.[/green]")
        time.sleep(1)

        