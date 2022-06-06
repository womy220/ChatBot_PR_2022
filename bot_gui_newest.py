from tkinter import *
from chatterbot import ChatBot #chatterbot ver. 1.0.4
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import time
# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Impara 14" #czcionki obsługujące polskie znaki
FONT_BOLD = "Impara 13 bold"
# stworzenie bota i przypisanie bazy danych, w której będą zapisywane konwersacje
bot = ChatBot('Bot', logic_adapters=["chatterbot.logic.BestMatch"], storage_adapter = 'chatterbot.storage.SQLStorageAdapter', database_uri = 'sqlite:///database.sqlite3')

# moduł do działań matematycznych
def math_module(request_split):
    r_fixed = request_split[5].replace('?','') # usunięcie znaku zapytania z końca zdania
    first_number = int(request_split[3]) # pierwsza liczba
    second_number = int(r_fixed) # druga liczba
    # obsługa możliwych działań
    if request_split[4] == '+' or request_split[4] == 'dodać' or request_split[4] == 'plus':
        return first_number + second_number
    elif request_split[4] == '-' or request_split[4] == 'odjąć' or request_split[4] == 'minus':
        return first_number - second_number
    elif request_split[4] == '*' or request_split[4] == 'razy':
        return first_number * second_number
    elif request_split[4] == '/' or request_split[4] == 'przez':
        return first_number / second_number

trainer = ChatterBotCorpusTrainer(bot)

trainer.train("conversations","humor") # nauczenie bota przygotowanych corpusów

trainer = ListTrainer(bot)

# obsługa wysłania wiadomości przez naciśniecie odpowiedniego przycisku
def send_enter(event):
    send = "You: " + request.get()
    txt.insert(END, "\n" + send) # wstawienie wysłanej wiadomości do pola tekstowego

    request_lower = request.get().lower() # przekształcenie wiadomości na małe litery
    request_lower_fixed = request_lower.replace('?', '') # usunięcie znaku zapytania z końca zdania
    request_split = request_lower.split() # podzielenie wiadomości na poszczególne słowa

    # zamknięcie programu po wysłaniu wiadomości 'narazie'
    if (request_lower == "narazie"):
        txt.insert(END, "\n" + "Bot: Narazie")
        root.quit()
    # moduł wyświetlający aktualną godzinę
    elif (request_lower_fixed == 'która jest godzina' or request_lower_fixed == "która godzina"):
        txt.insert(END, "\n" + "Bot: Jest " + time.strftime('%H:%M') + ".")
    # wywołanie modułu do działań matematycznych
    elif (request_split[0] == 'ile' and request_split[1] == 'to' and request_split[2] == 'jest'):
        response = math_module(request_split)   
        txt.insert(END, "\n" + "Bot: " + str(response))
    # default case
    else:
        trainer.train([request.get(),]) # nauczenie bota wysłanej przez użytkownika wiadomości
        response = bot.get_response(request.get()) # otrzymanie odpowiedzi
        txt.insert(END, "\n" + "Bot: " + str(response)) # wstawienie odpowiedzi do pola tekstowego

    request.delete(0, END) # wyczyszcenie pola do wpisywania wiadomości

# obsługa wysłania wiadomości przez naciśniecie przycisku 'Send'
def send():
    send = "You: " + request.get()
    txt.insert(END, "\n" + send) # wstawienie wysłanej wiadomości do pola tekstowego

    request_lower = request.get().lower() # przekształcenie wiadomości na małe litery
    request_lower_fixed = request_lower.replace('?', '') # usunięcie znaku zapytania z końca zdania
    request_split = request_lower.split() # podzielenie wiadomości na poszczególne słowa

    # zamknięcie programu po wysłaniu wiadomości 'narazie'
    if (request_lower == "narazie"):
        txt.insert(END, "\n" + "Bot: Narazie")
        root.quit()
    # moduł wyświetlający aktualną godzinę
    elif (request_lower_fixed == 'która jest godzina' or request_lower_fixed == "która godzina"):
        txt.insert(END, "\n" + "Bot: Jest " + time.strftime('%H:%M') + ".")
    # wywołanie modułu do działań matematycznych
    elif (request_split[0] == 'ile' and request_split[1] == 'to' and request_split[2] == 'jest'):
        response = math_module(request_split)   
        txt.insert(END, "\n" + "Bot: " + str(response))
    # default case
    else:
        trainer.train([request.get(),]) # nauczenie bota wysłanej przez użytkownika wiadomości
        response = bot.get_response(request.get()) # otrzymanie odpowiedzi
        txt.insert(END, "\n" + "Bot: " + str(response)) # wstawienie odpowiedzi do pola tekstowego

    request.delete(0, END) # wyczyszcenie pola do wpisywania wiadomości


lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="ChatBot", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

request = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
request.grid(row=2, column=0)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
			command=send).grid(row=2, column=1)
root.bind("<Up>",send_enter) # wysyłanie wiadomości po naciśnięciu strzałki w górę

root.mainloop()