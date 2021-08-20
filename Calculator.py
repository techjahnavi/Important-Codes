from tkinter import *


def click(event):
    global sc_value
    text = event.widget.cget('text')
    if text == '=':
        if sc_value.get().isdigit():
            value = int(sc_value.get())
        else:
            try:
                value = eval(screen.get())
            except Exception as e:
                print(e)
                value = "Error"
        sc_value.set(value)
        screen.update()
    elif text == 'C':  # for all clear
        sc_value.set("")
        screen.update()
    elif text == '<--':  # using for backspace
        sc_value.set(sc_value.get()[:-1])
        screen.update()
    else:
        try:
            sc_value.set(sc_value.get() + text)
            screen.update()
        except Exception:
            print("something is wrong")


root = Tk()
root.geometry("284x362")
root.maxsize(284, 362)
root.minsize(284, 362)
root.title("GUI Calculator")
root.wm_iconbitmap("calculator.ico")

sc_value = StringVar()
sc_value.set('')
screen = Entry(root, textvar=sc_value, font="lucida 20 bold")
screen.place(x=10, y=15, width=261, height=51)
screen.bind("<Key>", lambda e: "break")  # it helps to not to write anything

# Frame create
f1 = Frame(root, bg="grey").pack()

# create all the buttons
xpos = [10, 80, 150, 220, 10, 150, 220]
ypos = [130, 190, 250, 310, 80]
x_loop = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6]
y_loop = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
wpos = [51, 51, 51, 51, 51, 51, 51, 51, 51, 51,
        51, 51, 51, 51, 51, 51, 121, 51, 51, 51]
fix = ['9', '8', '7', '+', '6', '5', '4', '-', '3',
       '2', '1', '*', '%', '0', '.', '/', 'C', '<--', '=']
for y in range(0, 19):  # make All buttons in fix tuple
    b = Button(f1, text=fix[y], font="lucida 15 bold")
    b.place(x=xpos[x_loop[y]], y=ypos[y_loop[y]], width=wpos[y], height=41)
    b.bind("<Button-1>", click)

root.mainloop()
