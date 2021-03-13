import arcade as ac
from random import choice
from time import time


class Game(ac.View):
    def __init__(self, window: ac.Window):
        super(Game, self).__init__(window)

        self.mode = "game"  # game | end
        self.winner = None
        self.end_timer = None

        self.player_1 = Player(window)
        self.player_2 = Player(window)

        self.players = ac.SpriteList()
        self.ball = Ball(self)

        self.setup()

    def setup(self):
        self.player_1.setup(1)
        self.player_2.setup(2)

        self.players.append(self.player_1)
        self.players.append(self.player_2)
        self.ball.setup(self.players)

        self.start()

    def start(self):
        self.ball.center_y, self.ball.center_x = self.window.height // 2, self.window.width // 2
        self.ball.change_x, self.ball.change_y = choice((-1, 1)) * self.ball.speed, 0

        for player in self.players:
            player.center_y = self.window.height // 2

    def on_update(self, delta_time: float):
        if self.mode == "game":
            self.players.update()
            self.ball.update()

            if self.ball.right >= self.window.width:
                self.player_1.score += 1
                if self.player_1.score == 3:
                    self.mode = "end"
                    self.winner = "Player 1"
                    self.end_timer = time()
                self.start()
            elif self.ball.left <= 0:
                self.player_2.score += 1
                if self.player_2.score == 3:
                    self.mode = "end"
                    self.winner = "Player 2"
                    self.end_timer = time()
                self.start()
        else:
            if time() - self.end_timer >= 5:
                self.window.show_menu()

    def on_draw(self):
        ac.start_render()
        width, height = self.window.get_size()

        if self.mode == "end":
            ac.draw_text(text=f"{self.winner} won !", start_x=width // 2, start_y=height // 2,
                         color=(255, 255, 255),
                         anchor_x="center", anchor_y="center", font_size=width * 5 / 100)
            ac.draw_text(text=f"{5 - int(time()-self.end_timer)}", start_x=width-10, start_y=10,
                         anchor_x="right", anchor_y="bottom", color=(255, 255, 255), font_size=width * 2 / 100)
        else:
            self.ball.draw()
        self.players.draw()

        ac.draw_text(text=f"{self.player_1.score}", start_x=width // 2 - 20, start_y=height - 20,
                     color=(255, 0, 0),
                     anchor_x="right", anchor_y="top", font_size=width * 2 / 100)
        ac.draw_text(text=f"{self.player_2.score}", start_x=width // 2 + 20, start_y=height - 20,
                     color=(255, 0, 0),
                     anchor_x="left", anchor_y="top", font_size=width * 2 / 100)
        ac.draw_text(text=f"|", start_x=width // 2, start_y=height - 20,
                     color=(255, 0, 0),
                     anchor_x="center", anchor_y="top", font_size=width * 5 / 100)

    def on_key_press(self, symbol: int, modifiers: int):
        for player in self.players:
            player.key_press(symbol)

    def on_key_release(self, _symbol: int, _modifiers: int):
        for player in self.players:
            player.key_release(_symbol)


class Player(ac.Sprite):
    setup_control_keys = (((ac.key.Q, ac.key.Z), (ac.key.D, ac.key.S)),
                          ((ac.key.RIGHT, ac.key.UP), (ac.key.LEFT, ac.key.DOWN)))

    def __init__(self, window: ac.Window):
        self.window = window
        super(Player, self).__init__(filename="assets/game/platform.png", scale=0.09, center_y=self.window.height // 2)
        self.speed = self.window.height / 200
        self.score = 0
        self.controls = None

        self.up_move, self.down_move = [False, False], [False, False]

    def setup(self, player_number):
        self.angle = 90
        if player_number == 1:
            self.center_x = 20
        else:
            self.center_x = self.window.width - 20
        self.controls = Player.setup_control_keys[player_number - 1]

    def update(self):
        self.center_y += self.speed * (any(self.up_move) - any(self.down_move))

        if self.top >= self.window.height or self.bottom <= 0:
            self.center_y -= self.speed * (any(self.up_move) - any(self.down_move))

    def key_press(self, key):
        if key in self.controls[0]:
            self.up_move[self.controls[0].index(key)] = True
        elif key in self.controls[1]:
            self.down_move[self.controls[1].index(key)] = True

    def key_release(self, key):
        if key in self.controls[0]:
            self.up_move[self.controls[0].index(key)] = False
        elif key in self.controls[1]:
            self.down_move[self.controls[1].index(key)] = False


class Ball(ac.Sprite):
    def __init__(self, game: Game):
        self.game = game
        self.window = game.window
        super(Ball, self).__init__(filename="assets/game/ball.png", scale=0.03)
        self.speed = 3
        self.players, self.player_1, self.player_2 = None, None, None

    def setup(self, players: ac.SpriteList):
        self.player_1, self.player_2 = self.players = players

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.bottom <= 0 or self.top >= self.window.height:
            self.change_y *= -1

        a = self.collides_with_list(self.players)
        if len(a) > 0:
            self.change_y += (self.center_y - a[0].center_y) * 0.1
            self.change_x *= -1
