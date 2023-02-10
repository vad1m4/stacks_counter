from tkinter import *
import json

# root
root = Tk()
root.config(background="#363636")
root.title("Stack counter")
root.resizable(False, False)

# icon
icon = PhotoImage(file="warped_fungus.png")
root.iconphoto(True, icon)

# frame and scrollbar
my_frame = Frame(root, background="#212121")
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

# listbox
my_listbox = Listbox(
    my_frame,
    width=40,
    font=("monaco 20"),
    yscrollcommand=my_scrollbar.set,
    background="#212121",
    highlightthickness=2,
    fg="WHITE",
    selectmode=EXTENDED,
)
my_listbox.config(highlightbackground="#212121", highlightcolor="#212121")
my_scrollbar.config(command=my_listbox.yview)

# pack and grid
my_scrollbar.pack(side=RIGHT, fill=Y)
my_frame.grid(row=0, column=0)
my_listbox.pack(pady=7, padx=7)

# defining
def edit():
    new_data = []
    for index, entry in enumerate(get_data()):
        if index in my_listbox.curselection():
            text = str(entry["quantity"]) + " " + entry["block"]
            my_entry.insert(0, text)
        else:
            new_data.append(entry)

    with open("data.json", "w") as f:
        json.dump(new_data, f, indent=4)

    for item in reversed(my_listbox.curselection()):
        my_listbox.delete(item)

def sort(e):
  return e["quantity"]

def delete():
    new_data = []
    for index, entry in enumerate(get_data()):
        if index in my_listbox.curselection():
            continue

        new_data.append(entry)

    with open("data.json", "w") as f:
        json.dump(new_data, f, indent=4)

    for item in reversed(my_listbox.curselection()):
        my_listbox.delete(item)

def delete_all():
    my_listbox.delete(0, END)
    with open("data.json", "w") as file:
        json.dump([], file)

def submit(_):
    try:
        text = my_entry.get()
        quantity, block = text.split(maxsplit=1)
        quantity = int(quantity)
        data = get_data()

        with open("data.json", "w") as f:
            data.append({"block": block.title(), "quantity": quantity})
            data.sort(key=sort,reverse=True) 
            json.dump(data, f, indent=4)
        my_entry.delete(0, END)
        my_listbox.delete(0, END)
        for i in get_data():
            text = count_stacks(i["quantity"], i["block"])
            my_listbox.insert(END, text)
    except:
        my_entry.delete(0, END)
        my_entry.insert(0, "Invalid input")

def copy():
    root.clipboard_clear()
    for i in get_data():
        text = count_stacks(i["quantity"], i["block"])
        root.clipboard_append(f"{text}\n")
        root.update()

def count_stacks(quantity, block):
    stacks = quantity // 64
    remains = quantity % 64
    return f"{stacks} stacks + {remains} {block}"

# get data
def get_data():
    with open("data.json") as f:
        return json.load(f)

# dump data
for i in get_data():
    text = count_stacks(i["quantity"], i["block"])
    my_listbox.insert(END, text)

# second frame for all buttons
my_buttons_frame = Frame(root, background="#363636")

# delete button
delete_button = Button(my_buttons_frame, text="Delete", command=delete)
delete_button.config(font=("monaco"), fg="#d45359", bg="#363636")
delete_button.pack(side=TOP, fill=BOTH, pady=7, padx=7)

# delete all button
delete_all_button = Button(my_buttons_frame, text="Delete all", command=delete_all)
delete_all_button.config(font=("monaco"), fg="#d45359", bg="#363636")
delete_all_button.pack(side=TOP, pady=7, fill=BOTH, padx=7)

# edit button
edit_button = Button(my_buttons_frame, text="Edit", command=edit)
edit_button.config(font=("monaco"), fg="WHITE", bg="#363636")
edit_button.pack(side=TOP, pady=7, padx=7, fill=BOTH)

# quit button
quit_button = Button(
    my_buttons_frame, text="Quit", command=root.destroy
)
quit_button.config(font=("monaco"), fg="WHITE", bg="#363636")
quit_button.pack(side=TOP, pady=7, padx=7, fill=BOTH)

# copy button
copy_button = Button(my_buttons_frame, text="Copy to clipboard", command=copy)
copy_button.config(font=("monaco"), fg="WHITE", bg="#363636")
copy_button.pack(side=TOP, pady=7, padx=7, fill=BOTH)

# grid
my_buttons_frame.grid(row=0, column=1, pady=7, sticky="sn")

# entry
my_entry = Entry(root, font=20, background="#363636", fg="WHITE")
my_entry.config(font=("monaco 13"))
my_entry.grid(row=1, column=0, columnspan=2, padx=7, pady=7, sticky="ew")
my_entry.bind("<Return>", submit)

# mainloop
root.mainloop()
