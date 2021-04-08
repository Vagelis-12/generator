from tkinter import *
from tkinter import ttk
import json
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

list_key = []
list_value = []
data=[]

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    return filename

def OpenFile():
    with open(UploadAction()) as json_file:
        features = json.load(json_file)
    
    for key, value in features.items():
        print("Primary key-",key,":")
        for inkey in value.items():
            print("The key is: ",inkey[0], "and the value is: ",inkey[1])
            list_key.append(inkey[0])
            list_value.append(inkey[1])

root = Tk()
root.title('Generator')
root.geometry("500x700")


#Style
style = ttk.Style()
style.theme_use("default")


style.configure("Treeview", 
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3"
	)
# Change selected color
style.map('Treeview', 
	background=[('selected', 'blue')])

# Create Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

# Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

#Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Keys", "Values")

# Formate Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Keys", anchor=W, width=140)
my_tree.column("Values", anchor=CENTER, width=140)


# Create Headings 
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Keys", text="Keys", anchor=W)
my_tree.heading("Values", text="Values", anchor=CENTER)


global count
count=0
# Add Data
OpenFile()
for num in range (len(list_key)):
	data.append([list_key[num], list_value[num]])

# Create striped row tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightgrey")



for record in data:
	if count % 2 == 0:
		my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('evenrow',))
	else:
		my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('oddrow',))

	count += 1


add_frame = Frame(root)
add_frame.pack(pady=20)

#Labels
nl = Label(add_frame, text="Keys")
nl.grid(row=0, column=0)

il = Label(add_frame, text="Values")
il.grid(row=0, column=1)


#Entry boxes
keys_box = Entry(add_frame)
keys_box.grid(row=1, column=0)

values_box = Entry(add_frame)
values_box.grid(row=1, column=1)

# Add Record
def add_record():
	my_tree.tag_configure('oddrow', background="white")
	my_tree.tag_configure('evenrow', background="lightgrey")

	global count
	if count % 2 == 0:
		my_tree.insert(parent='', index='end', iid=count, text="", values=(keys_box.get(), values_box.get()), tags=('evenrow',))
	else:
		my_tree.insert(parent='', index='end', iid=count, text="", values=(keys_box.get(), values_box.get()), tags=('oddrow',))

	count += 1

	# Clear the boxes
	keys_box.delete(0, END)
	values_box.delete(0, END)
	

# Remove one selected
def remove_one():
	x = my_tree.selection()[0]
	my_tree.delete(x)


# Select Record
def select_record():
	
	keys_box.delete(0, END)
	values_box.delete(0, END)

	selected = my_tree.focus()
	values = my_tree.item(selected, 'values')

	
	keys_box.insert(0, values[0])
	values_box.insert(0, values[1])



# Save updated record
def update_record():
	selected = my_tree.focus()
	my_tree.item(selected, text="", values=(keys_box.get(), values_box.get()))

	
	keys_box.delete(0, END)
	values_box.delete(0, END)
	
# Create Binding Click function
def clicker(e):
	select_record()

# Move Row up
def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Row Down
def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

test = 1
def writeToJSONFile(path, fileName, data):
    json.dump(data, path)
    path = './'

def check():
    data = []
    files = [('JSON File', '*.json')]
    fileName='new'
    filepos = asksaveasfile(filetypes = files,defaultextension = json,initialfile='new')
    writeToJSONFile(filepos, fileName, data)
        
   
   



#Buttons
move_up = Button(root, text="Move Up", command=up)
move_up.pack(pady=2)

move_down = Button(root, text="Move Down", command=down)
move_down.pack(pady=2)

select_button = Button(root, text="Select Record", command=select_record)
select_button.pack(pady=2)

update_button = Button(root, text="Save Record", command=update_record)
update_button.pack(pady=2)

add_record = Button(root, text="Add Record", command=add_record)
add_record.pack(pady=2)

remove_one = Button(root, text="Remove One Selected", command=remove_one)
remove_one.pack(pady=2)

submit = Button(text='Submit', bg='green', fg='white',command=check)
submit.pack(pady=2) 



temp_label = Label(root, text="")
temp_label.pack(pady=20)

# Bindings
#my_tree.bind("<Double-1>", clicker)
my_tree.bind("<ButtonRelease-1>", clicker)


root.mainloop()