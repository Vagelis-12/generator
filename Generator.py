import sys
import os
import uuid
import json
import itertools
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from itertools import chain


# Setup the root UI 
root =Tk()
root.title("Generator")
root.configure(bg="gray89")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.state('zoomed')


#Upload File
def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    return filename

#Open File
def OpenFile():
    with open(UploadAction()) as json_file:
        features = json.load(json_file)
        return features

#Function to create the Tree  
def json_tree(tree, parent, dictionary):
    for key in dictionary:
        uid = uuid.uuid4()
        if isinstance(dictionary[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            json_tree(tree, uid, dictionary[key])
        else:
            value = dictionary[key]
            if value is None:
                value = 'None'
            tree.insert(parent, 'end', uid, values=(key,value))
#Restart Program When Open Button Pressed
def restart_program():
     os.execl(sys.executable, sys.executable, *sys.argv)

#Open Button
open_button = Button(root, text='Open File', width=15,borderwidth = 1, bg="gray89", command=restart_program)
open_button.pack(side=TOP)

#Style
style = ttk.Style()
style.theme_use("winnative")
style.configure("Treeview", rowheight=45)
style.configure("Treeview.Heading", background="gray89")	

# Change selected color
style.map('Treeview',
	background=[('selected', 'grey')],)

# Setup the Frames
tree_frame = ttk.Frame(root, padding="3")
tree_frame.pack(pady=2)


add_frame = Frame(root,  bd = 0, bg="gray89")
add_frame.pack(pady=20)

# Setup the Tree
tree = ttk.Treeview(tree_frame,columns=('Keys', 'Values'))
tree.column('Keys', anchor=W, width=340)
tree.column('Values', width=340, anchor='center')
tree.heading('#0', text='Primary Keys')
tree.heading('Keys', text='Keys', anchor=W)
tree.heading('Values', text='Values')
json_tree(tree, '', OpenFile())
tree.pack(fill=BOTH, expand=1)


#Labels
ol = Label(add_frame, text="Primary Keys", bg="gray89")
ol.grid(row=0, column=0)

nl = Label(add_frame, text="Keys", bg="gray89")
nl.grid(row=0, column=1)

il = Label(add_frame, text="Values", bg="gray89")
il.grid(row=0, column=2)


#Entrys
primary_box = Entry(add_frame, bg="LightCyan2")
primary_box.focus_force()
primary_box.grid(row=1, column=0)

keys_box = Entry(add_frame, bg="LightCyan2")
keys_box.focus_force()
keys_box.grid(row=1, column=1)

values_box = Entry(add_frame, bg="LightCyan2")
values_box.focus_force()
values_box.grid(row=1, column=2)

# Select Record
def select_record():
    
    keys_box.delete(0, END)
    values_box.delete(0, END)
    primary_box.delete(0, END)

    selected = tree.focus()
    values = tree.item(selected, 'values')
    text = tree.item(selected, 'text')

    primary_box.insert(0, text)
    keys_box.insert(0, values[0])
    values_box.insert(0, values[1])


# Create Binding Click function
def clicker(e):
    select_record()

# Save updated record
def update_record():
    selected = tree.focus()
    tree.item(selected, text=(primary_box.get()), values=(keys_box.get(), values_box.get()))

    primary_box.delete(0, END)
    keys_box.delete(0, END)
    values_box.delete(0, END)

# Add Record
def add_record():
    tree.insert(parent=tree.parent(tree.focus()), index='end',text=primary_box.get(), values=(keys_box.get(), values_box.get()))
  
    # Clear the boxes
    keys_box.delete(0, END)
    values_box.delete(0, END)

# Add Primary Key
def add_primary():
    uid = uuid.uuid4()
    tree.insert('', '0', uid, text ='New Primary')
    tree.insert(uid, 'end', text ='', value=('keys','values'))

# Move Row up
def up():
    rows = tree.selection()
    for row in rows:
        tree.move(row, tree.parent(row), tree.index(row)-1)

# Move Row Down
def down():
    rows = tree.selection()
    for row in reversed(rows):
        tree.move(row, tree.parent(row), tree.index(row)+1)	

# Remove one selected
def remove_one():
    x = tree.selection()[0]
    tree.delete(x)

# Fuction running on submit()
# Converting tree values to dict, convert dict to json
def writeToJSONFile(path, fileName, output_dict):
    json.dump(output_dict, path, indent=2 )
    path = './'

output_dict={}
def check():
        for parent in tree.get_children():
            par = tree.item(parent)["text"]
            output_dict[par] = {}
            for child in tree.get_children(parent):
                data = tree.item(child)["values"]
                output_dict[par][data[0]] = data[1]
        
        files = [('JSON File', '*.json')]
        fileName = 'new'
        filepos = asksaveasfile(filetypes = files,defaultextension = json,initialfile='new')
        writeToJSONFile(filepos, fileName, output_dict)
        tkinter.messagebox.showinfo("", "Your file has been saved!")

#Buttons
update_button = Button(add_frame, text="Save Record",  width=15, borderwidth = 1 , bg="gray89", command=update_record)
update_button.grid(row=2, column=2)

remove_one = Button(add_frame, text="Delete Selected", width=15, borderwidth = 1 ,  bg="gray89", command=remove_one)
remove_one.grid(row=3, column=2)

add_record = Button(add_frame, text="Add Key/Value", width=15, borderwidth = 1 ,  bg="gray89", command=add_record)
add_record.grid(row=2, column=0)

move_up = Button(add_frame, text="Move Up", width=15, borderwidth = 1 , bg="gray89",command=up)
move_up.grid(row=2, column=1)

move_down = Button(add_frame, text="Move Down", width=15, borderwidth = 1 , bg="gray89", command=down)
move_down.grid(row=3, column=1)

add_primary_button = Button(add_frame, text="Add Primary Key",  width=15, borderwidth = 1 ,bg="gray89",command=add_primary)
add_primary_button.grid(row=3, column=0)

submit = Button(root,text='Submit', bg='green', fg='white', borderwidth = 1 , width=15, command=check)
submit.pack(side=BOTTOM) 

# Bindings
tree.bind("<ButtonRelease-1>", clicker)


# Limit windows minimum dimensions
root.update_idletasks()
root.minsize(800, 800)
root.mainloop()

