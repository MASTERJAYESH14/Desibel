from kivymd.app import MDApp #help in creating app
from kivymd.uix.button import MDFlatButton,MDFillRoundFlatIconButton,MDRectangleFlatButton
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.label import MDLabel, MDIcon
from kivy.lang.builder import Builder
from kivy.uix.scatterlayout import ScatterLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt


screen_helper="""
ScreenManager:
    Welcomescreen:
    Profilescreen:
    Mylayout:
    Graph:
<Welcomescreen>:
    name: 'welcome'
    background_color: 1,0,0,1
    MDLabel:
        text: 'Your own desi hearing aid'
        halign: 'center'
        pos_hint: {'center_x':0.5, 'center_y': 0.7}
        font_size: 50
        font_name: 'Arial'
    MDFillRoundFlatIconButton:
        text: 'Welcome to Desibel'
        pos_hint: {'center_x':0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'profile'

<Profilescreen>:
    name: 'profile'
    MDTextField:
        hint_text: 'Enter Username'
        helper_text_mode: 'on_focus'
        icon_right: 'android'
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size_hint: (0.2,0.2)
        width: 300
    MDFlatButton:
        text: 'proceed'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
        on_press: root.manager.current = 'layout'
<Mylayout>:
    name:'layout'
    GridLayout:
        cols:2
        size: root.width,root.height
        BoxLayout:
            size_hint_y: .8
            pos_hint: {"top":1}
            MDFillRoundFlatIconButton:
                text: 'Play sound'
                pos_hint: {'center_x':0.2, 'center_y':0.1}
                on_press: root.play_sounds()
            MDFillRoundFlatIconButton:
                text: 'Graph'
                pos_hint: {'center_x':0.5, 'center_y':0.1}
                on_press: root.manager.current = 'Graph'


        BoxLayout:
            orientation: 'vertical'
            Button:
                text: "I can hear"
                size: root.width, root.height
                on_press: root.can_hear()

            Button:
                text: "Barely hear"
                size: root.width, root.height
                on_press: root.barely_hear()
            Button:
                text: "Cannot hear"
                size: root.width, root.height
                on_press: root.cannot_hear()
<Graph>:
    name: 'Graph'
    MDFillRoundFlatIconButton:
        text: 'Back'
        pos_hint: {'center_x':0.5, 'center_y':0.1}
        on_press: root.manager.current = 'layout'

         

"""

class Welcomescreen(Screen):
    pass
class Profilescreen(Screen):
    pass

class Mylayout(Screen):
    frequencies=250
    db_levels=-5
    x=[]
    y=[]
    def play_sounds(self):
        p = pyaudio.PyAudio()

        # Define the duration for each frequency (in seconds)
        duration = 1
        # Function to play sounds
        def play_sound(dt):
            # Calculate the amplitude based on the dB level
            amplitude = 5 ** (self.db_levels / 10.0)
    
            # Generate the sine wave for the current frequency with the specified amplitude
            t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
            signal = amplitude * np.sin(2 * np.pi * self.frequencies * t)

            # Open an audio output stream
            self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
            self.stream.start_stream()

            # Write the signal to the stream 
            self.stream.write(signal.tobytes())
            time.sleep(duration)

                    # Stop and close the stream
            self.stream.stop_stream()
            self.stream.close()

        Clock.schedule_once(play_sound) 

        # Terminate the PyAudio instance
        p.terminate()
    # buttons integrated to functions
    def can_hear(self):
        self.db_levels=self.db_levels-5
        return(self.db_levels)
    def cannot_hear(self):
        self.db_levels=self.db_levels+5
        return(self.db_levels)
    
    def barely_hear(self):
        self.x.append(self.frequenices)
        self.y.append(self.db_levels)
        self.db_levels=5
        self.frequencies=self.frequencies*2
        return (self.frequencies,self.db_levels)
    
    
    #integrating button and graph
    def plotting(self):
        fig, ax = plt.subplots()
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Decibels (dB)')
        ax.set_title('Audiogram')
        plt.show()

class Graph(Screen):
        l=[]
        o=[]
        def plotting(self):
            self.l= Mylayout.x
            self.o=Mylayout.y
            plt.plot(self.o,self.l)
            plt.show()

#for changing screens
class Myscreenmanager(ScreenManager):
    pass


class DesibelApp(MDApp):
    def build(self):
        sm= Myscreenmanager()
        sm.add_widget(Welcomescreen(name='welcome'))
        sm.add_widget(Profilescreen(name='profile'))
        sm.add_widget(Mylayout(name='layout'))
        sm.add_widget(Mylayout(name='Graph'))
        p=pyaudio.PyAudio()
        scr=Builder.load_string(screen_helper)
        return scr
DesibelApp().run()

