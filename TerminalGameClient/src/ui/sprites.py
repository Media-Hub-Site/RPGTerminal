# -*- coding: utf-8 -*-
r"""
Motor de Sprites Pixel-Art estilo Chibi (OMORI / RPG Retro) para Terminal.
Utiliza bloques medios Unicode (▀, ▄, █) para renderizar 2 píxeles verticales por
celda de terminal, logrando píxeles cuadrados 1:1 en color verdadero (Rich) y
16 colores con transparencia (Asciimatics).

- Cada sprite es una cuadrícula de 16x20 píxeles -> 16 columnas x 10 líneas en consola.
- Orientación automática: jugador mira a la derecha ('right'), rival a la izquierda ('left').
- Múltiples poses por personaje ('idle' y 'attack').
"""

from typing import Dict, List, Tuple
from rich.text import Text

# ---------------------------------------------------------------------------
# Paletas de color por personaje
# Cada clave de píxel mapea a: (hex_rich, (asciimatics_fg, asciimatics_attr))
# Asciimatics colours: 0=BLACK, 1=RED, 2=GREEN, 3=YELLOW, 4=BLUE, 5=MAGENTA, 6=CYAN, 7=WHITE
# Asciimatics attrs: 1=BOLD (brillante), 2=NORMAL
# ---------------------------------------------------------------------------

