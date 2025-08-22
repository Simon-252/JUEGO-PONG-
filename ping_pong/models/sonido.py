import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {
            "rebotar": pygame.mixer.Sound("assets/sounds/sonido_1.mp3"),
            "score": pygame.mixer.Sound("assets/sounds/blip.mp3"),
            "victory": pygame.mixer.Sound("assets/sounds/game_over.mp3")
        }

        pygame.mixer.music.load("assets/sounds/musica-bit.mp3")
        pygame.mixer.music.set_volume(8.0)
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()