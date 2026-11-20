from utils.common import time
from utils.console import console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from utils.constants import pocion
from core.eventos import ERRORS
from core import UI_MAP


def Tienda_log(jugador):
    from ui.button_nav import select_menu_option

    pociones = {
        1: ('Pocion_Vida_B', pocion.Pocion_B_Precio, "Vida básica (+25 HP)"),
        2: ('Pocion_Stamina_B', pocion.Pocion_B_Precio, "Stamina básica (+25 SP)"),
        3: ('Pocion_Poder_B', pocion.Pocion_B_Precio, "Poder básico (+25 ATK)"),
        4: ('Pocion_Vida_A', pocion.Pocion_A_Precio, "Vida media (+40 HP)"),
        5: ('Pocion_Stamina_A', pocion.Pocion_A_Precio, "Stamina media (+40 SP)"),
        6: ('Pocion_Poder_A', pocion.Pocion_A_Precio, "Poder medio (+40 ATK)"),
        7: ('Pocion_Vida_S', pocion.Pocion_S_Precio, "Vida avanzada (+70 HP)"),
        8: ('Pocion_Stamina_S', pocion.Pocion_S_Precio, "Stamina avanzada (+70 SP)"),
        9: ('Pocion_Poder_S', pocion.Pocion_S_Precio, "Poder avanzado (+70 ATK)"),
        10: ('Pocion_Mix_SS', pocion.Pocion_SS_Precio, "Mix SS legendario (+35 all)"),
    }

    opciones = []
    for k, (item_name, precio, desc) in pociones.items():
        opciones.append((k, f"{item_name} [${precio}]", desc))
    opciones.append(('r', "Salir de la tienda", "Volver al combate"))

    try:
        producto = select_menu_option(
            f"🛒 TIENDA DE OBJETOS — Oro: ${jugador.moneda}",
            opciones,
            columnas=2
        )

        if producto is None or producto in ('r', 'R'):
            UI_MAP['salir_tienda']()
            return True

        if isinstance(producto, str) and producto.isdigit():
            producto = int(producto)

        if producto in pociones:
            item_name, precio, _ = pociones[producto]
            if moneyComprobator(jugador, producto):
                jugador.mochila.append(item_name)
                jugador.moneda -= precio
                with Live(Panel("[bold green]Comprando...[/bold green]", title="Tienda"), console=console, refresh_per_second=4, transient=True):
                    time.sleep(0.7)
        else:
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


