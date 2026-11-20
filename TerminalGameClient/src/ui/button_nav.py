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
from utils.console import console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live

# Flags Windows Console
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040
STD_INPUT_HANDLE = -10


class InputReader:
    """Lee pulsaciones de teclado y eventos de ratón en tiempo real sin bloquear el búfer."""

    def __init__(self):
        self.is_windows = sys.platform == "win32"
        self._orig_mode = None
        self._h_in = None
        if self.is_windows:
            try:
                import ctypes
                from ctypes import wintypes
                self.kernel32 = ctypes.windll.kernel32
                self._h_in = self.kernel32.GetStdHandle(STD_INPUT_HANDLE)
                mode = wintypes.DWORD()
                if self.kernel32.GetConsoleMode(self._h_in, ctypes.byref(mode)):
                    self._orig_mode = mode.value
                    # Habilitar mouse input y desactivar quick edit para recibir clicks
                    new_mode = (mode.value | ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS) & ~ENABLE_QUICK_EDIT_MODE
                    self.kernel32.SetConsoleMode(self._h_in, new_mode)
            except Exception:
                pass

    def restore(self):
        if self.is_windows and self._orig_mode is not None and self._h_in:
            try:
                self.kernel32.SetConsoleMode(self._h_in, self._orig_mode)
            except Exception:
                pass

    def read_event(self) -> Tuple[str, Any]:
        """
        Lee una tecla o evento.
        Retorna tupla: (tipo, valor)
        Tipos:
          - 'UP', 'DOWN', 'LEFT', 'RIGHT'
          - 'ENTER', 'ESCAPE'
          - 'CHAR' (con el caracter en mayúscula/minúscula)
        """
        if self.is_windows:
            import msvcrt
            while True:
                # Leer tecla de teclado estándar
                ch = msvcrt.getwch()
                if ch in ('\r', '\n'):
                    return ('ENTER', None)
                elif ch == ' ':
                    return ('ENTER', None)
                elif ch == '\x1b':
                    return ('ESCAPE', None)
                elif ch in ('\x00', '\xe0'):
                    # Tecla especial extendida (flechas, funciones)
                    code = msvcrt.getwch()
                    if code in ('H', '72'):
                        return ('UP', None)
                    elif code in ('P', '80'):
                        return ('DOWN', None)
                    elif code in ('K', '75'):
                        return ('LEFT', None)
                    elif code in ('M', '77'):
                        return ('RIGHT', None)
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
            # Fallback Unix / stdin
            import select
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n', ' '):
                return ('ENTER', None)
            return ('CHAR', ch)


def select_menu_option(
    titulo: str,
    opciones: List[Tuple[Any, str, str]],
    indice_inicial: int = 0,
    columnas: int = 1,
    header_info: Optional[str] = None,
    render_header_func: Optional[Any] = None
) -> Any:
    """
    Renderiza un menú de botones interactivo que se navega con flechas y ENTER.
    
    opciones: Lista de tuplas (valor_retorno, etiqueta_boton, descripcion_o_costo)
    Ejemplo: [(1, "Atacar", "-10 SP"), (2, "Esperar", "+15 SP y +15 HP"), ...]
    """
    if not opciones:
        return None

    indice = max(0, min(indice_inicial, len(opciones) - 1))
    reader = InputReader()
    import shutil

    try:
        while True:
            term_cols = shutil.get_terminal_size((100, 30)).columns

            # Ajustar columnas de forma responsiva: si la terminal es estrecha (< 70), usar 1 columna
            actual_cols = columnas
            if term_cols < 70 and actual_cols > 1:
                actual_cols = 1

            # Construir la cuadrícula de botones visuales compacta
            grid = Table.grid(padding=(0, 2), expand=True)
            cols = max(1, actual_cols)
            for _ in range(cols):
                grid.add_column(justify="center", ratio=1)

            # Generar botones compactos de 1 línea con estilo resaltado para la opción activa
            botones_filas: List[List[Any]] = []
            fila_actual = []

            for i, (val, label, desc) in enumerate(opciones):
                is_selected = (i == indice)
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

            # Limpiar y redibujar el panel de opciones
            os.system("cls")
            if render_header_func:
                render_header_func()
            elif header_info:
                console.print(header_info)

            console.print(Panel(grid, title=f"[bold yellow]{titulo}[/bold yellow]", border_style="bright_blue", padding=(0, 1)))
            console.print("[dim cyan]🠄 🠆 🠅 🠇 Navega con Flechas o WASD | [ENTER/Espacio] Seleccionar | [1-9 / Teclas] Atajo directo[/dim cyan]".center(min(term_cols, 100)))

            event_type, event_val = reader.read_event()

            if event_type == 'UP':
                indice = (indice - cols) % len(opciones)
            elif event_type == 'DOWN':
                indice = (indice + cols) % len(opciones)
            elif event_type == 'LEFT':
                indice = (indice - 1) % len(opciones)
            elif event_type == 'RIGHT':
                indice = (indice + 1) % len(opciones)
            elif event_type == 'ENTER':
                return opciones[indice][0]
            elif event_type == 'ESCAPE':
                return None
            elif event_type == 'CHAR' and event_val:
                # Comprobar si coincide con un atajo directo de las opciones
                char_press = event_val.lower()
                for i, (val, label, _) in enumerate(opciones):
                    val_str = str(val).lower()
                    if char_press == val_str or (len(label) > 0 and char_press == label[0].lower()):
                        return val
    finally:
        reader.restore()


