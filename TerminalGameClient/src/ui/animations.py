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


def _resolve_attack_choreography(attacker_name: str, action_name: str, is_special: bool):
    """
    Determina la coreografía única (estilo, color primario, color secundario)
    según el personaje y el nombre del ataque.
    Colores Asciimatics: 0=BLACK, 1=RED, 2=GREEN, 3=YELLOW, 4=BLUE, 5=MAGENTA, 6=CYAN, 7=WHITE
    """
    act = (action_name or "").lower()
    att = (attacker_name or "").lower()

    # Ataque básico físico: acercamiento rápido + golpe
    if "basico" in act or "básico" in act or act == "ataque":
        return ("melee_dash", 3, 7)

    # Naruto
    if "rasenshuriken" in act or "shuriken" in act:
        return ("projectile_spin", 6, 7)
    if "rasengan" in act:
        return ("dash_orb", 6, 4)

    # Sasuke
    if "chidori" in act or "raikiri" in act:
        return ("dash_lightning", 6, 7)

    # Goku / Vegeta
    if "kamehameha" in act:
        return ("beam", 6, 4)
    if "garlick" in act or "galick" in act:
        return ("beam", 5, 1)
    if "saiyajin" in act or "ssj" in act:
        return ("aura_burst", 3, 7)

    # Ichigo
    if "getsuga" in act:
        return ("projectile_spin", 4, 6)
    if "bankai" in act:
        return ("dash_slash", 1, 7)

    # Aizen
    if "kido" in act:
        return ("magic_seal", 5, 3)
    if "kyoka" in act:
        return ("magic_seal", 6, 5)

    # Kyo / Iori
    if "kyo" in att:
        return ("fire_rush", 1, 3)
    if "iori" in att:
        return ("fire_rush", 5, 1)

    # Kazuha
    if "kazuha" in att:
        return ("wind_vortex", 6, 1)

    # Alhacen
    if "alhacen" in att:
        return ("dendro_mirrors", 2, 3)

    # Fallback inteligente según si es especial o combo
    if is_special:
        return ("beam", 3, 7)
    return ("melee_dash", 3, 7)


