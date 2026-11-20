# -*- coding: utf-8 -*-
"""
Sistema de navegación interactiva para terminal:
- Flechas del teclado (↑, ↓, ←, →) y WASD
- Selección con ENTER o ESPACIO
- Atajos numéricos/letras directos (1..9, T, E, O, etc.)
- Soporte para clic de mouse en Windows Console si está disponible
"""

import sys
import os
import time
from typing import List, Tuple, Any, Optional
from utils.console import console, clear_screen
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

# Flags Windows Console
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040
STD_INPUT_HANDLE = -10


class InputReader:
    """Lee pulsaciones de teclado directamente en tiempo real sin interferencias."""

    def __init__(self):
        self.is_windows = sys.platform == "win32"

    def flush(self):
        """Descarta teclas residuales acumuladas en el buffer (ej. tras animaciones)."""
        if self.is_windows:
            try:
                import msvcrt
                while msvcrt.kbhit():
                    msvcrt.getwch()
            except Exception:
                pass

    def restore(self):
        pass

    def read_event(self) -> Tuple[str, Any]:
        """
        Lee una tecla presionada.
        Soporta teclas extendidas Win32 (\x00/\xe0 + H/P/K/M) y secuencias VT100 (\x1b[A/B/C/D).
        Retorna tupla: (tipo, valor)
        Tipos:
          - 'UP', 'DOWN', 'LEFT', 'RIGHT'
          - 'ENTER', 'ESCAPE'
          - 'CHAR' (con el caracter presionado)
        """
        if self.is_windows:
            import msvcrt
            while True:
                ch = msvcrt.getwch()
                if ch == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt()
                elif ch in ('\r', '\n', ' '):
                    return ('ENTER', None)
                elif ch == '\x1b':
                    # Puede ser ESCAPE o una secuencia ANSI de flechas (\x1b[A, \x1b[B, \x1b[C, \x1b[D)
                    if msvcrt.kbhit():
                        nxt = msvcrt.getwch()
                        if nxt in ('[', 'O') and msvcrt.kbhit():
                            code = msvcrt.getwch()
                            if code == 'A':
                                return ('UP', None)
                            elif code == 'B':
                                return ('DOWN', None)
                            elif code == 'D':
                                return ('LEFT', None)
                            elif code == 'C':
                                return ('RIGHT', None)
                        continue
                    return ('ESCAPE', None)
                elif ch in ('\x00', '\xe0'):
                    # Tecla especial extendida Win32 (flechas de dirección)
                    code = msvcrt.getwch()
                    if code == 'H':
                        return ('UP', None)
                    elif code == 'P':
                        return ('DOWN', None)
                    elif code == 'K':
                        return ('LEFT', None)
                    elif code == 'M':
                        return ('RIGHT', None)
                    continue
                elif ch.lower() == 'w':
                    return ('UP', None)
                elif ch.lower() == 's':
                    return ('DOWN', None)
                elif ch.lower() == 'a':
                    return ('LEFT', None)
                elif ch.lower() == 'd':
                    return ('RIGHT', None)
                else:
                    return ('CHAR', ch)
        else:
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n', ' '):
                return ('ENTER', None)
            if ch == '\x1b':
                return ('ESCAPE', None)
            return ('CHAR', ch)


