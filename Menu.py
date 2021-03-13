import arcade as ac
import arcade.gui as gui
import os


class Menu(ac.View):
    def __init__(self, window: ac.Window):
        super(Menu, self).__init__(window)
        self.ui_manager = gui.UIManager()
        self.ui_elements = ac.SpriteList()

        self.setup()

    def setup(self):
        width, height = self.window.get_size()
        self.ui_elements.append(Button(self.window,
                                       "assets/menu/play_unselected.png", hover_texture="assets/menu/play_selected.png",
                                       center_x=width // 3, center_y=height // 2, click_callback=self.window.start_game,
                                       scale=0.3))

        self.ui_elements.append(Button(self.window,
                                       "assets/menu/title.png",
                                       center_x=width // 3, center_y=height * 5 // 7))

        self.ui_elements.append(Button(self.window,
                                       "assets/menu/controls.png",
                                       center_x=width // 3, center_y=height // 5, scale=0.5))

        self.ui_elements.append(Button(self.window, "assets/menu/ball.png", center_x=width, center_y=0, scale=1))
        self.ui_elements.append(Button(self.window, "assets/menu/ball.png", center_x=width * 4 // 5,
                                       center_y=height * 3 // 4, scale=0.15))
        self.ui_elements.append(Button(self.window, "assets/menu/ball.png", center_x=width * 5 // 8,
                                       center_y=height // 2, scale=0.1))

        self.ui_elements.append(Button(self.window,
                                       "assets/menu/exit_unselected.png", hover_texture="assets/menu/exit_selected.png",
                                       center_x=width - 50, center_y=height - 50, scale=0.15,
                                       click_callback=self.window.close))

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        ac.start_render()
        self.ui_elements.draw()
        for element in self.ui_elements:
            element.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for element in ac.get_sprites_at_point((x, y), self.ui_elements):
            element.mouse_click()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for element in self.ui_elements:
            element.mouse_motion((x, y))


class Button(ac.Sprite):
    def __init__(self, window: ac.Window, normal_texture: str, hover_texture=None, center_x=0, center_y=0,
                 click_callback: callable = None, text: str = "", scale: float = 1):
        super(Button, self).__init__(filename=normal_texture, scale=scale, center_x=center_x, center_y=center_y)
        self.window = window

        if hover_texture is not None:
            self.hover_texture = ac.load_texture(hover_texture)
            self.textures.append(self.hover_texture)
        else:
            self.hover_texture = None
        self.text = text
        self.click_callback = click_callback

    def draw(self):
        ac.draw_text(self.text, start_x=self.center_x, start_y=self.center_y, anchor_x="center", anchor_y="center",
                     color=(255, 0, 0))

    def mouse_click(self):
        if self.click_callback is not None:
            self.click_callback()

    def mouse_motion(self, mouse_position: tuple):
        if self.hover_texture is not None:
            index = self.textures.index(self.hover_texture)
            if self.collides_with_point(mouse_position):
                if self.cur_texture_index != index:
                    ac.play_sound(self.window.musics["select"])
                    self.cur_texture_index = index
                    self.set_texture(index)
            else:
                if self.cur_texture_index != 0:
                    self.cur_texture_index = 0
                    self.set_texture(0)
