import pyinputplus
from tkinter import *
from translate import Translator
import PyPDF2
import tkinter as tk
import requests
import time
import configparser
from base64 import b64decode
import webbrowser
import openai
from openai.error import InvalidRequestError
import subprocess


class OmniBotApp:
    def __init__(self):
        self.screen = Tk()
        self.screen.title("OMNI-BOT")
        self.screen.configure(bg="lightgray")

        # Language Translator
        self.LanguageChoices = ['Hindi', 'English', 'French', 'German', 'Spanish', 'Kannada', 'Telugu']
        self.InputLanguageChoice = StringVar()
        self.TranslateLanguageChoice = StringVar()

        self.InputLanguageChoice.set('English')
        self.TranslateLanguageChoice.set('Telugu')

        # Calculator
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        # Text-to-Image Generation
        self.image_prompt = StringVar()

        # Weather App
        self.weather_city = StringVar()

        # PDF Toolkit
        self.pdf_file_path = StringVar()

        # Create GUI
        self.create_gui()

    def create_gui(self):
        # Language Translator GUI
        language_translator_frame = Frame(self.screen, bg="lightgray")
        language_translator_frame.pack(padx=10, pady=10)

        language_translator_label = Label(language_translator_frame, text="Language Translator", bg="lightgray", font=('Arial', 16, 'bold'))
        language_translator_label.pack(pady=10)

        input_language_label = Label(language_translator_frame, text="Choose Input Language", bg="lightgray", font=('Arial', 14))
        input_language_label.pack(pady=5)

        input_language_menu = OptionMenu(language_translator_frame, self.InputLanguageChoice, *self.LanguageChoices)
        input_language_menu.config(font=('Arial', 12))
        input_language_menu.pack(pady=5)

        translate_language_label = Label(language_translator_frame, text="Choose Translated Language", bg="lightgray", font=('Arial', 14))
        translate_language_label.pack(pady=5)

        translate_language_menu = OptionMenu(language_translator_frame, self.TranslateLanguageChoice, *self.LanguageChoices)
        translate_language_menu.config(font=('Arial', 12))
        translate_language_menu.pack(pady=5)

        text_label = Label(language_translator_frame, text="Enter Text", bg="lightgray", font=('Arial', 14))
        text_label.pack(pady=5)

        text_entry = Entry(language_translator_frame, font=('Arial', 12))
        text_entry.pack(pady=5)

        translate_button = Button(language_translator_frame, text="Translate", command=self.translate, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        translate_button.pack(pady=10)

        # Calculator GUI
        calculator_frame = Frame(self.screen, bg="lightgray")
        calculator_frame.pack(padx=10, pady=10)

        calculator_label = Label(calculator_frame, text="Calculator", bg="lightgray", font=('Arial', 16, 'bold'))
        calculator_label.pack(pady=10)

        self.solution = Entry(calculator_frame, background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), font_size=48, multiline=False)
        self.solution.pack(pady=10)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "+"],
            [".", "0", "C", "-"],
        ]

        for row in buttons:
            h_layout = Frame(calculator_frame, bg="lightgray")
            h_layout.pack()
            for label in row:
                button = Button(
                    h_layout, text=label, font_size=30, background_color=(0.5, 0.5, 0.5, 1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
                button.bind(on_press=self.on_button_press)
                button.pack(side=LEFT, padx=5, pady=5)

        equal_button = Button(
            calculator_frame, text="=", font_size=30, background_color=(1, 0, 0, 1),  # Red color for equals button
            background_normal="", background_down="button_pressed.png",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equal_button.bind(on_press=self.on_solution)
        equal_button.pack(pady=10)

        # Text-to-Image Generation GUI
        text_to_image_frame = Frame(self.screen, bg="lightgray")
        text_to_image_frame.pack(padx=10, pady=10)

        text_to_image_label = Label(text_to_image_frame, text="Text-to-Image Generation", bg="lightgray", font=('Arial', 16, 'bold'))
        text_to_image_label.pack(pady=10)

        image_prompt_label = Label(text_to_image_frame, text="Enter Image Prompt", bg="lightgray", font=('Arial', 14))
        image_prompt_label.pack(pady=5)

        image_prompt_entry = Entry(text_to_image_frame, font=('Arial', 12), textvariable=self.image_prompt)
        image_prompt_entry.pack(pady=5)

        generate_image_button = Button(text_to_image_frame, text="Generate Image", command=self.generate_image, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        generate_image_button.pack(pady=10)

        # Weather App GUI
        weather_app_frame = Frame(self.screen, bg="lightgray")
        weather_app_frame.pack(padx=10, pady=10)

        weather_app_label = Label(weather_app_frame, text="Weather App", bg="lightgray", font=('Arial', 16, 'bold'))
        weather_app_label.pack(pady=10)

        city_label = Label(weather_app_frame, text="Enter City", bg="lightgray", font=('Arial', 14))
        city_label.pack(pady=5)

        city_entry = Entry(weather_app_frame, font=('Arial', 12), textvariable=self.weather_city)
        city_entry.pack(pady=5)

        get_weather_button = Button(weather_app_frame, text="Get Weather", command=self.get_weather, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        get_weather_button.pack(pady=10)

        # PDF Toolkit GUI
        pdf_toolkit_frame = Frame(self.screen, bg="lightgray")
        pdf_toolkit_frame.pack(padx=10, pady=10)

        pdf_toolkit_label = Label(pdf_toolkit_frame, text="PDF Toolkit", bg="lightgray", font=('Arial', 16, 'bold'))
        pdf_toolkit_label.pack(pady=10)

        extract_text_button = Button(pdf_toolkit_frame, text="Extract Text", command=self.extract_text, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        extract_text_button.pack(pady=5)

        merge_pdfs_button = Button(pdf_toolkit_frame, text="Merge PDFs", command=self.merge_pdfs, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        merge_pdfs_button.pack(pady=5)

        identify_page_numbers_button = Button(pdf_toolkit_frame, text="Identify Page Numbers", command=self.identify_page_numbers, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        identify_page_numbers_button.pack(pady=5)

        extract_images_button = Button(pdf_toolkit_frame, text="Extract Images", command=self.extract_images, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        extract_images_button.pack(pady=5)

        split_pdf_button = Button(pdf_toolkit_frame, text="Split PDF", command=self.split_pdf, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        split_pdf_button.pack(pady=5)

        rotate_pdf_button = Button(pdf_toolkit_frame, text="Rotate PDF", command=self.rotate_pdf, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        rotate_pdf_button.pack(pady=5)

        encrypt_pdf_button = Button(pdf_toolkit_frame, text="Encrypt PDF", command=self.encrypt_pdf, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
        encrypt_pdf_button.pack(pady=5)

        self.screen.mainloop()

    def translate(self):
        input_text = pyinputplus.inputStr("Enter Text: ")
        input_language = self.InputLanguageChoice.get().lower()
        translate_language = self.TranslateLanguageChoice.get().lower()

        translator = Translator(from_lang=input_language, to_lang=translate_language)
        translation = translator.translate(input_text)

        messagebox.showinfo("Translation", translation)

    def on_button_press(self, instance):
        current_button = instance.text
        text = self.solution.text

        if current_button == "C":
            self.solution.text = ""
        else:
            if text and (self.last_button in self.operators and current_button in self.operators):
                return
            elif text == "" and current_button in self.operators:
                return
            elif text and self.last_button == "." and current_button == ".":
                return
            else:
                new_text = text + current_button
                self.solution.text = new_text

        self.last_button = current_button
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(self.solution.text))
                self.solution.text = solution
            except:
                self.solution.text = "Error"

    def generate_image(self):
        prompt = self.image_prompt.get()
        try:
            images = []
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size='512x512',
                response_format='url'
            )
            for image in response['data']:
                images.append(image.url)
            for image in images:
                webbrowser.open(image)
        except InvalidRequestError as e:
            print(e)

    def get_weather(self):
        city = self.weather_city.get()
        api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=06c921750b9a82d8f5d1294e1586276f"

        json_data = requests.get(api).json()
        if json_data.get('cod') != 200:
            messagebox.showerror("Invalid City Name", "Please enter a valid city name.")
            return

        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S %p', time.gmtime(json_data['sys']['sunrise'] - 21600))
        sunset = time.strftime('%I:%M:%S %p', time.gmtime(json_data['sys']['sunset'] - 21600))

        final_info = f"Weather Condition: {condition}\nTemperature: {temp}°C"
        final_data = f"Min Temperature: {min_temp}°C\nMax Temperature: {max_temp}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nWind Speed: {wind} m/s\nSunrise: {sunrise}\nSunset: {sunset}"

        messagebox.showinfo("Weather Information", final_info + "\n\n" + final_data)

    def extract_text(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            pdf_file.close()

            temp_file = 'temp.txt'
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(text)

            subprocess.Popen(['notepad.exe', temp_file])

            messagebox.showinfo('Text Extraction', 'Text extracted successfully!')

    def merge_pdfs(self):
        pdf_paths = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])
        if pdf_paths:
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if output_path:
                pdf_merger = PyPDF2.PdfMerger()
                for pdf_path in pdf_paths:
                    pdf_merger.append(pdf_path)
                with open(output_path, 'wb') as output_file:
                    pdf_merger.write(output_file)
                messagebox.showinfo('PDF Merge', 'PDFs merged successfully!')
            else:
                messagebox.showwarning('Output File Not Selected', 'PDF merge canceled. No output file selected.')

    def identify_page_numbers(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_numbers = ', '.join([str(page + 1) for page in range(len(pdf_reader.pages))])
            messagebox.showinfo('Page Numbers', f'The PDF has the following page numbers:\n{page_numbers}')
            pdf_file.close()

    def extract_images(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            image_count = 0
            for page in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page]
                if '/XObject' in page_obj['/Resources']:
                    x_object = page_obj['/Resources']['/XObject'].get_object()
                    for obj in x_object:
                        if x_object[obj]['/Subtype'] == '/Image':
                            image_count += 1
            messagebox.showinfo('Image Extraction', f'The PDF contains {image_count} image(s).')
            pdf_file.close()

    def split_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            output_folder = filedialog.askdirectory()
            if output_folder:
                for page in range(len(pdf_reader.pages)):
                    pdf_writer = PyPDF2.PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[page])
                    output_path = f'{output_folder}/page_{page + 1}.pdf'
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                messagebox.showinfo('PDF Split', 'PDF split successfully!')
            else:
                messagebox.showwarning('Output Folder Not Selected', 'PDF split canceled. No output folder selected.')

    def rotate_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            rotation_angle = askinteger("Rotation Angle", "Enter the rotation angle (90, 180, or 270 degrees):",
                                        minvalue=1, maxvalue=360)

            if rotation_angle not in [90, 180, 270]:
                messagebox.showerror('Invalid Rotation Angle', 'Please enter a valid rotation angle (90, 180, or 270 degrees).')
                return

            for page in range(len(pdf_reader.pages)):
                rotated_page = pdf_reader.pages[page].rotate(rotation_angle)
                pdf_writer.add_page(rotated_page)

            output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if output_path:
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                messagebox.showinfo('PDF Rotation', 'PDF rotated successfully!')

    def encrypt_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if pdf_path:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            password = askstring('Encrypt PDF', 'Enter password:')
            if password is None or password.strip() == '':
                messagebox.showerror('Invalid Password', 'Please enter a valid password.')
                return

            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

            pdf_writer.encrypt(password)
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if output_path:
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                messagebox.showinfo('PDF Encryption', 'PDF encrypted successfully!')


if __name__ == '__main__':
    OmniBotApp()
