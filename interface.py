from tkinter import *
import RSA
from tkinter import messagebox as mb
import random
import time

backgroundColor="grey"
btnBackgroundColor="orange"
root = Tk()
root.title("Практика 2 ")
root.geometry('800x900')
root.resizable(False, False)
root.configure(background=backgroundColor)

public_key_lbl = Label(text="Открытые ключи", font="Arial 14", background=backgroundColor)
public_key_lbl.place(x=100, y=300)

n_lbl = Label(text="N:", font="Arial 11", background=backgroundColor)
n_lbl.place(x=70, y=350)
n_entry = Entry(width="100")
n_entry.place(x=100, y=350)

s_lbl = Label(text="S:", font="Arial 11", background=backgroundColor)
s_lbl.place(x=70, y=400)
s_entry = Entry(width="100")
s_entry.place(x=100, y=400)

private_key_lbl = Label(text="Закрытый ключ", font="Arial 14", background=backgroundColor)
private_key_lbl.place(x=100, y=430)

e_lbl = Label(text="E:", font="Arial 11", background=backgroundColor)
e_lbl.place(x=70, y=460)
e_entry = Entry(width="100")
e_entry.place(x=100, y=460)

generate_keys__btn = Button(text="Сгенерировать ключи", font="Arial 11", width="20", bg="cyan2")
generate_keys__btn.place(x=320, y=500)

input_lbl = Label(text="Исходное соообщение", font="Arial 14", background=backgroundColor)
input_lbl.place(x=65, y=30)
input_text = Text(width="83", height="8")
input_text.place(x=65, y=80)

output_lbl = Label(text="Результат шифрования/дешифрования", font="Arial 14", background=backgroundColor)
output_lbl.place(x=250, y=560)
output_text = Text(width="94", height="9")
output_text.place(x=20, y=600)

encrypt_btn = Button(text="Зашифровать", font="Arial 11", width="15", bg=btnBackgroundColor, state='disabled')
encrypt_btn.place(x=250, y=240)

decrypt_btn = Button(text="Расшифровать", font="Arial 11", width="15", bg=btnBackgroundColor, state='disabled')
decrypt_btn.place(x=450, y=240)

def generate_keys_clicked(event):
    n_entry.configure(state='normal')
    s_entry.configure(state='normal')
    e_entry.configure(state='normal')
    n_entry.delete(0, END)
    s_entry.delete(0, END)
    e_entry.delete(0, END)
    start = time.time()
    array_keys = RSA.generate_keys()
    print(f"Время создания ключей = {time.time() - start}")
    n = array_keys[0]
    s = array_keys[1]
    e = array_keys[2]
    n_entry.insert(0, n)
    s_entry.insert(0, s)
    e_entry.insert(0, e)
    n_entry.configure(state='readonly')
    s_entry.configure(state='readonly')
    e_entry.configure(state='readonly')
    encrypt_btn.config(state='normal')
    decrypt_btn.config(state='normal')

def encrypt_clicked(event):
    output_text.delete(1.0, END)
    key_n = int(n_entry.get())
    key_s = int(s_entry.get())
    message = input_text.get(1.0, END)
    if message == '\n':
        mb.showerror("Ошибка", "Сообщение отсутствует! Введите текст и повторите попытку!")
        return
    numbers = ""
    bloсks = []
    tableSymbols = RSA.create_char_table()
    start = time.time()
    for letter in message.lower():
        numbers += str(tableSymbols[letter])
    while len(numbers) > 13:
        block_length = random.randint(2, 13)
        while numbers[block_length] == '0':
            block_length += 1
        bloсks.append(numbers[:block_length])
        numbers = numbers[block_length:]
    if numbers:
        bloсks.append(numbers)
    result = ""
    for i in range(len(bloсks)):
        result = result + str(pow(int(bloсks[i]), key_s, key_n)) + " "
    print(f"Время шифрования сообщения = {time.time() - start}")
    output_text.insert(1.0, result)
    

def decrypt_clicked(event):
    output_text.delete(1.0, END)
    key_n = int(n_entry.get())
    key_e = int(e_entry.get())
    message = input_text.get(1.0, END)
    tableSymbols = RSA.create_char_table()
    reverseTable = {value: key for key, value in tableSymbols.items()}
    if message == '\n':
        mb.showerror("Ошибка", "Сообщение отсутствует! Введите текст и повторите попытку!")
        return
    numbers = message.split()
    decryptedMessage = ""
    result = ""
    start = time.time()
    for i in range(len(numbers)):
        decryptedMessage = decryptedMessage + str(pow(int(numbers[i]), key_e, key_n))
    while len(decryptedMessage) != 0:
        symbol = int(decryptedMessage[:4])
        decryptedMessage = decryptedMessage[4:]
        if str(reverseTable.get(symbol)) == "None":
            mb.showerror("Ошибка", "Операция невозможна")
            return
        result = result + str(reverseTable.get(symbol))
    print(f"Время расшифровывания сообщения = {time.time() - start}")
    output_text.insert(1.0, result)

def paste(event):
    input_text.delete(1.0, END)
    out = output_text.get(1.0, END)
    input_text.insert(1.0, out)

generate_keys__btn.bind('<Button-1>', generate_keys_clicked)
input_text.bind('<Button-3>', paste)
encrypt_btn.bind('<Button-1>', encrypt_clicked)
decrypt_btn.bind('<Button-1>', decrypt_clicked)
root.mainloop()