import pygame.font


class Button:
    """建立按钮类"""

    def __init__(self, ai_game, msg):  # 按钮上显示msg信息
        """初始化按钮属性"""
        self.screen = ai_game.screen  # 便于后续程序引用
        self.screen_rect = self.screen.get_rect()

        # 设置按钮尺寸及其它属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 创建按钮上面的字
        self._prep_msg(msg)  # 要渲染成图像的文本msg

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)  # 将文本msg渲染为图像并存储
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # 让文本图像居中于按钮上

    def draw_button(self):
        """绘制一个按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
