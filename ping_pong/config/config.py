import pygame # Importa la librería Pygame, necesaria para inicializar la ventana y usar fuentes.
from config.constantes import ANCHO_VENTANA, ALTO_VENTANA # Importa las dimensiones de la ventana desde el módulo de constantes.

# --- Variables globales para la configuración del juego ---
# Estas variables almacenan la configuración actual y se pueden modificar desde el menú de opciones.
# Son globales para que su estado persista y pueda ser accedido por otras partes del juego.
VELOCIDAD_OPONENTE = 6 # Velocidad predeterminada de la paleta controlada por la IA.
VELOCIDAD_BOLA = 8     # Velocidad predeterminada de la bola.
PUNTAJE_LIMITE = 2     # Puntaje que un jugador debe alcanzar para ganar la partida.

def abrir_opciones():
    """
    Abre la pantalla de configuración del juego, permitiendo al usuario
    ajustar la velocidad de la bola, la dificultad del oponente y el puntaje límite.
    Las variables globales VELOCIDAD_BOLA, VELOCIDAD_OPONENTE y PUNTAJE_LIMITE
    se actualizan directamente con la selección del usuario.
    """
    # Declara el uso de variables globales para poder modificarlas dentro de esta función.
    global VELOCIDAD_BOLA, VELOCIDAD_OPONENTE, PUNTAJE_LIMITE

    pygame.init() # Inicializa Pygame (si no se ha inicializado ya).
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA)) # Crea la superficie de la ventana para las opciones.
    fuente = pygame.font.SysFont(None, 36) # Define la fuente para el texto de las opciones.
    reloj = pygame.time.Clock() # Crea un reloj para controlar el framerate de la pantalla de opciones.

    # --- Estructura de datos para las opciones del menú ---
    # Cada diccionario representa una opción y contiene:
    # - "titulo": El texto descriptivo que se muestra al usuario.
    # - "opciones": Una lista de las etiquetas de las opciones visibles al usuario (ej. "Lenta", "Normal").
    # - "valores": Una lista de los valores numéricos correspondientes a cada opción (ej. 6, 8).
    # - "idx_actual": El índice de la opción seleccionada actualmente en las listas "opciones" y "valores".
    opciones_menu = [
        {"titulo": "Velocidad de la bola: ", "opciones": ["Lenta", "Normal", "Rápida"], "valores": [6, 8, 10], "idx_actual": 0},
        {"titulo": "Dificultad del oponente: ", "opciones": ["Fácil", "Normal", "Difícil"], "valores": [4, 6, 8], "idx_actual": 0},
        # Para el puntaje límite, las "opciones" mostradas son los mismos que los "valores" internos.
        {"titulo": "Puntaje límite: ", "opciones": [2, 5, 10], "valores": [2, 5, 10], "idx_actual": 0},
    ]

    # --- Inicialización de los índices actuales de las opciones ---
    # Se busca la posición de la configuración global actual en la lista de valores de cada opción.
    opciones_menu[0]["idx_actual"] = opciones_menu[0]["valores"].index(VELOCIDAD_BOLA)
    opciones_menu[1]["idx_actual"] = opciones_menu[1]["valores"].index(VELOCIDAD_OPONENTE)
    opciones_menu[2]["idx_actual"] = opciones_menu[2]["valores"].index(PUNTAJE_LIMITE)

    seleccionado = None # Índice de la opción actualmente seleccionada por teclado (para navegación).
    modo_input = "teclado" # Controla si la interacción es por teclado o ratón (para resaltar).
    animacion_flecha = [False] * len(opciones_menu) # Banderas para activar una breve animación al cambiar opciones con teclado.

    # ---- Funciones auxiliares para el dibujado ----
    def dibujar_flecha(pos, izquierda=False, activa=False):
        """
        Dibuja una flecha (< o >) en la pantalla con un tamaño y color que pueden variar
        si está activa (seleccionada o en hover).

        Args:
            pos (tuple): Las coordenadas (x, y) donde se dibujará la esquina superior izquierda de la flecha.
            izquierda (bool): True para dibujar la flecha "<", False para ">".
            activa (bool): True si la flecha debe dibujarse con el estado "activo" (más grande, color amarillo).

        Returns:
            pygame.Rect: El rectángulo que ocupa la flecha dibujada, útil para detección de clics.
        """
        tamaño = 28 if activa else 20 # Tamaño de la fuente de la flecha.
        color = (255, 255, 0) if activa else (200, 200, 200) # Color de la flecha (amarillo si activa).
        texto = "<" if izquierda else ">" # Carácter de la flecha.
        font = pygame.font.SysFont(None, tamaño) # Crea una fuente con el tamaño especificado.
        render = font.render(texto, True, color) # Renderiza el texto de la flecha.
        pantalla.blit(render, pos) # Dibuja la flecha en la pantalla.
        return render.get_rect(topleft=pos) # Devuelve el rectángulo que ocupa la flecha.

    def centro_horizontal(surface_width):
        """
        Calcula la coordenada X necesaria para centrar una superficie horizontalmente en la pantalla.

        Args:
            surface_width (int): El ancho de la superficie (texto o grupo de elementos) a centrar.

        Returns:
            int: La coordenada X donde debe empezar a dibujarse la superficie para que quede centrada.
        """
        return ANCHO_VENTANA // 2 - surface_width // 2

    # ---- Bucle principal de la pantalla de opciones ----
    activo = True # Bandera para controlar la ejecución del bucle de opciones.
    while activo:
        pantalla.fill((30, 30, 30)) # Rellena la pantalla con un color gris oscuro para el fondo.
        mouse_pos = pygame.mouse.get_pos() # Obtiene la posición actual del cursor del ratón.
        mouse_clicked = False # Bandera para saber si se ha hecho clic con el ratón en este frame.
        hover_opcion = None # Índice de la opción sobre la que el ratón está actualmente.

        # --- Manejo de eventos (entrada del usuario) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                activo = False # Si el usuario cierra la ventana, se sale del bucle de opciones.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True # Marca que se ha hecho clic con el ratón.
            elif event.type == pygame.MOUSEMOTION:
                modo_input = "mouse" # Si el ratón se mueve, el modo de entrada es "mouse".
            elif event.type == pygame.KEYDOWN:
                modo_input = "teclado" # Si se presiona una tecla, el modo de entrada es "teclado".
                if seleccionado is None:
                    seleccionado = 0 # Si ninguna opción está seleccionada, selecciona la primera.
                if event.key == pygame.K_DOWN:
                    # Mueve la selección hacia abajo, ciclando al principio si llega al final.
                    seleccionado = (seleccionado + 1) % len(opciones_menu)
                elif event.key == pygame.K_UP:
                    # Mueve la selección hacia arriba, ciclando al final si llega al principio.
                    seleccionado = (seleccionado - 1) % len(opciones_menu)
                elif event.key == pygame.K_LEFT and seleccionado is not None:
                    # Si se presiona izquierda y hay una opción seleccionada:
                    # Disminuye el índice de la opción actual (ciclando si llega al principio).
                    current_idx = opciones_menu[seleccionado]["idx_actual"]
                    opciones_len = len(opciones_menu[seleccionado]["opciones"])
                    opciones_menu[seleccionado]["idx_actual"] = (current_idx - 1) % opciones_len
                    animacion_flecha[seleccionado] = True # Activa la animación de la flecha para esta opción.
                elif event.key == pygame.K_RIGHT and seleccionado is not None:
                    # Si se presiona derecha y hay una opción seleccionada:
                    # Aumenta el índice de la opción actual (ciclando si llega al final).
                    current_idx = opciones_menu[seleccionado]["idx_actual"]
                    opciones_len = len(opciones_menu[seleccionado]["opciones"])
                    opciones_menu[seleccionado]["idx_actual"] = (current_idx + 1) % opciones_len
                    animacion_flecha[seleccionado] = True # Activa la animación de la flecha para esta opción.
                elif event.key == pygame.K_RETURN:
                    # Si se presiona ENTER, aplica la configuración actual y sale del bucle de opciones.
                    VELOCIDAD_BOLA = opciones_menu[0]["valores"][opciones_menu[0]["idx_actual"]]
                    VELOCIDAD_OPONENTE = opciones_menu[1]["valores"][opciones_menu[1]["idx_actual"]]
                    PUNTAJE_LIMITE = opciones_menu[2]["valores"][opciones_menu[2]["idx_actual"]]
                    activo = False

        # --- Bucle de renderizado y lógica de interacción visual de las opciones ---
        for i, opcion_data in enumerate(opciones_menu):
            titulo = opcion_data["titulo"] # Título de la opción (ej. "Velocidad de la bola: ")
            # Valor actual de la opción para mostrar (ej. "Normal", "5", "Difícil").
            valor_display = str(opcion_data["opciones"][opcion_data["idx_actual"]])
            y = ALTO_VENTANA // 2 - 60 + i * 60 # Calcula la posición Y para cada opción.

            # Renderiza los componentes de la línea de la opción: flechas, valor y título.
            # El color varía si la opción está seleccionada o en hover.
            render_flecha_izq = fuente.render("<", True, (255, 255, 0) if seleccionado == i or hover_opcion == i else (200, 200, 200))
            render_valor = fuente.render(valor_display, True, (255, 255, 0) if seleccionado == i or hover_opcion == i else (255, 255, 255))
            render_flecha_der = fuente.render(">", True, (255, 255, 0) if seleccionado == i or hover_opcion == i else (200, 200, 200))
            render_titulo = fuente.render(titulo, True, (255, 255, 255))

            # Calcular anchos y posiciones para centrar la línea completa (título + < valor >).
            espacio_entre_flecha_valor = 5 # Espacio en píxeles entre la flecha y el valor.
            # Ancho total de la parte interactiva (< valor >).
            ancho_parte_valor_con_flechas = render_flecha_izq.get_width() + espacio_entre_flecha_valor + \
                                            render_valor.get_width() + espacio_entre_flecha_valor + \
                                            render_flecha_der.get_width()
            # Ancho total de la línea completa (título y la parte interactiva).
            ancho_total_linea = render_titulo.get_width() + ancho_parte_valor_con_flechas
            # Coordenada X para centrar toda la línea.
            x_linea_completa = centro_horizontal(ancho_total_linea)

            # Define las coordenadas X individuales para cada componente de la línea.
            x_titulo = x_linea_completa
            x_flecha_izq = x_titulo + render_titulo.get_width()
            x_valor = x_flecha_izq + render_flecha_izq.get_width() + espacio_entre_flecha_valor
            x_flecha_der = x_valor + render_valor.get_width() + espacio_entre_flecha_valor

            # Dibuja los elementos en la pantalla.
            pantalla.blit(render_titulo, (x_titulo, y))
            
            # Dibuja las flechas usando la función auxiliar para manejar su estado activo/inactivo.
            rect_izq = dibujar_flecha((x_flecha_izq, y), izquierda=True,
                activa=(animacion_flecha[i] and seleccionado == i) or \
                       (pygame.Rect(x_flecha_izq, y, render_flecha_izq.get_width(), render_flecha_izq.get_height()).collidepoint(mouse_pos) and modo_input == "mouse")
            )
            pantalla.blit(render_valor, (x_valor, y)) # Dibuja el valor actual de la opción.
            rect_der = dibujar_flecha((x_flecha_der, y), izquierda=False,
                activa=(animacion_flecha[i] and seleccionado == i) or \
                       (pygame.Rect(x_flecha_der, y, render_flecha_der.get_width(), render_flecha_der.get_height()).collidepoint(mouse_pos) and modo_input == "mouse")
            )

            # Restablece la bandera de animación de la flecha una vez que se ha dibujado.
            if animacion_flecha[i]:
                animacion_flecha[i] = False

            # --- Detección de hover y clic del ratón para las opciones ---
            # Crea un rectángulo que abarca toda la sección interactiva de la opción (flechas y valor).
            rect_opcion_interactiva = pygame.Rect(x_flecha_izq, y, ancho_parte_valor_con_flechas, render_valor.get_height())
            
            # Si el ratón está sobre la opción y el modo de entrada es ratón.
            if rect_opcion_interactiva.collidepoint(mouse_pos) and modo_input == "mouse":
                hover_opcion = i # Marca que esta opción está en hover.
                if mouse_clicked:
                    seleccionado = i # Si se hace clic en el área interactiva, selecciona esta opción.
            # Si el ratón ya no está sobre la opción y el modo de entrada es ratón.
            elif modo_input == "mouse" and hover_opcion == i and not rect_opcion_interactiva.collidepoint(mouse_pos):
                hover_opcion = None # Desactiva el estado de hover.

            # Si se ha hecho clic con el ratón, verifica si fue en las flechas individuales.
            if mouse_clicked:
                if rect_izq.collidepoint(mouse_pos):
                    # Si se hizo clic en la flecha izquierda, decrementa el índice de la opción.
                    current_idx = opciones_menu[i]["idx_actual"]
                    opciones_len = len(opciones_menu[i]["opciones"])
                    opciones_menu[i]["idx_actual"] = (current_idx - 1) % opciones_len
                elif rect_der.collidepoint(mouse_pos):
                    # Si se hizo clic en la flecha derecha, incrementa el índice de la opción.
                    current_idx = opciones_menu[i]["idx_actual"]
                    opciones_len = len(opciones_menu[i]["opciones"])
                    opciones_menu[i]["idx_actual"] = (current_idx + 1) % opciones_len

        pygame.display.flip() # Actualiza toda la pantalla para mostrar los cambios de este frame.
        reloj.tick(30) # Limita el framerate de la pantalla de opciones a 30 FPS.

def obtener_configuracion():
    """
    Devuelve la configuración actual del juego (velocidad de bola, oponente y puntaje límite).

    Returns:
        tuple: Una tupla que contiene (VELOCIDAD_BOLA, VELOCIDAD_OPONENTE, PUNTAJE_LIMITE).
    """
    return VELOCIDAD_BOLA, VELOCIDAD_OPONENTE, PUNTAJE_LIMITE