# add greek letters

import os
import wikipedia
from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.slider import Slider
from kivy.graphics import Rectangle
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

from sys import platform as sysplatform
if sysplatform == 'linux' or sysplatform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 50)
    Config.set('graphics', 'top', 40)
    Config.set('graphics', 'height', 496)
    Config.set('graphics', 'width', 800)
    Config.write()


class ScreenMan(ScreenManager):
    background = './img/background.jpg'

    def __init__(self, **kwargs):
        super(ScreenMan, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size,
                                  pos=self.pos,
                                  source=self.background)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


sm = ScreenMan(transition=NoTransition())


class SelectModal(ModalView):
    search_param = ListProperty([])
    
    title = 'Select an option'
    def __init__(self, selection_callback, **kwargs):
        super(SelectModal, self).__init__(**kwargs)
        self.search_param=['Test', 'Bechdel test', '.test', 'COVID-19 testing', 'Test (assessment)', 'TeST Gliders', 'Standardized test', 'Mirror test', 'Turing test', 'ACT (test)'] #test
        self.selection_callback = selection_callback
        self.layout = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': .5}
        )
        self.grid = GridLayout(
            size_hint=(None, 2),
            cols=1,
            spacing=5
        )
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)
    
    def on_open(self):
        self.grid.clear_widgets(self.grid.children)
        for n, label in enumerate(self.search_param):
            btn = Button(
                text=label,
                font_size='50dp',
                size_hint_x=None,
                width=Window.width,
                height=Window.height/5.0
            )
            btn.num = n
            btn.bind(on_press=self.selection_callback,
                     on_release=self.dismiss)
            self.grid.add_widget(btn)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.searchbtn = Button(
            text='Search',
            font_size='40dp',
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(.4, .1)
        )
        self.searchbtn.bind(on_release=self.search)
        self.add_widget(self.searchbtn)

        self.clipbtn = Button(
            text='Read Clipboard',
            font_size='40dp',
            pos_hint={'center_x': .5, 'center_y': .4},
            size_hint=(.4, .1)
        )
        self.clipbtn.bind(on_release=self.readclip)
        self.add_widget(self.clipbtn)

        self.txt = TextInput(
            text="",
            font_size='40dp',
            pos_hint={'center_x': .5, 'center_y': .8},
            size_hint=(.8, .2)
        )
        self.add_widget(self.txt)

    def search(self, event):
        self.app.modal.search_param = wikipedia.search(
                                        str(self.txt.text))
        
        self.app.modal.open()

    def readclip(self, event):
        content = Clipboard.paste().replace('\n', ' ').split(' ')
        self.app.clip_set_content(content)


class ReaderScreen(Screen):
    content=ListProperty([])
    paused=BooleanProperty(True)
    pos_in_text=NumericProperty(0)
    def on_enter(self):
        self.paused = True

    def __init__(self, **kwargs):
        # test
        # with open('./testdata.txt', 'r', encoding='utf-8') as f:
        #     self.content = eval(f.read())
        if platform == 'android':
            slider_cursor_size = (200, 200)
        else:
            slider_cursor_size = (80, 80)
        super(ReaderScreen, self).__init__(**kwargs)

        self.resetbtn = Button(
            text="Reset",
            font_size='40dp',
            pos_hint={'center_x':.2, 'center_y':.1},
            size_hint=(.3, .1))
        self.resetbtn.bind(on_press=self.reset)
        self.add_widget(self.resetbtn)

        self.text_label = Label(
            text="",
            font_size='45dp',
            pos_hint={'center_x':.5, 'center_y':.7},
            size_hint=(.1, 1)
            )
        self.add_widget(self.text_label)

        self.stopbtn = Button(
            text="Exit",
            font_size='40dp',
            pos_hint={'center_x':.8, 'center_y':.1},
            size_hint=(.3, .1),
        )
        self.stopbtn.bind(on_press=self.stop)
        self.add_widget(self.stopbtn)

        self.gobackbtn = Button(
            text="<<",
            font_size='60dp',
            pos_hint={'center_x': .1, 'center_y': .45},
            size_hint=(.1, .1)
        )
        self.add_widget(self.gobackbtn)

        self.fontslider = Slider(
            orientation='horizontal',
            step=1,
            value=55,
            range=(10, 100),
            pos_hint={'center_x': .5, 'center_y': .35},
            cursor_size=slider_cursor_size,
            size_hint=(.9, .1)
        )
        self.add_widget(self.fontslider)

        self.speedslider = Slider(
            orientation='horizontal',
            step=.00001,
            value=.25,
            range=(.01, .47),
            pos_hint={'center_x': .5, 'center_y': .2},
            cursor_image="./img/bunny.png",
            cursor_size=slider_cursor_size,
            size_hint=(.9, .1)
        )
        self.speedslider.defaultvalue=1
        self.add_widget(self.speedslider)

        self.wpm = Label(
            text='WPM - 240',
            pos_hint={'center_x': .5, 'center_y': .1},
            font_size='40dp',
            size_hint=(.1, .1)
        )
        self.add_widget(self.wpm)

    def reset(self, event):
        self.pos_in_text = 0
        self.read_text(1)

    def reset_read(self):
        value = .5 - self.speedslider.value
        self.wpm.text = self.calc(value)
        if not self.paused:
            Clock.unschedule(self.read_text)
            Clock.schedule_interval(self.read_text, value)

    def calc(self, value):
        try:
            value = (1/value)* 60
            return "WPM - %s" % str(int(value))
        except ZeroDivisionError:
            return 'WPM -'

    def on_touch_up(self, touch):
        if self.speedslider.collide_point(*touch.pos):
            self.reset_read()
        elif self.fontslider.collide_point(*touch.pos):
            self.text_label.font_size = "%sdp" % self.fontslider.value
        elif self.gobackbtn.collide_point(*touch.pos):
            self.pos_in_text -= 10
            if self.pos_in_text < 0:
                self.pos_in_text = 0
            self.read_text(1)
        else:
            self.pause(1)
        return super().on_touch_up(touch)
    
    def pause(self, event):
        if self.paused:
            self.paused = False
            self.reset_read()
            
        else:
            self.paused = True
            Clock.unschedule(self.read_text)

    def stop(self, event):
        self.remove_widget(self.startbtn)
        self.add_widget(self.startbtn)
        self.text_label.text = ''
        Clock.unschedule(self.read_text)
        sm.current = 'main'

    def read_text(self, dt):
        try:
            self.text_label.text = self.content[self.pos_in_text]
            self.pos_in_text += 1
        except IndexError:
            self.text_label.text = '...'
            Clock.unschedule(self.read_text)
        


class WikiApp(App):
    def __init__(self, **kwargs):
        super(WikiApp, self).__init__(**kwargs)
        self.modal = SelectModal(self.selection_callback)

    def build(self):
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ReaderScreen(name='reader'))
        
        return sm
    
    def set_content(self, event):
        reader = sm.get_screen('reader')
        reader.pos_in_text=0
        reader.content = (
            (wikipedia.page(
            event.parent.parent.parent.search_param[event.num]).content).split())
    
    def clip_set_content(self, content):
        reader = sm.get_screen('reader')
        reader.pos_in_text = 0
        reader.content = content
        sm.current = 'reader'

    def selection_callback(self, event):
        try:
            self.set_content(event)
            sm.current='reader'
        except wikipedia.DisambiguationError as e:
            self.layermodal = SelectModal(self.selection_callback)
            self.layermodal.search_param = e.options
            self.layermodal.open()

if __name__ == "__main__":
    WikiApp().run()