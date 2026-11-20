from utils.common import os
from utils.console import console, Table, Panel


def Tienda(jugador):
    os.system("cls")
    console.rule("TIENDA", style="green")

    console.print("[green]!Bienvenido¡, ¿que desea llevar?[/green]\n")
    console.print(f"[yellow]Money: {jugador.moneda}[/yellow]")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", justify="center", style="cyan", no_wrap=True)
    table.add_column("Item", style="green")
    table.add_column("Precio", justify="right", style="yellow")
    table.add_column("Clase", style="magenta")

    items = [
        ("1", "Pocion_Vida_B", "$20", "B"),
        ("2", "Pocion_Stamin_B", "$20", "B"),
        ("3", "Pocion_Poder_B", "$20", "B"),
        ("4", "Pocion_Vida_A", "$40", "A"),
        ("5", "Pocion_Stamin_A", "$40", "A"),
        ("6", "Pocion_Poder_A", "$40", "A"),
        ("7", "Pocion_Vida_S", "$80", "S"),
        ("8", "Pocion_Stamin_S", "$80", "S"),
        ("9", "Pocion_Poder_S", "$80", "S"),
        ("10", "Pocion_Mix_SS", "$100", "SS"),
    ]

    for it in items:
        table.add_row(*it)

    console.print(Panel(table, title="Productos disponibles", border_style="blue"))
    console.print("\n[B]= Basico: 25.pts\n"
        "[A]= Intermedio: 40.pts\n"
        "[S]= Avanzado: 70.pts\n"
        "[SS]= Legendario: 35.pts All stats                          [bold yellow]R = Salir[/bold yellow]\n")
    
    
    


    # INSTALAR INTELLICODE EN EXTENSIONES DE VS

