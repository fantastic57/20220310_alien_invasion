import pygame.font


class Text:
    """开始界面显示的文本及帮助"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen  # 便于后续程序引用
        self.button = ai_game.play_button
        self.stats = ai_game.stats
        self.button_rect = self.button.rect
        self.settings = ai_game.settings
        # 标题颜色及字号
        self.title_color = (254, 129, 125)
        self.title_font = pygame.font.SysFont(None, 96)
        # 帮助文本颜色及字号
        self.text_color = (7, 7, 7)
        self.text_font = pygame.font.SysFont(None, 36)

        self.title = "Alien Invasion"
        self.help_1 = "Click 'Play' to start"
        self.help_2 = "Press '<-' or '->' to move"
        self.help_3 = "Press 'Space' to shoot"
        self._prep_text()  # 要渲染成图像的文本msg

    def _prep_text(self):
        """将文字渲染成图像"""
        # 将文本title渲染为图像并存储
        self.title_image = self.title_font.render(self.title, True, self.title_color, self.settings.bg_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.centerx = self.button_rect.centerx  # 标题图像位置
        self.title_image_rect.centery = self.button_rect.centery - 150
        # 将文本help1渲染为图像并存储
        self.help_1_image = self.text_font.render(self.help_1, True, self.text_color, self.settings.bg_color)
        self.help_1_image_rect = self.help_1_image.get_rect()
        self.help_1_image_rect.centerx = self.button_rect.centerx  # help1图像位置
        self.help_1_image_rect.centery = self.button_rect.centery + 100
        # 将文本help2渲染为图像并存储
        self.help_2_image = self.text_font.render(self.help_2, True, self.text_color, self.settings.bg_color)
        self.help_2_image_rect = self.help_2_image.get_rect()
        self.help_2_image_rect.centerx = self.button_rect.centerx  # help2图像位置
        self.help_2_image_rect.centery = self.button_rect.centery + 150
        # 将文本help3渲染为图像并存储
        self.help_3_image = self.text_font.render(self.help_3, True, self.text_color, self.settings.bg_color)
        self.help_3_image_rect = self.help_3_image.get_rect()
        self.help_3_image_rect.centerx = self.button_rect.centerx  # help2图像位置
        self.help_3_image_rect.centery = self.button_rect.centery + 200
        # 将文本last_score渲染为图像并存储
        self.rounded_score = round(self.stats.score, -1)  # 圆整得分为10的倍数
        self.last_score = "{:,}".format(self.rounded_score)  # 将数值转变为字符串时在其中插入逗号
        self.last_score = "Last score: " + self.last_score
        self.last_score_image = self.text_font.render(self.last_score, True, self.text_color, self.settings.bg_color)
        self.last_score_image_rect = self.last_score_image.get_rect()
        self.last_score_image_rect.centerx = self.button_rect.centerx  # help2图像位置
        self.last_score_image_rect.centery = self.button_rect.centery + 250

    def show_text(self):
        """在屏幕上显示帮助文本信息"""
        self._prep_text()
        self.screen.blit(self.title_image, self.title_image_rect)  # 标题
        self.screen.blit(self.help_1_image, self.help_1_image_rect)  # help1
        self.screen.blit(self.help_2_image, self.help_2_image_rect)  # help2
        self.screen.blit(self.help_3_image, self.help_3_image_rect)  # help3
        self.screen.blit(self.last_score_image, self.last_score_image_rect)  # last_score
