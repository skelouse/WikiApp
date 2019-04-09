import wikipedia
import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


class SelectBtn(Button):
    def __init__(self, **kwargs):
        super(SelectBtn, self).__init__(**kwargs)
        self.font_size = '40dp'
        self.size_hint_x = None
        self.height = Window.height/4.0
        self.width = Window.width/1.22

class SelectSearch(Popup):
    def __init__(self, search_param=0,
                 _parent=0, a=0, **kwargs):
        super(SelectSearch, self).__init__(**kwargs)
        self._parent = _parent
        self.title = 'Select an option'
        self.layout = ScrollView(
            scroll_type=['bars'],
            bar_width='80dp',
            size=(Window.width, Window.height),
            pos_hint={'center_x': .5},
            bar_color=([.81, .55, .55, 1]),  #
            bar_inactive_color=([.55, .17, .17, 1]))  #)
        
        self.grid = GridLayout(
            size_hint=(None, 2),
            cols=1
        )
        self.search_param = search_param
        for i in search_param:
            self.btn = SelectBtn()
            self.btn.text = i
            self.btn.bind(on_press=self.callback)
            self.grid.add_widget(self.btn)

        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)
    
    def callback(self, event):
        self.dismiss()
        self._parent.search(event.text, self.search_param)
        




class SearchG(Screen):
    def __init__(self, **kwargs):
        super(SearchG, self).__init__(**kwargs)
        self.wait_time = 0.3
        self.pos_in_text = 0
        self.paused = False

        self.searchbtn = Button(text="Search",
                          font_size='40dp',
                          pos_hint={'center_x':.5, 'center_y':.5},
                          size_hint=(None, None),
                          size=(Window.width/4, Window.height/6))
        self.searchbtn.bind(on_press=self.search1)
        self.add_widget(self.searchbtn)

        self.upspeedbtn = Button(text="+",
                          font_size='80dp',
                          pos_hint={'center_x':.9, 'center_y':.9},
                          size_hint=(None, None),
                          size=(Window.width/8, Window.height/8))
        self.upspeedbtn.bind(on_press=self.upspeed)
        #self.add_widget(self.upspeedbtn)

        self.downspeedbtn = Button(text="-",
                          font_size='80dp',
                          pos_hint={'center_x':.9, 'center_y':.75},
                          size_hint=(None, None),
                          size=(Window.width/8, Window.height/8))
        self.downspeedbtn.bind(on_press=self.downspeed)
        #self.add_widget(self.downspeedbtn)

        self.pausebtn = Button(text="Pause",
                          font_size='40dp',
                          pos_hint={'center_x':.2, 'center_y':.1},
                          size_hint=(None, None),
                          size=(Window.width/4, Window.height/6))
        self.pausebtn.bind(on_press=self.pause)
        #self.add_widget(self.pausebtn)

        self.txt = TextInput(text="",
                          font_size='40dp',
                          pos_hint={'center_x':.5, 'center_y':.8},
                          size_hint=(None, None),
                          size=(Window.width/4, Window.height/6))
        self.add_widget(self.txt)
        self.text_label = Label(text="",
                          font_size='80dp',
                          pos_hint={'center_x':.5, 'center_y':.5},
                          size_hint=(None, None),
                          size=(Window.width/4, Window.height/6))

        self.stopbtn = Button(text="Stop",
                          font_size='40dp',
                          pos_hint={'center_x':.8, 'center_y':.1},
                          size_hint=(None, None),
                          size=(Window.width/4, Window.height/6))
        self.stopbtn.bind(on_press=self.stop)


    def search1(self, event):
        a = wikipedia.search(str(self.txt.text))
        popup = SelectSearch(a, self)
        popup.open()

        
    def search(self, position, a):
        self.content = ((wikipedia.page(a[a.index(position)]).content).split())

        if self.pos_in_text == 0:
            self.remove_widget(self.searchbtn)
            self.remove_widget(self.txt)
            self.remove_widget(self.downspeedbtn)
            self.remove_widget(self.upspeedbtn)
            self.remove_widget(self.pausebtn)
            self.remove_widget(self.stopbtn)
            self.add_widget(self.downspeedbtn)
            self.add_widget(self.upspeedbtn)
            self.add_widget(self.pausebtn)
            self.add_widget(self.text_label)
            self.add_widget(self.stopbtn)
        Clock.unschedule(self.read_text)
        Clock.schedule_interval(self.read_text, self.wait_time)

    def read_text(self, dt):
        self.text_label.text = self.content[self.pos_in_text]
        self.pos_in_text += 1

    def upspeed(self ,event):
        self.wait_time -= .05
        self.search(1)

    def downspeed(self, event):
        self.wait_time += .05
        self.search(1)

    def pause(self, event):
        if self.paused:
            Clock.schedule_interval(self.read_text, self.wait_time)
            self.paused = False
        else:
            self.paused = True
            Clock.unschedule(self.read_text)

    def stop(self, event):
        self.remove_widget(self.searchbtn)
        self.remove_widget(self.txt)
        self.remove_widget(self.downspeedbtn)
        self.remove_widget(self.upspeedbtn)
        self.remove_widget(self.pausebtn)
        self.remove_widget(self.stopbtn)
        self.remove_widget(self.text_label)
        self.add_widget(self.searchbtn)
        self.add_widget(self.txt)
        self.pos_in_text = 0
        Clock.unschedule(self.read_text)


class WikiApp(App):
    def __init__(self, **kwargs):
        super(WikiApp, self).__init__(**kwargs)
    def build(self):
        sm.add_widget(SearchG(name='search'))
        return sm


sm = ScreenManager(transition=NoTransition())


if __name__ == ("__main__"):
    WikiApp().run()



