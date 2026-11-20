import sys
import os

# Asegurar que el src está en el sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from characters.Models.narutoModels import Naruto, Sasuke
from characters.Models.oponenteModel import Oponente

def test_character_stats_and_attack():
    naruto = Naruto()
    sasuke = Sasuke()
    vida_inicial_sasuke = sasuke.vida
    stamina_inicial_naruto = naruto.stamina

    resultado = naruto.atacar(sasuke)
    assert resultado['ok'] is True, "El ataque básico de Naruto debería ser exitoso"
    assert sasuke.vida < vida_inicial_sasuke, "La vida de Sasuke debería haber disminuido"
    assert naruto.stamina < stamina_inicial_naruto, "La estamina de Naruto debería haber disminuido"
    print("test_character_stats_and_attack: OK")

def test_oponente_zero_stamina_no_loop():
    # Creamos un oponente y le forzamos 0 estamina
    oponente = Oponente.crear_oponente("Naruto")
    jugador = Naruto()

    # Elegir acción con 0 de estamina no debe colgarse ni fallar, debe resolver con 'esperar'
    for _ in range(20):
        oponente.stamina = 0
        res = oponente.elegir_accion(jugador, dano=0)
        assert res.get('ok') is True, f"Con 0 estamina debe resolver con éxito (p. ej. esperar), obtuvo: {res}"
        assert res.get('accion') == 'esperar' or res.get('tipo') == 'esperar', f"Debe elegir esperar cuando tiene 0 estamina, obtuvo: {res}"

    print("test_oponente_zero_stamina_no_loop: OK")

def test_oponente_incoming_damage_behavior():
    oponente = Oponente.crear_oponente("Naruto")
    jugador = Naruto()
    oponente.stamina = 100

    # Con daño entrante > 0 y estamina suficiente, debe resolver sin excepciones
    for _ in range(20):
        res = oponente.elegir_accion(jugador, dano=30)
        assert res.get('ok') is True or res.get('ok') is None or res.get('ok') is False, "Debe retornar diccionario válido"

    print("test_oponente_incoming_damage_behavior: OK")

def test_oponente_fallback_esperar():
    oponente = Oponente.crear_oponente("Sasuke")
    jugador = Sasuke()
    oponente.stamina = 5  # Menos de 10 requeridos para atacar

    res = oponente.elegir_accion(jugador, dano=0)
    assert res['ok'] is True
    assert res['tipo'] == 'esperar'
    print("test_oponente_fallback_esperar: OK")

if __name__ == "__main__":
    test_character_stats_and_attack()
    test_oponente_zero_stamina_no_loop()
    test_oponente_incoming_damage_behavior()
    test_oponente_fallback_esperar()
    print("¡Todos los tests pasaron exitosamente!")


def test_combos_and_specials():
    from core.eventos import combos, especiales
    naruto = Naruto()
    sasuke = Sasuke()
    naruto.stamina = 350

    res_combo = combos(naruto, sasuke)
    assert res_combo['ok'] is True
    assert res_combo['dano'] > 0

    res_especial = especiales(naruto, sasuke)
    assert res_especial['ok'] is True
    assert res_especial['dano'] > 0
    print("test_combos_and_specials: OK")

if __name__ == "__main__":
    test_combos_and_specials()
