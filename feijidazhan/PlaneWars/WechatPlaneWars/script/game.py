import sys
import pygame
from pygame.locals import *

from hero import Hero
from scene import Scene
from enemy import EnemySpawnMachine
from sound import Sound


class Game:
    """游戏主逻辑"""
    def __init__(self):
        self._game_state = 'RUN'                                # 当前游戏状态，分为RUN, GAMEOVER
        self._is_paused = False                                 # 是否暂停
        self._score = 0                                         # 玩家分数
        self._clock = pygame.time.Clock()                       # 游戏帧率

        self.scene = Scene(self)                                # 游戏场景
        self.hero = Hero(self)                                  # 玩家飞机
        self.enemy_spawn_machine = EnemySpawnMachine(self)      # 敌机制造
        self.sounds = Sound()                                   # 音乐音效

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def is_paused(self):
        return self._is_paused

    @is_paused.setter
    def is_paused(self, value):
        self._is_paused = value

    def start(self):
        """游戏开始"""
        # 播放背景音乐
        self.sounds.play('bg')

        while True:
            # 处理事件
            pos = self._handle_events()

            if self._game_state != 'GAMEOVER':
                self.scene.update()                     # 更新场景
                self.hero.update(pos)                   # 更新玩家飞机
                self.enemy_spawn_machine.update()       # 更新敌军飞机
                self._handle_collision()                # 处理碰撞
            else:
                self.scene.draw_logo()                  # 绘制飞机大战logo
                self.scene.draw_text_buttons()          # 绘制重新开始和退出游戏按钮

            self._clock.tick(60)
            pygame.display.flip()

    def _handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self._handle_mousedown_event(event)
            elif event.type == MOUSEMOTION:
                return self._handle_mousemotion_event(event)

        return None
    
    def _handle_mousedown_event(self, event):
        """处理鼠标按下事件"""
        if self._game_state == 'RUN':
            # 暂停
            if not self._is_paused and self.scene.pause_rect.collidepoint(event.pos):
                self._is_paused = True
                self.sounds.pause('bg')
            # 继续
            elif self.scene.resume_rect.collidepoint(event.pos):
                self._is_paused = False
                self.sounds.unpause('bg')
        else:
            # 重新开始
            if self.scene.buttons['Restart'].is_pressed(event.pos):
                self.restart()
            # 退出游戏
            elif self.scene.buttons['Exit'].is_pressed(event.pos):
                pygame.quit()
                sys.exit()

    def _handle_mousemotion_event(self, event):
        """处理鼠标移动事件"""
        # 玩家飞机随用户鼠标而移动，不过玩家得按下左键先，而且要按在飞机上
        if self._game_state == 'RUN' and event.buttons[0]:
            return event.pos

    def _handle_collision(self):
        """处理碰撞逻辑"""
        # 检测子弹和敌机碰撞
        collide_dict = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_spawn_machine.enemies,
                                                  True, False, pygame.sprite.collide_mask)
        collide_enemies_list = []

        if collide_dict:
            for collide_enemies in collide_dict.values():
                collide_enemies_list.extend(collide_enemies)
        
        if collide_enemies_list:
            for collide_enemy in collide_enemies_list:
                if collide_enemy.current_hp == 1:
                    self.sounds.play('enemy'+str(collide_enemy.type)+'_down')
                collide_enemy.hit_by_bullet()

        # 检测我方飞机和敌机碰撞
        enemy = pygame.sprite.spritecollideany(self.hero, self.enemy_spawn_machine.enemies, 
                                               pygame.sprite.collide_mask)
        # 如果发生碰撞
        if enemy:
            self.hero.is_collide = True
            self.hero.bullets.empty()
            self.enemy_spawn_machine.enemies.empty()
            self.sounds.fadeout('bg')
            self.sounds.play('game_over')

    def restart(self):
        """重新开始"""
        self._game_state = 'RUN'
        self._score = 0
        self.hero.reset()
        self.sounds.play('bg')
