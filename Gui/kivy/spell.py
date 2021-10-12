from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.spelling import Spelling
from kivy.core.window import Window
Window.size = (600,400)

Builder.load_file('spell.kv')


class MyLayout(Widget):
    def press(self):
        # create instance for spelling
        s = Spelling()

        # select the language
        s.select_language('en_IN')

        # see the language options
        # print(s.list_lanhuages())

        # Grab the word
        word = self.ids.word_input.text

        options = s.suggest(word)
        x = ''
        for item in options:
            x = f'{x} {item}'
        # update our label
        self.ids.word_label.text = f'{x}'


class AwecomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    AwecomeApp().run()