PALETAS: Dict[str, Dict[str, Tuple[str, Tuple[int, int]]]] = {
    'Naruto': {
        'K': ('#141418', (0, 2)),   # Contorno oscuro
        'H': ('#FFD700', (3, 1)),   # Cabello rubio brillante
        'h': ('#E6A800', (3, 2)),   # Sombra cabello
        'W': ('#FFE0BD', (7, 1)),   # Piel
        'E': ('#0099FF', (6, 1)),   # Ojos azules
        'B': ('#2B4C8C', (4, 1)),   # Banda ninja azul
        'S': ('#CBD5E1', (7, 2)),   # Placa metálica
        'C': ('#FF6B00', (3, 1)),   # Traje naranja
        'c': ('#222228', (0, 2)),   # Hombros/detalles negros
    },
    'Sasuke': {
        'K': ('#101016', (0, 2)),   # Contorno
        'H': ('#1C223D', (4, 2)),   # Cabello azul oscuro Uchiha
        'h': ('#2F3B69', (4, 1)),   # Reflejo cabello
        'W': ('#F5E8DC', (7, 1)),   # Piel clara
        'E': ('#FF1E1E', (1, 1)),   # Ojo Sharingan rojo
        'B': ('#F1F5F9', (7, 1)),   # Cuello alto blanco
        'S': ('#3B4C8A', (4, 1)),   # Detalle azul
        'C': ('#283663', (4, 2)),   # Túnica azul marino
        'c': ('#E2E8F0', (7, 2)),   # Pantalón/vendaje blanco
    },
    'Goku': {
        'K': ('#121216', (0, 2)),
        'H': ('#1E1E24', (0, 2)),   # Cabello negro Saiyan
        'h': ('#3A3A46', (7, 2)),   # Brillo cabello
        'W': ('#FFDBB5', (7, 1)),   # Piel
        'E': ('#111111', (0, 2)),   # Ojo negro
        'B': ('#1D4ED8', (4, 1)),   # Camiseta/cinturón azul
        'S': ('#1D4ED8', (4, 1)),
        'C': ('#FF6A00', (3, 1)),   # Gi naranja
        'c': ('#D95300', (1, 1)),   # Sombra gi
    },
    'Vegeta': {
        'K': ('#121216', (0, 2)),
        'H': ('#1B1B22', (0, 2)),   # Cabello flama negro
        'h': ('#383844', (7, 2)),
        'W': ('#FAD6B4', (7, 1)),
        'E': ('#111111', (0, 2)),
        'B': ('#EAB308', (3, 1)),   # Hombreras doradas
        'S': ('#F8FAFC', (7, 1)),   # Armadura blanca
        'C': ('#1D4ED8', (4, 1)),   # Traje azul Saiyan
        'c': ('#F8FAFC', (7, 1)),   # Botas/guantes blancos
    },
    'Ichigo': {
        'K': ('#121216', (0, 2)),
        'H': ('#FF7A00', (3, 1)),   # Cabello naranja brillante
        'h': ('#CC5500', (1, 1)),
        'W': ('#F7DFC8', (7, 1)),
        'E': ('#4A2C1A', (3, 2)),
        'B': ('#F8FAFC', (7, 1)),   # Cinta/cuello blanco
        'S': ('#94A3B8', (6, 2)),   # Espada Zangetsu
        'C': ('#1E1E26', (0, 2)),   # Shihakusho negro
        'c': ('#E2E8F0', (7, 1)),   # Detalle blanco
    },
    'Aizen': {
        'K': ('#121216', (0, 2)),
        'H': ('#5C3A21', (3, 2)),   # Cabello castaño
        'h': ('#7C5032', (3, 2)),
        'W': ('#F7E3D2', (7, 1)),
        'E': ('#3B2618', (3, 2)),
        'B': ('#F8FAFC', (7, 1)),   # Haori de Capitán blanco
        'S': ('#94A3B8', (6, 1)),   # Lentes / brillo
        'C': ('#F8FAFC', (7, 1)),   # Capa blanca
        'c': ('#1E1E26', (0, 2)),   # Túnica interior negra
    },
    'Kyo': {
        'K': ('#121216', (0, 2)),
        'H': ('#3E2723', (3, 2)),   # Cabello castaño oscuro
        'h': ('#5D4037', (3, 2)),
        'W': ('#FFE0C2', (7, 1)),
        'E': ('#1E1E24', (0, 2)),
        'B': ('#FFFFFF', (7, 1)),   # Banda blanca KOF
        'S': ('#EF4444', (1, 1)),   # Fuego / guantes rojos
        'C': ('#1F2937', (0, 2)),   # Chaqueta negra
        'c': ('#F8FAFC', (7, 1)),   # Camiseta blanca
    },
    'Iori': {
        'K': ('#121216', (0, 2)),
        'H': ('#DC2626', (1, 1)),   # Cabello rojo carmesí
        'h': ('#991B1B', (1, 2)),
        'W': ('#F5E4D7', (7, 1)),
        'E': ('#1E1E24', (0, 2)),
        'B': ('#F8FAFC', (7, 1)),   # Camisa blanca
        'S': ('#A855F7', (5, 1)),   # Llama púrpura
        'C': ('#18181B', (0, 2)),   # Chaqueta negra
        'c': ('#DC2626', (1, 1)),   # Pantalón rojo
    },
    'Kazuha': {
        'K': ('#121216', (0, 2)),
        'H': ('#E5E7EB', (7, 1)),   # Cabello platino
        'h': ('#EF4444', (1, 1)),   # Mechón rojo icónico
        'W': ('#FCE6D4', (7, 1)),
        'E': ('#DC2626', (1, 1)),   # Ojo rubí
        'B': ('#DC2626', (1, 1)),   # Bufanda/hoja de arce
        'S': ('#F59E0B', (3, 1)),   # Detalle dorado
        'C': ('#991B1B', (1, 2)),   # Haori rojo samurái
        'c': ('#1F2937', (0, 2)),   # Armadura oscura
    },
    'Alhacen': {
        'K': ('#121216', (0, 2)),
        'H': ('#94A3B8', (7, 2)),   # Cabello gris plateado
        'h': ('#2DD4BF', (6, 1)),   # Puntas turquesa
        'W': ('#F7E2D0', (7, 1)),
        'E': ('#14B8A6', (6, 1)),   # Ojos verde-turquesa
        'B': ('#EAB308', (3, 1)),   # Audífonos / detalle dorado
        'S': ('#2DD4BF', (6, 1)),   # Gema Dendro
        'C': ('#0F766E', (6, 2)),   # Capa verde-petróleo
        'c': ('#1E293B', (0, 2)),   # Traje oscuro
    },
}

# ---------------------------------------------------------------------------
# Plantillas de cabezas (16x11) y cuerpos (16x9) -> Sprite completo 16x20
# Orientación base: mirando hacia la DERECHA (→)
# ---------------------------------------------------------------------------

