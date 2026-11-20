from utils.common import time, os
from utils.console import console, Panel
from core import UI_MAP


def bienvenida():
    try:
        os.system("cls")
        UI_MAP['intro']()
        console.print("[yellow] *** Bienvenido al juego RPG *** [/yellow]\n")
        enter = input("   Presiona enter para empezar\n")
    except ValueError:
        pass

def volver_a_jugar_UI():
    console.print("[yellow]Gracias por jugar[/yellow]") # estos textos son amarillos
    console.rule()
    console.print("[yellow]Juego terminado[/yellow]")
    time.sleep(2.5)
    console.print("\n¿Deseas volver a jugar?")
    console.print("1 = SI\n2 = NON")

    
def eleccion_UI():
    os.system("cls")
    console.print(f"[bold yellow]Elige tu Personaje:[/bold yellow]\n")

    console.print(f"""[cyan]
1. Naruto                 6. Kazuha   
2. Sasuke                 7. Vegeta     
3. Iori                   8. Alhacen  
4. Kyo                    9. Goku     
5. Ichigo                10. Aizen
[/cyan]""")
    
    console.print(f"\n[green]0. Elegir aleatoriamente[/green]")


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

    console.print(Panel(opts, title="Opciones", border_style="green"))

    # Mostrar habilidades especiales
    if jugador.nombre in MOVIMIENTOS:
        console.print("[blue]╔═════════════ HABILIDADES ESPECIALES ═════════════╗[/blue]")
        for key, (nombre, costo) in MOVIMIENTOS[jugador.nombre].items():
            console.print(f"  {key}. {nombre:<25} [-{costo} stamina]")
        console.print("[blue]╚══════════════════════════════════════════════════╝[/blue]")
    else:
        console.print("[red]⚠ Este personaje no tiene habilidades definidas.[/red]")

        