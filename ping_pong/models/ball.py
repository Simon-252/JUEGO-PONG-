import pygame
# Importa las constantes ANCHO_VENTANA y ALTO_VENTANA desde el módulo 'constantes' en 'config'.
# Estas constantes son necesarias para centrar la bola y para la lógica de colisión con los bordes de la pantalla.
from config.constantes import ANCHO_VENTANA, ALTO_VENTANA
import random # Se importa el módulo 'random' para generar direcciones aleatorias al reiniciar la bola.

class Bola():
    """
    Representa la bola del juego de Pong.
    Maneja su posición, movimiento, reinicio y detección de colisiones.
    """
    def __init__(self, x, y, ancho, alto):
        """
        Inicializa una nueva instancia de Bola.

        Args:
            x (int): La coordenada X inicial para el rectángulo de la bola (aunque se sobrescribe con el centro).
            y (int): La coordenada Y inicial para el rectángulo de la bola (aunque se sobrescribe con el centro).
            ancho (int): El ancho de la bola.
            alto (int): El alto de la bola.
        """
        # Crea el objeto Rect de Pygame que representa la bola.
        # Este Rect se usa para dibujar la bola y detectar colisiones.
        self.rect = pygame.Rect(x, y, ancho, alto)
        
        # Centra la bola en el medio de la ventana al inicio del juego o al reiniciar.
        self.rect.center = (ANCHO_VENTANA / 2, ALTO_VENTANA / 2)
        
        # Define la dirección inicial de la bola en el eje X (1 para derecha, -1 para izquierda).
        self.x_speed = 1
        # Define la dirección inicial de la bola en el eje Y (1 para abajo, -1 para arriba).
        self.y_speed = 1

    def mover(self, velocidad):
        """
        Actualiza la posición de la bola en la pantalla.

        Args:
            velocidad (int): La velocidad base de la bola, se multiplica por x_speed e y_speed.
        """
        velocidad_bola = velocidad # Asigna la velocidad recibida a una variable local para claridad.
        
        # Actualiza la posición X de la bola multiplicando su dirección por la velocidad.
        self.rect.x += self.x_speed * velocidad_bola
        # Actualiza la posición Y de la bola multiplicando su dirección por la velocidad.
        self.rect.y += self.y_speed * velocidad_bola

    def reiniciar(self):
        """
        Reinicia la posición de la bola al centro de la pantalla
        y le asigna una dirección X e Y aleatoria.
        """
        # Vuelve a centrar la bola en el medio de la ventana.
        self.rect.center = (ANCHO_VENTANA / 2, ALTO_VENTANA / 2)
        
        # Asigna una nueva dirección horizontal aleatoria (izquierda o derecha).
        self.x_speed = random.choice([1, -1])
        # Asigna una nueva dirección vertical aleatoria (arriba o abajo).
        self.y_speed = random.choice([1, -1])
        
    def colisiona_con(self, otro_rect):
        """
        Verifica si la bola colisiona con otro objeto rectangular.

        Args:
            otro_rect (pygame.Rect): El rectángulo del objeto con el que se desea verificar la colisión.

        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        # Utiliza el método incorporado de Pygame 'colliderect' para detectar la colisión entre dos rectángulos.
        return self.rect.colliderect(otro_rect)