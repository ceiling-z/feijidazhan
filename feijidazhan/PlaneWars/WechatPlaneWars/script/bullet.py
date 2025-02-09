import os
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, game) -> None:
        super().__init__()
        self._game = game       # 游戏主逻辑
        self.image = None       # 当前图片
        self.mask = None        # 图片遮罩
        self.rect = None        # 图片位置

        self._main()

    def _main(self):
        """主入口"""
        self._load_image()

    def _load_image(self):
        """加载图片"""
        image_path = os.path.join(os.path.dirname(__file__), '../res/image')
        self.image = pygame.image.load(os.path.join(image_path, 'bullet1.png'))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.midtop = self._game.hero.rect.midtop

    def _draw(self):
        """绘制到屏幕"""
        self._game.scene.screen.blit(self.image, self.rect)

    def update(self):
        """更新"""
        # 不断更新子弹位置
        if not self._game.is_paused:
            self.rect.top -= 12
        
        # 到屏幕外就被删除
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self._draw()