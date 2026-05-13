import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import google.generativeai as genai

# UI Theme: Royal Black & Cyan
Window.clearcolor = (0, 0, 0, 1)

class JarvisApp(App):
    def build(self):
        # API CONFIGURATION
        GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=GEMINI_KEY)
        
        # --- FIXED MODEL INITIALIZATION ---
        # "models/" prefix is mandatory to avoid 404
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header: JARVIS OMNI-ENGINE
        self.header = Label(
            text="[b][color=00d4ff]JARVIS OMNI-ENGINE V64[/color][/b]",
            markup=True, font_size='24sp', size_hint_y=0.1
        )
        self.layout.add_widget(self.header)

        # Chat Window
        self.scroll = ScrollView(size_hint_y=0.6)
        self.output = Label(
            text="Neural Link Active. Ready for your command, Sir.",
            text_size=(Window.width - 40, None),
            halign='left', valign='top',
            color=(0, 0.83, 1, 1),
            markup=True
        )
        self.output.bind(texture_size=self.output.setter('size'))
        self.scroll.add_widget(self.output)
        self.layout.add_widget(self.scroll)

        # User Input Field
        self.user_input = TextInput(
            hint_text="Ask me anything, Sir...",
            multiline=False, size_hint_y=0.1,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.83, 1, 1)
        )
        self.layout.add_widget(self.user_input)

        # Action Button
        self.btn = Button(
            text="ACTIVATE BRAIN LINK", 
            size_hint_y=0.15,
            background_color=(0, 0.5, 0.7, 1),
            font_size='18sp',
            bold=True
        )
        self.btn.bind(on_press=self.process_command)
        self.layout.add_widget(self.btn)

        return self.layout

    def process_command(self, instance):
        query = self.user_input.text
        if query:
            self.output.text += f"\n\n[color=ffffff][You]:[/color] {query}"
            self.user_input.text = ""
            
            try:
                # Character Roleplay for Dilansh Jain
                response = self.model.generate_content(
                    f"System: JARVIS. Owner: Dilansh Jain. Instruction: Respond as a royal AI. Query: {query}"
                )
                self.output.text += f"\n\n[color=00d4ff][Jarvis]:[/color] {response.text}"
            except Exception as e:
                # Error Handling to prevent crash
                self.output.text += f"\n\n[color=ff4444][System Error]:[/color] Sir, the link failed: {str(e)}"

if __name__ == "__main__":
    JarvisApp().run()
