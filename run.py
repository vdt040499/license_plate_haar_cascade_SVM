from tkinter import *
from subprocess import Popen
from tkinter import messagebox

# Command to run on Raspberry Pi
# args1 = ['python3', 'read_plate.py']
# Popen(args1)

# args2 = ['python3', 'api.py']
# Popen(args2)

#Command to run on Win
# Popen('python read_plate.py')

# Popen('python api.py')


root = Tk()
root.title("Login")
root.geometry("1366x768+0+0")
root.resizable(0, 0)

def handle_login():
    username = username_var.get()
    password = password_var.get()
    if username == 'admin' and password == '123456':
        args1 = ['python3', 'read_plate.py']
        Popen(args1)
        root.destroy()

def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=root)
    if sure == True:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", Exit)

label1 = Label(root)
label1.place(relx=0, rely=0, width=1366, height=768)
img = PhotoImage(file="./images/login.png")
label1.configure(image=img)

username_var = StringVar()
password_var = StringVar()

username = Entry(root, highlightthickness=0)
username.place(relx=0.373, rely=0.273, width=374, height=24)
username.configure(font="-family {Poppins} -size 10")
username.configure(relief="flat")
username.configure(textvariable=username_var)

password = Entry(root, highlightthickness=0)
password.place(relx=0.373, rely=0.384, width=374, height=24)
password.configure(font="-family {Poppins} -size 10")
password.configure(relief="flat")
password.configure(show="*")
password.configure(textvariable=password_var)

login_btn = Button(root, highlightthickness=0)
login_btn.place(relx=0.366, rely=0.685, width=356, height=43)
login_btn.configure(relief="flat")
login_btn.configure(overrelief="flat")
login_btn.configure(activebackground="#D2463E")
login_btn.configure(cursor="hand2")
login_btn.configure(foreground="#ffffff")
login_btn.configure(background="#D2463E")
login_btn.configure(font="-family {Poppins SemiBold} -size 20")
login_btn.configure(borderwidth="0")
login_btn.configure(text="""LOGIN""")
login_btn.configure(command=handle_login)

root.mainloop()