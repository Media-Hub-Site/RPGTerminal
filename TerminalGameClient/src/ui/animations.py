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
from ui.sprites import (
    get_sprite,
    get_effect_sprite,
    render_sprite_rich,
    render_sprite_asciimatics,
)

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
    """
    Reproduce la pantalla de título completa con Asciimatics:
    - Logo gigante con tipografía Figlet + estrellas/partículas
    - Subtítulo oficial MediaHub
    - Texto interactivo animado: '[ Presiona ENTER para comenzar ]'
    - Espera la pulsación de ENTER/Espacio directamente dentro de la animación
    """
    if not CONFIG_ANIMACIONES['animaciones_activas']:
        return

    try:
        from asciimatics.screen import Screen
        from asciimatics.scene import Scene
        from asciimatics.effects import Stars, Print
        from asciimatics.renderers import FigletText, StaticRenderer
        from asciimatics.event import KeyboardEvent

        def _scene(screen):
            effects = []
            if CONFIG_ANIMACIONES['efectos_extra']:
                effects.append(Stars(screen, 45))

            title_renderer = FigletText("RPG TERMINAL", font="slant")
            sub_renderer = StaticRenderer(["═══ MEDIAHUB RETRO BATTLE EDITION ═══"])
            enter_prompt = StaticRenderer(["[ Presiona ENTER o ESPACIO para empezar ]"])

            x_title = max(1, (screen.width - 60) // 2)
            y_title = max(1, (screen.height - 14) // 2)

            effects.append(Print(screen, title_renderer, y_title, x_title, colour=Screen.COLOUR_CYAN, transparent=True))
            effects.append(Print(screen, sub_renderer, y_title + 8, max(1, (screen.width - 37) // 2), colour=Screen.COLOUR_YELLOW, transparent=True))
            effects.append(Print(screen, enter_prompt, y_title + 11, max(1, (screen.width - 42) // 2), colour=Screen.COLOUR_GREEN, transparent=True))

            scene = Scene(effects, -1)  # -1 = duración indefinida hasta que el usuario presione tecla

            def check_key(event):
                if isinstance(event, KeyboardEvent):
                    if event.key_code in (10, 13, 32):  # Enter o Espacio
                        raise SystemExit(0)
                return event

            try:
                screen.play([scene], stop_on_resize=True, repeat=True, unhandled_input=check_key)
            except SystemExit:
                pass

        Screen.wrapper(_scene)
    except Exception:
        # Fallback si el entorno no admite pantalla completa
        console.rule("[bold cyan]⚔️ RPG TERMINAL ⚔️[/bold cyan]")
        console.print("[yellow]═══ MEDIAHUB RETRO BATTLE EDITION ═══[/yellow]".center(70))
        try:
            input("\n   Presiona ENTER para empezar...")
        except Exception:
            pass


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

        att_idle = render_sprite_asciimatics(attacker_name, facing="right", pose="idle")
        att_attack = render_sprite_asciimatics(attacker_name, facing="right", pose="attack")
        def_idle = render_sprite_asciimatics(defender_name, facing="left", pose="idle")
        effect_sprite = get_effect_sprite('ulti' if is_special else 'atacar')

        def _combat(screen):
            effects = []

            # Capa 0 (fondo opcional): Estrellas/partículas
            if CONFIG_ANIMACIONES['efectos_extra'] and is_special:
                effects.append(Stars(screen, 25))

            # Posiciones relativas a la resolución de la terminal
            h = screen.height
            w = screen.width

            y_pos = max(3, (h - 12) // 2)
            x_att = max(4, w // 6)
            x_def = max(x_att + 26, (w * 4) // 6)

            # Capa 1: Personajes chibi pixel-art enfrentados (atacante anima idle -> ataque)
            att_renderer = StaticRenderer(images=[att_idle, att_attack, att_attack])
            def_renderer = StaticRenderer(images=[def_idle])

            effects.append(Print(screen, att_renderer, y_pos, x_att, speed=4, transparent=True))
            effects.append(Print(screen, def_renderer, y_pos, x_def, transparent=True))

            # Nombres sobre los sprites
            att_label = StaticRenderer(images=[f"[{attacker_name}]"])
            def_label = StaticRenderer(images=[f"[{defender_name}]"])
            effects.append(Print(screen, att_label, max(0, y_pos - 2), x_att + 2, colour=Screen.COLOUR_GREEN, transparent=True))
            effects.append(Print(screen, def_label, max(0, y_pos - 2), x_def + 2, colour=Screen.COLOUR_RED, transparent=True))

            # Capa 2: Efecto de impacto / Acción (se dibuja encima del defensor)
            fx_renderer = StaticRenderer(images=[effect_sprite])
            effects.append(Print(screen, fx_renderer, y_pos + 2, max(x_att + 18, x_def - 10), colour=Screen.COLOUR_YELLOW, transparent=True))

            # Capa 3: Letrero de daño o acción
            if damage > 0:
                dmg_text = StaticRenderer(images=[f">> -{damage} HP! <<"])
                effects.append(Print(screen, dmg_text, max(0, y_pos - 1), x_def, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_RED, transparent=False))
            else:
                act_text = StaticRenderer(images=[f">> {action_name.upper()}! <<"])
                effects.append(Print(screen, act_text, max(0, y_pos - 1), max(2, (x_att + x_def) // 2 - 6), colour=Screen.COLOUR_CYAN, transparent=True))

            scene = Scene(effects, 24)
            screen.play([scene], stop_on_resize=True, repeat=False)

        Screen.wrapper(_combat)
    except Exception:
        # Fallback Rich en consola
        render_rich_combat_frame(attacker_name, defender_name, action_name, damage)


def render_rich_combat_frame(attacker_name: str, defender_name: str, action_name: str, damage: int):
    """Renderizado alternativo con Rich mostrando sprites chibi pixel-art lado a lado."""
    att_sprite = render_sprite_rich(attacker_name, facing="right", pose="attack")
    def_sprite = render_sprite_rich(defender_name, facing="left", pose="idle")

    table = Table.grid(expand=True)
    table.add_column(justify="center", width=22)
    table.add_column(justify="center", width=22)
    table.add_column(justify="center", width=22)

    table.add_row(
        f"[bold green]{attacker_name}[/bold green]",
        f"[bold yellow]⚔️ {action_name} ⚔️[/bold yellow]",
        f"[bold red]{defender_name}[/bold red]",
    )

    mid = f"\n\n\n\n[bold red]-{damage} HP[/bold red]" if damage > 0 else "\n\n\n\n[yellow]⚡[/yellow]"
    table.add_row(att_sprite, mid, def_sprite)

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

        winner_idle = render_sprite_asciimatics(winner_name, facing="right", pose="idle")
        winner_attack = render_sprite_asciimatics(winner_name, facing="right", pose="attack")

        def _victory(screen):
            effects = []
            if CONFIG_ANIMACIONES['efectos_extra']:
                effects.append(Stars(screen, 50))

            vic_renderer = FigletText("VICTORIA", font="slant")
            hero_renderer = StaticRenderer(images=[winner_idle, winner_attack])
            label = StaticRenderer(images=[f"★ {winner_name} ES EL GANADOR ★"])

            x_vic = max(1, (screen.width - 50) // 2)
            y_vic = 2
            x_hero = max(1, (screen.width - 18) // 2)

            effects.append(Print(screen, vic_renderer, y_vic, x_vic, colour=Screen.COLOUR_YELLOW, transparent=True))
            effects.append(Print(screen, hero_renderer, y_vic + 7, x_hero, speed=5, transparent=True))
            effects.append(Print(screen, label, y_vic + 18, max(1, (screen.width - len(winner_name) - 18) // 2), colour=Screen.COLOUR_CYAN, transparent=True))

            scene = Scene(effects, 35)
            screen.play([scene], stop_on_resize=True, repeat=False)

        Screen.wrapper(_victory)
    except Exception:
        console.print(Panel(f"[bold yellow]★ ¡VICTORIA DE {winner_name.upper()}! ★[/bold yellow]", border_style="gold1"))
        time.sleep(1.5)
