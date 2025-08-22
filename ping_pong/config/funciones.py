# Función para verificar el ganador del juego
def verificar_ganador(player_score, opponent_score, player_2_score, puntaje_limite, modo):
    """
    Verifica si algún jugador ha alcanzado el puntaje límite y, por lo tanto, ha ganado el juego.

    Args:
        player_score (int): La puntuación actual del Jugador 1.
        opponent_score (int): La puntuación actual del Oponente (IA).
        player_2_score (int): La puntuación actual del Jugador 2 (si aplica).
        puntaje_limite (int): El puntaje que un jugador debe alcanzar para ganar.
        modo (str): El modo de juego actual ("1" para 1 vs IA, "2" para 2 jugadores).

    Returns:
        str or None: El nombre del jugador que ganó ("Jugador", "Máquina", "Jugador 2"),
                     o None si nadie ha ganado aún.
    """
    # Verificación del Jugador 1 (siempre presente)
    if player_score >= puntaje_limite:
        return "Jugador"
    
    # Verificación específica para el modo 1 jugador
    if modo == "1" and opponent_score >= puntaje_limite:
        return "Máquina"
    
    # Verificación específica para el modo 2 jugadores
    if modo == "2" and player_2_score >= puntaje_limite:
        return "Jugador 2"
    
    # Si ninguno ha alcanzado el puntaje, devuelve None
    return None

# Funciones de movimiento vertical (no se modifican)
def mover_verticalmente(rect, direccion, velocidad, alto_ventana):
    if (direccion == "arriba" or direccion == "w") and rect.top > 0:
        rect.top -= velocidad
    elif (direccion == "abajo" or direccion == "s") and rect.bottom < alto_ventana:
        rect.bottom += velocidad