import sys
from time import sleep

import pygame

from setting import Settings
from game_stats import GameStats
from button import Button
from scoreboad import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建资源"""
        pygame.init()  # 初始化游戏设置
        self.settings = Settings()  # 创建设置类实例

        # 创建显示窗口，宽高背景颜色
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 创建显示窗口，全屏游戏
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width  # 不能预先知道屏幕大小，更新屏幕宽度
        # self.settings.screen_height = self.screen.get_rect().height  # 不能预先知道屏幕大小，更新屏幕高度

        # 创建play按钮
        self.play_button = Button(self, "Play")

        # 创建统计信息及计分板
        self.stats = GameStats(self)  # 创建游戏统计类实例
        self.sb = Scoreboard(self)  # 创建计分板实例

        pygame.display.set_caption("Alien Invasion")  # 游戏名
        self.ship = Ship(self)  # 创建飞船类实例，实参self指向当前实例
        self.bullets = pygame.sprite.Group()  # 创建编组子弹
        self.aliens = pygame.sprite.Group()  # 创建编组外星人, 类似于空列表
        self._create_fleet()  # 创建外星人们

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()  # 监控键盘输入指令，无论何时都要做，帮助退出游戏
            if self.stats.game_active:  # 游戏是否在进行
                self.ship.update()  # 调整飞船位置
                self._update_bullets()  # 调整子弹位置等信息
                self._update_aliens()  # 调整外星人位置信息

            self._update_screen()  # 将结果绘制并刷新，无论何时都要做

    def _check_events(self):
        """监视按键和操作，每次用户按键，都注册一个事件，通过pygame.event.get()获取"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 按右上角x退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 检查是否按下按键
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 检查是否松开按键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 检测鼠标点击的位置
                self._check_play_button(mouse_pos)  # 开始游戏

    def _check_play_button(self, mouse_pos):
        """在玩家点击按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  # 鼠标单击的位置在play按钮的rect内 且 游戏处于未开始状态 开始游戏
            self.stats.reset_stats()  # 重置游戏统计信息（几次机会和几分）
            self.settings.initialize_dynamic_settings()  # 重置游戏设置
            self.stats.game_active = True  # 开始游戏
            self.sb.pre_score()  # 准备得分信息
            self.sb.pre_level()  # 准备等级信息
            self.sb.pre_ships()  # 准备飞船信息
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 重新创建外星人并使得飞船居中
            self._create_fleet()  # 创建新外星人
            self.ship.centre_ship()  # 飞船放回到屏幕底部中央，等于重新开始
            # 隐藏游戏光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:  # 检查是否是->右箭头
            self.ship.moving_right = True  # 向右移动飞船
        elif event.key == pygame.K_LEFT:  # 检查是否是<-左箭头
            self.ship.moving_left = True  # 向左移动飞船
        elif event.key == pygame.K_SPACE:  # 检查是否是空格键
            self._fire_bullet()  # 发射子弹
        elif event.key == pygame.K_q:  # 按q也能退出游戏
            sys.exit()

    def _check_keyup_events(self, event):
        """响应松开按键"""
        if event.key == pygame.K_RIGHT:  # 检查是否是->右箭头
            self.ship.moving_right = False  # 停止移动飞船
        if event.key == pygame.K_LEFT:  # 检查是否是<-左箭头
            self.ship.moving_left = False  # 停止移动飞船

    def _fire_bullet(self):
        """创建一颗子弹，并加入bullets编组"""
        if len(self.bullets) < self.settings.bullet_allowed:  # 子弹最多数量
            new_bullet = Bullet(self)  # 创建子弹实例
            self.bullets.add(new_bullet)  # 加入编组

    def _update_bullets(self):
        """更新子弹的位置并消除子弹"""
        self.bullets.update()  # 调整子弹位置
        # 删除消失的子弹
        for bullet in self.bullets.copy():  # python要求列表的长度在循环中不变，因此遍历副本
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 子弹命中外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """子弹命中外星人"""
        # 检查是否有子弹击中外星人，如果有，删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  # 比较子弹与外星人，True为删除
        # 计分
        if collisions:
            for aliens in collisions.values():  # 所有击杀都算上
                self.stats.score += self.settings.alien_points * len(aliens)  # 一次杀了几只外星人
                self.sb.pre_score()
                self.sb.check_highest_score()

        # 若全部击杀，则更新外星人
        if not self.aliens:
            self.bullets.empty()  # 清空子弹
            self._create_fleet()
            self.settings.increase_speed()  # 提高游戏难度
            self.stats.level += 1  # 提高等级
            self.sb.pre_level()  # 绘制等级

    def _create_fleet(self):
        """创建外星人组"""
        # 计算一行能有几个外星人
        alien = Alien(self)  # 创建一个外星人，仅用于计算，不加入外星人组
        alien_width, alien_height = alien.rect.size  # 外星人尺寸
        available_space_x = self.settings.screen_width - (2 * alien_width)  # 行可用空间为屏幕大小减去左右空白
        numbers_alien_x = available_space_x // (2 * alien_width)  # //为整除，一行能有几个外星人
        # 计算能有几行外星人
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height  # 列可用空间
        numbers_rows = available_space_y // (2 * alien_height)  # 能有几行

        # 创建外星人群
        for row_number in range(numbers_rows):  # 从0数到能加几行外星人
            # 创建一行外星人
            for alien_number in range(numbers_alien_x):  # 从0数到能加几个外星人
                self._create_alien(alien_number, row_number)  # 依次创建外星人并入队

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将它放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number  # 每个右移一个位置
        alien.rect.x = alien.x  # 外星人x位置
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # 外星人y位置
        self.aliens.add(alien)  # 将外星人加入组

    def _check_fleet_edges(self):
        """检查外星人是否运动到屏幕边缘"""
        for alien in self.aliens.sprites():
            if alien.check_edges():  # 检查外星人是否运动到屏幕边缘
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """外星人下移并改变移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # 外星人下移
        self.settings.fleet_direction *= -1  # 改变方向标志

    def _update_aliens(self):
        """更新外星人位置信息"""
        self._check_fleet_edges()  # 先检测是否运动到屏幕边缘，再决定怎么运动
        self.aliens.update()
        # 检测外星人与飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检测外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()  # 类似于外星人撞到飞船
                break

    def _ship_hit(self):
        """当外星人与飞船碰撞响应"""
        self.stats.ships_left -= 1  # 少一艘飞船
        self.sb.pre_ships()  # 显示在左上角
        print(self.stats.ships_left)
        if self.stats.ships_left > 0:
            self.aliens.empty()  # 清除外星人
            self.bullets.empty()  # 清除子弹
            self._create_fleet()  # 创建新外星人
            self.ship.centre_ship()  # 飞船放回到屏幕底部中央，等于重新开始
            sleep(0.5)  # 暂停一下
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  # 游戏结束，鼠标出现

    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.fill(self.settings.bg_color)  # 每次循环都重新绘制屏幕
        self.ship.blitme()  # 在屏幕上绘制飞船
        for bullet in self.bullets.sprites():  # 遍历所有子弹并绘制
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 在屏幕上绘制外星人

        self.sb.show_score()  # 显示得分等信息

        # 如果游戏处于非活动状态，绘制Play按钮
        if not  self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # 让最近绘制的屏幕可见


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
