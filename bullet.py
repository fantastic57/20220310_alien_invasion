import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):  # 继承了Sprite类
    """管理飞船发射的子弹"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹"""
        super().__init__()  # 继承Sprite类的方法
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0）创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  # 创建一个矩形代表子弹
        self.rect.midtop = ai_game.ship.rect.midtop  # 子弹位置取决于飞船位置，子弹从飞船中发出

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)  # 以便能微调子弹速度、

    def update(self):
        """向上移动子弹，类似飞船左右移动"""
        self.y -= self.settings.bullet_speed  # 子弹向上移动，代表y逐渐减小，能设置子弹运动速度
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)