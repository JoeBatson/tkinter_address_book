import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import db_handler


root = tk.Tk()
root.title("Address Book")

window_width = 700
window_height = 400

def window_position(window, w_width, w_height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - w_width) // 2
    y = (screen_height - w_height) // 2
    window.geometry(f"{w_width}x{w_height}+{x}+{y}")
    
window_position(root, window_width, window_height)


frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="news")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)  

frame.grid_columnconfigure(0, weight=1)  
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=1)

search_results = {} #Holds the information from a database search.
selected_entry_id = None 

def enter_data():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_label_entry.get()
    city = city_entry.get()
    state = state_combobox.get()
    
    if not (first_name and last_name and address and city and state):
        messagebox.showinfo("", "Please fill out the information completely.")
        return

    else:
        db_handler.insert_data(first_name.lower().strip(), last_name.lower().strip(), address.lower().strip(), city.lower().strip(), state)

        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        address_label_entry.delete(0, tk.END)
        city_entry.delete(0, tk.END)
        state_combobox.set("")


def search_data():
    global search_results
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()

    if not first_name and not last_name:
        display_listbox.delete(0, tk.END)
        display_listbox.insert(tk.END, "You must enter a first or last name.")
        return

    if first_name.upper() == "ALL" or last_name.upper() == "ALL":
        name_search = db_handler.get_all_entries()

    else:
        name_search = db_handler.search_entries(first_name, last_name)

    display_listbox.delete(0, tk.END)
    search_results.clear()

    if name_search:
        for index, row in enumerate(name_search):
            formatted_row = f"{row[1].capitalize()} {row[2].capitalize()} - {row[3].title()}, {row[4].title()}, {row[5]}"
            display_listbox.insert(tk.END, formatted_row)
            search_results[index] = row
    else:
        display_listbox.insert(tk.END, "No matching records found.\n")


def on_select(event):
    global selected_entry_id
    selected_index = display_listbox.curselection()
    
    if selected_index:
        row_data = search_results.get(selected_index[0])
        
        if row_data:
            selected_entry_id = row_data[0]
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            address_label_entry.delete(0, tk.END)
            city_entry.delete(0, tk.END)
            
            first_name_entry.insert(0, row_data[1]), 
            last_name_entry.insert(0, row_data[2])
            address_label_entry.insert(0, row_data[3])
            city_entry.insert(0, row_data[4])
            state_combobox.set(row_data[5])


def edit_address():
    global selected_entry_id
    
    if selected_entry_id is None:
        messagebox.showinfo("", "Select an entry to edit first.")
        return

    response = messagebox.askokcancel("Title", "Are you sure you want to make changes to this address?")

    if response:
        new_info = (first_name_entry.get(),
        last_name_entry.get(),
        address_label_entry.get(),
        city_entry.get(),
        state_combobox.get())
            
        db_handler.edit_address(selected_entry_id, new_info)  # Update database
    
    else:
        messagebox.showinfo(message="Edit canceled")
    

    search_data()  # Refresh the displayed data


def clear_screen():
    display_listbox.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    address_label_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    state_combobox.set("")


def delete_entry():
    global selected_entry_id
    
    if selected_entry_id is None:
        messagebox.showinfo("", "Please select an entry to delete first.")
        return

    warning = messagebox.showwarning("Warning", "WARNING!!!".center(30))
    response = messagebox.askokcancel("", "ARE YOU SURE YOU WANT TO DELETE THIS CONTACT?")

    if response:
        db_handler.delete_address(selected_entry_id)
        selected_entry_id = None
        display_listbox.delete(display_listbox.curselection()[0])

    

user_info_frame = tk.LabelFrame(frame, text="Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="new")

first_name_label = tk.Label(user_info_frame, text="First Name")
last_name_label = tk.Label(user_info_frame, text="Last Name")
address_label = tk.Label(user_info_frame, text="Address")
city_label = tk.Label(user_info_frame, text="City")
state_label = tk.Label(user_info_frame, text="State")
all_search = tk.Label(user_info_frame, text='Type "ALL" to search all names')

first_name_label.grid(row=0, column=0, padx=8, pady=0, sticky="w")
last_name_label.grid(row=0, column=1, sticky="w")
address_label.grid(row=2, column=0, padx=8, pady=0, sticky="w")
city_label.grid(row=2, column=1, sticky="w")
state_label.grid(row=2, column=2, padx=8, sticky="w")
all_search.grid(row=1, column=2, padx=10, sticky="n")

first_name_entry = tk.Entry(user_info_frame, width=30)
last_name_entry = tk.Entry(user_info_frame, width=30)
address_label_entry = tk.Entry(user_info_frame, width=30)
city_entry = tk.Entry(user_info_frame, width=30)

first_name_entry.grid(row=1, column=0, padx=10, pady=(0, 10))
last_name_entry.grid(row=1, column=1, padx=0, pady=(0, 10))
address_label_entry.grid(row=3, column=0, padx=0, pady=(0, 10))
city_entry.grid(row=3, column=1, padx=0, pady=(0, 10))

state_combobox = ttk.Combobox(user_info_frame, state="readonly", values=['','Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])
state_combobox.grid(row=3, column=2, padx=10, pady=(0, 10))

button_frame = tk.LabelFrame(frame, borderwidth=0)
button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="new")

button_add = tk.Button(button_frame, text="Add", width=13, height=1, command=enter_data)
button_search = tk.Button(button_frame, text="Search", width=13, height=1, command=search_data)
button_edit = tk.Button(button_frame, text="Edit", width=13, height=1, command=edit_address)
button_clear = tk.Button(button_frame, text="Clear", width=13, height=1, command=clear_screen)
button_delete = tk.Button(button_frame, text="Delete", width=13, height=1, command=delete_entry)

button_add.grid(row=0, column=0)
button_search.grid(row=0, column=1)
button_edit.grid(row=0, column=2)
button_clear.grid(row=0, column=3)
button_delete.grid(row=0, column=4)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(4, weight=1)

display_frame = tk.LabelFrame(frame, text="Display")
display_frame.grid(row=2, column=0, sticky="news", padx=20, pady=(10, 20))

display_frame.grid_columnconfigure(0, weight=1)
display_frame.grid_rowconfigure(0, weight=1)

display_listbox = tk.Listbox(display_frame, height=10, font=('Arial', 12))
display_listbox.grid(row=0, column=0, padx=3, pady=(3, 5), sticky="news")
display_listbox.bind('<<ListboxSelect>>', on_select)

if __name__ == "__main__":
    root.mainloop()











