# -*- coding: utf-8 -*-
"""
Motor de animaciones en CMD basado en Asciimatics con capas, sprites y efectos.
Cumple con las especificaciones de Issue #2:
- Transparencia activada (transparent=True)
- Capas ordenadas en Scene
- Modo de efectos extra opcional (partículas/estrellas)
- Fallback seguro a Rich si la terminal no soporta pantalla completa
"""
import sys
import time
from utils.console import console
from rich.panel import Panel
from rich.table import Table
from ui.sprites import get_sprite, get_effect_sprite

# Bandera global para habilitar/deshabilitar efectos extra (partículas, sacudidas)
CONFIG_ANIMACIONES = {
    'efectos_extra': True,
    'animaciones_activas': True
}

def set_efectos_extra(habilitado: bool):
    """Permite alternar el modo de efectos extra."""
    CONFIG_ANIMACIONES['efectos_extra'] = habilitado

def set_animaciones_activas(habilitado: bool):
    """Permite encender o apagar las animaciones de pantalla completa."""
    CONFIG_ANIMACIONES['animaciones_activas'] = habilitado


def play_intro_animation():
    """Reproduce la animación de bienvenida con título Figlet y estrellas."""
    if not CONFIG_ANIMACIONES['animaciones_activas']:
        return

    try:
        from asciimatics.screen import Screen
        from asciimatics.scene import Scene
        from asciimatics.effects import Stars, Print
        from asciimatics.renderers import FigletText, StaticRenderer

        def _scene(screen):
            effects = []
            if CONFIG_ANIMACIONES['efectos_extra']:
                effects.append(Stars(screen, 40))

            title_renderer = FigletText("RPG TERMINAL", font="slant")
            sub_renderer = StaticRenderer(["═══ MEDIAHUB RETRO BATTLE EDITION ═══"])

            x_title = max(1, (screen.width - 60) // 2)
            y_title = max(1, (screen.height - 12) // 2)

            effects.append(Print(screen, title_renderer, y_title, x_title, colour=Screen.COLOUR_CYAN, transparent=True))
            effects.append(Print(screen, sub_renderer, y_title + 8, max(1, (screen.width - 37) // 2), colour=Screen.COLOUR_YELLOW, transparent=True))

            scene = Scene(effects, 35)
            screen.play([scene], stop_on_resize=True, repeat=False)

        Screen.wrapper(_scene)
    except Exception:
        # Fallback elegante usando Rich
        console.rule("[bold cyan]⚔️ RPG TERMINAL ⚔️[/bold cyan]")
        console.print("[yellow]═══ MEDIAHUB RETRO BATTLE EDITION ═══[/yellow]".center(70))
        time.sleep(1)


def play_combat_animation(attacker_name: str, defender_name: str, action_name: str, damage: int, is_special: bool = False):
    """
    Reproduce una animación de combate con asciimatics:
    - Atacante y defensor dibujados en capas con sprites ASCII
    - Efecto de impacto / proyectil en capa superior
    - Números de daño flotantes
    """
    if not CONFIG_ANIMACIONES['animaciones_activas']:
        return

    try:
        from asciimatics.screen import Screen
        from asciimatics.scene import Scene
        from asciimatics.effects import Print, Stars
        from asciimatics.renderers import StaticRenderer

        attacker_sprite = get_sprite(attacker_name).split('\n')
        defender_sprite = get_sprite(defender_name).split('\n')
        effect_sprite = get_effect_sprite('ulti' if is_special else 'atacar').split('\n')

        def _combat(screen):
            effects = []

            # Capa 0 (fondo opcional): Estrellas/partículas
            if CONFIG_ANIMACIONES['efectos_extra'] and is_special:
                effects.append(Stars(screen, 25))

            # Posiciones relativas a la resolución de la terminal
            h = screen.height
            w = screen.width

            y_pos = max(2, (h - 14) // 2)
            x_att = max(2, w // 6)
            x_def = max(x_att + 26, (w * 4) // 6)

            # Capa 1: Personajes enfrentados
            att_renderer = StaticRenderer(attacker_sprite)
            def_renderer = StaticRenderer(defender_sprite)

            effects.append(Print(screen, att_renderer, y_pos, x_att, colour=Screen.COLOUR_GREEN, transparent=True))
            effects.append(Print(screen, def_renderer, y_pos, x_def, colour=Screen.COLOUR_RED, transparent=True))

            # Nombres sobre los sprites
            att_label = StaticRenderer([f"[{attacker_name}]"])
            def_label = StaticRenderer([f"[{defender_name}]"])
            effects.append(Print(screen, att_label, max(0, y_pos - 2), x_att + 2, colour=Screen.COLOUR_GREEN, transparent=True))
            effects.append(Print(screen, def_label, max(0, y_pos - 2), x_def + 2, colour=Screen.COLOUR_RED, transparent=True))

            # Capa 2: Efecto de impacto / Acción (se dibuja encima del defensor)
            fx_renderer = StaticRenderer(effect_sprite)
            effects.append(Print(screen, fx_renderer, y_pos + 2, max(x_att + 18, x_def - 10), colour=Screen.COLOUR_YELLOW, transparent=True))

            # Capa 3: Letrero de daño o acción
            if damage > 0:
                dmg_text = StaticRenderer([f">> -{damage} HP! <<"])
                effects.append(Print(screen, dmg_text, max(0, y_pos - 1), x_def, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED, transparent=False))
            else:
                act_text = StaticRenderer([f">> {action_name.upper()}! <<"])
                effects.append(Print(screen, act_text, max(0, y_pos - 1), max(2, (x_att + x_def) // 2 - 6), colour=Screen.COLOUR_CYAN, transparent=True))

            scene = Scene(effects, 24)
            screen.play([scene], stop_on_resize=True, repeat=False)

        Screen.wrapper(_combat)
    except Exception:
        # Fallback Rich en consola
        render_rich_combat_frame(attacker_name, defender_name, action_name, damage)


def render_rich_combat_frame(attacker_name: str, defender_name: str, action_name: str, damage: int):
    """Renderizado alternativo con Rich mostrando sprites lado a lado."""
    att_lines = get_sprite(attacker_name).split('\n')
    def_lines = get_sprite(defender_name).split('\n')
    max_lines = max(len(att_lines), len(def_lines))

    table = Table.grid(expand=True)
    table.add_column(justify="center", width=25)
    table.add_column(justify="center", width=20)
    table.add_column(justify="center", width=25)

    table.add_row(f"[bold green]{attacker_name}[/bold green]", f"[bold yellow]⚔️ {action_name} ⚔️[/bold yellow]", f"[bold red]{defender_name}[/bold red]")

    for i in range(max_lines):
        line_a = att_lines[i] if i < len(att_lines) else ""
        line_d = def_lines[i] if i < len(def_lines) else ""
        mid = f"[bold red]-{damage} HP[/bold red]" if i == max_lines // 2 and damage > 0 else " "
        table.add_row(f"[green]{line_a}[/green]", mid, f"[red]{line_d}[/red]")

    console.print(Panel(table, border_style="cyan"))
    time.sleep(1.2)


def play_victory_animation(winner_name: str):
    """Reproduce animación de victoria con asciimatics."""
    if not CONFIG_ANIMACIONES['animaciones_activas']:
        return

    try:
        from asciimatics.screen import Screen
        from asciimatics.scene import Scene
        from asciimatics.effects import Stars, Print
        from asciimatics.renderers import FigletText, StaticRenderer

        winner_sprite = get_sprite(winner_name).split('\n')

        def _victory(screen):
            effects = []
            if CONFIG_ANIMACIONES['efectos_extra']:
                effects.append(Stars(screen, 50))

            vic_renderer = FigletText("VICTORIA", font="slant")
            hero_renderer = StaticRenderer(winner_sprite)
            label = StaticRenderer([f"★ {winner_name} ES EL GANADOR ★"])

            x_vic = max(1, (screen.width - 50) // 2)
            y_vic = 2
            x_hero = max(1, (screen.width - 20) // 2)

            effects.append(Print(screen, vic_renderer, y_vic, x_vic, colour=Screen.COLOUR_YELLOW, transparent=True))
            effects.append(Print(screen, hero_renderer, y_vic + 6, x_hero, colour=Screen.COLOUR_GREEN, transparent=True))
            effects.append(Print(screen, label, y_vic + 18, max(1, (screen.width - len(winner_name) - 18) // 2), colour=Screen.COLOUR_CYAN, transparent=True))

            scene = Scene(effects, 35)
            screen.play([scene], stop_on_resize=True, repeat=False)

        Screen.wrapper(_victory)
    except Exception:
        console.print(Panel(f"[bold yellow]★ ¡VICTORIA DE {winner_name.upper()}! ★[/bold yellow]", border_style="gold1"))
        time.sleep(1.5)
