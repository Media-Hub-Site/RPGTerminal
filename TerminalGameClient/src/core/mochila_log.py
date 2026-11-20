from utils.common import time
from utils.console import console
from core import UI_MAP
from core.eventos import ERRORS
from utils.console import console, Table, Panel, Live


def Mochila_log(jugador):
    try:
        usar = input("\n¿Que producto deseas usar? ").strip()

        if usar.lower() == 'r':
            return True

        if usar.isdigit():
            usar = int(usar)
        else:
            console.print("[red]Debes ingresar un número válido.[/red]")
            return

        # Llama al comprobador (que se encarga de TODO)
        mochilaComprobator(usar, jugador)

        # Este UI_MAP ya llama a la animación visual que tú tengas para “usar poción”
        UI_MAP['pocion']()

        # ❌ Ya NO imprimimos aquí el ítem usado.
        # Se imprime dentro de mochilaComprobator sin riesgos

        time.sleep(1)

    except ValueError as e:
        ERRORS['VALUEERROR'](e)



def mochilaComprobator(cual_usar, jugador):
    from utils.constants import pocion

    if not jugador.mochila:
        console.print("[red]Tu mochila está vacía.[/red]")
        return

    try:
        item = jugador.mochila[cual_usar - 1]
    except IndexError:
        console.print("[red]Ítem inválido.[/red]")
        return

    efectos = {
        'Pocion_Vida_B': ('vida', pocion.Pocion_B, "+25 Vida"),
        'Pocion_Stamina_B': ('stamina', pocion.Pocion_B, "+25 Stamina"),
        'Pocion_Poder_B': ('poder', pocion.Pocion_B, "+25 Poder"),
        'Pocion_Vida_A': ('vida', pocion.Pocion_A, "+40 Vida"),
        'Pocion_Stamina_A': ('stamina', pocion.Pocion_A, "+40 Stamina"),
        'Pocion_Poder_A': ('poder', pocion.Pocion_A, "+40 Poder"),
        'Pocion_Vida_S': ('vida', pocion.Pocion_S, "+70 Vida"),
        'Pocion_Stamina_S': ('stamina', pocion.Pocion_S, "+70 Stamina"),
        'Pocion_Poder_S': ('poder', pocion.Pocion_S, "+70 Poder"),
        'Pocion_Mix_SS': ('mix', pocion.Pocion_SS, "+45 Vida +45 Stamina +45 Poder"),
    }

    if item in efectos:
        stat, cantidad, mensaje = efectos[item]

        if stat == 'mix':
            jugador.vida += cantidad
            jugador.stamina += cantidad
            jugador.poder += cantidad
        else:
            setattr(jugador, stat, getattr(jugador, stat) + cantidad)

        # Animación con Live
        with Live(
            Panel("[green]Aplicando poción...[/green]", title="Usando ítem"),
            console=console,
            refresh_per_second=4,
            transient=True
        ):
            time.sleep(1.0)

        console.print(f"\n[green]{mensaje}[/green]")

        # Imprimir ítem usado SIN provocar IndexError
        console.print(f"Has usado [green]{item}[/green]")

        # Remover el ítem del inventario
        jugador.mochila.pop(cual_usar - 1)

    else:
        console.print("[yellow]No puedes usar este ítem.[/yellow]")



def inventory(jugador):
    """Render the player's inventory as a Rich Table inside a Panel."""
    slots = 10
    mochila = jugador.mochila if jugador.mochila else []

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Slot", justify="center", style="cyan", no_wrap=True)
    table.add_column("Item", justify="left", style="green")

    for i in range(slots):
        item_name = mochila[i] if i < len(mochila) else "[dim]Vacío[/dim]"
        table.add_row(str(i + 1), item_name)

    panel = Panel(table, title="Inventario", border_style="green")
    console.print(panel)
