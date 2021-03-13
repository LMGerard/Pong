import arcade as ac
import Game
import Menu

BASE_WINDOW_WIDTH = 1000
BASE_WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pong by Loupio"


class Pong(ac.Window):
    musics = {
        "select": ac.load_sound("assets/menu/button_select.mp3"),
        "music": ac.load_sound("assets/game/thefatrat-windfall.mp3"),
        "ping_pong": ac.load_sound("assets/game/ping_pong.mp3")
    }

    def __init__(self):
        super(Pong, self).__init__(BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT, WINDOW_TITLE)
        self.set_fullscreen()

        self.show_menu()

    def start_game(self):
        self.show_view(Game.Game(self))

    def show_menu(self):
        self.show_view(Menu.Menu(self))


if __name__ == '__main__':
    app = Pong()
    ac.run()
