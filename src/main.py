
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.config import Config



import jieba
# from dictionary.dictionary import Dictionary
from dictionary.search import Search
from gui.prettify import colorise_characters_and_pinyin, pretty_definition
Config.set('kivy', 'keyboard_mode', 'system')




class SearchBox(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dictionary = Search.from_json('dictionary/dict.json')
        

    # when text is changed (on_text), the following function is run
    def on_text(self, *args):
        # get the current running app
        app = App.get_running_app()
        # set the current screen back to the search list
        app.root.ids.sm.current = 'SearchList'
        # search the phrase in the dictionary
        results = self.dictionary.search(self.text, gui_flag=True)
        # add the results to the data attribute of the rv
        rv = app.root.ids.sm.get_screen('SearchList').children[0]
        rv.rv_data = results

    # the following function removes all white space
    def insert_text(self, substring, from_undo=False):
        s = substring.replace(' ', '')
        return super().insert_text(s, from_undo=from_undo)


# The following class relates to the functionality of the previous and next word buttons when on the word screen

class PrevNextButton(Button):

    def update_information(self, index_change):
        app = App.get_running_app()
        word_screen = app.root.ids.sm.get_screen('WordScreen').children[0]
        search_screen = app.root.ids.sm.get_screen('SearchList').children[0]
        self.index = word_screen.index
        # get the dictionary of the word that replaces the current one on the word screen
        info = search_screen.data[self.index + index_change]
        # update the contents of the word screen
        # word_screen.ids.word_title.text = f"[size=80]{info['simplified']}[/size]"
        # word_screen.ids.word_title.text += '\t' + info['pinyin']
        # word_screen.ids.word_body.text = f"[size=60]{info['definition']}[/size]"
        header, definitions = pretty_definition(info)
        word_screen.ids.word_title.text = header
        word_screen.ids.word_body.text = definitions
        # update the index of the word_screen
        word_screen.index += index_change
        # set screen to word screen
        app.root.ids.sm.current = 'WordScreen'

    def go_back(self):
        app = App.get_running_app()
        app.root.ids.sm.current = 'WordScreen'
        self.index = app.root.ids.sm.get_screen('WordScreen').children[0].index
        if self.index == 0:
            print("last word")
        else:
            self.update_information(index_change=-1)
            app.root.ids.sm.current = 'WordScreen'

    def go_forward(self):
        app = App.get_running_app()
        self.index = app.root.ids.sm.get_screen('WordScreen').children[0].index
        n_words = len(app.root.ids.sm.get_screen(
            'SearchList').children[0].data)
        if self.index == (n_words - 1):
            print("last word")
        else:
            self.update_information(index_change=+1)
            app.root.ids.sm.current = 'WordScreen'


class SearchList(RecycleView):
    rv_data = ListProperty()
    states = ListProperty(['normal'] * 50) # brute force longer than needed

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dictionary = Search()

    def clear_states(self):
        for i, _ in enumerate(self.states):
            self.states[i] = 'normal'

    def on_states(self, *args):
        pass
        #print(self.states)




class Word(BoxLayout):
    ''' Add selection support to the Label '''
    idx = NumericProperty() # set by the rv list

    def update_information(self):
        '''Update the information in the WordScreen
        whenever one of the words is clicked'''
        app = App.get_running_app()
        word_screen = app.root.ids.sm.get_screen('WordScreen').children[0]
        #word_screen.index = self.idx
        # get the dictionary of the word that will be displayed on the word screen
        #info = rv.data[index]
        # update the contents of the word screen
        # word_screen.ids.word_title.text = pretty_definition(self)
        # word_screen.ids.word_title.text = f"[size=80]{self.simplified}[/size]"
        # word_screen.ids.word_title.text += '\t' + self.pinyin
        # word_screen.ids.word_body.text = f"[size=60]{self.definition}[/size]"
        word_dict = {'simplified': self.simplified,
                             'pinyin': self.pinyin,
                             'definition': self.definition,
                             'pinyin_num': self.pinyin_num,
        }
        header, definitions = pretty_definition(word_dict)
        word_screen.ids.word_title.text = header
        word_screen.ids.word_body.text = definitions
        app.root.ids.sm.transition.direction='left'
        app.root.ids.sm.current = 'WordScreen'

# the following classes relate to the WordScreen and the information
# presented there

class WordScreen(BoxLayout):
    index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InfoLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NextButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Program(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        s = Screen(name='SearchList')
        s.add_widget(SearchList())
        self.ids.sm.add_widget(s)

        s = Screen(name='WordScreen')
        s.add_widget(WordScreen())
        self.ids.sm.add_widget(s)


class MainApp(App):
    def build(self):
        return Program()


if __name__ == "__main__":
    MainApp().run()
