from tkinter import *
import tkinter as tk
import webbrowser as wb
import re 
import requests
import json


exiting = ["quit", "exit"]

joke_words = ["joke", "funny"]

quotes = ["quotes", "quote"]

weather = ["weather"]

url = "https://dad-jokes.p.rapidapi.com/random/joke"

headers = {
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
    'x-rapidapi-key': "cc4bcff068msh4a1c941cf322004p176518jsndd2a674ed7ad"
    }

search_words = ['find', 'search', 'fetch']

ui = Tk()
ui.geometry("275x100")
ui.configure(bg = "#81d68f")
enter_button = tk.PhotoImage(file = "enter.png")
send_img = tk.PhotoImage(file = "right.png")

title_bar = LabelFrame(ui, bg="#81d68f")
title_bar.pack(expand=1, fill = X)
title_bar.pack_propagate(0)

avoid= ['hey', 'like', 'hows', 'whats', 'can', 'you', 'this', 'that', 'me', 'help', 'more', 'about', 'the', 'of', 'tell', 'some', 'in']
trigger_words = ["find", "search", 'weather', 'fetch']

e_username = Entry(ui, width = 30, bg = '#81d68f')
e_username.pack()


label = Label(ui, text = "Enter your username", bg = "#81d68f", padx=2, pady=2)
label.pack()

# url opening
def callback(url):
    wb.open_new_tab(url)

# new window 
def new_window():
    chat_ui = Toplevel(ui)
    chat_ui.geometry("500x600")
    chat_ui.configure(bg = "#6eb5b3")
    user_name = e_username.get()
    greeting_label = Label(chat_ui, text = f"Bot: Hello {user_name}, how can I help you?", bg = "#6eb5b3")
    greeting_label.pack(side = LEFT)
    chat_entry = Entry(chat_ui, width= 250, bg = "#6eb5b3")
    chat_entry.pack()
    e_username.delete(0, END)

    def process():
        content = chat_entry.get()
        split_content = re.split(r'''\s+|[?!@#%^&]\s*''', content)
        split_content2 = split_content.copy()
        print(split_content2)
        chat_entry.delete(0, END)
        empty = []
        
        for i in split_content:
            if i not in avoid:
                empty.append(i)
        empty2 = empty.copy()
        del empty2[0]
        converted_string = " ".join(map(str, empty2))
        if any(word in empty for word in search_words):
            findings = requests.get(f"https://en.wikipedia.org/wiki/{converted_string}")
            send_label = Label(chat_ui, bg='#6eb5b3', text = f"Bot: Here is what I found {findings.url}", fg = "blue", cursor= "hand2")
            send_label.pack()
            send_label.bind("<Button-1>", lambda e: callback(findings.url))

        if any(word in empty for word in weather):
            request_weaher = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={converted_string}&appid=26bfd75cb951c14b7bcda707fbbc14f5")
            json_weather = json.loads(request_weaher.text)
            label_weather = Label(chat_ui, bg = '#6eb5b3', text = f'''Bot: {json_weather["sys"]["country"]}, {json_weather['name']} , Current tempreature: {round(json_weather['main']['temp'] - 273.15)}°C , Humidity: {json_weather['main']['humidity']} , It is {json_weather["weather"][0]["main"]} right now''')
            label_weather.pack()

        if any(word in content for word in joke_words):
            response = requests.request("GET", url, headers=headers)
            json_data = json.loads(response.text)
            send_label2 = Label(chat_ui, text = "bot: " + json_data["body"][0]["setup"] + "\n" + json_data
            ["body"][0]["punchline"], bg = "#6eb5b3")
            send_label2.pack()

        if any(word in content for word in quotes):
            response_q = requests.get('https://zenquotes.io/api/random')
            json_q = json.loads(response_q.text)
            label_q = Label(chat_ui, bg = '#6eb5b3', text = "bot: " + json_q[0]["q"] + '\n' + "-" + json_q[0]["a"])
            label_q.pack()

    send_button = Button(chat_ui, image = send_img, command = process, bg = "#6eb5b3", border=0)
    send_button.pack()
    chat_ui.bind("<Return>", lambda occurance: process())

entry_button = Button(ui, image= enter_button, command = new_window, border= 0, bg = '#81d68f')
entry_button.pack()
ui.bind("<Return>", lambda event: new_window())


ui.mainloop()