def select_menu_option(
    titulo: str,
    opciones: List[Tuple[Any, str, str]],
    indice_inicial: int = 0,
    columnas: int = 1,
    header_info: Optional[str] = None,
    render_header_func: Optional[Any] = None,
    header_renderable: Optional[Any] = None
) -> Any:
    """
    Renderiza un menú de botones interactivo que se navega con flechas y ENTER.
    Utiliza Rich Live para actualizar in-situ sin parpadeos, sin scrollbars y
    sin duplicar cabeceras en terminales Windows.
    """
    if not opciones:
        return None

    from rich.live import Live
    from rich.console import Group
    import shutil

    indice = max(0, min(indice_inicial, len(opciones) - 1))
    reader = InputReader()

    def build_display(current_idx: int) -> Group:
        term_cols = shutil.get_terminal_size((100, 30)).columns
        actual_cols = columnas
        if term_cols < 70 and actual_cols > 1:
            actual_cols = 1

        grid = Table.grid(padding=(0, 2), expand=True)
        cols = max(1, actual_cols)
        for _ in range(cols):
            grid.add_column(justify="center", ratio=1)

        botones_filas: List[List[Any]] = []
        fila_actual = []

        for i, (val, label, desc) in enumerate(opciones):
            is_selected = (i == current_idx)
            shortcut = str(val).upper()

            if is_selected:
                btn_text = f"[bold black on yellow] ▶ [{shortcut}] {label} ◀ [/bold black on yellow] [bold bright_yellow]{desc}[/bold bright_yellow]"
                border_style = "bright_yellow"
            else:
                btn_text = f"[bold white][{shortcut}] {label}[/bold white] [dim]({desc})[/dim]"
                border_style = "grey50"

            panel_btn = Panel(btn_text, border_style=border_style, padding=(0, 1))
            fila_actual.append(panel_btn)

            if len(fila_actual) == cols:
                botones_filas.append(fila_actual)
                fila_actual = []

        if fila_actual:
            while len(fila_actual) < cols:
                fila_actual.append("")
            botones_filas.append(fila_actual)

        for f in botones_filas:
            grid.add_row(*f)

        elements = []
        if header_renderable is not None:
            elements.append(header_renderable)
        elif header_info is not None:
            elements.append(header_info)

        elements.append(Panel(grid, title=f"[bold yellow]{titulo}[/bold yellow]", border_style="bright_blue", padding=(0, 1)))
        hint = "[dim cyan]🠄 🠆 🠅 🠇 Navega con Flechas o WASD | [ENTER/Espacio] Seleccionar | [1-9 / Teclas] Atajo directo[/dim cyan]"
        elements.append(hint.center(min(term_cols, 100)))

        return Group(*elements)

    # Limpiar buffer previo de forma definitiva antes de iniciar el Live Display
    os.system("cls")
    reader.flush()

    try:
        with Live(build_display(indice), console=console, auto_refresh=False, transient=True) as live:
            while True:
                live.update(build_display(indice), refresh=True)
                event_type, event_val = reader.read_event()

                term_cols = shutil.get_terminal_size((100, 30)).columns
                cols_count = 1 if (term_cols < 70 and columnas > 1) else max(1, columnas)

                if event_type == 'UP':
                    indice = (indice - cols_count) % len(opciones)
                elif event_type == 'DOWN':
                    indice = (indice + cols_count) % len(opciones)
                elif event_type == 'LEFT':
                    indice = (indice - 1) % len(opciones)
                elif event_type == 'RIGHT':
                    indice = (indice + 1) % len(opciones)
                elif event_type == 'ENTER':
                    return opciones[indice][0]
                elif event_type == 'ESCAPE':
                    return None
                elif event_type == 'CHAR' and event_val:
                    char_press = event_val.lower()
                    for i, (val, label, _) in enumerate(opciones):
                        if char_press == str(val).lower():
                            return val
    finally:
        reader.restore()


