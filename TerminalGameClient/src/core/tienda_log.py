from utils.common import time
from utils.console import console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from utils.constants import pocion
from core.eventos import ERRORS
from core import UI_MAP


def Tienda_log(jugador):
    try:
        producto = input("\nElige el producto: ")

        if producto.isdigit():
            producto = int(producto)
            
        pociones = {
            1: 'Pocion_Vida_B',
            2: 'Pocion_Stamin_B',
            3: 'Pocion_Poder_B',
            4: 'Pocion_Vida_A',
            5: 'Pocion_Stamin_A',
            6: 'Pocion_Poder_A',
            7: 'Pocion_Vida_S',
            8: 'Pocion_Stamin_S',
            9: 'Pocion_Poder_S',
            10: 'Pocion_Mix_SS',
        }
        match producto:
            case 1:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_B_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 2:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_B_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 3:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_B_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 4:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_A_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 5:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_A_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 6:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_A_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 7:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_S_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 8:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_S_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 9:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_S_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 10:
                if moneyComprobator(jugador, producto):
                    jugador.mochila.append(pociones[producto])
                    jugador.moneda -= pocion.Pocion_SS_Precio
                    with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                        time.sleep(0.7)
            case 'r' | 'R':
                UI_MAP['salir_tienda']()
                return True
            case _:
                ERRORS['ERROR']()
    except ValueError as e:
        ERRORS['VALUEERROR'](e)
        

def moneyComprobator(jugador, producto):
    """Check if the player has enough coins for the chosen product.

    Returns True if purchase can continue, False otherwise.
    """
    if producto in range(1, 4):
        price = pocion.Pocion_B_Precio
    elif producto in range(4, 7):
        price = pocion.Pocion_A_Precio
    elif producto in range(7, 10):
        price = pocion.Pocion_S_Precio
    elif producto == 10:
        price = pocion.Pocion_SS_Precio
    else:
        UI_MAP['error']()
        console.print("[red]No tenemos mas productos[/red]")
        time.sleep(2)
        return False

    if jugador.moneda >= price:
        UI_MAP['money']()
        return True
    else:
        UI_MAP['error']()
        console.print("\n[red]No tienes monedas suficientes para ese producto[/red]")
        time.sleep(2)
        return False

"""
EN ESTA PARTE SE AGREGARAN MOCHILAS DE INVENTARIO Y MONEDAS
"""


