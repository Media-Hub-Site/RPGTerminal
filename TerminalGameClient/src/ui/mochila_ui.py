from utils.common import os
from utils.console import console, Table, Panel
from core.mochila_log import inventory, Mochila_log


def Mochila(jugador):
    os.system("cls")
    console.rule("MOCHILA", style="green")
    console.print(f"[bold]{len(jugador.mochila)}/10[/bold]       Money: [yellow]{jugador.moneda}[/yellow]\n")
    console.rule(characters="-", style="cyan")
    inventory(jugador)
    console.rule(characters="-", style="cyan")

    console.print("\n[R] = Salir\n", style="bold yellow")
    
    Mochila_log(jugador)






###
# Un comprobador de pociones, para que detecte que pocion es la que tienes en cada slot

###






