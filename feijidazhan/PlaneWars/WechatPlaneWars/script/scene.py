import os
import pygame
from pygame.locals import *


class Scene:
    """绘制界面"""
    def __init__(self, game):
        # 主逻辑和屏幕
        self._game = game
        self._screen = None
        
        # 背景
        self._background = None
        self._background_y = None
        self._background_rect = None

        # 按钮
        self._buttons = None
        self._pause_image = None
        self._resume_image = None
        self._pause_rect = None
        self._resume_rect = None

        # logo
        self._logo = None
        self._logo_rect = None

        # 分数
        self._score_color = None
        self._score_font = None

        # 入口
        self._main()

    @property
    def screen(self):
        return self._screen

    @property
    def buttons(self):
        return self._buttons

    @property
    def pause_rect(self):
        return self._pause_rect

    @property
    def resume_rect(self):
        return self._resume_rect

    def _main(self):
        """类入口"""
        self._init_screen()
        self._load_image()
        self._init_buttons()
        self._init_score_font()

    def _init_screen(self):
        """初始化屏幕"""
        pygame.init()

        # 设置大小、标题和图标
        self._screen = pygame.display.set_mode((480, 852))
        pygame.display.set_caption('微信飞机大战')

        icon_path = os.path.join(os.path.dirname(__file__), '../res/image/icon.ico')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

    def _load_image(self):
        """加载图片"""
        image_path = os.path.join(os.path.dirname(__file__), '../res/image')
        self._background = pygame.image.load(os.path.join(image_path, 'background.png')).convert_alpha()
        self._background_rect = self._background.get_rect()
        self._background_y = float(self._background_rect.y)

        self._logo = pygame.image.load(os.path.join(image_path, 'logo.png')).convert_alpha()
        self._logo_rect = self._logo.get_rect()
        self._logo_rect.centerx = self._screen.get_rect().centerx
        self._logo_rect.centery = self._screen.get_rect().centery - 150

        self._pause_image = pygame.image.load(os.path.join(image_path, 'game_pause.png')).convert_alpha()
        self._resume_image = pygame.image.load(os.path.join(image_path, 'game_resume.png')).convert_alpha()
        self._pause_rect = self._pause_image.get_rect()
        self._resume_rect = self._resume_image.get_rect()
        self._pause_rect.topleft = (400, 15)
        self._resume_rect.topleft = (400, 15)
        
    def _init_buttons(self):
        """初始化文本按钮"""
        button_names_list = ['Restart', 'Exit']
        self._buttons = {name:Button(self._screen, name) for name in button_names_list}
        
    def _init_score_font(self):
        """初始化分数字体"""
        self._score_color = (0, 0, 0)
        font_path = os.path.join(os.path.dirname(__file__), '../res/font')
        self._score_font = pygame.font.Font(os.path.join(font_path, 'comici.ttf'), 35)

    def _move_background(self):
        """移动背景"""
        # 不断改变_background_y的值
        if not self._game.is_paused:
            if self._background_y < self._background_rect.height:
                self._background_y += 1.5
            else:
                self._background_y = 0

            self._background_rect.y = self._background_y

        # 两张背景图片拼接
        self._screen.blit(self._background, (0, self._background_rect.y))
        self._screen.blit(self._background, (0, self._background_rect.y-self._background_rect.height))

    def _draw_score(self):
        """绘制分数"""
        score_image = self._score_font.render(str(self._game.score), True, self._score_color)
        self._screen.blit(score_image, (20, 10))

    def _draw_pause_resume(self):
        """绘制暂停和继续"""
        if not self._game.is_paused:
            self._screen.blit(self._pause_image, self._pause_rect)
        else:
            self._screen.blit(self._resume_image, self._resume_rect)
            
    def draw_text_buttons(self):
        """绘制文本按钮"""
        for btn in self._buttons.values():
            btn.draw()
            
    def draw_logo(self):
        """绘制飞机大战文字logo"""
        self._screen.blit(self._logo, self._logo_rect)

    def update(self):
        self._move_background()             # 移动背景
        self._draw_score()                  # 绘制分数
        self._draw_pause_resume()           # 绘制暂停和继续按钮


class Button:
    """文本按钮"""
    def __init__(self, screen, text):
        self._screen = screen
        self._border_color = (96, 96, 96)
        self._border_rect = pygame.Rect(0, 0, 180, 40)
        self._border_rect.center = self._screen.get_rect().center

        if text == 'Restart':
            self._border_rect.centery += 100
        elif text == 'Exit':
            self._border_rect.centery += 150

        text_color = self._border_color
        font = pygame.font.Font(None, 40)
        self._text_image = font.render(text, True, text_color)
        self._text_rect = self._text_image.get_rect()
        self._text_rect.center = self._border_rect.center

    def draw(self):
        pygame.draw.rect(self._screen, self._border_color, self._border_rect, 3)
        self._screen.blit(self._text_image, self._text_rect)
    
    def is_pressed(self, pos):
        return self._border_rect.collidepoint(pos)