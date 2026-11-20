from utils.common import time
from utils.colors import Color
from utils.console import console
from rich.panel import Panel
from utils.errors import ERRORS
from core import UI_MAP


def Juego():
    from core.eventos import R, resultado, volver_a_jugar
    from ui.menu_ui import bienvenida, volver_a_jugar_UI, eleccion_UI
    from characters.Models.BaseModel import Personaje
    from characters.Models.oponenteModel import Oponente
    from core.eventos import resultado
    while True:
        bienvenida()

        while True:
            # Elegir personaje de forma interactiva con teclado / flechas / atajos
            jugador = Personaje.elegir_Personaje()
            if jugador:
                break


        # Crear un oponente distinto al jugador seleccionado
        oponente = Oponente.crear_oponente(jugador.nombre)

        R.PuntoR(jugador=jugador, oponente=oponente)
        vida_maxima_j, vida_maxima_o = R.vida_maxima(jugador=jugador, oponente=oponente)

        # Menú RPG interactivo
        MenuLogic(jugador, oponente, vida_maxima_j, vida_maxima_o)

        # Partida Terminada
        result = resultado(jugador.nombre, oponente.nombre, jugador.vida, oponente.vida)

        #Opcion de volver a jugar
        volver_a_jugar_UI()
        volver_a_jugar(jugador, oponente, result)
    #_________________________________________________




def MenuLogic(jugador, oponente, vida_maxima_j, vida_maxima_o):
    from ui.menu_ui import menu_UI, opciones_UI
    from ui.button_nav import select_menu_option

    MOVIMIENTOS = {
        "Naruto": {4: ("Rasengan", 60), 7: ("Esquivar", 15), 8: ("RasenShuriken", 150)},
        "Sasuke": {4: ("Chidori", 60), 7: ("Esquivar", 15), 8: ("Raikiri", 150)},
        "Ichigo": {4: ("Getsuga Tensho", 50), 7: ("Esquivar", 15), 8: ("Bankai", 160)},
        "Aizen": {4: ("Kido", 50), 7: ("Esquivar", 15), 8: ("Kyokasuigetsu", 130)},
        "Kazuha": {4: ("Elemental", 50), 7: ("Esquivar", 15), 8: ("Ulti", 130)},
        "Alhacen": {4: ("Elemental", 50), 7: ("Esquivar", 15), 8: ("Ulti", 130)},
        "Iori": {4: ("Combo", 50), 7: ("Esquivar", 15), 8: ("Especial", 130)},
        "Kyo": {4: ("Combo", 50), 7: ("Esquivar", 15), 8: ("Especial", 130)},
        "Goku": {4: ("Kamehameha", 50), 7: ("Esquivar", 15), 8: ("Super Saiyajin", 130)},
        "Vegeta": {4: ("Garlick Gun", 50), 7: ("Esquivar", 15), 8: ("Super Saiyajin", 130)},
    }

    c = None
    while True: 
        # Construir opciones interactivas para el combate
        opciones_combate = [
            (1, "Atacar", "-10 SP"),
            (2, "Esperar", "+15 SP y +15 HP"),
        ]

        if jugador.nombre in MOVIMIENTOS:
            for k, (nom, costo) in MOVIMIENTOS[jugador.nombre].items():
                opciones_combate.append((k, nom, f"-{costo} SP"))

        opciones_combate.extend([
            ('t', "Tienda", "Comprar pociones"),
            ('e', "Mochila", "Ver inventario"),
            ('o', "Opciones", "Efectos visuales"),
        ])

        try:
            accion = select_menu_option(
                f"⚔️ MENÚ DE COMBATE — {jugador.nombre} vs {oponente.nombre}",
                opciones_combate,
                columnas=2,
                render_header_func=lambda: menu_UI(jugador, oponente, vida_maxima_j, vida_maxima_o)
            )

            if accion is None:
                continue

            if isinstance(accion, str) and accion.isdigit():
                accion = int(accion)

            match accion:
                case 1: #JUGADOR ATACA Y OPONENTE ELIGE ACCIÓN
                    c = atacar_(jugador, oponente)     
                case 2: #JUGADOR ESPERA Y OPONENTE ELIGE ACCIÓN
                    c = esperar_(jugador, oponente)
                case 4: #JUGADOR REALIZA UN COMBO Y OPONENTE ELIGE ACCIÓN
                    c = combos_(jugador, oponente)
                case 8: #JUGADOR REALIZA UN ULTIMATE Y OPONENTE ELIGE ACCIÓN
                    c = especiales_(jugador, oponente)
                case 't' | 'T': #JUGADOR INGRESA A LA TIENDA
                    tienda_(jugador)
                case 'e' | 'E': #JUGADOR INGRESA A SU MOCHILA
                    mochila_(jugador)
                case 'o' | 'O': #OPCIONES Y CONFIGURACIÓN DE EFECTOS
                    opciones_UI()
                case 7: #JUGADOR ESQUIVA Y OPONENTE ELIGE ACCIÓN
                    c = esquivar_(jugador, oponente)
                case _:
                    ERRORS['ERROR']()
        except ValueError as e:
            ERRORS['VALUEERROR'](e)
        
        if c:
            break
            