def play_combat_animation(attacker_name: str, defender_name: str, action_name: str, damage: int, is_special: bool = False):
    """
    Reproduce una animación de combate coreografiada frame a frame con Asciimatics:
    - Cada personaje y ataque tiene su propia animación única (dash con Rasengan,
      rayo Kamehameha / Garlick Gun, proyectil RasenShuriken / Getsuga, embestida
      eléctrica Chidori, corte veloz Bankai, aura Super Saiyajin, sellos Kido,
      llamas de Kyo/Iori, vórtice Anemo de Kazuha, espejos Dendro de Alhacen).
    - Movimiento suave, partículas de energía, sacudida de impacto (hit-shake)
      y destello en el defensor.
    """
    if not CONFIG_ANIMACIONES['animaciones_activas']:
        return

    try:
        from asciimatics.screen import Screen
        from asciimatics.scene import Scene
        from asciimatics.effects import Effect
        from ui.sprites import draw_sprite_asciimatics

        style, c_pri, c_sec = _resolve_attack_choreography(attacker_name, action_name, is_special)
        total_frames = 38 if (is_special or style in ("beam", "aura_burst", "magic_seal", "wind_vortex", "dendro_mirrors")) else 32

        class CombatChoreography(Effect):
            def __init__(self, screen):
                super().__init__(screen)
                self._frame = 0

            def reset(self):
                self._frame = 0

            def _safe_print(self, text: str, x: int, y: int, colour: int = 7, attr: int = 1, bg: int = 0):
                if 0 <= y < self._screen.height and x < self._screen.width:
                    if x < 0:
                        text = text[-x:]
                        x = 0
                    if text:
                        max_len = self._screen.width - x
                        self._screen.print_at(text[:max_len], x, y, colour=colour, attr=attr, bg=bg)

            def _draw_orb(self, cx: int, cy: int, radius: int, frame: int, col1: int, col2: int):
                spin = ["◎", "◉", "◌", "●"]
                ch_core = spin[frame % len(spin)]
                if radius <= 1:
                    self._safe_print(f"({ch_core})", cx - 1, cy, col1, 1)
                elif radius == 2:
                    self._safe_print(" ▄▀▄ ", cx - 2, cy - 1, col1, 1)
                    self._safe_print(f"█ {ch_core} █", cx - 2, cy, col2, 1)
                    self._safe_print(" ▀▄▀ ", cx - 2, cy + 1, col1, 1)
                else:
                    self._safe_print("  ▄▄▄  ", cx - 3, cy - 2, col1, 1)
                    self._safe_print(" █████ ", cx - 3, cy - 1, col2, 1)
                    self._safe_print(f"██ {ch_core} ██", cx - 3, cy, 7, 1)
                    self._safe_print(" █████ ", cx - 3, cy + 1, col2, 1)
                    self._safe_print("  ▀▀▀  ", cx - 3, cy + 2, col1, 1)

            def _draw_impact_burst(self, cx: int, cy: int, frame: int, col1: int, col2: int):
                if frame % 2 == 0:
                    self._safe_print("  \\  |  /  ", cx - 5, cy - 2, col1, 1)
                    self._safe_print("-- ✦ ★ ✦ --", cx - 5, cy, col2, 1)
                    self._safe_print("  /  |  \\  ", cx - 5, cy + 2, col1, 1)
                else:
                    self._safe_print(" *  \\|/  * ", cx - 5, cy - 2, col2, 1)
                    self._safe_print("══ ▓███▓ ══", cx - 5, cy, 7, 1)
                    self._safe_print(" *  /|\\  * ", cx - 5, cy + 2, col2, 1)

            def _update(self, frame_no):
                f = self._frame
                self._frame += 1

                w = self._screen.width
                h = self._screen.height

                # Limpiar frame anterior para movimiento limpio sin estelas fantasma
                self._screen.clear_buffer(7, 0, 0)

                y_base = max(4, (h - 10) // 2)
                x_att_start = max(4, w // 6)
                x_def_base = max(x_att_start + 26, (w * 4) // 6)
                if x_def_base + 18 >= w:
                    x_def_base = max(x_att_start + 18, w - 20)

                # Línea de suelo de la arena
                floor_y = y_base + 10
                if floor_y < h:
                    self._safe_print("═" * max(10, w - 4), 2, floor_y, colour=4, attr=2)

                # Banner superior de técnica
                banner = f" ★ {attacker_name.upper()} USA: {action_name.upper()}! ★ "
                self._safe_print(banner, max(1, (w - len(banner)) // 2), max(0, y_base - 3), colour=c_pri, attr=1)

                # Estado por defecto de los personajes
                x_att = x_att_start
                y_att = y_base
                att_pose = "idle"

                x_def = x_def_base
                y_def = y_base
                def_flash = None
                show_dmg = False

                # ---------------------------------------------------------
                # COREOGRAFÍAS ÚNICAS POR ESTILO DE ATAQUE
                # ---------------------------------------------------------
                if style == "dash_orb":
                    # NARUTO RASENGAN: Carga esfera -> corre hacia el rival -> impacto explosivo
                    if f < 10:
                        att_pose = "attack"
                        # Dibujar carga de Rasengan frente a Naruto
                        r = 1 if f < 5 else 2
                        self._draw_orb(x_att + 17, y_att + 5, r, f, c_pri, c_sec)
                        if f % 2 == 0:
                            self._safe_print("✦", x_att + 15 + (f % 4), y_att + 3, 7, 1)
                    elif f < 20:
                        # Embestida rápida hacia el enemigo llevando el Rasengan
                        t = (f - 10) / 10.0
                        x_att = int(x_att_start + (x_def_base - 15 - x_att_start) * t)
                        att_pose = "attack"
                        # Estela de velocidad detrás
                        self._safe_print("═══", max(0, x_att - 4), y_att + 4, c_pri, 2)
                        self._safe_print("══", max(0, x_att - 3), y_att + 7, c_sec, 2)
                        self._draw_orb(x_att + 16, y_att + 5, 2, f, c_pri, c_sec)
                    elif f < 28:
                        # Impacto del Rasengan en el enemigo
                        x_att = x_def_base - 15
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -1)
                        def_flash = 6 if f % 2 == 0 else 7
                        show_dmg = True
                        self._draw_orb(x_def + 4, y_def + 5, 3, f, c_pri, c_sec)
                        self._draw_impact_burst(x_def + 6, y_def + 5, f, c_pri, 7)
                    else:
                        # Retorno rápido
                        t = (f - 28) / max(1, total_frames - 28)
                        x_att = int((x_def_base - 15) * (1 - t) + x_att_start * t)
                        show_dmg = True

                elif style == "beam":
                    # GOKU KAMEHAMEHA / VEGETA GARLICK GUN: Carga en su sitio -> rayo masivo
                    if f < 12:
                        att_pose = "attack"
                        r = 1 if f < 6 else 2
                        self._draw_orb(x_att + 17, y_att + 5, r, f, c_pri, c_sec)
                        # Partículas convergiendo hacia la bola de energía
                        dist = max(1, 12 - f)
                        self._safe_print("✦", x_att + 17 + dist, y_att + 5 - (dist // 3), c_pri, 1)
                        self._safe_print("✦", x_att + 17 + dist, y_att + 5 + (dist // 3), c_sec, 1)
                    elif f < 30:
                        att_pose = "attack"
                        # El rayo se extiende desde el atacante hasta atravesar al defensor
                        beam_start = x_att + 16
                        beam_end = x_def_base + 16
                        progress = min(1.0, (f - 12) / 6.0)
                        cur_end = int(beam_start + (beam_end - beam_start) * progress)
                        length = max(1, cur_end - beam_start)

                        # Dibujar haz de energía multicapa (borde + núcleo blanco brillante)
                        edge_char = "▀" if f % 2 == 0 else "▓"
                        bot_char = "▄" if f % 2 == 0 else "▓"
                        self._safe_print(edge_char * length, beam_start, y_att + 3, c_sec, 1)
                        self._safe_print("█" * length, beam_start, y_att + 4, c_pri, 1)
                        self._safe_print("█" * length, beam_start, y_att + 5, 7, 1)
                        self._safe_print("█" * length, beam_start, y_att + 6, c_pri, 1)
                        self._safe_print(bot_char * length, beam_start, y_att + 7, c_sec, 1)

                        # Cabeza de la bola de energía al frente del rayo
                        self._draw_orb(cur_end, y_att + 5, 3, f, c_pri, 7)

                        if cur_end >= x_def_base:
                            x_def = x_def_base + (2 if f % 2 == 0 else -2)
                            def_flash = 7 if f % 2 == 0 else c_pri
                            show_dmg = True
                    else:
                        show_dmg = True
                        if f < 34:
                            self._draw_impact_burst(x_def + 8, y_def + 5, f, c_pri, 7)

                elif style == "projectile_spin":
                    # NARUTO RASENSHURIKEN / ICHIGO GETSUGA TENSHO: Proyectil volador + explosión
                    if f < 8:
                        att_pose = "attack"
                        self._draw_orb(x_att + 16, y_att + 4, 2, f, c_pri, c_sec)
                    elif f < 22:
                        att_pose = "attack"
                        t = (f - 8) / 14.0
                        px = int((x_att + 16) + (x_def_base + 4 - (x_att + 16)) * t)
                        if "getsuga" in (action_name or "").lower():
                            # Media luna cortante (Getsuga Tensho)
                            self._safe_print("  ▄▄█", px, y_att + 2, c_sec, 1)
                            self._safe_print("   ███", px, y_att + 3, c_pri, 1)
                            self._safe_print("    ███", px, y_att + 4, 7, 1)
                            self._safe_print("    ███", px, y_att + 5, 7, 1)
                            self._safe_print("   ███", px, y_att + 6, c_pri, 1)
                            self._safe_print("  ▀▀█", px, y_att + 7, c_sec, 1)
                        else:
                            # Shuriken giratorio (RasenShuriken)
                            blades = [" ╲ │ ╱ ", " ──◉── ", " ╱ │ ╲ "] if f % 2 == 0 else ["  ─┼─  ", " ╲ ◉ ╱ ", "  ─┼─  "]
                            for idx, line in enumerate(blades):
                                self._safe_print(line, px - 3, y_att + 3 + idx, c_pri if idx != 1 else 7, 1)
                    elif f < 31:
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = c_pri if f % 2 == 0 else 7
                        show_dmg = True
                        self._draw_orb(x_def + 8, y_def + 5, 3, f, c_pri, c_sec)
                        self._draw_impact_burst(x_def + 8, y_def + 5, f, c_pri, 7)
                    else:
                        show_dmg = True

                elif style == "dash_lightning":
                    # SASUKE CHIDORI / RAIKIRI: Chispas -> embestida relámpago -> descarga
                    if f < 9:
                        att_pose = "attack"
                        sparks = ["⚡", "╱", "╲", "*"]
                        self._safe_print(sparks[f % 4], x_att + 16, y_att + 3, c_pri, 1)
                        self._safe_print("⚡⚡", x_att + 15, y_att + 5, 7, 1)
                        self._safe_print(sparks[(f + 2) % 4], x_att + 17, y_att + 7, c_pri, 1)
                    elif f < 17:
                        t = (f - 9) / 8.0
                        x_att = int(x_att_start + (x_def_base - 14 - x_att_start) * t)
                        att_pose = "attack"
                        # Rastro eléctrico
                        for bx in range(x_att_start + 8, x_att, 4):
                            self._safe_print("⚡" if (bx + f) % 2 == 0 else "═", bx, y_att + 5, c_pri, 1)
                    elif f < 26:
                        x_att = x_def_base - 14
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = 6 if f % 2 == 0 else 7
                        show_dmg = True
                        # Rayos verticales sobre el enemigo
                        for ly in range(max(0, y_def - 2), min(h, y_def + 10)):
                            self._safe_print("⚡" if (ly + f) % 2 == 0 else "║", x_def + 8, ly, c_pri, 1)
                        self._draw_impact_burst(x_def + 8, y_def + 5, f, c_pri, 7)
                    else:
                        t = (f - 26) / max(1, total_frames - 26)
                        x_att = int((x_def_base - 14) * (1 - t) + x_att_start * t)
                        show_dmg = True

                elif style == "dash_slash":
                    # ICHIGO BANKAI: Corte dimensional atravesando al rival
                    if f < 10:
                        att_pose = "attack"
                        for ay in range(y_att, y_att + 10):
                            self._safe_print("░" if (ay + f) % 2 == 0 else "▒", x_att - 2, ay, c_pri, 1)
                            self._safe_print("░" if (ay + f) % 2 == 0 else "▒", x_att + 17, ay, c_pri, 1)
                    elif f < 16:
                        # Atraviesa a velocidad supersónica
                        t = (f - 10) / 6.0
                        x_att = int(x_att_start + (min(w - 18, x_def_base + 14) - x_att_start) * t)
                        att_pose = "attack"
                        self._safe_print("═══════════════", x_att_start + 6, y_att + 5, c_pri, 1)
                    elif f < 28:
                        x_att = min(w - 18, x_def_base + 14)
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = 1 if f % 2 == 0 else 7
                        show_dmg = True
                        # Gran corte diagonal sobre el enemigo
                        for s in range(-4, 5):
                            self._safe_print("╱", x_def + 8 - s * 2, y_def + 5 + s, c_pri, 1)
                            self._safe_print("╲", x_def + 8 + s * 2, y_def + 5 + s, 7, 1)
                    else:
                        show_dmg = True

                elif style == "aura_burst":
                    # GOKU / VEGETA SUPER SAIYAJIN: Columna de aura dorada + embestida relámpago
                    if f < 14:
                        att_pose = "attack"
                        # Columna de aura dorada envolviendo al atacante
                        for ay in range(max(0, y_att - 2), min(h, y_att + 10)):
                            ch = "▲" if (ay + f) % 2 == 0 else "▓"
                            self._safe_print(ch, x_att - 2, ay, c_pri, 1)
                            self._safe_print(ch, x_att + 17, ay, c_pri, 1)
                        self._safe_print("★ ⚡ ★ ⚡ ★", x_att + 3, max(0, y_att - 2), c_pri, 1)
                    elif f < 22:
                        t = (f - 14) / 8.0
                        x_att = int(x_att_start + (x_def_base - 14 - x_att_start) * t)
                        att_pose = "attack"
                        self._safe_print("▓▓▓▓▓", max(0, x_att - 5), y_att + 4, c_pri, 1)
                        self._safe_print("▓▓▓▓▓", max(0, x_att - 5), y_att + 6, c_pri, 1)
                    elif f < 32:
                        x_att = x_def_base - 14
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = 3 if f % 2 == 0 else 7
                        show_dmg = True
                        self._draw_impact_burst(x_def + 8, y_def + 5, f, c_pri, 7)
                    else:
                        show_dmg = True

                elif style == "magic_seal":
                    # AIZEN KIDO / KYOKASUIGETSU: Sello mágico sobre el enemigo + pilar de energía
                    att_pose = "attack"
                    if f < 14:
                        # Dibujar jaula/sello mágico alrededor del enemigo
                        self._safe_print("╔═══ ✦ ═══╗", x_def + 2, max(0, y_def - 1), c_pri, 1)
                        self._safe_print("╚═══ ✦ ═══╝", x_def + 2, min(h - 1, y_def + 10), c_pri, 1)
                        if f > 6:
                            for sy in range(y_def, y_def + 10):
                                self._safe_print("║", x_def + 2, sy, c_sec, 1)
                                self._safe_print("║", x_def + 12, sy, c_sec, 1)
                    elif f < 28:
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = c_pri if f % 2 == 0 else 7
                        show_dmg = True
                        # Pilar vertical de energía mágica
                        for sy in range(max(0, y_def - 2), min(h, y_def + 10)):
                            self._safe_print("░▒▓███▓▒░", x_def + 3, sy, c_pri if (sy + f) % 2 == 0 else c_sec, 1)
                    else:
                        show_dmg = True

                elif style == "fire_rush":
                    # KYO / IORI: Embestida con llamas + pilar de fuego
                    if f < 14:
                        t = f / 14.0
                        x_att = int(x_att_start + (x_def_base - 14 - x_att_start) * t)
                        att_pose = "attack"
                        # Estela de fuego en el suelo
                        for fx in range(x_att_start, x_att, 3):
                            self._safe_print("▲", fx, min(h - 1, y_att + 9), c_pri if (fx + f) % 2 == 0 else c_sec, 1)
                    elif f < 26:
                        x_att = x_def_base - 14
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        def_flash = c_pri if f % 2 == 0 else c_sec
                        show_dmg = True
                        # Pilar de llamas ascendiendo
                        for fy in range(max(0, y_def - 1), min(h, y_def + 10)):
                            flame = "▲▓█▓▲" if (fy + f) % 2 == 0 else "▓▲█▲▓"
                            self._safe_print(flame, x_def + 5, fy, c_pri if fy % 2 == 0 else c_sec, 1)
                    else:
                        t = (f - 26) / max(1, total_frames - 26)
                        x_att = int((x_def_base - 14) * (1 - t) + x_att_start * t)
                        show_dmg = True

                elif style == "wind_vortex":
                    # KAZUHA: Torbellino Anemo + hojas otoñales
                    att_pose = "attack"
                    if f < 10:
                        # Kazuha salta ligeramente
                        y_att = max(2, y_base - 2)
                    if 6 <= f < 28:
                        x_def = x_def_base + (2 if f % 2 == 0 else -2)
                        y_def = max(2, y_base - (2 if f < 20 else 0))
                        def_flash = 6 if f % 2 == 0 else 7
                        show_dmg = (f >= 14)
                        # Espirales de viento y hojas rojas/amarillas
                        for vy in range(y_base - 1, y_base + 10):
                            offset = (vy + f) % 4
                            self._safe_print("~~~" if offset < 2 else "≈≈≈", x_def + 2 + offset, vy, c_pri, 1)
                            if (vy + f) % 3 == 0:
                                self._safe_print("🍁", x_def + 12 - offset, vy, c_sec, 1)
                    elif f >= 28:
                        show_dmg = True

                elif style == "dendro_mirrors":
                    # ALHACEN: Espejos prismáticos verdes + haces láser sincronizados
                    att_pose = "attack"
                    # Dibujar 3 espejos alrededor del rival
                    if f < 28:
                        self._safe_print("◆", x_def + 8, max(0, y_def - 2), c_pri, 1)
                        self._safe_print("◆", max(0, x_def - 4), y_def + 4, c_pri, 1)
                        self._safe_print("◆", min(w - 2, x_def + 20), y_def + 4, c_pri, 1)
                    if 10 <= f < 28:
                        x_def = x_def_base + (1 if f % 2 == 0 else -1)
                        def_flash = 2 if f % 2 == 0 else 7
                        show_dmg = True
                        # Haces láser convergiendo al enemigo
                        for ly in range(max(0, y_def - 1), y_def + 6):
                            self._safe_print("║", x_def + 8, ly, c_pri, 1)
                        self._safe_print("══════", max(0, x_def - 3), y_def + 4, c_sec, 1)
                        self._safe_print("══════", x_def + 13, y_def + 4, c_sec, 1)
                        self._draw_impact_burst(x_def + 8, y_def + 5, f, c_pri, c_sec)
                    elif f >= 28:
                        show_dmg = True

                else:
                    # MELEE_DASH (Ataque Básico): Acercamiento rápido, golpe y retroceso
                    if f < 10:
                        t = f / 10.0
                        x_att = int(x_att_start + (x_def_base - 14 - x_att_start) * t)
                        att_pose = "attack"
                    elif f < 18:
                        x_att = x_def_base - 14
                        att_pose = "attack"
                        x_def = x_def_base + (2 if f % 2 == 0 else -1)
                        def_flash = 1 if f % 2 == 0 else 7
                        show_dmg = True
                        self._draw_impact_burst(x_def + 5, y_def + 5, f, c_pri, c_sec)
                    else:
                        t = (f - 18) / max(1, total_frames - 18)
                        x_att = int((x_def_base - 14) * (1 - t) + x_att_start * t)
                        show_dmg = True

                # Dibujar sprites de ambos personajes
                draw_sprite_asciimatics(self._screen, defender_name, x_def, y_def, facing="left", pose="idle", flash_colour=def_flash)
                draw_sprite_asciimatics(self._screen, attacker_name, x_att, y_att, facing="right", pose=att_pose)

                # Etiquetas de nombres
                self._safe_print(f"[{attacker_name}]", x_att + 2, max(0, y_att - 1), colour=2, attr=1)
                self._safe_print(f"[{defender_name}]", x_def + 2, max(0, y_def - 1), colour=1, attr=1)

                # Cartel flotante de daño al impactar
                if show_dmg and damage > 0:
                    dmg_str = f" >> -{damage} HP! << "
                    self._safe_print(dmg_str, max(0, x_def), max(0, y_def - 2), colour=7, attr=1, bg=1)

            @property
            def stop_frame(self):
                return total_frames

        def _combat(screen):
            scene = Scene([CombatChoreography(screen)], total_frames)
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
    """Reproduce animación de victoria con asciimatics y audio sincronizado."""
    try:
        from core.eventos import sonido_win
        sonido_win(winner_name)
    except Exception:
        pass

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
