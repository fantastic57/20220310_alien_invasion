import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen  # 便于后续程序引用
        self.settings = ai_game.settings  # 便于后续程序引用

        # 加载外星人并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()  # 获得外星人尺寸

        # 每个外星人最初都在屏幕的左上角
        self.rect.x = self.rect.width  # 左边距为外星人宽度
        self.rect.y = self.rect.height  # 上边距为外星人高度

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人碰到屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        # 若外星人rect属性的right大于等于屏幕的right，说明在屏幕外；若left属性小于等于0，说明在屏幕外
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """左右移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction  # 每次更新左右移动一些
        self.rect.x = self.x