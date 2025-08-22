import pygame
# Importa las constantes ANCHO_VENTANA y ALTO_VENTANA desde el módulo 'constantes' en 'config'.
# Estas constantes son esenciales para posicionar y limitar el movimiento del jugador.
from config.constantes import ANCHO_VENTANA, ALTO_VENTANA
# Importa la función 'mover_verticalmente' desde el módulo 'funciones' en 'config'.
# Esta función es una utilidad para manejar el movimiento vertical de un rectángulo (como el del jugador).
from config.funciones import mover_verticalmente

class Jugador:
    """
    Representa un jugador (o la paleta del jugador) en el juego de Pong.
    Puede ser controlado por un usuario o por la IA.
    """
    def __init__(self, rol, ancho, alto):
        """
        Inicializa una nueva instancia de Jugador.

        Args:
            rol (str): El rol del jugador ("jugador1", "jugador2", "maquina").
                       Define su posición inicial en la pantalla.
            ancho (int): El ancho de la paleta del jugador.
            alto (int): El alto de la paleta del jugador.
        """
        # Define la posición inicial en X de la paleta según su rol.
        # "jugador1" se posiciona en el lado derecho de la pantalla.
        # "jugador2" o "maquina" se posicionan en el lado izquierdo.
        if rol == "jugador1":
            x = ANCHO_VENTANA - 20 - ancho # 20 píxeles desde el borde derecho
        else:  # "jugador2" o "maquina"
            x = 20 # 20 píxeles desde el borde izquierdo
        
        # Calcula la posición inicial en Y para centrar verticalmente la paleta.
        y = (ALTO_VENTANA - alto) // 2
        
        # Crea el objeto Rect de Pygame que representa la paleta del jugador.
        # Este Rect se usa para dibujar el jugador y detectar colisiones.
        self.rect = pygame.Rect(x, y, ancho, alto)
        
        # Almacena el rol del jugador. Esto puede ser útil para la lógica del juego
        # (ej. qué teclas lo controlan o si es una IA).
        self.rol = rol

    def mover(self, direccion, velocidad):
        """
        Mueve la paleta del jugador verticalmente.

        Este método utiliza la función de utilidad 'mover_verticalmente'
        para manejar la lógica real del movimiento y asegurar que el jugador
        no se salga de los límites de la pantalla.

        Args:
            direccion (str): La dirección en la que mover ("arriba" o "abajo").
            velocidad (int): La cantidad de píxeles que la paleta se moverá en esa dirección.
        """
        # Llama a la función auxiliar para mover el rectángulo del jugador.
        # Se le pasa el propio rect del jugador, la dirección, la velocidad y el límite de la pantalla.
        mover_verticalmente(self.rect, direccion, velocidad, ALTO_VENTANA)