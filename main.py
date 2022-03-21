import json
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_gen():
    """generate secure random alpha-numeric character"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 12))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 6))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 6))]
    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    pass_input.delete(0, END)
    pyperclip.copy(password)
    message_section.config(text=f"Copied Password \n to clipboard")
    pass_input.insert(END, password)
# ---------------------------- SEARCH  ------------------------------- # 
def search():
    website_entry = website_input.get()
    try:
        with open("password.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        message_section.config(text="No data file found (empty)")
    else:
        if website_entry in data:
            email = data[website_entry]["Email"]
            password = data[website_entry]["Password"]
            email_input.delete(0, END)
            pass_input.delete(0, END)
            email_input.insert(END, email)
            pass_input.insert(END, password)
            message_section.config(text=" Filled in the\ndata for you")
        else:
            message_section.config(text=f"No data found on\n{website_entry}")



# ---------------------------- SAVE PASSWORD ------------------------------- #


def write_data():
    """write the data that was entered to the UI to a file"""
    website_entry = website_input.get()
    email_entry = email_input.get()
    pass_entry = pass_input.get()
    new_data = {
        website_entry: {
            "Email": email_entry,
            "Password": pass_entry,
        }
    }
    if len(website_entry) == 0 or len(pass_entry) == 0:
        messagebox.showinfo(title="Empty Field Detected", message="it appears you have left some fields empty,"
                                                                  " could you fix that?")
    else:
        save_data = messagebox.askokcancel(title="SAVE to data?", message=f" This is the detail received \n Website: "
                                                                  f"{website_entry} \n Email: {email_entry}\n "
                                                                  f"Password: {pass_entry} \n does this "
                                                                  f"look good? should I save?")

        if save_data:
            try:
                with open("password.json", mode="r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("password.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #      Updating data with new data
                data.update(new_data)
                with open("password.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_input.delete(0, END)
                pass_input.delete(0, END)
    
# ---------------------------- UI SETUP ------------------------------- #

# constant


FONT = ("Fira code", 11)
window = Tk()
window.title("Password Manager")
window.maxsize(width=550, height=400)
window.minsize(width=550, height=400)
window.config(padx=50, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg="#f0f0f0")
logo_img = PhotoImage(file="test.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website", font=FONT)
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username", font=FONT)
email_label.grid(column=0, row=2)
pass_label = Label(text="Password", font=FONT)
pass_label.grid(column=0, row=3)

message_section = Label(text="", font=FONT)
message_section.grid(column=1, row=5)

# Inputs(Entries)
website_input = Entry(width=33)
website_input.grid(column=1, row=1)
website_input.focus()

email_input = Entry(width=51)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(END, "email@email.com")

pass_input = Entry(width=33)
pass_input.grid(column=1, row=3)

# Buttons
search = Button(text="Search", command=search)
search.grid(column=2, row=1)

generate_pass = Button(text="Generate Password", command=password_gen)
generate_pass.grid(column=2, row=3)

add_pass = Button(text="Add", width=43, command=write_data)
add_pass.grid(column=1, row=4, columnspan=2)


window.mainloop()
