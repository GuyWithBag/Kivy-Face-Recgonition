
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MainApp(App): 
    def build(self): 
        layout = BoxLayout(orientation="vertical")
        return layout
    
if __name__ == "__main__": 
    MainApp().run()