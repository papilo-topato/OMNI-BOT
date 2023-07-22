from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


class FlamesApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        Window.clearcolor = (1, 0.9, 0.9, 1)  # Set the window background color to a romantic color

        title_label = Label(text='FLAMES', font_size='40sp', color=(1, 0, 0.5, 1), bold=True, size_hint=(1, None),
                            height=100)  # Set the title label with compelling style
        layout.add_widget(title_label)

        scroll_view = ScrollView()
        inner_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll_view.add_widget(inner_layout)
        layout.add_widget(scroll_view)

        label_name1 = Label(text='Your Name:', font_size='30sp', color=(1, 0, 0, 1), bold=True)  # Set label style
        inner_layout.add_widget(label_name1)
        self.input_name1 = TextInput(multiline=False, font_size='30sp')
        self.input_name1.bind(on_text_validate=self.on_enter_name1)  # Bind Enter key to move to name2 input
        inner_layout.add_widget(self.input_name1)

        label_name2 = Label(text='Other Person Name:', font_size='30sp', color=(1, 0, 0, 1), bold=True)  # Set label style
        inner_layout.add_widget(label_name2)
        self.input_name2 = TextInput(multiline=False, font_size='30sp')
        self.input_name2.bind(on_text_validate=self.calculate_flames)  # Bind Enter key to calculate_flames method
        inner_layout.add_widget(self.input_name2)

        button_calculate = Button(text='Calculate', font_size='30sp', background_color=(0.2, 0.6, 0.8, 1))
        button_calculate.bind(on_release=self.calculate_flames)
        inner_layout.add_widget(button_calculate)

        self.result_label = Label(text='', font_size='36sp', color=(1, 0, 0, 1), bold=True)  # Set label style
        inner_layout.add_widget(self.result_label)

        return layout

    def on_enter_name1(self, instance):
        self.input_name2.focus = True  # Move the cursor to the name2 input field

    def calculate_flames(self, instance):
        name1 = self.input_name1.text
        name2 = self.input_name2.text

        # Removing spaces and converting names to lowercase
        name1 = name1.replace(" ", "").lower()
        name2 = name2.replace(" ", "").lower()

        # FLAMES calculation logic
        common_chars = set(name1) & set(name2)
        remaining_count = len(name1) + len(name2) - 2 * len(common_chars)

        flames = ["Friends", "Lovers", "Admirers", "Married", "Enemies", "Siblings"]
        result = flames[remaining_count % len(flames)]

        # Display the result
        self.result_label.text = f"Your relationship with the other person is:\n{result}"


if __name__ == '__main__':
    FlamesApp().run()
