from .JuegoDeCartas import JuegoDeCartas
import random
from servidor.src.model.usuario import Usuario


class BlackJack(JuegoDeCartas):
    _plantarse: bool = False
    _cartas: dict[str,int] = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
            "J":10,"Q":10,"K":10,"A":11}
    _apuesta: int = 1

    def __init__(self, jugador: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int ,_plantarse: bool, _apuesta: int):
        super().__init__(jugador, capacidad, capacidadMinima, valor_entrada_mesa)
        self._apuesta = _apuesta
        self._plantarse = _plantarse

    def ganador(self, mano_jugador, mano_crupier):
        puntos_jugador = self.calcular_puntos(mano_jugador)
        puntos_crupier = self.calcular_puntos(mano_crupier)
        if puntos_jugador > 21:
            print("El jugador ha perdido, se ha pasado de 21 puntos.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")
        elif puntos_crupier > 21:
            print("El crupier ha perdido, se ha pasado de 21 puntos.")
        elif puntos_jugador > puntos_crupier:
            print("El jugador ha ganado.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")
        elif puntos_jugador < puntos_crupier or puntos_crupier == 21:
            print("El crupier ha ganado.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")

    def calcular_puntos(self, mano) -> int:
        # Calcula los puntos de la mano dada
        puntos = sum(BlackJack._cartas[carta] for carta in mano)
        # Si hay un As y los puntos son mayores a 21, resta 10 puntos
        if 'A' in mano and puntos > 21:
            puntos -= 10
        return puntos


    def separar(self, jugador: Usuario):
        print("falta implementar separar()")
        pass

    def retirarse(self, jugador: Usuario):
        print("falta implementar retirarse()")
        pass

    def repartir_cartas(self) -> str:
        # Reparte una carta al jugador o al crupier y devuelve el valor de la carta.
        return random.choice(list(BlackJack._cartas.keys()))

    def cartasIniciales(self):
        # Reparte dos cartas al jugador y devuelve el valor de las cartas.
        mano_inicial = [self.repartir_cartas(), self.repartir_cartas()]
        return mano_inicial

    def mostrar_CartasYPuntos(self, mano_jugador, mano_crupier):
        # Muestra las cartas de la mano.
        print(f"Mano del jugador: {mano_jugador}  || Puntos: {self.calcular_puntos(mano_jugador)}")
        print(f"Mano visible del crupier: {mano_crupier[0]}")
        # Muestra los puntos de el jugador y de crupier.

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass

    def crear_sala_activa_con_jugador(self, jugador: Usuario) -> str:
        """
        Crea una nueva sala de BlackJack activa con el jugador especificado.
        Returns:
            str: ID de la sala creada o None si hay error
        """
        try:
            import asyncio
            from servidor.src.model.salaDeJuego.SalaDeJuegoServicio import SalaDeJuegoServicio
            
            servicio = SalaDeJuegoServicio()
            jugadores_iniciales = [{
                'id': jugador.get_id(),
                'nombre': jugador.get_nombre(),
                'saldo': jugador.get_saldo()
            }]
            
            # Crear la sala usando el servicio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            sala_id = loop.run_until_complete(
                servicio.crear_sala_de_juego_activa("BlackJack", jugadores_iniciales)
            )
            loop.close()
            
            return sala_id
        except Exception as e:
            print(f"Error creando sala activa: {e}")
            return None
    

    def inicializar_juego(self):
        """Inicializa el juego de BlackJack para 4 jugadores más el crupier."""
        # Agregar el usuario real si se proporciona
        manos_jugadores = [self.cartasIniciales() for _ in range(4)]
        mano_crupier = self.cartasIniciales()
        plantados = [False] * 4
        jugadores=self.get_jugadores()
        for i, mano in enumerate(manos_jugadores):
            while not plantados[i]:
                print(f"{jugadores[3].get_nombre()} esta esperando a los demás jugadores...")
                print(f"\nTurno de {jugadores[i].get_nombre()}:")
                self.mostrar_CartasYPuntos(mano, mano_crupier)
                puntos = self.calcular_puntos(mano)
                if puntos >= 21:
                    plantados[i] = True
                    break
                plantarse = str(input(f"{jugadores[i].get_nombre()}, ¿Quieres plantarte? (S/N): ").lower())
                if plantarse == "n":
                    mano.append(self.repartir_cartas())
                elif plantarse == "s":
                    plantados[i] = True

        # Turno del crupier
        puntos_crupier = self.calcular_puntos(mano_crupier)
        while puntos_crupier < 17:
            mano_crupier.append(self.repartir_cartas())
            puntos_crupier = self.calcular_puntos(mano_crupier)
        print(f"\nMano final del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")

        # Determinar ganadores
        for i, mano in enumerate(manos_jugadores):
            print(f"\nResultado para {jugadores[i].get_nombre()}:")
            self.ganador(mano, mano_crupier)

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"cartas: {self._cartas}\n"
        )

if __name__ == "__main__":
    inicializar_juego = BlackJack("222222", 10, 5, 10, True, 1)
    inicializar_juego.inicializar_juego()
