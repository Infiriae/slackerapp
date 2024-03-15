import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

Builder.load_string('''
<Button@Button>:
    font_size: 18
    background_color: (.4, .4, .4, 8)
    color: (.5, .5, 1, 1)
    size_hint: (1, 0.1)

<TextInput@TextInput>:
    hint_text: 'Enter text here'
    size_hint: (1, 0.3)
    multiline: True
    padding: 10, 10
    font_size: 14
    background_color: (0.9, 0.9, 0.9, 1)
    foreground_color: (0, 0, 0, 1)
''')

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.name = "menu"
        
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)
        
        self.button_layout = BoxLayout(orientation='horizontal')
        layout.add_widget(self.button_layout)
        
        self.button1 = Button(text='Gem')
        self.button1.bind(on_press=self.GoToGem)
        self.button_layout.add_widget(self.button1)
        
        self.button2 = Button(text='Quit')
        self.button2.bind(on_press=self.exit_app)
        self.button_layout.add_widget(self.button2)

        self.button3 = Button(text='Namelist')
        self.button3.bind(on_press=self.namelist)
        self.button_layout.add_widget(self.button3)
        
    def GoToGem(self, instance):
        self.manager.current = "Gem"

    def namelist(self, instance):
        screen_names = [self.manager.current_screen.__getattribute__]
        print(screen_names)
    
    def exit_app(self, instance):
        App.get_running_app().stop()
        

class GemMenu(Screen):
    def __init__(self, **kwargs):
        super(GemMenu, self).__init__(**kwargs)
        self.name = "Gem"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)
        self.wacts = TextInput(hint_text='Actions')
        self.thoughts = TextInput(hint_text='Thoughts')
        layout.add_widget(self.wacts)
        layout.add_widget(self.thoughts)
        self.button = Button(text='Take Action')
        self.button.bind(on_press=self.send_json)
        layout.add_widget(self.button)
        self.back_button = Button(text='Back to Menu')
        self.back_button.bind(on_press=self.go_to_menu)
        layout.add_widget(self.back_button)

    def send_json(self, instance):
        url = 'https://hooks.slack.com/workflows/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'
        data = {"gem":self.wacts.text,"thoughts": self.thoughts.text}
        if data["gem"] == "" and data["thoughts"] == "":
            print("Please enter some information")
        else:
            response = requests.post(url, json=data)
            print(response.text)
            self.wacts.text = ""
            self.thoughts.text = ""

    def go_to_menu(self, instance):
        self.manager.current = "menu"

    def go_to_menu(self, instance):
        self.manager.current = "menu"

class SlackerApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GemMenu(name='Gem'))
        return sm

    def send_json(self, instance):
        url = 'https://hooks.slack.com/workflows/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'
        data = {"gem":self.wacts.text,"thoughts": self.thoughts.text}
        if data["gem"] == "" and data["thoughts"] == "":
            print("Please enter some information")
        else:
            response = requests.post(url, json=data)
            print(response.text)
            self.wacts.text = ""
            self.thoughts.text = ""

if __name__ == "__main__":
    app = SlackerApp()
    app.run()