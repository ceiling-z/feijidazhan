import os
import pygame


class Sound:
    def __init__(self):
        # 背景音乐
        sound_path = os.path.join(os.path.dirname(__file__), '../res/sound')
        pygame.mixer.music.load(os.path.join(sound_path, 'game_music.wav'))
        self._music = pygame.mixer.music

        # 音效
        self._sound_effect = {}
        sound_effect_names = ['bullet', 'enemy1_down', 'enemy2_down', 'enemy3_down', 'game_over']

        for name in sound_effect_names:
            self._sound_effect[name] = pygame.mixer.Sound(f'{os.path.join(sound_path, name)}.wav')
        
    def play(self, name):
        """播放"""
        if name == 'bg':
            self._music.play(-1)
        else:
            self._sound_effect[name].play()

    def pause(self, name):
        """暂停"""
        if name == 'bg':
            self._music.pause()
    
    def unpause(self, name):
        """继续"""
        if name == 'bg':
            self._music.unpause()
    
    def fadeout(self, name):
        """渐退"""
        if name == 'bg':
            self._music.fadeout(1000)
