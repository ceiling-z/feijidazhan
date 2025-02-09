import os
import random
import pygame
from pygame.sprite import Group, Sprite


class Enemy(Sprite):
    def __init__(self, game, left_top):
        super().__init__()
        self.game = game
        self.left_top = left_top
        self.score = 0
        self.current_hp = 0
        self.is_hit_by_bullet = False
        self.images_list = []
        self.image_index = 0
        self.image = None
        self.mask = None
        self.rect = None
    
    def load_image(self, image_name_list, size):
        image_path = os.path.join(os.path.dirname(__file__), '../res/image')
        self.images_list = [pygame.image.load(os.path.join(image_path, name)).convert_alpha() for name in image_name_list]
        self.image = self.images_list[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(self.left_top, size)

    def hit_by_bullet(self):
        if self.current_hp > 0:
            self.current_hp -= 1
            self.is_hit_by_bullet = True

    def draw(self):
        self.game.scene.screen.blit(self.image, self.rect)


    def update(self):
        if not self.game.is_paused:
            self.rect.top += 2

        if self.rect.top >= self.game.scene.screen.get_rect().bottom:
            self.kill()
        else:
            self.draw()

class SmallEnemy(Enemy):
    size = (57, 43)
    type = 1

    def __init__(self, game, left_top):
        super().__init__(game, left_top)
        self.current_hp = 1
        self.score = 2
        
        self.load_image(['enemy1.png', 'enemy1_down1.png', 'enemy1_down2.png', 'enemy1_down3.png', 
                         'enemy1_down4.png'], self.size)

    def update(self):
        """更新"""
        super().update()
        if self.current_hp > 0:
            self.image_index = 0
        else:
            if self.image_index < len(self.images_list) - 1:
                self.image_index += 1
            else:
                self.kill()
                self.game.score += self.score
        
        self.image = self.images_list[self.image_index]


class MediumEnemy(Enemy):
    size = (69, 99)
    type = 2

    def __init__(self, game, left_top):
        super().__init__(game, left_top)
        self.current_hp = 10
        self.score = 10

        self.load_image(['enemy2.png', 'enemy2_hit.png', 'enemy2_down1.png', 'enemy2_down2.png', 
                         'enemy2_down3.png', 'enemy2_down4.png'], self.size)


    def update(self):
        """更新"""
        super().update()
        if self.current_hp > 0:
            if self.is_hit_by_bullet:
                self.image_index = 1
                self.is_hit_by_bullet = False
            else:
                self.image_index = 0
        else:
            if self.image_index < len(self.images_list) - 1:
                self.image_index += 1
            else:
                self.kill()
                self.game.score += self.score
        
        self.image = self.images_list[self.image_index]



class BigEnemy(Enemy):
    size = (169, 258)
    type = 3
    
    def __init__(self, game, left_top):
        super().__init__(game, left_top)
        self.current_hp = 25
        self.score = 100

        self.load_image(['enemy3_n1.png', 'enemy3_n2.png', 'enemy3_hit.png', 'enemy3_down1.png', 
                         'enemy3_down2.png', 'enemy3_down3.png', 'enemy3_down4.png', 
                         'enemy3_down5.png', 'enemy3_down6.png'], self.size)

    def update(self):
        """更新"""
        super().update()
        if self.current_hp > 0:
            if self.is_hit_by_bullet:
                self.image_index = 2
                self.is_hit_by_bullet = False
            else:
                self.image_index = (self.image_index + 1) % 2
        else:
            if self.image_index < len(self.images_list) - 1:
                self.image_index += 1
            else:
                self.kill()
                self.game.score += self.score
        
        self.image = self.images_list[self.image_index]

    
class EnemySpawnMachine:
    """敌机生产机器"""
    def __init__(self, game):
        self._game = game
        self._enemies = Group()
        self._max_num = 18

    @property
    def enemies(self):
        return self._enemies

    def update(self):
        if len(self._enemies) < self._max_num:
            screen_rect = self._game.scene.screen.get_rect()

            weighted_list = [SmallEnemy] * 30 + [MediumEnemy] * 3 + [BigEnemy] * 1
            enemy = random.choice(weighted_list)

            left = random.randint(0, screen_rect.width-enemy.size[0])
            top = random.randint(-screen_rect.height, -enemy.size[1])

            self._enemies.add(enemy(self._game, (left, top)))

        self._enemies.update()