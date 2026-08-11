# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from random import randint

Window.size = (360, 640)

# ----- Game widget (رسم اللعبة وميكانيك الحركة) -----
class GameWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.car_width = 60
        self.car_height = 90
        self.car_x = (self.width - self.car_width) / 2
        self.car_y = 50
        self.obstacles = []  # كل عنصر: dict {rect, x, y, size}
        self.spawn_timer = 0
        self.score = 0
        self.coins = 0
        self.speed = 3
        self.paused = False

        with self.canvas:
            Color(0.1, 0.6, 0.9)  # خلفية الطريق
            self.bg = Rectangle(pos=self.pos, size=self.size)
            Color(1, 0, 0)  # السيارة
            self.car_rect = Rectangle(pos=(self.car_x, self.car_y),
                                      size=(self.car_width, self.car_height))

        self.bind(pos=self._update_bg, size=self._update_bg)
        Clock.schedule_interval(self.update, 1/60)

    def _update_bg(self, *a):
        self.bg.pos = self.pos
        self.bg.size = self.size
        # ضبط موضع السيارة عند تغيير الحجم
        if not hasattr(self, "car_initialized") or not self.car_initialized:
            self.car_x = (self.width - self.car_width) / 2
            self.car_rect.pos = (self.car_x, self.car_y)
            self.car_initialized = True

    def move_left(self, *a):
        self.car_x = max(10, self.car_x - 20)
        self.car_rect.pos = (self.car_x, self.car_y)

    def move_right(self, *a):
        self.car_x = min(self.width - self.car_width - 10, self.car_x + 20)
        self.car_rect.pos = (self.car_x, self.car_y)

    def spawn_obstacle(self):
        size = randint(30, 60)
        x = randint(10, int(self.width - size - 10))
        y = int(self.height + 20)
        with self.canvas:
            Color(0, 0, 0)  # عقبة سوداء
            rect = Rectangle(pos=(x, y), size=(size, size))
        self.obstacles.append({"rect": rect, "x": x, "y": y, "size": size})

    def update(self, dt):
        if self.paused:
            return

        # توليد عقبات تدريجيًا
        self.spawn_timer += dt
        if self.spawn_timer > max(0.6, 1.5 - self.score * 0.02):
            self.spawn_timer = 0
            self.spawn_obstacle()

        # تحريك العقبات لأسفل، وفحص الاصطدام
        to_remove = []
        for ob in self.obstacles:
            ob["y"] -= self.speed
            ob["rect"].pos = (ob["x"], ob["y"])
            # خارج الشاشة
            if ob["y"] + ob["size"] < -50:
                to_remove.append(ob)
                self.score += 1
                if self.score % 5 == 0:
                    self.coins += 10
                    self.speed += 0.3

            # فحص تصادم بسيط
            if (self.car_x < ob["x"] + ob["size"] and
                self.car_x + self.car_width > ob["x"] and
                self.car_y < ob["y"] + ob["size"] and
                self.car_y + self.car_height > ob["y"]):
                # اصطدام -> إيقاف اللعبة مؤقتًا
                self.paused = True

        for ob in to_remove:
            try:
                self.canvas.remove(ob["rect"])
            except Exception:
                pass
            if ob in self.obstacles:
                self.obstacles.remove(ob)

    def reset(self):
        # مسح العقبات وإعادة الحالة
        for ob in list(self.obstacles):
            try:
                self.canvas.remove(ob["rect"])
            except Exception:
                pass
        self.obstacles.clear()
        self.score = 0
        self.coins = 0
        self.speed = 3
        self.paused = False
        self.car_x = (self.width - self.car_width) / 2
        self.car_rect.pos = (self.car_x, self.car_y)


