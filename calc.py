import tkinter as tk
import math

history_list = []

# ---------- FUNCTIONS ----------

def press(v):
    entry.insert(tk.END, v)

def clear():
    entry.delete(0, tk.END)

def backspace():
    entry.delete(len(entry.get())-1, tk.END)

def calculate():
    try:
        expr = entry.get()

        # Replace symbols
        expr = expr.replace("^","**")
        expr = expr.replace("√","math.sqrt")
        expr = expr.replace("π","math.pi")
        expr = expr.replace("e","math.e")

        # auto close brackets
        expr += ")" * (expr.count("(") - expr.count(")"))

        # SAFE EVAL WITH MATH ACCESS
        result = eval(expr, {"__builtins__":None,"math":math}, {})

        history_list.append(f"{entry.get()} = {result}")
        update_history()

        entry.delete(0, tk.END)
        entry.insert(0, result)

    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0,"ERROR")

def update_history():
    history_box.delete(0, tk.END)
    for item in history_list[-10:]:
        history_box.insert(tk.END,item)

def key_input(event):
    if event.char in "0123456789+-*/.^()":
        press(event.char)
    elif event.keysym=="Return":
        calculate()
    elif event.keysym=="BackSpace":
        backspace()

def toggle_theme():
    global dark
    dark = not dark

    if dark:
        bg="#1e1e1e"; fg="white"; btn="#3a3a3a"
    else:
        bg="white"; fg="black"; btn="#e0e0e0"

    root.configure(bg=bg)
    entry.configure(bg=btn, fg=fg)
    history_box.configure(bg=btn, fg=fg)

    for b in buttons:
        b.configure(bg=btn, fg=fg)

# ---------- UI ----------

root = tk.Tk()
root.title("Scientific Calculator")
root.resizable(False,False)
dark=True
root.configure(bg="#1e1e1e")

entry = tk.Entry(root,font=("Segoe UI",20),
                 bg="#3a3a3a",fg="white",
                 bd=0,justify="right")
entry.grid(row=0,column=0,columnspan=6,padx=10,pady=10,ipady=10)

root.bind("<Key>", key_input)

# ---------- BUTTONS ----------

btn_text = [
'7','8','9','/','sin','cos',
'4','5','6','*','tan','log',
'1','2','3','-','√','^',
'0','.','=','+','π','e'
]

buttons=[]
r=1; c=0

for t in btn_text:
    if t=="=":
        cmd=calculate
    elif t=="sin":
        cmd=lambda: press("math.sin(")
    elif t=="cos":
        cmd=lambda: press("math.cos(")
    elif t=="tan":
        cmd=lambda: press("math.tan(")
    elif t=="log":
        cmd=lambda: press("math.log10(")
    else:
        cmd=lambda x=t: press(x)

    b=tk.Button(root,text=t,width=6,height=2,
                font=("Segoe UI",11),
                bg="#3a3a3a",fg="white",
                bd=0,command=cmd)
    b.grid(row=r,column=c,padx=4,pady=4)
    buttons.append(b)

    c+=1
    if c==6:
        c=0; r+=1

# ---------- EXTRA BUTTONS ----------

tk.Button(root,text="C",command=clear,
          width=13,height=2,
          bg="#ff9500",fg="white",bd=0).grid(row=r,column=0,columnspan=2,pady=5)

tk.Button(root,text="⌫",command=backspace,
          width=13,height=2,
          bg="#ff9500",fg="white",bd=0).grid(row=r,column=2,columnspan=2)

tk.Button(root,text="Theme",command=toggle_theme,
          width=13,height=2,
          bg="#f335b0",fg="white",bd=0).grid(row=r,column=4,columnspan=2)

# ---------- HISTORY ----------

history_box=tk.Listbox(root,width=38,height=6,
                       bg="#3a3a3a",fg="white",
                       bd=0)
history_box.grid(row=r+1,column=0,columnspan=6,pady=10)

root.mainloop()
