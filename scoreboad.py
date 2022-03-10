import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息"""

    def __init__(self, ai_game):
        """初始化得分信息"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # 显示得分信息时用的字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.pre_score()
        # 准备最高得分图像
        self.pre_highest_score()
        # 准备等级图像
        self.pre_level()
        # 准备剩余飞船数量
        self.pre_ships()

    def pre_score(self):
        """将得分转换为一副渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # 圆整得分为10的倍数
        score_str = "{:,}".format(rounded_score)  # 将数值转变为字符串时在其中插入逗号
        score_str = "Score: "+ score_str
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)  # 字符串渲染为图像
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 得分增大的时候向左延伸
        self.score_rect.top = 20

    def pre_highest_score(self):
        """将最高得分转换为一副渲染的图像"""
        highest_rounded_score = round(self.stats.highest_score, -1)  # 圆整得分为10的倍数
        highest_score_str = "{:,}".format(highest_rounded_score)  # 将数值转变为字符串时在其中插入逗号
        highest_score_str = 'Highest Score: '+highest_score_str
        self.highest_score_image = self.font.render(highest_score_str, True, self.text_color,self.settings.bg_color)  # 字符串渲染为图像
        # 在屏幕顶部中央显示得分
        self.highest_score_rect = self.score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx - 50  # 当前窗口下的中心位置
        self.highest_score_rect.top = self.score_rect.top  # 与当前得分保持一致

    def check_highest_score(self):
        """检查出现了新的最高得分"""
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.pre_highest_score()

    def pre_level(self):
        """将等级转换为一副渲染的图像"""
        level_str = str(self.stats.level)  # 将数值转变为字符串
        level_str = "Level: " + level_str
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)  # 字符串渲染为图像
        # 在得分以下显示等级
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  # 在得分以下

    def pre_ships(self):
        """显示还剩多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):  # 根据还剩几条船运行一个循环
            ship = Ship(self.ai_game)  # 创建新飞船实例
            ship.rect.x = 10 + ship_number * ship.rect.width  # 新飞船横坐标
            ship.rect.y = 10  # 新飞船纵坐标
            self.ships.add(ship)  # 添加新飞船到ships编组Group中

    def show_score(self):
        """在屏幕上显示得分等信息"""
        self.screen.blit(self.score_image, self.score_rect)  # 当前得分
        self.screen.blit(self.highest_score_image, self.highest_score_rect)  # 最高得分
        self.screen.blit(self.level_image, self.level_rect)  # 当前等级
        self.ships.draw(self.screen)