def atacar_(jugador, oponente):
    console.rule()
    resultado = jugador.atacar(oponente)
    ok = resultado['ok']
    msg = resultado['msg']
    dano = resultado['dano']

    if ok:
        try:
            from ui.animations import play_combat_animation
            play_combat_animation(jugador.nombre, oponente.nombre, 'Ataque Básico', dano, is_special=False)
        except Exception:
            pass
        console.print(Panel(f"{msg}", title="Éxito", style="green"))
        time.sleep(1.5)
    else:
        console.print(Panel(f"{msg}", title="Error", style="red"))
        time.sleep(1.5)
        return

    c = comprobar(jugador, oponente)
    if c:
        return True

    resultado_ = oponente.elegir_accion(jugador, dano)
    ok_ = resultado_['ok']
    msg_ = resultado_['msg']
    dano_ = resultado_.get('dano', 0)
    if ok_:
        if dano_ > 0:
            try:
                from ui.animations import play_combat_animation
                play_combat_animation(oponente.nombre, jugador.nombre, resultado_.get('ataque', 'Ataque'), dano_, is_special=False)
            except Exception:
                pass
        console.print(f'\n[yellow]{msg_}[/yellow]')
    else:
        console.print(f'\n[red]{msg_}[/red]')
    time.sleep(1.5)

    c = comprobar(jugador, oponente)
    if c:
        return True

        
        
    
     


def esperar_(jugador, oponente):
    resultado = jugador.esperar()
    ok = resultado['ok']
    msg = resultado['msg']
    dano = resultado['dano']

    console.print(f'[cyan]{jugador.nombre} decide esperar y recuperar stamina y vida.[/cyan]')
    time.sleep(2)

    resultado_ = oponente.elegir_accion(jugador, dano)
    ok_ = resultado_['ok']
    msg_ = resultado_['msg']
    dano_ = resultado_.get('dano', 0)
    if ok_:
        if dano_ > 0:
            try:
                from ui.animations import play_combat_animation
                play_combat_animation(oponente.nombre, jugador.nombre, resultado_.get('ataque', 'Ataque'), dano_, is_special=False)
            except Exception:
                pass
        console.print(f'\n[yellow]{msg_}[/yellow]')
    else:
        console.print(f'\n[red]{msg_}[/red]')
    time.sleep(1.5)

    c = comprobar(jugador, oponente)
    if c:
        return True

    if ok:
        console.print(f"\n[cyan]{msg}[/cyan]")
        time.sleep(2)
    else:
        console.print(f'\n[red]{msg}[/red]')
        time.sleep(2)
    


    c = comprobar(jugador, oponente)
    if c:
        return True

    



