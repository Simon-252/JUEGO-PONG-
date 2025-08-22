from config.constantes import ANCHO_VENTANA, ALTO_VENTANA
import pygame, sys

def mostrar_menu():
    """
    Muestra el menú principal del juego Pong.
    Permite al usuario seleccionar entre jugar solo, jugar con 2 jugadores,
    acceder a las opciones o salir del juego.

    Returns:
        str: La acción seleccionada por el usuario ("jugar solo", "2jugadores", "opciones", "salir").
    """
    pygame.init()
    SCREEN = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    FONT = pygame.font.SysFont("Consolas", int(ANCHO_VENTANA / 20))
    pygame.display.set_caption("Pong - Menú Principal")

    while True:
        SCREEN.fill("black")

        titulo = FONT.render("¡Bienvenido a Pong!", True, "white")
        SCREEN.blit(titulo, (
            ANCHO_VENTANA // 2 - titulo.get_width() // 2,
            ALTO_VENTANA // 4
        ))

        # --- Se define un ancho común para todos los botones ---
        ancho_boton = 600
        alto_boton = 50
        
        # --- Se definen los rectángulos de los botones con el nuevo ancho ---
        # La posición en 'x' es la misma para todos para que estén centrados.
        boton_jugar = pygame.Rect(ANCHO_VENTANA // 2 - ancho_boton // 2, ALTO_VENTANA // 2 - 60, ancho_boton, alto_boton)
        boton_2jugadores = pygame.Rect(ANCHO_VENTANA // 2 - ancho_boton // 2, ALTO_VENTANA // 2 + 10, ancho_boton, alto_boton)
        boton_opciones = pygame.Rect(ANCHO_VENTANA // 2 - ancho_boton // 2, ALTO_VENTANA // 2 + 80, ancho_boton, alto_boton)
        boton_salir = pygame.Rect(ANCHO_VENTANA // 2 - ancho_boton // 2, ALTO_VENTANA // 2 + 150, ancho_boton, alto_boton)

        pygame.draw.rect(SCREEN, "white", boton_jugar)
        pygame.draw.rect(SCREEN, "white", boton_2jugadores)
        pygame.draw.rect(SCREEN, "white", boton_opciones)
        pygame.draw.rect(SCREEN, "white", boton_salir)

        texto_jugar = FONT.render("Jugar Solo", True, "black")
        texto_2jugadores = FONT.render("Jugar 2 Jugadores", True, "black")
        texto_opciones = FONT.render("Opciones", True, "black")
        texto_salir = FONT.render("Salir", True, "black")

        # El texto se centra dentro de cada botón de forma correcta.
        SCREEN.blit(texto_jugar, (boton_jugar.centerx - texto_jugar.get_width() // 2, boton_jugar.centery - texto_jugar.get_height() // 2))
        SCREEN.blit(texto_2jugadores, (boton_2jugadores.centerx - texto_2jugadores.get_width() // 2, boton_2jugadores.centery - texto_2jugadores.get_height() // 2))
        SCREEN.blit(texto_opciones, (boton_opciones.centerx - texto_opciones.get_width() // 2, boton_opciones.centery - texto_opciones.get_height() // 2))
        SCREEN.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width() // 2, boton_salir.centery - texto_salir.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    return "jugar solo"
                elif boton_2jugadores.collidepoint(event.pos):
                    return "2jugadores"
                elif boton_opciones.collidepoint(event.pos):
                    return "opciones"
                elif boton_salir.collidepoint(event.pos):
                    return "salir"