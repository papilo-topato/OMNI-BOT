import pyinputplus
from tkinter import *
from translate import Translator

screen = Tk()
screen.title("Language Translator with GUI by RAGHURAM K S")
screen.configure(bg="lightgray")

LanguageChoices = ['Hindi', 'English', 'French', 'German', 'Spanish', 'Kannada', 'Telugu']
InputLanguageChoice = StringVar()
TranslateLanguageChoice = StringVar()

InputLanguageChoice.set('English')
TranslateLanguageChoice.set('Telugu')

def translate():
    translator = Translator(from_lang=InputLanguageChoice.get(), to_lang=TranslateLanguageChoice.get())
    translation = translator.translate(TextVar.get())
    OutputVar.set(translation)

# Choice for input language
InputLanguageChoiceMenu = OptionMenu(screen, InputLanguageChoice, *LanguageChoices)
InputLanguageChoiceMenu.config(font=('Arial', 14))
Label(screen, text="Choose Input Language", bg="lightgray", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
InputLanguageChoiceMenu.grid(row=0, column=1, padx=10, pady=10)
 
# Choice for translated language
NewLanguageChoiceMenu = OptionMenu(screen, TranslateLanguageChoice, *LanguageChoices)
NewLanguageChoiceMenu.config(font=('Arial', 14))
Label(screen, text="Choose Translated Language", bg="lightgray", font=('Arial', 14)).grid(row=0, column=2, padx=10, pady=10)
NewLanguageChoiceMenu.grid(row=0, column=3, padx=10, pady=10)

Label(screen, text="Enter Text", bg="lightgray", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
TextVar = StringVar()
TextBox = Entry(screen, textvariable=TextVar, width=30, font=('Arial', 12))
TextBox.grid(row=1, column=1, padx=10, pady=10)
 
Label(screen, text="Translated Text", bg="lightgray", font=('Arial', 14)).grid(row=1, column=2, padx=10, pady=10)
OutputVar = StringVar()
TextBox = Entry(screen, textvariable=OutputVar, width=30, font=('Arial', 12))
TextBox.grid(row=1, column=3, padx=10, pady=10)
 
# Button for translation
B = Button(screen, text="Translate", command=translate, relief=GROOVE, font=('Arial', 14), bg='lightblue', fg='black')
B.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
 
mainloop()