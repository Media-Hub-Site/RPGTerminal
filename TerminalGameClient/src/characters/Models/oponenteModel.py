from .BaseModel import Personaje
from utils.common import random
from utils.data import characters_list

class Oponente(Personaje):
    def __init__(self, personaje):
        # Llamamos directamente al constructor de la clase base Personaje
        # en lugar de usar super() para evitar llamar al __init__ de la
        # clase de personaje (p. ej. Kyo) cuando usamos herencia dinámica.
        Personaje.__init__(
            self,
            nombre=personaje.nombre,
            vida=personaje.vida,
            poder=personaje.poder,
            stamina=personaje.stamina,
            tipo=personaje.tipo
        )

    @staticmethod
    def crear_oponente(nombre_jugador):
        """Crea un oponente aleatorio distinto del jugador."""
        # Personaje base distinto al jugador
        candidatos = [c.__class__() for c in characters_list if c.nombre != nombre_jugador]
        personaje = random.choice(candidatos)

        # Crea una clase combinada entre Oponente y la clase del personaje
        clase_dinamica = type("OponenteDinamico", (Oponente, personaje.__class__), {})
        return clase_dinamica(personaje)

    def elegir_accion(self, rival, dano):
        POWER_MAP = {
            'Naruto': {
                'combo': lambda r: self.Rasengan(r),
                'ulti': lambda r: self.RasenShuriken(r)
            },
            'Sasuke': {
                'combo': lambda r: self.Chidori(r),
                'ulti': lambda r: self.Raikiri(r)
            },
            'Ichigo': {
                'combo': lambda r: self.getsuga(r),
                'ulti': lambda r: self.bankai(r)
            },
            'Aizen': {
                'combo': lambda r: self.kido(r),
                'ulti': lambda r: self.kyokasuigetsu(r)
            },
            'Kyo': {
                'combo': lambda r: self.combo(r),
                'ulti': lambda r: self.ulti(r)
            },
            'Iori': {
                'combo': lambda r: self.combo(r),
                'ulti': lambda r: self.ulti(r)
            },
            'Kazuha': {
                'combo': lambda r: self.K_elemental(r),
                'ulti': lambda r: self.K_ulti(r)
            },
            'Alhacen': {
                'combo': lambda r: self.A_elemental(r),
                'ulti': lambda r: self.A_ulti(r)
            },
            'Goku': {
                'combo': lambda r: self.Kamehameha(r),
                'ulti': lambda r: self.Ssj(r)
            },
            'Vegeta': {
                'combo': lambda r: self.GarlickGun(r),
                'ulti': lambda r: self.Ssj(r)
            },
        }

        char_powers = POWER_MAP.get(self.nombre, {})
        combo_fn = char_powers.get('combo')
        ulti_fn = char_powers.get('ulti')

        # Determinar acciones válidas según la estamina y la situación
        acciones_disponibles = ['esperar']

        if dano > 0:
            acciones_disponibles.append('esquivar')

        if self.stamina >= 10:
            acciones_disponibles.append('atacar')

        if self.stamina >= 60 and combo_fn:
            acciones_disponibles.append('combo')

        if self.stamina >= 150 and ulti_fn:
            acciones_disponibles.append('ulti')

        accion = random.choice(acciones_disponibles)

        if accion == 'atacar':
            resultado = self.atacar(rival)
        elif accion == 'esperar':
            resultado = self.esperar()
        elif accion == 'esquivar':
            resultado = self.esquivar(rival, dano)
        elif accion == 'combo' and combo_fn:
            resultado = combo_fn(rival)
        elif accion == 'ulti' and ulti_fn:
            resultado = ulti_fn(rival)
        else:
            resultado = self.esperar()

        # Fallback garantizado: si la acción no fue exitosa (p. ej. ok es False), el oponente descansa y recupera recursos
        if not resultado.get('ok', True) and resultado.get('ok') is not None:
            resultado = self.esperar()

        return resultado
