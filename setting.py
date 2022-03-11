class Settings:
    """存储游戏中所有设置类"""

    def __init__(self):
        """初始化游戏静态设置"""
        # 屏幕设置
        self.screen_width = 1200  # 设置显示器宽度
        self.screen_height = 800  # 设置显示器高度
        self.bg_color = (230, 230, 230)  # 设置显示器背景颜色
        # 飞船设置
        self.ship_limit = 3  # 三次机会
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3  # 子弹最多个数
        # 外星人设置
        self.fleet_drop_speed = 3  # 垂直移动速度

        self.speedup_scale = 1.2  # 加快游戏节奏
        self.score_scale = 1.5  # 提高得分
        self.initialize_dynamic_settings

    def initialize_dynamic_settings(self):
        """初始化动态参数"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.2  # 外星人水平移动速度
        self.fleet_direction = 1  # 1为右移，-1为左移
        self.alien_points = 10  # 每个外星人多少分

    def increase_speed(self):
        """提高速度设置和外星人得分"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
