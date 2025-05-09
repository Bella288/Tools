from tkinter import *
from tkinter.ttk import *
#strftime for sys time
from time import strftime

#create window
root = Tk()
root.title('Clock')
root.config(background='purple')
#Disp. time on label

def time():
    stringt = strftime('%H:%M:%S')
    lblt.config(text=stringt)
    lblt.after(1000, time)
lblt = Label(root, font=('calibri', 40, 'bold'),
            background='purple',
            foreground='white')
lblt.pack(anchor='n')
time()

#Disp. date on label
def date():
    stringd = strftime('%m/%d/%Y')
    lbld.config(text=stringd)
lbld = Label(root, font=('calibri', 20, 'bold'),
            background='purple',
            foreground='white')
lbld.pack(anchor='center')
date()

def t2():
    stringd = strftime('%I:%M:%S %p on %A, %B %d, %Y')
    lblt2.config(text=stringd)
    lblt2.after(1000, t2)
lblt2 = Label(root, font=('calibri', 10, 'bold'),
            background='purple',
            foreground='white')
lblt2.pack(anchor='s')
t2()


root.mainloop()
