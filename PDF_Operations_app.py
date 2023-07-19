import PyPDF2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askinteger, askstring
import subprocess


# Create the main window
root = tk.Tk()
root.title("PDF Toolkit")
root.geometry("600x400")  # Set the window size

# Create a custom font with increased size
custom_font = ("Arial", 14)

# Define custom colors
background_color = "#D6EDFF"  # Light blue
button_color = "#3C8DBC"  # Dark blue
button_text_color = "#FFFFFF"  # White
label_text_color = "#000000"  # Black

# Configure window background color
root.configure(bg=background_color)

# Function to handle text extraction
def extract_text():
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if pdf_path:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_file.close()

        # Save the extracted text to a temporary file
        temp_file = 'temp.txt'
        with open(temp_file, 'w', encoding='utf-8') as file:
            file.write(text)

        # Open the temporary file in Notepad
        subprocess.Popen(['notepad.exe', temp_file])

        messagebox.showinfo('Text Extraction', 'Text extracted successfully!')

# Function to handle PDF merging
def merge_pdfs():
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

# Function to identify page numbers in a PDF
def identify_page_numbers():
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if pdf_path:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_numbers = ', '.join([str(page + 1) for page in range(len(pdf_reader.pages))])
        messagebox.showinfo('Page Numbers', f'The PDF has the following page numbers:\n{page_numbers}')
        pdf_file.close()

# Function to extract images from a PDF
def extract_images():
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

# Function to split a PDF
def split_pdf():
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

# Function to rotate a PDF
def rotate_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if pdf_path:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Prompt user to enter rotation angle using a dialog box
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

# Function to encrypt a PDF
def encrypt_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if pdf_path:
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Prompt user to enter password using a dialog box
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

# Create the widgets with custom font and colors
operation_label = tk.Label(root, text="Choose an operation:", font=custom_font, bg=background_color, fg=label_text_color)
operation_label.pack(pady=10)

button_frame = tk.Frame(root, bg=background_color)
button_frame.pack()

# Extract Text Button
extract_text_button = tk.Button(button_frame, text="Extract Text", command=extract_text, font=custom_font,
                                bg=button_color, fg=button_text_color)
extract_text_button.grid(row=0, column=0, padx=10, pady=10)

# Merge PDFs Button
merge_pdfs_button = tk.Button(button_frame, text="Merge PDFs", command=merge_pdfs, font=custom_font,
                              bg=button_color, fg=button_text_color)
merge_pdfs_button.grid(row=0, column=1, padx=10, pady=10)

# Identify Page Numbers Button
identify_page_numbers_button = tk.Button(button_frame, text="Identify Page Numbers", command=identify_page_numbers,
                                         font=custom_font, bg=button_color, fg=button_text_color)
identify_page_numbers_button.grid(row=0, column=2, padx=10, pady=10)

# Extract Images Button
extract_images_button = tk.Button(button_frame, text="Extract Images", command=extract_images, font=custom_font,
                                  bg=button_color, fg=button_text_color)
extract_images_button.grid(row=1, column=0, padx=10, pady=10)

# Split PDF Button
split_pdf_button = tk.Button(button_frame, text="Split PDF", command=split_pdf, font=custom_font,
                             bg=button_color, fg=button_text_color)
split_pdf_button.grid(row=1, column=1, padx=10, pady=10)

# Rotate PDF Button
rotate_pdf_button = tk.Button(button_frame, text="Rotate PDF", command=rotate_pdf, font=custom_font,
                              bg=button_color, fg=button_text_color)
rotate_pdf_button.grid(row=1, column=2, padx=10, pady=10)

# Encrypt PDF Button
encrypt_pdf_button = tk.Button(button_frame, text="Encrypt PDF", command=encrypt_pdf, font=custom_font,
                               bg=button_color, fg=button_text_color)
encrypt_pdf_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
