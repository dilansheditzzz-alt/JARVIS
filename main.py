import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import google.generativeai as genai

# UI Colors - Royal Blue & Black Theme
Window.clearcolor = (0, 0, 0, 1)

class JarvisApp(App):
    def build(self):
        # API Configuration
        GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=GEMINI_KEY)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

        # Main Layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header
        self.header = Label(
            text="[b][color=00d4ff]JARVIS OMNI-ENGINE V64[/color][/b]",
            markup=True, font_size='24sp', size_hint_y=0.1
        )
        self.layout.add_widget(self.header)

        # Scrollable Chat Display
        self.scroll = ScrollView(size_hint_y=0.6)
        self.output = Label(
            text="System Online. Awaiting Command, Sir...",
            text_size=(Window.width - 40, None),
            halign='left', valign='top',
            color=(0, 0.83, 1, 1)
        )
        self.output.bind(texture_size=self.output.setter('size'))
        self.scroll.add_widget(self.output)
        self.layout.add_widget(self.scroll)

        # Input Box
        self.user_input = TextInput(
            hint_text="Enter Command, Sir...",
            multiline=False, size_hint_y=0.1,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.83, 1, 1)
        )
        self.layout.add_widget(self.user_input)

        # Brain Link Button
        self.btn = Button(
            text="BRAIN LINK", size_hint_y=0.15,
            background_color=(0, 0.6, 0.8, 1),
            font_weight='bold'
        )
        self.btn.bind(on_press=self.process_command)
        self.layout.add_widget(self.btn)

        return self.layout

    def process_command(self, instance):
        query = self.user_input.text
        if query:
            self.output.text += f"\n\n[You]: {query}"
            self.user_input.text = ""
            
            try:
                # Prompt Engineering for Jarvis Personality
                prompt = f"You are JARVIS. Owner: Dilansh Jain from Tonk. Task: {query}"
                response = self.model.generate_content(prompt)
                self.output.text += f"\n\n[Jarvis]: {response.text}"
            except Exception as e:
                self.output.text += f"\n\n[Error]: Sir, connection failed. {str(e)}"

if __name__ == "__main__":
    JarvisApp().run()