# ----- شاشات التطبيق -----
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        layout.add_widget(Label(text="اللعبة الرئيسية", font_size=32, size_hint=(1, .2)))
        btn_play = Button(text="ابدأ اللعبة", size_hint=(1, .12))
        btn_shop = Button(text="المتجر", size_hint=(1, .12))
        btn_multi = Button(text="اللعب الجماعي", size_hint=(1, .12))
        btn_quit = Button(text="خروج", size_hint=(1, .12))

        btn_play.bind(on_release=lambda *a: self.start_game())
        btn_shop.bind(on_release=lambda *a: self.manager.transition_to("shop"))
        btn_multi.bind(on_release=lambda *a: self.manager.transition_to("multiplayer"))
        btn_quit.bind(on_release=lambda *a: App.get_running_app().stop())

        layout.add_widget(btn_play)
        layout.add_widget(btn_shop)
        layout.add_widget(btn_multi)
        layout.add_widget(btn_quit)
        self.add_widget(layout)

    def start_game(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        self.game_widget = GameWidget(size_hint=(1, .78))
        info_bar = BoxLayout(size_hint=(1, .12), padding=6, spacing=6)
        self.score_label = Label(text="النقاط: 0  |  عملات: 0", halign="left")
        info_bar.add_widget(self.score_label)

        controls = BoxLayout(size_hint=(1, .1), spacing=10, padding=10)
        btn_left = Button(text="◀", font_size=30)
        btn_right = Button(text="▶", font_size=30)
        btn_restart = Button(text="إعادة", size_hint=(.3, 1))
        btn_back = Button(text="رجوع", size_hint=(.3, 1))

        btn_left.bind(on_release=lambda *a: self.game_widget.move_left())
        btn_right.bind(on_release=lambda *a: self.game_widget.move_right())
        btn_restart.bind(on_release=lambda *a: self.restart_game())
        btn_back.bind(on_release=lambda *a: self.back_to_menu())

        controls.add_widget(btn_left)
        controls.add_widget(btn_right)
        controls.add_widget(btn_restart)
        controls.add_widget(btn_back)

        root.add_widget(self.game_widget)
        root.add_widget(info_bar)
        root.add_widget(controls)
        self.add_widget(root)

        Clock.schedule_interval(self.update_labels, 0.2)

    def update_labels(self, dt):
        self.score_label.text = f"النقاط: {int(self.game_widget.score)}  |  عملات: {int(self.game_widget.coins)}"

    def restart_game(self):
        self.game_widget.reset()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "game"

    def back_to_menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main_menu"


class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="المتجر", font_size=28, size_hint=(1, .15)))
        layout.add_widget(Label(text="هنا يمكنك شراء ترقيات (وهمي)", size_hint=(1, .1)))
        btn_buy1 = Button(text="ترقية المحرك - 1000 عملة", size_hint=(1, .12))
        btn_back = Button(text="رجوع", size_hint=(1, .12))
        btn_back.bind(on_release=lambda *a: self.go_back())
        layout.add_widget(btn_buy1)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main_menu"


class MultiplayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="اللعب الجماعي", font_size=28, size_hint=(1, .15)))
        self.room_input = TextInput(hint_text="ادخل كود الغرفة", size_hint=(1, .12))
        btn_join = Button(text="اتصل بالغرفة", size_hint=(1, .12))
        btn_create = Button(text="انشئ غرفة", size_hint=(1, .12))
        self.status_label = Label(text="", size_hint=(1, .2))
        btn_back = Button(text="رجوع", size_hint=(1, .12))

        btn_join.bind(on_release=self.join_room)
        btn_create.bind(on_release=self.create_room)
        btn_back.bind(on_release=self.go_back)

        layout.add_widget(self.room_input)
        layout.add_widget(btn_join)
        layout.add_widget(btn_create)
        layout.add_widget(self.status_label)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def join_room(self, instance):
        code = self.room_input.text.strip()
        if code:
            self.status_label.text = f"متصل بالغرفة: {code}"
        else:
            self.status_label.text = "من فضلك ادخل كود الغرفة"

    def create_room(self, instance):
        self.status_label.text = "تم إنشاء الغرفة: #9982\nبانتظار لاعب..."

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main_menu"


# ----- مدير الشاشات مع طريقة انتقاليه مدمجة سهلة الاستخدام -----
class MyScreenManager(ScreenManager):
    def transition_to(self, name):
        self.transition = SlideTransition(direction="left")
        self.current = name


class UltimateGameApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ShopScreen(name="shop"))
        sm.add_widget(MultiplayerScreen(name="multiplayer"))
        return sm


if __name__ == "__main__":
    UltimateGameApp().run()