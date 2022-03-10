class GameStats:
    """统计游戏信息"""

    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False  # 游戏刚启动时处于暂停状态
        self.highest_score = 0  # 最高得分，永远不会清除

    def reset_stats(self):
        """reset游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit  # 可以有几次机会
        self.score = 0  # 得分
        self.level = 1  # 等级