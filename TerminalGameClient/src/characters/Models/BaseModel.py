from utils.common import random
from utils.console import console
from rich.table import Table
from rich.panel import Panel
from core import SOUNDS_MAP
from utils.errors import ERRORS



class Personaje:
    def __init__(self, nombre, vida, poder, stamina, tipo):
        self.nombre = nombre
        self.vida = vida
        self.poder = poder
        self.stamina = stamina
        self.dano = 0
        self.moneda = 100
        self.mochila = []
        self.tipo = tipo

    def atacar(self, rival):
        SOUNDS_MAP[self.nombre]['atacar']()
        ataque = 'ataque basico'
        tipo = 'basico'

        if self.stamina < 10:
            return {
                'ok': False,
                'ataque': ataque,
                'dano': 0,
                'tipo': tipo,
                'msg': 'No tienes suficiente stamina',
            }

        self.dano = 30
        self.stamina -= 10
        rival.vida -= self.dano
        
        return {
            'ok': True,
            'ataque': ataque,
            'dano': self.dano,
            'tipo': tipo,
            'msg': f'{self.nombre} ha realizado un {ataque} y hace {self.dano} de daño a {rival.nombre}',
        }
    
    @staticmethod
    def mostrar_estado(jugador, oponente, vida_maxima_j, vida_maxima_o):
        from ui.sprites import render_sprite_rich

        def make_bar(current, maximum, length=10):
            ratio = max(0.0, min(1.0, current / maximum)) if maximum > 0 else 0.0
            filled = int(ratio * length)
            empty = length - filled
            return "█" * filled + "░" * empty

        bar_j = make_bar(jugador.vida, vida_maxima_j)
        bar_o = make_bar(oponente.vida, vida_maxima_o)

        sprite_j = render_sprite_rich(jugador.nombre, facing="right", pose="idle")
        sprite_o = render_sprite_rich(oponente.nombre, facing="left", pose="idle")

        arena = Table.grid(expand=True)
        arena.add_column(justify="center", ratio=5)
        arena.add_column(justify="center", ratio=2)
        arena.add_column(justify="center", ratio=5)

        arena.add_row(
            f"[bold cyan]▶ {jugador.nombre} (TÚ)[/bold cyan]",
            "[bold red]⚔️  VS  ⚔️[/bold red]",
            f"[bold magenta]{oponente.nombre} (RIVAL) ◀[/bold magenta]"
        )

        arena.add_row(sprite_j, "\n\n\n\n[yellow]• • •[/yellow]", sprite_o)

        stats_j = f"❤️ HP: [green]{bar_j}[/green] {int(jugador.vida)}/{vida_maxima_j} | 🔋 SP: [yellow]{jugador.stamina}[/yellow] | ⚔️ ATK: [magenta]{jugador.poder}[/magenta]"
        stats_o = f"❤️ HP: [green]{bar_o}[/green] {int(oponente.vida)}/{vida_maxima_o} | 🔋 SP: [yellow]{oponente.stamina}[/yellow] | ⚔️ ATK: [magenta]{oponente.poder}[/magenta]"

        arena.add_row(stats_j, " ", stats_o)
        console.print(Panel(arena, title="[bold yellow]CAMPO DE BATALLA RPG[/bold yellow]", border_style="bright_blue", padding=(0, 1)))


    def esperar(self):
        SOUNDS_MAP[self.nombre]['esperar']()
        self.stamina += 15
        self.vida += 15

        return {
            'ok': True,
            'accion': 'esperar',
            'dano': 0,
            'tipo': 'esperar',
            'msg': f'{self.nombre} ha esperado y se prepara para el combate',
        }

    def esquivar(self, atacante, dano):
        SOUNDS_MAP[self.nombre]['try_esquivar']()
        esquivo = random.choice(['esquivar', 'no_esquivar'])

        if dano <= 0:
            return {
                'ok': None,
                'accion': 'esquivar',
                'dano': 0,
                'tipo': 'esquivar',
                'msg': f'{self.nombre} se desplaza y se prepara para el combate'
                }
        
        if esquivo == 'esquivar':
            # Se esquiva el ataque, no pierde vida
            self.vida += dano
            return {
                'ok': True,
                'accion': 'esquivar',
                'dano': 0,
                'tipo': 'esquivar',
                'msg': f'{self.nombre} esquivó el ataque de {atacante.nombre}!',
            }
        else:
            SOUNDS_MAP[self.nombre]['no_esquivar']()
            # Recibe daño reducido
            dano_recibido = dano / 1.5
            self.vida -= dano_recibido
            return {
                'ok': False,
                'accion': 'esquivar',
                'dano': dano_recibido,
                'tipo': 'esquivar',
                'msg': f'{self.nombre} intentó esquivar y recibió {dano_recibido:.1f} de daño de {atacante.nombre}!',
            }


    def elegir_Personaje():
        from utils.data import characters_list, characters_dict
        from ui.button_nav import select_character_grid

        try:
            eleccion = select_character_grid()
            match eleccion:
                case 0:
                    rndm = random.choice(characters_list)
                    return rndm.__class__()
                case 1:
                    return characters_dict['Naruto'].__class__()
                case 2:
                    return characters_dict['Sasuke'].__class__()
                case 3:
                    return characters_dict['Goku'].__class__()
                case 4:
                    return characters_dict['Vegeta'].__class__()
                case 5:
                    return characters_dict['Ichigo'].__class__()
                case 6:
                    return characters_dict['Aizen'].__class__()
                case 7:
                    return characters_dict['Kyo'].__class__()
                case 8:
                    return characters_dict['Iori'].__class__()
                case 9:
                    return characters_dict['Kazuha'].__class__()
                case 10:
                    return characters_dict['Alhacen'].__class__()
                case _:
                    ERRORS['ERROR']()
        except ValueError as e:
            ERRORS['VALUEERROR'](e)



def vida_barra(self, jugador, oponente, vida_maxima_j, vida_maxima_o):
        if self.nombre == jugador.nombre:
            porcentaje_vida = jugador.vida / vida_maxima_j
        if self.nombre == oponente.nombre:
            porcentaje_vida = oponente.vida / vida_maxima_o
        
        total_bloques = 10

        # Calcula cuántos bloques llenos deben mostrarse
        bloques_llenos = int(porcentaje_vida * total_bloques)
        
        # Construye la barra de vida
        barra_vida = '█' * bloques_llenos + ' ' * (total_bloques - bloques_llenos)
        
        print(f"  |  vida:   |{barra_vida}| ({int(porcentaje_vida * 100)}%)")