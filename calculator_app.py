from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


class MainApp(App):
    def build(self):
        self.icon = "calculator.png"
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), font_size=48, multiline=False)
        main_layout.add_widget(self.solution)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "+"],
            [".", "0", "C", "-"],
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label, font_size=30, background_color=(0.5, 0.5, 0.5, 1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equal_button = Button(
            text="=", font_size=30, background_color=(1, 0, 0, 1),  # Red color for equals button
            background_normal="", background_down="button_pressed.png",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equal_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equal_button)

        Window.bind(on_keyboard=self.on_keyboard)  # Enable keyboard input
        self.history = TextInput(readonly=True, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1), font_size=18)
        main_layout.add_widget(self.history)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            self.solution.text = ""
        elif button_text == '.':
            if '.' not in current:
                new_text = current + button_text
                self.solution.text = new_text
        else:
            if current and (
                    self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(self.solution.text))
                self.solution.text = solution
                self.history.text += f"{text} = {solution}\n"  # Add calculation to history
            except ZeroDivisionError:
                self.solution.text = "Error: Division by zero"
            except Exception:
                self.solution.text = "Error: Invalid expression"

    def on_keyboard(self, window, key, *args):
        if key == 273:  # Up Arrow Key
            self.history.focus = True
            return True
        elif key == 274:  # Down Arrow Key
            self.history.focus = False
            self.solution.focus = True
            return True
        elif key == 13:  # Enter Key
            self.on_solution(None)
            return True
        elif chr(key) in self.operators:  # Operators
            self.solution.text += chr(key)
            return True
        elif chr(key) == '.':  # Decimal Point
            if '.' not in self.solution.text:
                self.solution.text += '.'
            return True
        elif chr(key) in [str(i) for i in range(10)]:  # Numbers 0-9
            self.solution.text += chr(key)
            return True
        elif key == 8:  # Backspace
            self.solution.text = self.solution.text[:-1]
            return True

    def on_start(self):
        Window.size = (400, 600)  # Initial window size


if __name__ == "__main__":
    app = MainApp()
    app.run()
