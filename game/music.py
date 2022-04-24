import pygame


class Music:
    """
    Class for the level music - so we can include ability to pause/unpause
    """
    def __init__(self):
        pygame.mixer.music.load('../sounds/level.mp3')
        pygame.mixer.music.set_volume(0.5)

    def play(self):
        pygame.mixer.music.play(-1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
