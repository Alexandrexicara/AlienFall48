import pygame
import os

from config import *


class SoundManager:


    def __init__(self):

        pygame.mixer.init()

        self.sounds = {}



    def load(self, name, file):

        path = os.path.join(
            "assets",
            "sounds",
            file
        )

        self.sounds[name] = pygame.mixer.Sound(
            path
        )



    def play(self, name):

        if name in self.sounds:

            self.sounds[name].play()



    def set_volume(self, volume):

        for sound in self.sounds.values():

            sound.set_volume(
                volume
            )



class MusicManager:


    def __init__(self):

        self.volume = MUSIC_VOLUME



    def play(self, file):

        path = os.path.join(

            "assets",
            "music",
            file

        )


        pygame.mixer.music.load(
            path
        )


        pygame.mixer.music.set_volume(
            self.volume
        )


        pygame.mixer.music.play(
            -1
        )



    def stop(self):

        pygame.mixer.music.stop()



    def volume(self, value):

        pygame.mixer.music.set_volume(
            value
        )
