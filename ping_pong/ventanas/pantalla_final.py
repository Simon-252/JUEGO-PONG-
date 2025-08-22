import pygame, sys
from config.constantes import ANCHO_VENTANA, ALTO_VENTANA

def pantalla_final(ganador):
    """
    Muestra la pantalla final del juego, anunciando al ganador y ofreciendo
    opciones para reiniciar, ir al menú principal o salir.

    Args:
        ganador (str): El nombre del jugador o de la IA que ha ganado la partida.

    Returns:
        str: Una cadena que indica la acción seleccionada por el usuario ("reiniciar", "menu", "salir").
    """
    # --- Mover la inicialización de Pygame y las variables SCREEN/FONT aquí ---
    pygame.init()
    SCREEN = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    FONT = pygame.font.SysFont("Consolas", int(ANCHO_VENTANA/20))
    pygame.display.set_caption("Pong - Pantalla Final")

    while True:
        SCREEN.fill("black")

        # Renderiza y posiciona el mensaje del ganador
        texto_ganador = FONT.render(f"¡Ganó {ganador}!", True, "white")
        SCREEN.blit(texto_ganador, (ANCHO_VENTANA // 2 - texto_ganador.get_width() // 2, ALTO_VENTANA // 4))

        # --- Define las dimensiones de los botones para un centrado correcto ---
        ancho_boton = 400
        alto_boton = 50
        
        # Define las posiciones X e Y de los botones.
        # La posición X se calcula para centrar el botón.
        x_posicion = ANCHO_VENTANA // 2 - ancho_boton // 2

        boton_reiniciar = pygame.Rect(x_posicion, ALTO_VENTANA // 2 - 60, ancho_boton, alto_boton)
        boton_menu = pygame.Rect(x_posicion, ALTO_VENTANA // 2 + 10, ancho_boton, alto_boton)
        boton_salir = pygame.Rect(x_posicion, ALTO_VENTANA // 2 + 80, ancho_boton, alto_boton)

        pygame.draw.rect(SCREEN, "white", boton_reiniciar)
        pygame.draw.rect(SCREEN, "white", boton_menu)
        pygame.draw.rect(SCREEN, "white", boton_salir)

        texto_reiniciar = FONT.render("Reiniciar", True, "black")
        texto_menu = FONT.render("Main Menu", True, "black")
        texto_salir = FONT.render("Salir", True, "black")

        SCREEN.blit(texto_reiniciar, (boton_reiniciar.centerx - texto_reiniciar.get_width() // 2, boton_reiniciar.centery - texto_reiniciar.get_height() // 2))
        SCREEN.blit(texto_menu, (boton_menu.centerx - texto_menu.get_width() // 2, boton_menu.centery - texto_menu.get_height() // 2))
        SCREEN.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width() // 2, boton_salir.centery - texto_salir.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    return "reiniciar"
                if boton_menu.collidepoint(event.pos):
                    return "menu"
                if boton_salir.collidepoint(event.pos):
                    return "salir"