CABEZAS_CHIBI: Dict[str, List[str]] = {
    # Naruto: pelo en punta + banda ninja con placa metálica
    'Naruto': [
        "....K..KK..K....",
        "...KHKHHHHKHK...",
        "..KHHHHHHHHHHK..",
        ".KHHhHHHHHHHHHK.",
        ".KBBBBBBBBBBSSK.",
        ".KHHHHWWWWWWHHK.",
        ".KHHHWWWWWWWWK..",
        ".KHHHWWWWWEWWK..",
        "..KHHWWWWWEWWK..",
        "...KKWWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Sasuke: pelo Uchiha con puntas hacia atrás + flequillo
    'Sasuke': [
        ".....KKKKKK.....",
        "...KKHHHHHHKK...",
        ".KKHHHHHHHHHHK..",
        "KHHhHHHHHHHHHHK.",
        ".KHHHHHHHHHHHHK.",
        "..KHHHHHHWWWHHK.",
        "..KHHHHWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Goku: picos grandes icónicos atrás y arriba
    'Goku': [
        "..KK..KKKK..K...",
        ".KHHKKHHHHKHK...",
        "KHHHHhHHHHHHHK..",
        ".KHHHHHHHHHHHHK.",
        "KHHHHHHHHHHHHHK.",
        ".KKHHHHHWWWWWKK.",
        "..KHHHHWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Vegeta: pelo alto en forma de flama
    'Vegeta': [
        ".....KKKKKK.....",
        "....KHHHHHHK....",
        "...KHHhHHHHHK...",
        "...KHHHHHHHHK...",
        "..KHHHHHHHHHHK..",
        "..KHHHHHWWWWWK..",
        "..KHHHHWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KKHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Ichigo: pelo naranja en punta + espada Zangetsu detrás
    'Ichigo': [
        ".KS..KKKKKK.....",
        ".KSKKHHHHHHKK...",
        "..KHHHHHHHHHHK..",
        ".KHHhHHHHHHHHHK.",
        ".KHHHHHHHHHHHHK.",
        "..KHHHHHWWWWWHK.",
        "..KHHHWWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Aizen: pelo peinado atrás con mechón cayendo al frente
    'Aizen': [
        "....KKKKKKKK....",
        "...KHHHHHHHHK...",
        "..KHHhHHHHHHHK..",
        "..KHHHHHHHHHHHK.",
        "..KHHHHHHHHHHHK.",
        "..KHHHHHWWWWWHK.",
        "..KHHHHWWSSWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Kyo: banda blanca frontal + pelo castaño
    'Kyo': [
        "....KKKKKKKK....",
        "...KHHHHHHHHK...",
        "..KHHhHHHHHHHK..",
        "..KHHHHHHHHHHHK.",
        "..KBBBBBBBBBBBK.",
        "..KHHHHWWWWWWWK.",
        "..KHHHWWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Iori: flequillo largo rojo cubriendo la parte trasera/lateral
    'Iori': [
        "....KKKKKKKK....",
        "...KHHHHHHHHK...",
        "..KHHhHHHHHHHK..",
        ".KHHHHHHHHHHHHK.",
        ".KHHHHHHHHHHHHK.",
        ".KHHHHHHHWWWWWK.",
        ".KHHHHHHWWWWWWK.",
        "..KHHHHWWWEWWWK.",
        "..KHHHHWWWEWWWK.",
        "...KHHHWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Kazuha: cabello platino con mechón rojo + coleta baja
    'Kazuha': [
        "....KKKKKKKK....",
        "...KHHHHHHHHK...",
        "..KHHHHhHHHHHK..",
        "..KHHHHhHHHHHHK.",
        "..KHHHHhHHHHHHK.",
        ".KKHHHHhWWWWWHK.",
        ".KHHHHWWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KKHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
    # Alhacen: cabello gris/turquesa + audífonos dorados
    'Alhacen': [
        "....KKKKKKKK....",
        "...KHHHHHHHHK...",
        "..KHHhHHHHHHHK..",
        "..KHHHHHHHHHHHK.",
        "..KHHBBHHHHHHHK.",
        "..KHHBBHWWWWWHK.",
        "..KHHBBWWWWWWWK.",
        "..KHHHWWWWEWWWK.",
        "..KHHHWWWWEWWWK.",
        "...KHHWWWWWWWK..",
        "....KKKWWWWKK...",
    ],
}

# Cuerpo compacto chibi estilo OMORI (16x9) - pose Idle (mirando a la derecha)
CUERPO_IDLE: List[str] = [
    "....KBBCCBBK....",
    "...KCCCCCCCCK...",
    "...KCCcWWcCCK...",
    "...KCCCWWCCCK...",
    "...KBBBBBBBBK...",
    "....KCCCCCCK....",
    "....KccKKccK....",
    "...KccK..KccK...",
    "...KKKK..KKKK...",
]

# Cuerpo pose Ataque / Avance (16x9) - brazo extendido con energía/golpe
CUERPO_ATTACK: List[str] = [
    "....KBBCCBBK....",
    "...KCCCCCCCCKK..",
    "...KCCCCCCCWWWK.",
    "...KCCCCCCCCKK..",
    "...KBBBBBBBBK...",
    "....KCCCCCCK....",
    "...KccK..KccK...",
    "..KccK....KccK..",
    "..KKKK....KKKK..",
]


def _get_pixel_grid(nombre: str, facing: str = "right", pose: str = "idle") -> List[str]:
    """Combina cabeza + cuerpo en una cuadrícula 16x20 y voltea si mira a la izquierda."""
    cabeza = CABEZAS_CHIBI.get(nombre, CABEZAS_CHIBI['Naruto'])
    cuerpo = CUERPO_ATTACK if pose == "attack" else CUERPO_IDLE
    grid = cabeza + cuerpo
    if facing == "left":
        return [row[::-1] for row in grid]
    return grid


def render_sprite_rich(nombre: str, facing: str = "right", pose: str = "idle") -> Text:
    """
    Renderiza el sprite chibi 16x20 como un objeto Rich Text usando bloques medios (▀, ▄, █)
    con colores TrueColor (24-bit), ocupando 16 columnas x 10 líneas.
    """
    grid = _get_pixel_grid(nombre, facing=facing, pose=pose)
    paleta = PALETAS.get(nombre, PALETAS['Naruto'])

    text = Text()
    for y in range(0, len(grid), 2):
        top_row = grid[y]
        bot_row = grid[y + 1] if y + 1 < len(grid) else "." * len(top_row)

        for x in range(len(top_row)):
            t_ch = top_row[x]
            b_ch = bot_row[x]
            t_col = paleta[t_ch][0] if t_ch in paleta else None
            b_col = paleta[b_ch][0] if b_ch in paleta else None

            if t_col is None and b_col is None:
                text.append(" ")
            elif t_col == b_col:
                text.append("█", style=t_col)
            elif t_col is not None and b_col is None:
                text.append("▀", style=t_col)
            elif t_col is None and b_col is not None:
                text.append("▄", style=b_col)
            else:
                text.append("▀", style=f"{t_col} on {b_col}")

        if y + 2 < len(grid):
            text.append("\n")

    return text


def render_sprite_asciimatics(nombre: str, facing: str = "right", pose: str = "idle") -> str:
    """
    Renderiza el sprite chibi 16x20 en formato string con etiquetas de color
    nativas de Asciimatics (${fg,attr,bg}) y bloques medios (▀, ▄, █).
    """
    grid = _get_pixel_grid(nombre, facing=facing, pose=pose)
    paleta = PALETAS.get(nombre, PALETAS['Naruto'])

    lines: List[str] = []
    for y in range(0, len(grid), 2):
        top_row = grid[y]
        bot_row = grid[y + 1] if y + 1 < len(grid) else "." * len(top_row)
        line_parts: List[str] = []

        for x in range(len(top_row)):
            t_ch = top_row[x]
            b_ch = bot_row[x]
            t_info = paleta[t_ch][1] if t_ch in paleta else None
            b_info = paleta[b_ch][1] if b_ch in paleta else None

            if t_info is None and b_info is None:
                line_parts.append(" ")
            elif t_info is not None and b_info is None:
                fg, attr = t_info
                line_parts.append(f"${{{fg},{attr},0}}▀")
            elif t_info is None and b_info is not None:
                fg, attr = b_info
                line_parts.append(f"${{{fg},{attr},0}}▄")
            elif t_info == b_info:
                fg, attr = t_info
                line_parts.append(f"${{{fg},{attr},0}}█")
            else:
                tfg, tattr = t_info
                bfg, _ = b_info
                line_parts.append(f"${{{tfg},{tattr},{bfg}}}▀")

        lines.append("".join(line_parts))

    return "\n".join(lines)


def get_sprite(nombre: str, facing: str = "right", pose: str = "idle") -> str:
    """Devuelve una versión monocromática en bloques Unicode (compatibilidad / tests)."""
    grid = _get_pixel_grid(nombre, facing=facing, pose=pose)
    lines: List[str] = []
    for y in range(0, len(grid), 2):
        top_row = grid[y]
        bot_row = grid[y + 1] if y + 1 < len(grid) else "." * len(top_row)
        row_chars = []
        for x in range(len(top_row)):
            t = top_row[x] != "."
            b = bot_row[x] != "."
            if not t and not b:
                row_chars.append(" ")
            elif t and b:
                row_chars.append("█")
            elif t:
                row_chars.append("▀")
            else:
                row_chars.append("▄")
        lines.append("".join(row_chars))
    return "\n".join(lines)


SPRITES_PERSONAJES = {name: get_sprite(name) for name in PALETAS}

SPRITES_EFECTOS = {
    'atacar': r"""
   \  \  |  /  /  
  --= [IMPACTO] =--
   /  /  |  \  \  """.strip('\n'),

    'esperar': r"""
      .  *  .     
    *  (REGEN) *  
      .  *  .     """.strip('\n'),

    'esquivar': r"""
   ( ( ( ESQUIVE ) ) )
     ░ ▒ ▓ █ ▓ ▒ ░   """.strip('\n'),

    'combo': r"""
  ═══► [COMBO!] ◄═══
   ⚡ ░▒▓███▓▒░ ⚡  """.strip('\n'),

    'ulti': r"""
  ★ ★ [ULTIMATE!] ★ ★
  ▒▓███████████████▓▒
  ★ ★  [IMPACTO]  ★ ★""".strip('\n'),
}


def draw_sprite_asciimatics(screen, nombre: str, x: int, y: int, facing: str = "right", pose: str = "idle", flash_colour=None):
    """
    Dibuja el sprite chibi 16x20 directamente en una pantalla de Asciimatics
    en las coordenadas (x, y) con transparencia real y soporte de flash de impacto.
    """
    grid = _get_pixel_grid(nombre, facing=facing, pose=pose)
    paleta = PALETAS.get(nombre, PALETAS['Naruto'])
    max_h = screen.height
    max_w = screen.width

    for row_idx, py in enumerate(range(0, len(grid), 2)):
        sy = y + row_idx
        if sy < 0 or sy >= max_h:
            continue
        top_row = grid[py]
        bot_row = grid[py + 1] if py + 1 < len(grid) else "." * len(top_row)

        for col_idx in range(len(top_row)):
            sx = x + col_idx
            if sx < 0 or sx >= max_w:
                continue
            t_ch = top_row[col_idx]
            b_ch = bot_row[col_idx]
            t_info = paleta[t_ch][1] if t_ch in paleta else None
            b_info = paleta[b_ch][1] if b_ch in paleta else None

            if t_info is None and b_info is None:
                continue

            if flash_colour is not None:
                if t_info is not None and b_info is None:
                    screen.print_at("▀", sx, sy, colour=flash_colour, attr=1, bg=0)
                elif t_info is None and b_info is not None:
                    screen.print_at("▄", sx, sy, colour=flash_colour, attr=1, bg=0)
                else:
                    screen.print_at("█", sx, sy, colour=flash_colour, attr=1, bg=0)
            else:
                if t_info is not None and b_info is None:
                    fg, attr = t_info
                    screen.print_at("▀", sx, sy, colour=fg, attr=attr, bg=0)
                elif t_info is None and b_info is not None:
                    fg, attr = b_info
                    screen.print_at("▄", sx, sy, colour=fg, attr=attr, bg=0)
                elif t_info == b_info:
                    fg, attr = t_info
                    screen.print_at("█", sx, sy, colour=fg, attr=attr, bg=0)
                else:
                    tfg, tattr = t_info
                    bfg, _ = b_info
                    screen.print_at("▀", sx, sy, colour=tfg, attr=tattr, bg=bfg)


def get_effect_sprite(tipo: str) -> str:
    """Devuelve el sprite ASCII del efecto."""
    return SPRITES_EFECTOS.get(tipo, SPRITES_EFECTOS['atacar'])
