from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp
import random


class GuessGame(BoxLayout):

    def init(self, **kwargs):
        super().init(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(15),
            **kwargs
        )

        self.correct_guess = random.randint(1, 10)
        self.attempts = 0

        self.title = Label(
            text="لعبة خمن الرقم",
            font_size="28sp",
            bold=True,
            size_hint=(1, 0.18)
        )

        self.instruction = Label(
            text="خمن رقم من 1 إلى 10",
            font_size="20sp",
            size_hint=(1, 0.12)
        )

        self.entry = TextInput(
            hint_text="اكتب الرقم هنا",
            font_size="24sp",
            halign="center",
            multiline=False,
            input_filter="int",
            size_hint=(1, 0.15)
        )

        self.guess_button = Button(
            text="خمن",
            font_size="20sp",
            size_hint=(1, 0.15)
        )

        self.result = Label(
            text="خمن رقم من 1 إلى 10",
            font_size="18sp",
            size_hint=(1, 0.15)
        )

        self.attempts_label = Label(
            text="المحاولات: 0",
            font_size="18sp",
            size_hint=(1, 0.10)
        )

        self.new_game_button = Button(
            text="لعبة جديدة",
            font_size="18sp",
            size_hint=(1, 0.15)
        )

        self.guess_button.bind(
            on_release=self.check_guess
        )

        self.new_game_button.bind(
            on_release=self.new_game
        )

        self.entry.bind(
            on_text_validate=self.check_guess
        )

        self.add_widget(self.title)
        self.add_widget(self.instruction)
        self.add_widget(self.entry)
        self.add_widget(self.guess_button)
        self.add_widget(self.result)
        self.add_widget(self.attempts_label)
        self.add_widget(self.new_game_button)

    def check_guess(self, instance):
        text = self.entry.text.strip()

        if not text:
            self.result.text = "اكتب رقمًا أولًا"
            return

        try:
            guess = int(text)
        except ValueError:
            self.result.text = "اكتب رقمًا صحيحًا فقط"
            return

        if guess < 1 or guess > 10:
            self.result.text = "اكتب رقمًا من 1 إلى 10"
            return

        self.attempts += 1

        self.attempts_label.text = (
            f"المحاولات: {self.attempts}"
        )

        if guess == self.correct_guess:
            self.result.text = (
                f"صح! الرقم هو {self.correct_guess}"
            )

            self.guess_button.disabled = True

        elif guess < self.correct_guess:
            self.result.text = "أعلى من كده"

        else:
            self.result.text = "أقل من كده"

        self.entry.text = ""

    def new_game(self, instance):
        self.correct_guess = random.randint(1, 10)
        self.attempts = 0

        self.entry.text = ""

        self.result.text = (
            "خمن رقم من 1 إلى 10"
        )

        self.attempts_label.text = (
            "المحاولات: 0"
        )

        self.guess_button.disabled = False

        self.entry.focus = True


class GuessGameApp(App):

    def build(self):
        return GuessGame()


if name == "main":
    GuessGameApp().run()
