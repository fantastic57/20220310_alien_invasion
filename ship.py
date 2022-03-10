import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self,ai_game):  #需要一个实例输入
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen  # 将screen赋给了一个属性，以便后面的程序轻松访问
        self.screen_rect = ai_game.screen.get_rect()  # 访问屏幕的属性rect，以便能正确放置飞船位置
        self.settings = ai_game.settings  # 将settings赋给一个属性，以便后面的程序轻松访问

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()  # 访问飞船的属性rect，以便指定飞船位置

        # 对于每艘新飞船，都放置在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船的位置属性x
        self.x = float(self.rect.x)  # rect只存储整数

        # 初始化移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志更新飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:  #防止向右超出屏幕
            self.x += self.settings.ship_speed  # 根据设置里面的速度向右移动
        if self.moving_left and self.rect.left > 0:  #防止向左超出屏幕,pygame中（0，0）在左上角
            self.x -= self.settings.ship_speed  # 根据设置里面的速度向左移动

        self.rect.x = self.x  # 更新飞船位置

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def centre_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)