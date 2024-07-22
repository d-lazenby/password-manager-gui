import json
import pyperclip
import re
import secrets
import string
from tkinter import *
from tkinter import messagebox


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password(length=16, nums=1, special_chars=1, uppercase=1, lowercase=1):

    # Define the possible characters for the password
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Combine all characters
    all_characters = letters + digits + symbols

    password = ''
    # Generate password
    for _ in range(length):
        password += secrets.choice(all_characters)
    
    constraints = [
        (nums, r'\d'),
        (special_chars, fr'[{symbols}]'),
        (uppercase, r'[A-Z]'),
        (lowercase, r'[a-z]')
    ]

    # Check constraints        
    if all(
        constraint <= len(re.findall(pattern, password))
        for constraint, pattern in constraints
    ):
        pass
    else:
        generate_password()

    
    # insert password 
    password_entry.insert(0, password)
    # copy password to clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    # append website, email and password to file in appropriate format
    website, email, password = website_entry.get(), email_entry.get(), password_entry.get()
    new_data = {
        website: 
            {
                "email": email,
                "password": password,
                }
            }
    
    # check fields are filled
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave fields empty!")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # read data from file
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                # save updated data
                json.dump(new_data, data_file, indent=4)
        else:    
            # update with new data
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                # save updated data
                json.dump(data, data_file, indent=4)
        finally:   
            # clear values in website, email and password fields
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")
 
# ---------------------------- SEARCH ------------------------------- # 
           
def find_password():
    search_website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        if search_website in data:
            search_result = data[search_website]
            messagebox.showinfo(title=f"{search_website}", message=f"Email: {search_result['email']}\nPassword: {search_result['password']}")
        else:
            messagebox.showerror(title=f"{search_website}", message="No details for the website exist.")       
        

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=None)

canvas = Canvas(width=200, height=200, bg=None)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = Entry(width=38)
email_entry.insert(0, "name@email.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

generate = Button(text="Generate Password", command=generate_password)
generate.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()