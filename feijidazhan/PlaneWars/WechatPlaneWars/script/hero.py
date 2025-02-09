import os
import pygame
from pygame.locals import *
from pygame.sprite import Group

from bullet import Bullet


class Hero:
    """玩家飞机"""
    def __init__(self, game):
        self._game = game               # 游戏主逻辑

        self.image = None               # 飞机当前图片
        self.mask = None                # 图片遮罩
        self.rect = None                # 飞机位置

        self._image_index = None        # 当前图片索引
        self._images_list = None        # 飞机图片列表
        self._is_collide = None         # 是否发生碰撞

        self._frames = 0                # 子弹频率
        self._bullets = Group()         # 子弹分组

        self._main()

    @property
    def bullets(self):
        return self._bullets

    @property
    def is_collide(self):
        return self._is_collide

    @is_collide.setter
    def is_collide(self, value):
        self._is_collide = value

    def _main(self):
        """主入口"""
        self._load_image()
        self.reset()

    def _load_image(self):
        """加载飞机图片"""
        # 加载有关我方飞机的所有图片
        image_path = os.path.join(os.path.dirname(__file__), '../res/image')
        image_name_list = ['hero1.png', 'hero2.png', 'hero_blowup_n1.png', 'hero_blowup_n2.png', 'hero_blowup_n3.png', 'hero_blowup_n4.png']
        self._images_list = [pygame.image.load(os.path.join(image_path, name)).convert_alpha() for name in image_name_list]

        # 将第一个元素作为飞机正常状态图片
        self.image = self._images_list[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def reset(self):
        """重设飞机状态"""
        # 将飞机设置在屏幕中间
        self.rect.midbottom = self._game.scene.screen.get_rect().midbottom
        self._is_collide = False
        self._image_index = 0

    def _draw(self):
        """绘制飞机图片"""
        if self._is_collide:
            # 飞机爆炸和游戏失败
            if self._image_index < len(self._images_list) - 1:
                self._image_index += 1
            else:
                pygame.time.delay(200)
                self._game.game_state = 'GAMEOVER'
        else:
            # hero1.png和hero2.png相互交换，尾部喷射
            self._image_index = not self._image_index

        # 将图片映射到屏幕上
        self.image = self._images_list[self._image_index]
        self._game.scene.screen.blit(self.image, self.rect)
        
    def update(self, pos):
        """更新"""
        # 绘制飞机图
        self._draw()

        # 如果暂停则跳过
        if not self._game.is_paused:
            # 鼠标按在飞机里面才可以移动飞机
            if pos and self.rect.collidepoint(pos):
                self.rect.center = pos

            # 更新子弹
            self._frames += 1
            if not (self._frames % 5):
                self._bullets.add(Bullet(self._game))
                self._frames = 0
                self._game.sounds.play('bullet')
        
        self._bullets.update()