def select_character_grid() -> int:
    """
    Selector visual de personajes estilo galería interactiva con flechas y ENTER.
    Diseño de 2 paneles (Split-View):
    - Izquierda: Vista previa grande en tiempo real del luchador con sprite chibi OMORI,
      pose animada y detalles elementales.
    - Derecha: Matriz compacta de selección de luchadores.
    Todo el contenido cabe limpiamente en ~22 líneas verticales (pantalla completa o pequeña),
    y utiliza actualización ANSI fluida para evitar parpadeos molestos al moverte.
    """
    import shutil
    from ui.sprites import render_sprite_rich

    personajes = [
        (1, "Naruto", "Viento", "Rasengan / Shuriken"),
        (2, "Sasuke", "Fuego", "Chidori / Raikiri"),
        (3, "Goku", "Ki", "Kamehameha / SSJ"),
        (4, "Vegeta", "Ki", "Garlick Gun / SSJ"),
        (5, "Ichigo", "Espíritu", "Getsuga / Bankai"),
        (6, "Aizen", "Kido", "Kido / Kyokasuigetsu"),
        (7, "Kyo", "Fuego", "Combos / Llamas"),
        (8, "Iori", "Llama", "Fuego Púrpura / Especial"),
        (9, "Kazuha", "Anemo", "Torbellino Otoñal"),
        (10, "Alhacen", "Dendro", "Espejos Prismáticos"),
        (0, "🎲 Aleatorio", "Azar", "Luchador sorpresa"),
    ]

    from rich.live import Live
    from rich.console import Group
    import shutil

    indice = 0
    reader = InputReader()

    def build_character_view(current_idx: int) -> Group:
        term_cols = shutil.get_terminal_size((100, 30)).columns
        sel_num, sel_name, sel_elem, sel_spec = personajes[current_idx]

        # ---------------- Panel Izquierdo: Vista Previa ----------------
        prev_table = Table.grid(expand=True)
        prev_table.add_column(justify="center")

        if sel_num == 0:
            sprite_prev = Panel("[bold yellow]🎲\n\n?[/bold yellow]", padding=(3, 4), border_style="green")
            prev_table.add_row(sprite_prev)
            prev_table.add_row("[bold green]LUCHADOR SORPRESA[/bold green]")
            prev_table.add_row("[dim cyan]Selección aleatoria[/dim cyan]")
            prev_table.add_row("[dim yellow]¡Cualquiera puede tocar![/dim yellow]")
        else:
            sprite_prev = render_sprite_rich(sel_name, facing="right", pose="attack")
            prev_table.add_row(sprite_prev)
            prev_table.add_row(f"[bold yellow]{sel_name}[/bold yellow]")
            prev_table.add_row(f"[cyan]<{sel_elem}>[/cyan]")
            prev_table.add_row(f"[dim yellow]Técnicas: {sel_spec}[/dim yellow]")

        prev_panel = Panel(prev_table, title="[bold cyan]VISTA PREVIA[/bold cyan]", border_style="bright_cyan", padding=(0, 1))

        # ---------------- Panel Derecho: Lista de Luchadores ----------------
        list_table = Table.grid(padding=(0, 1), expand=True)
        list_table.add_column(ratio=1)
        list_table.add_column(ratio=1)

        for r in range(0, 10, 2):
            row_panels = []
            for c in range(2):
                num, name, elem, _ = personajes[r + c]
                is_sel = (r + c == current_idx)
                if is_sel:
                    btn = f"[bold black on yellow] ▶ [{num}] {name} ◀ [/bold black on yellow] [bold bright_yellow]<{elem}>[/bold bright_yellow]"
                    border_style = "bright_yellow"
                else:
                    btn = f"[bold white][{num}] {name}[/bold white] [dim]<{elem}>[/dim]"
                    border_style = "grey50"
                p = Panel(btn, border_style=border_style, padding=(0, 1))
                row_panels.append(p)
            list_table.add_row(*row_panels)

        is_rndm_sel = (current_idx == 10)
        if is_rndm_sel:
            rndm_btn = "[bold black on yellow] ▶ [0] 🎲 Elegir aleatoriamente ◀ [/bold black on yellow]"
            rndm_border = "bright_yellow"
        else:
            rndm_btn = "[bold green][0] 🎲 Elegir aleatoriamente[/bold green]"
            rndm_border = "green"
        list_table.add_row(Panel(rndm_btn, border_style=rndm_border, padding=(0, 1)), "")

        list_panel = Panel(list_table, title="[bold yellow]SELECCIONA TU LUCHADOR[/bold yellow]", border_style="bright_blue", padding=(0, 1))

        layout = Table.grid(padding=(0, 2), expand=True)
        layout.add_column(ratio=2, justify="center")
        layout.add_column(ratio=4)
        layout.add_row(prev_panel, list_panel)

        main_panel = Panel(layout, title="[bold yellow]⚔️ MENÚ DE SELECCIÓN DE LUCHADOR ⚔️[/bold yellow]", border_style="bright_blue", padding=(0, 1))
        hint = "[dim cyan]🠄 🠆 🠅 🠇 Flechas o WASD para moverte | [ENTER/Espacio] Elegir | [0-9] Atajo directo[/dim cyan]"
        return Group(main_panel, hint.center(min(term_cols, 100)))

    os.system("cls")
    reader.flush()

    try:
        with Live(build_character_view(indice), console=console, auto_refresh=False, transient=True) as live:
            while True:
                live.update(build_character_view(indice), refresh=True)
                event_type, event_val = reader.read_event()

                if event_type == 'UP':
                    if indice == 10:
                        indice = 8  # Subir desde aleatorio a fila previa
                    elif indice >= 2:
                        indice -= 2
                    else:
                        indice = 10
                elif event_type == 'DOWN':
                    if indice == 10:
                        indice = 0
                    elif indice + 2 <= 9:
                        indice += 2
                    else:
                        indice = 10
                elif event_type == 'LEFT':
                    indice = (indice - 1) % 11
                elif event_type == 'RIGHT':
                    indice = (indice + 1) % 11
                elif event_type == 'ENTER':
                    return personajes[indice][0]
                elif event_type == 'CHAR' and event_val:
                    if event_val.isdigit():
                        val_int = int(event_val)
                        if val_int == 0:
                            return 0
                        elif 1 <= val_int <= 9:
                            return val_int
    finally:
        reader.restore()
