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
<Welcomescreen>:
    name: 'welcome'
    MDLabel:
        text: 'Your own desi hearing aid'
        halign: 'center'
        color: 0.204, 0.204, 0.204, 0.204, 1
        pos_hint: {'center_x':0.5, 'center_y': 0.8}
        font_size: 50
        font_name: 'Comic'
    MDFillRoundFlatIconButton:
        text: 'Welcome to Desibel'
        pos_hint: {'center_x':0.5, 'center_y': 0.2}
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
                text: 'Graph->'
                pos_hint: {'center_x':0.4, 'center_y':0.1}
                on_press: root.plotting(root.frequencies,root.db_levels)

        BoxLayout:
            orientation: 'vertical'
            Button:
                text: "I can hear"
                size: root.width, root.height
                on_press: root.can_hear(root.frequencies,root.db_levels)

            Button:
                text: "Barely hear"
                size: root.width, root.height
                on_press: root.barely_hear(root.frequencies,root.db_levels)
            Button:
                text: "Cannot hear"
                size: root.width, root.height
                on_press: root.cannot_hear(root.frequencies,root.db_levels)

         

"""

class Welcomescreen(Screen):
    pass
class Profilescreen(Screen):
    pass

class Mylayout(Screen):
    frequencies=250
    db_levels=5
    def play_sounds(self,frequenies,db_levels):
        p = pyaudio.PyAudio()
        # Define the duration for each frequency (in seconds)
        duration = 1
        # Function to play sounds
        def play_sound(dt):
                # Calculate the amplitude based on the dB level
            amplitude = 10 ** (db_levels / 10.0)

                    # Generate the sine wave for the current frequency with the specified amplitude
            t = np.linspace(0, duration, int(44100 * duration), endpoint=False)
            signal = amplitude * np.sin(2 * np.pi * frequenies * t)

                 # Open an audio output stream
            self.stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
            self.stream.start_stream()

                    # Write the signal to the stream and wait for the duration
            self.stream.write(signal.tobytes())
            time.sleep(duration)

                    # Stop and close the stream
            self.stream.stop_stream()
            self.stream.close()

        Clock.schedule_once(play_sound)  # Schedule sound generation for the next frame

        # Terminate the PyAudio instance
        p.terminate()
    def can_hear(self,frequencies,db_levels):
        db_levels=db_levels-5
        self.play_sounds(frequencies,db_levels)
    def cannot_hear(self,frequencies,db_levels):
        db_levels=db_levels+5
        self.play_sounds(frequencies,db_levels)
    def barely_hear(self,frequencies,db_levels):
        db_levels=0
        frequencies=frequencies*2
        return frequencies,db_levels
    def plotting(self,frequencies,db_levels):
        fig, ax = plt.subplots()
        ax.plot(frequencies, db_levels)
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Decibels (dB)')
        ax.set_title('Audiogram')
        plt.show()
class Myscreenmanager(ScreenManager):
    pass


class DesibelApp(MDApp):
    def build(self):
        sm= Myscreenmanager()
        sm.add_widget(Welcomescreen(name='welcome'))
        sm.add_widget(Profilescreen(name='profile'))
        sm.add_widget(Mylayout(name='layout'))
        p=pyaudio.PyAudio()
        scr=Builder.load_string(screen_helper)
        return scr
DesibelApp().run()