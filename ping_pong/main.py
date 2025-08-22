import pygame, sys
from config.constantes import (
    ANCHO_VENTANA, ALTO_VENTANA, ANCHO_JUGADOR, ALTO_JUGADOR,
    VELOCIDAD_JUGADOR, ANCHO_BOLA, ALTO_BOLA, FPS
)
from models.player import Jugador
from models.ball import Bola
from ventanas.pantalla_final import pantalla_final
from config.funciones import verificar_ganador
from ventanas.menu import mostrar_menu
from config.config import abrir_opciones, obtener_configuracion
from models.sonido import SoundManager

def jugar_partida(modo):
    """
    Función principal que contiene el bucle del juego.
    
    Args:
        modo (str): "1" para un jugador (vs. IA) o "2" para dos jugadores.
    """

    VELOCIDAD_BOLA, VELOCIDAD_OPONENTE, PUNTAJE_LIMITE = obtener_configuracion()
    
    global SCREEN, FONT, CLOCK
    FONT = pygame.font.SysFont("Consolas", int(ANCHO_VENTANA/20))
    SCREEN = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Pong!")
    CLOCK = pygame.time.Clock()

    player = Jugador("jugador1", ANCHO_JUGADOR, ALTO_JUGADOR)
    opponent = None
    player_2 = None
    
    if modo == "1":
        opponent = Jugador("maquina", ANCHO_JUGADOR, ALTO_JUGADOR)
    elif modo == "2":
        player_2 = Jugador("jugador2", ANCHO_JUGADOR, ALTO_JUGADOR)

    ball = Bola(0, 0, ANCHO_BOLA, ALTO_BOLA)
    player_score = 0
    opponent_score = 0
    player_2_score = 0

    running = True
    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys_pressed = pygame.key.get_pressed()
        
        # Movimiento del Jugador 1
        if keys_pressed[pygame.K_UP]:
            player.mover("arriba", VELOCIDAD_JUGADOR)
        if keys_pressed[pygame.K_DOWN]:
            player.mover("abajo", VELOCIDAD_JUGADOR)
        
        # Movimiento del Jugador 2 (en modo 2 jugadores)
        if modo == "2":
            if keys_pressed[pygame.K_w]:
                player_2.mover("arriba", VELOCIDAD_JUGADOR)
            if keys_pressed[pygame.K_s]:
                player_2.mover("abajo", VELOCIDAD_JUGADOR)

        # --- Lógica de la Bola y Colisiones ---
        # Rebote en los bordes superior e inferior de la pantalla
        if ball.rect.top <= 0 or ball.rect.bottom >= ALTO_VENTANA:
            ball.y_speed *= -1
            sound_manager.play("rebotar")

        # Lógica de puntuación y reinicio de la bola
        if ball.rect.left <= 0:
            # Si la bola sale por la izquierda, anota el jugador del lado derecho
            if modo == "1":
                player_score += 1 
                sound_manager.play("score")
            elif modo == "2":
                player_score += 1
                sound_manager.play("score")
            ball.reiniciar()
        
        if ball.rect.right >= ANCHO_VENTANA:
            # Si la bola sale por la derecha, anota el jugador del lado izquierdo
            if modo == "1":
                opponent_score += 1
                sound_manager.play("score")
            elif modo == "2":
                player_2_score += 1
                sound_manager.play("score")
            ball.reiniciar()
        
        # Detección de colisión de la bola con las paletas y rebote
        # La colisión debe verificar la dirección de la bola para evitar que se quede pegada
        if ball.colisiona_con(player.rect) and ball.x_speed > 0:
            ball.x_speed *= -1
            sound_manager.play("rebotar")
        if modo == "1" and ball.colisiona_con(opponent.rect) and ball.x_speed < 0:
            ball.x_speed *= -1
            sound_manager.play("rebotar")
        elif modo == "2" and ball.colisiona_con(player_2.rect) and ball.x_speed < 0:
            ball.x_speed *= -1
            sound_manager.play("rebotar")

        # Movimiento del oponente/IA (solo en modo 1)
        if modo == "1":
            if opponent.rect.centery < ball.rect.centery:
                opponent.mover("abajo", VELOCIDAD_OPONENTE)
            elif opponent.rect.centery > ball.rect.centery:
                opponent.mover("arriba", VELOCIDAD_OPONENTE)

        ball.mover(VELOCIDAD_BOLA)
        
        # --- Lógica de Dibujado ---
        SCREEN.fill("Black")
        pygame.draw.rect(SCREEN, "white", player.rect)
        pygame.draw.circle(SCREEN, "white", ball.rect.center, ANCHO_BOLA // 2)

        if modo == "1":
            pygame.draw.rect(SCREEN, "white", opponent.rect)
            opponent_score_text = FONT.render(str(opponent_score), True, "white")
            SCREEN.blit(opponent_score_text, (ANCHO_VENTANA/2 - 50, 50))
        elif modo == "2":
            pygame.draw.rect(SCREEN, "yellow", player_2.rect)
            player_2_score_text = FONT.render(str(player_2_score), True, "white")
            SCREEN.blit(player_2_score_text, (ANCHO_VENTANA/2 - 50, 50))

        player_score_text = FONT.render(str(player_score), True, "white")
        SCREEN.blit(player_score_text, (ANCHO_VENTANA/2 + 50, 50))
        
        # Verificación de Ganador y Lógica de Pantalla Final
        ganador = verificar_ganador(player_score, opponent_score, player_2_score, PUNTAJE_LIMITE, modo)
        
        if ganador:
            sound_manager.play("victory")
            decision = pantalla_final(ganador)
            if decision == "menu":
                return
            elif decision == "reiniciar":
                jugar_partida(modo)
                return
            elif decision == "salir":
                running = False
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    global sound_manager
    sound_manager = SoundManager()
    while True:
        decision = mostrar_menu()
        if decision == "jugar solo":
            jugar_partida("1")
        elif decision == "2jugadores":
            jugar_partida("2")
        elif decision == "opciones":
            abrir_opciones()
        elif decision == "salir":
            pygame.quit()
            sys.exit()