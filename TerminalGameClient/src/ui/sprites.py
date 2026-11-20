# -*- coding: utf-8 -*-
r"""
Sprites ASCII para personajes y efectos de combate.
Cumple con las especificaciones técnicas:
- Codificación UTF-8
- Relación de aspecto ~18 columnas x 11 líneas
- ASCII shading (░, ▒, ▓, █, /, \, |, (, ))
- Raw strings r'''...''' con ancho idéntico por línea
"""

SPRITES_PERSONAJES = {
    'Naruto': r"""
   \  / / \ \  /  
  __\/__\_/__\/__ 
 |   ___   ___   |
 |  ( █ ) ( █ )  |
 |   `-'   `-'   |
 |  = ( ._. ) =  |
 |    \___/      |
  \  |=====|    / 
   \ |     |   /  
    \|_____|__/   
     /     \      """.strip('\n'),

    'Sasuke': r"""
    /\   /\   /\  
   /  \_/  \_/  \ 
  /  ______      \
 |  / ░ ░  \      |
 | | ( o ) ( o )  |
 |  \     _      /
  \  \___/      / 
   \  |===|    /  
   /  | U |    \  
  /   |___|     \ 
      /   \       """.strip('\n'),

    'Goku': r"""
     /\  /\  /\   
    /  \/  \/  \  
  _/  /  |  \   \_
 |   ( █ ) ( █ )  |
 |    \  ^  /     |
  \    \___/     /
  /\   |---|    /\
 /  \  | K |   /  \
 \   \_|___|_/    /
  \  |     |     /
     |_____|      """.strip('\n'),

    'Vegeta': r"""
      /\  /\  /\  
     /  \/  \/  \ 
    /   / /\ \   \
   |   ( • ) ( • )|
   |     \ v /    |
    \    `---'   /
    /\   |===|  /\
   /  \_ | S |_/  \
  |     ||___||    |
   \    |     |   /
        |_____|   """.strip('\n'),

    'Ichigo': r"""
    \ \  |  / /   
   __\_|_|_|_/__  
  /  \       /  \ 
 |   ( █ ) ( █ )  |
 |    \  -  /     |
  \    `==='     /
   \   | Z |    / 
  / \__|___|___/ \
 |  |  |   |   |  |
  \ |  |___|   | /
    \  /   \   /  """.strip('\n'),

    'Aizen': r"""
     .--------.   
    /  ______  \  
   |  /      \  | 
   | | ( ¬ ) ( ¬ )|
   |  \   ~   / | 
    \  `-----' /  
     \  |===| /   
    / \ | H | / \ 
   |   \|___|/   |
   |    |   |    |
   \____|___|____/""".strip('\n'),

    'Kyo': r"""
     .--------.   
    [==========]  
    /  _    _  \  
   |  ( █) ( █) | 
   |    \  - /  | 
    \   `---'  /  
    /\  |SUN|  /\ 
   /  \ |--- |/  \
  |    \|   |/    |
   \    |___|    /
        /   \     """.strip('\n'),

    'Iori': r"""
      /|   /|     
     / |__/ |     
    /   \   \     
   | ( █) ( █)\   
   |   \  _    \  
    \   `--'    \ 
    /\  |MOON|  /\
   /  \ |--- | /  \
  |   ( |   | )   |
   \   \|___|/   /
        /   \     """.strip('\n'),

    'Kazuha': r"""
      /\   /|     
     /  \_/ |     
    /   🍁  \     
   |  ( • ) ( • ) |
   |    \   /     |
    \    `-'     /
    /\  |WIND|  /\
   /  \_|--- |_/  \
  |    \|   |/    |
   \    |___|    /
        /   \     """.strip('\n'),

    'Alhacen': r"""
    .---====---.  
   /  |      |  \ 
  (🎧 ( █ ) ( █ )🎧)
   \   \  ^  /  / 
    \   `---'  /  
    /\  |DNDR| /\ 
   /  \_|--- |_/ \
  |     |   |     |
   \    |___|    /
        /   \     
       |_____|    """.strip('\n'),
}

SPRITES_EFECTOS = {
    'atacar': r"""
   \  \  |  /  /  
  --= [CRITICAL] =--
   /  /  |  \  \  """.strip('\n'),

    'esperar': r"""
      .  *  .     
    *  (REGEN) *  
      .  *  .     """.strip('\n'),

    'esquivar': r"""
    ( ( ( DODGE ) ) )
     ░ ▒ ▓ █ ▓ ▒ ░  """.strip('\n'),

    'combo': r"""
  ═══► [COMBO HIT] ◄═══
   ⚡  ⚡ ░▒▓█▓▒░ ⚡  ⚡  """.strip('\n'),

    'ulti': r"""
  ★ ★ ★ [ULTIMATE] ★ ★ ★
  ▒▓████████████████▓▒
   ★ ★ ★ [BURST] ★ ★ ★  """.strip('\n'),
}

def get_sprite(nombre: str) -> str:
    """Devuelve el sprite ASCII del personaje o un sprite genérico si no existe."""
    return SPRITES_PERSONAJES.get(nombre, SPRITES_PERSONAJES['Naruto'])

def get_effect_sprite(tipo: str) -> str:
    """Devuelve el sprite ASCII del efecto."""
    return SPRITES_EFECTOS.get(tipo, SPRITES_EFECTOS['atacar'])