def combos_(jugador, oponente):
    from core.eventos import combos
    resultado = combos(jugador, oponente)
    ok = resultado['ok']
    msg = resultado['msg']
    dano = resultado['dano']
    if ok:
        try:
            from ui.animations import play_combat_animation
            play_combat_animation(jugador.nombre, oponente.nombre, resultado.get('ataque', resultado.get('tipo', 'Combo')), dano, is_special=False)
        except Exception:
            pass
        console.print(f"\n[cyan]{msg}[/cyan]")
        time.sleep(1.5)
    else:
        console.print(f'\n[red]{msg}[/red]')
        time.sleep(1.5)
        return

    c = comprobar(jugador, oponente)
    if c:
        return True

    resultado_ = oponente.elegir_accion(jugador, dano)
    ok_ = resultado_['ok']
    msg_ = resultado_['msg']
    dano_ = resultado_.get('dano', 0)
    if ok_:
        if dano_ > 0:
            try:
                from ui.animations import play_combat_animation
                play_combat_animation(oponente.nombre, jugador.nombre, resultado_.get('ataque', 'Ataque'), dano_, is_special=False)
            except Exception:
                pass
        console.print(Panel(f"{msg_}", title="Acción oponente", style="yellow"))
    else:
        console.print(Panel(f"{msg_}", title="Error", style="red"))
    time.sleep(1.5)


    c = comprobar(jugador, oponente)
    if c:
        return True

    


def tienda_(jugador):
    from core.tienda_log import Tienda_log
    UI_MAP['tienda']()
    while True:
        confirm = Tienda_log(jugador)
        if confirm:
            break





def mochila_(jugador):
    from core.mochila_log import Mochila_log
    UI_MAP['mochila']()
    while True:
        confirm = Mochila_log(jugador)
        if confirm:
            break



def esquivar_(jugador, oponente):
    console.print(f'\n[cyan]{jugador.nombre} decide esquivar el ataque[/cyan]')
    time.sleep(2)
    dano = 0

    resultado_ = oponente.elegir_accion(jugador, dano)
    ok_ = resultado_['ok']
    msg_ = resultado_['msg']
    dano_ = resultado_.get('dano', 0)
    if ok_:
        console.print(f'\n[yellow]{msg_}[/yellow]')
    else:
        console.print(f'\n[red]{msg_}[/red]')
    time.sleep(2)

    resultado = jugador.esquivar(oponente, dano_)
    ok = resultado['ok']
    msg = resultado['msg']


    c = comprobar(jugador, oponente)
    if c:
        return True

    
    if ok:
        console.print(f"\n[cyan]{msg}[/cyan]")
        time.sleep(2)
    elif ok == None:
        console.print(f"\n[yellow]{msg}[/yellow]")
        time.sleep(2)
    else:
        console.print(f'\n[red]{msg}[/red]')
        time.sleep(2)
        return


    c = comprobar(jugador, oponente)
    if c:
        return True

    
def especiales_(jugador, oponente):
    from core.eventos import especiales
    resultado = especiales(jugador, oponente)
    ok = resultado['ok']
    msg = resultado['msg']
    dano = resultado['dano']

    if ok:
        try:
            from ui.animations import play_combat_animation
            play_combat_animation(jugador.nombre, oponente.nombre, resultado.get('ataque', resultado.get('tipo', 'Ultimate')), dano, is_special=True)
        except Exception:
            pass
        console.print(f"\n[cyan]{msg}[/cyan]")
        time.sleep(1.5)
    else:
        console.print(f'\n[red]{msg}[/red]')
        time.sleep(1.5)
        return


    c = comprobar(jugador, oponente)
    if c:
        return True


    


    resultado_ = oponente.elegir_accion(jugador, dano)
    ok_ = resultado_['ok']
    msg_ = resultado_['msg']
    dano_ = resultado_.get('dano', 0)
    if ok_:
        if dano_ > 0:
            try:
                from ui.animations import play_combat_animation
                play_combat_animation(oponente.nombre, jugador.nombre, resultado_.get('ataque', 'Ataque'), dano_, is_special=False)
            except Exception:
                pass
        console.print(f'\n[yellow]{msg_}[/yellow]')
    else:
        console.print(f'\n[red]{msg_}[/red]')
    time.sleep(1.5)


    c = comprobar(jugador, oponente)
    if c:
        return True

    






def comprobar(jugador, oponente):
    if jugador.vida <= 0 or oponente.vida <= 0:
        return True
    else:
        return False


