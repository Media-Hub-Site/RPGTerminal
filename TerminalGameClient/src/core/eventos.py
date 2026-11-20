from utils.common import os, time
from utils.colors import Color
from utils.console import console
from core.sound import sound
from core import SOUNDS_MAP, UI_MAP
   
# _______________________________________________________________________
def combos(self, rival):
    # Mapeo de (tipo, nombre) → acción especial
    acciones_combo = {
    'Naruto': {
        'rasengan': lambda rival: self.Rasengan(rival),
    },
    'Sasuke': {
        'chidori': lambda rival: self.Chidori(rival),
    },
    'Ichigo': {
        'getsuga': lambda rival: self.getsuga(rival),
    },
    'Aizen': {
        'kido': lambda rival: self.kido(rival),
    },
    'Kyo': {
        'kyo_1': lambda rival: self.combo(rival),
    },
    'Iori': {
        'iori_1': lambda rival: self.combo(rival),
    },
    'Kazuha': {
        'k_elemental': lambda rival: self.K_elemental(rival),
    },
    'Alhacen': {
        'a_elemental': lambda rival: self.A_elemental(rival),
    },
    'Goku': {
        'kamehameha': lambda rival: self.Kamehameha(rival),
    },
    'Vegeta': {
        'garlick_gun': lambda rival: self.GarlickGun(rival),
    },
}
    accion = list(acciones_combo.get(self.nombre, {}).values())

    if accion:
        return accion[0](rival)
    else:
        console.print(f"⚠️ No hay un combo definido para {self.nombre}.", style="red")


    
    

def especiales(self, rival):
    # Mapeo de (tipo, nombre) → acción especial
    acciones_combo = {
    'Naruto': {
        'rasengan': lambda rival: self.RasenShuriken(rival),
    },
    'Sasuke': {
        'chidori': lambda rival: self.Raikiri(rival),
    },
    'Ichigo': {
        'getsuga': lambda rival: self.bankai(rival),
    },
    'Aizen': {
        'kido': lambda rival: self.kyokasuigetsu(rival),
    },
    'Kyo': {
        'kyo_1': lambda rival: self.ulti(rival),
    },
    'Iori': {
        'iori_1': lambda rival: self.ulti(rival),
    },
    'Kazuha': {
        'k_elemental': lambda rival: self.K_ulti(rival),
    },
    'Alhacen': {
        'a_elemental': lambda rival: self.A_ulti(rival),
    },
    'Goku': {
        'kamehameha': lambda rival: self.Ssj(rival),
    },
    'Vegeta': {
        'garlick_gun': lambda rival: self.Ssj(rival),
    },
}
    accion = list(acciones_combo.get(self.nombre, {}).values())

    if accion:
        return accion[0](rival)
    else:
        console.print(f"⚠️ No hay un combo definido para {self.nombre}.", style="red")





def resultado(jugador_nombre, oponente_nombre, jugador_vida, oponente_vida):
    os.system("cls")
    console.print("El ganador de esta reñida pelea es..")
    time.sleep(2)
    jugador_gana = oponente_vida <= 0 and jugador_vida > 0
    oponente_gana = oponente_vida > 0 and jugador_vida <= 0

    if jugador_gana or oponente_gana:
        winner = jugador_nombre if jugador_gana else oponente_nombre
        try:
            from ui.animations import play_victory_animation
            play_victory_animation(winner)
        except Exception:
            pass
        console.print(f"\n[green][!{winner}¡][/green]\n")
        sonido_win(winner)
        time.sleep(2.5)
        return True if jugador_gana else False

        
        
    

class R:
    
    oponente_r = 0
    oponente_s = 0
    jugador_r = 0
    jugador_s = 0

    @classmethod
    def PuntoR(cls, jugador, oponente):
        
        cls.oponente_r = oponente.vida
        cls.oponente_s = oponente.stamina
        cls.jugador_r = jugador.vida
        cls.jugador_s = jugador.stamina

        
    def vida_maxima(jugador, oponente):

        vida_maxima_j = jugador.vida
        vida_maxima_o = oponente.vida

        return vida_maxima_j, vida_maxima_o

    @classmethod
    def Reset(cls, jugador, oponente):
        
        oponente.vida = cls.oponente_r
        oponente.stamina = cls.oponente_s
        jugador.vida = cls.jugador_r
        jugador.stamina = cls.jugador_s
        jugador.moneda += 100
        oponente.moneda += 100



def sonido_win(nombre):

    tipos = {
        'Naruto': SOUNDS_MAP['Naruto']['win'],
        'Sasuke': SOUNDS_MAP['Sasuke']['win'],
        'Ichigo': SOUNDS_MAP['Ichigo']['win'],
        'Aizen': SOUNDS_MAP['Aizen']['win'],
        'Goku': SOUNDS_MAP['Goku']['win'],
        'Vegeta': SOUNDS_MAP['Vegeta']['win'],
        'Kazuha': SOUNDS_MAP['Kazuha']['win'],
        'Alhacen': SOUNDS_MAP['Alhacen']['win'],
        'Iori': SOUNDS_MAP['Iori']['win'],
        'Kyo': SOUNDS_MAP['Kyo']['win'],
    }

    if nombre in tipos:
        tipos[nombre]()
    else:
        tipos[nombre]()
# _______________________________________________________________________
# _______________________________________________________________________

def volver_a_jugar(jugador, oponente, resultado):
    from ui.button_nav import select_menu_option

    if resultado:
        UI_MAP['win']()
    else:
        UI_MAP['derrota']()

    opciones = [
        (1, "Volver a jugar", "Iniciar una nueva partida"),
        (2, "Salir del juego", "Cerrar RPG Terminal")
    ]

    while True:
        try:
            eleccion = select_menu_option(
                "🎮 ¿DESEAS VOLVER A JUGAR?",
                opciones,
                columnas=2
            )
            if eleccion == 1:
                R.Reset(jugador, oponente)
                break
            elif eleccion in (2, None):
                sound.sGameOver()
                console.print("\n[bold yellow]**************** Terminando el programa. **************[/bold yellow]\n")
                for i in range(3+1):
                    console.print(i)
                    time.sleep(1)
                raise SystemExit()
            else:
                error()
        except ValueError as e:
            valueError(e)
        
# _______________________________________________________________________
#-------------------------------------------------------------------------
    
from utils.errors import ERRORS, error, valueError
