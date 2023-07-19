import tkinter as tk
import requests
import time

def get_weather(event=None):
    city = textField.get()
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=06c921750b9a82d8f5d1294e1586276f"

    json_data = requests.get(api).json()
    if json_data.get('cod') != 200:
        label1.config(text="Invalid city name", font=f, fg='red')
        label2.config(text="", font=f)
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

    label1.config(text=final_info, font=f, fg='black')
    label2.config(text=final_data, font=f, fg='black')

def on_entry_click(event):
    if textField.get() == "Enter place":
        textField.delete(0, "end")
        textField.config(fg='black')

def on_focus_out(event):
    if textField.get() == "":
        textField.insert(0, "Enter place")
        textField.config(fg='gray')

def on_key_press(event):
    if event.keysym == "Return":
        get_weather()
    elif event.keysym == "Up":
        auto_label.focus()
        auto_label.event_generate("<Up>")
    elif event.keysym == "Down":
        auto_label.focus()
        auto_label.event_generate("<Down>")
    else:
        city = textField.get()
        if len(city) >= 3:
            suggestions = []
            for suggestion in cities_list:
                if city.lower() in suggestion.lower():
                    suggestions.append(suggestion)

            auto_label.delete(0, "end")
            for suggestion in suggestions:
                auto_label.insert("end", suggestion)
                auto_label.insert("end", "\n")
            auto_label.focus_set()

def on_suggestion_select(event):
    index = auto_label.curselection()
    if index:
        selected_city = auto_label.get(index)
        textField.delete(0, "end")
        textField.insert("end", selected_city)
        get_weather()

def on_suggestion_scroll(event):
    if event.num == 4:
        auto_label.yview_scroll(-1, "units")
    elif event.num == 5:
        auto_label.yview_scroll(1, "units")

canvas = tk.Tk()
canvas.geometry("600x500")
canvas.title("Weather App")
canvas.configure(bg='light blue')
f = ("Arial", 14)
t = ("Arial", 24, "bold")

textField = tk.Entry(canvas, justify='center', width=20, font=t)
textField.pack(pady=20)
textField.insert(0, "Enter place")
textField.config(fg='gray', bg='white')
textField.bind('<FocusIn>', on_entry_click)
textField.bind('<FocusOut>', on_focus_out)
textField.bind('<KeyRelease>', on_key_press)

get_weather_button = tk.Button(canvas, text="Get Weather", font=f, command=get_weather, bg='#ffff00', fg='black', height=2, width=15)
get_weather_button.pack()

label1 = tk.Label(canvas, font=f, bg='light blue')
label1.pack(pady=20)
label2 = tk.Label(canvas, font=f, bg='light blue')
label2.pack()

cities_list = [
    "London", "New York", "Paris", "Tokyo", "Sydney", "Los Angeles", "Berlin", "Rome", "Barcelona", "Toronto",
    "Amsterdam", "Vienna", "Athens", "Cairo", "Dubai", "Moscow", "Bangkok", "Singapore", "Seoul", "Beijing",
    "Shanghai", "Hong Kong", "Mumbai", "Delhi", "Rio de Janeiro", "Buenos Aires", "Mexico City", "Cape Town",
    "Johannesburg", "Nairobi", "Riyadh", "Dublin", "Edinburgh", "Stockholm", "Oslo", "Copenhagen", "Helsinki",
    "Warsaw", "Prague", "Budapest", "Lisbon", "Madrid", "Milan", "Zurich", "Geneva", "Brussels", "Lyon", "Munich",
    "Frankfurt", "Amman", "Jerusalem", "Istanbul", "Lima", "Santiago", "Bogota", "Caracas", "Quito", "La Paz",
    "Havana", "San Juan", "San Francisco", "Chicago", "Miami", "Boston", "Seattle", "Melbourne", "Vancouver",
    "Montreal", "Dublin", "Barcelona", "Amsterdam", "Prague", "Vienna", "Stockholm", "Athens", "Cairo", "Cape Town",
    "Nairobi", "Marrakech", "Zurich", "Helsinki", "Dubai", "Kuala Lumpur", "Bangkok", "Tokyo", "Seoul", "Beijing",
    "Shanghai", "Hong Kong", "Jaipur", "Kolkata", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad", "Pune", "Surat",
    "Kochi", "Varanasi", "Agra", "Goa", "Amritsar", "Udaipur", "Mysore", "Lucknow", "Ooty", "Shimla", "Srinagar",
    "Rishikesh"
]


auto_label = tk.Listbox(canvas, font=f, bg='white', fg='black', selectbackground='gray', selectforeground='white')
auto_label.pack()
auto_label.bind("<<ListboxSelect>>", on_suggestion_select)
auto_label.bind("<Button-4>", on_suggestion_scroll)
auto_label.bind("<Button-5>", on_suggestion_scroll)

canvas.bind("<Return>", on_key_press)
canvas.mainloop()
