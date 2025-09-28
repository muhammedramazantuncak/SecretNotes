
from tkinter import *
from PIL import Image, ImageTk
import pybase64
from tkinter import messagebox

# window oluşturma

window = Tk()
window["bg"] = "light grey"
window.title("Top Secret")
window.minsize(600,700)

# font oluşturma

def font_maker(size):
    font_ex = ("Courier",size,"bold")
    return font_ex

# yer belirleyici oluşturma

def placer(argument,x,y):
    argument.place(relx=x,rely=y,anchor="center")

# resim ekleme

def adding_image(name,w,h):
    image = Image.open(name)
    resized_image = image.resize((w,h))
    img: PhotoImage = ImageTk.PhotoImage(resized_image) # img : PhotoImage kısmı sadece tip belirtiyor
    image_label = Label(image=img, bg="light grey")     # böylece IDE'nin kafası karışmıyo
                                                        # aynı name: str = "Ali" gibi
    image_label.image = img
    placer(image_label, 0.5, 0.10)

adding_image("top_secret.png",130,130)

# label oluşturma

def label_maker(text,size,x,y):
    label_ex = Label()
    label_ex.config(text=text,bg="light grey",fg="black",font=font_maker(size))
    placer(label_ex,x,y)

label_maker("Please enter your note's title",12,0.5,0.22)
label_maker("Please enter your note to the box",12,0.5,0.35)
label_maker("Pleas enter your password to encrypt your note",12,0.5,0.78)

# entry oluşturma

title_entry = Entry(width=45)
title_entry.focus()
placer(title_entry,0.5,0.28)


password_entry = Entry(width=45,show="*")
placer(password_entry,0.5,0.83)

# password değerini alma

value_dict = {}

# text oluşturma

note_text = Text(width=40,height=15)
placer(note_text,0.5,0.57)

# girişleri alma

def get_entries(argument):
    if isinstance(argument,Entry):
        return argument.get()
    elif isinstance(argument,Text):
        return argument.get("1.0","end-1c")
    else:
        return None

# click fonksiyonu oluşturma

def encrypt_button():
    if not get_entries(title_entry) or not get_entries(note_text) or not get_entries(password_entry):
        messagebox.showwarning("Blank", "You can not leave blank the relevant fields")
        return
    secret = get_entries(note_text)
    secret = secret.encode("utf-8") # text'teki yazıları byte tipine dönüştürme
    secret = pybase64.b64encode(secret).decode("utf-8") # base 64'e çevirme
    value = get_entries(password_entry)
    value_dict[secret] = value
    print(value_dict)
    note_text.delete(1.0, END)  # text box temizleme
    note_text.insert(END,secret)

    with open("top_secret.txt","a") as a:
        a.write(f"YourTitle: {get_entries(title_entry)}\nYourSecretNote: {secret}\n\n")

def decrypt_button():
    try:
        secret = get_entries(note_text)
        if secret in value_dict:
            if get_entries(password_entry) != value_dict[secret]:
                messagebox.showwarning("Incorrect!", "Incorrect Password , Try Again")
                return
            elif get_entries(password_entry) == value_dict[secret]:
                note_text.delete(1.0,END)
                secret = secret.encode("utf-8")
                secret = pybase64.b64decode(secret)
                secret = secret.decode("utf-8")
                note_text.insert(END, secret)
    except UnicodeError:
        messagebox.showerror("Attempts", "Too Many Attempts On Decrypt Button")
    except KeyError:
        messagebox.showerror("Error", "You Press Decrypt Button Before Encrypt The Text")

def clear_button():
    note_text.delete(1.0,END)
    title_entry.delete(0,END)
    password_entry.delete(0,END)

# buton oluşturma

def button_maker(text,x,y,function):
    button_ex = Button()
    button_ex.config(text=text,width=20,command=function)
    placer(button_ex,x,y)

button_maker("Save & Encrypt",0.5,0.89,lambda: [(encrypt_button()),(clear_button())])
button_maker("Decrypt",0.5,0.93,decrypt_button)
button_maker("Clear",0.5,0.97,clear_button)


window.mainloop()