def select_character_grid() -> int:
    """
    Selector visual de personajes estilo galería interactiva con flechas y ENTER.
    Totalmente responsivo: adapta el número de columnas (5, 3 o 2) según el ancho
    real de la terminal para evitar desbordes y barras de desplazamiento horizontales.
    Retorna el número de personaje elegido (1 a 10, o 0 para aleatorio).
    """
    import shutil
    from ui.sprites import render_sprite_rich

    personajes = [
        (1, "Naruto", "Viento"),
        (2, "Sasuke", "Fuego"),
        (3, "Goku", "Ki"),
        (4, "Vegeta", "Ki"),
        (5, "Ichigo", "Espíritu"),
        (6, "Aizen", "Kido"),
        (7, "Kyo", "Fuego"),
        (8, "Iori", "Llama"),
        (9, "Kazuha", "Anemo"),
        (10, "Alhacen", "Dendro"),
        (0, "🎲 Aleatorio", "Azar"),
    ]

    indice = 0
    reader = InputReader()

    try:
        while True:
            os.system("cls")
            term_cols = shutil.get_terminal_size((100, 30)).columns

            # Determinar columnas responsivas
            if term_cols >= 115:
                num_cols = 5
            elif term_cols >= 75:
                num_cols = 3
            else:
                num_cols = 2

            grid = Table.grid(padding=(0, 1), expand=True)
            for _ in range(num_cols):
                grid.add_column(justify="center", ratio=1)

            # Construir tarjetas para los 10 personajes (0 a 9)
            cards = []
            for i in range(10):
                num, name, elem = personajes[i]
                is_sel = (i == indice)
                sprite = render_sprite_rich(name, facing="right", pose="attack" if is_sel else "idle")
                title = f"[bold black on yellow] {num}. {name} [/bold black on yellow]" if is_sel else f"[bold white]{num}. {name}[/bold white]"
                card_content = Table.grid(expand=True)
                card_content.add_column(justify="center")
                card_content.add_row(sprite)
                card_content.add_row(title)
                card_content.add_row(f"[cyan]<{elem}>[/cyan]")
                card_panel = Panel(card_content, border_style="bright_yellow" if is_sel else "grey50", padding=(0, 0))
                cards.append(card_panel)

            # Distribuir tarjetas en filas según num_cols
            for r in range(0, 10, num_cols):
                row_items = cards[r:r + num_cols]
                while len(row_items) < num_cols:
                    row_items.append("")
                grid.add_row(*row_items)

            console.print(Panel(grid, title="[bold yellow]⚔️ ELIGE TU LUCHADOR (Flechas + ENTER) ⚔️[/bold yellow]", border_style="bright_blue"))

            # Opción 0 Aleatorio
            is_rndm_sel = (indice == 10)
            rndm_style = "bold black on yellow" if is_rndm_sel else "green"
            console.print(f"[{rndm_style}] [0] 🎲 Elegir aleatoriamente [/{rndm_style}]".center(min(term_cols, 100)))
            console.print("[dim cyan]🠄 🠆 🠅 🠇 Flechas/WASD para moverte | [ENTER] Elegir | [0-9] Atajo directo[/dim cyan]".center(min(term_cols, 100)))

            event_type, event_val = reader.read_event()

            if event_type == 'UP':
                if indice == 10:
                    indice = max(0, 10 - num_cols)
                elif indice >= num_cols:
                    indice -= num_cols
                else:
                    indice = 10
            elif event_type == 'DOWN':
                if indice == 10:
                    indice = 0
                elif indice + num_cols < 10:
                    indice += num_cols
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
                elif event_val.lower() == 'a':
                    return 0
    finally:
        reader.restore()
