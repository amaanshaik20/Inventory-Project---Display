import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys
from tkinter import  ttk
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk, font
import tkinter.font as tkFont

app = tk.Tk()
app.geometry("700x500")
app.title("INSERT LOOKUP")

# Label above the frame
instruction_label = ttk.Label(app, text="ADD LOOKUP TYPE", foreground="black", font=font.Font(size=11,weight='bold'))
instruction_label.place(relx=0.1, rely=0.1)



# Create a frame to hold the labels and entry fields with a scrollbar
frame = tk.Frame(app, borderwidth=2, relief="groove", border=2, bg="grey")
frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Function to add labels and entry fields to the scrollable frame
def add_label_and_entry(label_text, row):
    label = ttk.Label(scrollable_frame, text=label_text, font= custom_font)
    label.grid(row=row, column=0, sticky='w', padx=10, pady=5)  # Adjusted padx and pady for spacing

    if label_text == "ENABLED FLAG":
        entry = ttk.Combobox(scrollable_frame, values=['Y', 'N'], font=custom_font, width=18)
    else:
        entry = ttk.Entry(scrollable_frame,font=custom_font, width=20)
        
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry


# Create a custom font
custom_font = tkFont.Font(family="Verdana", size=10)

# Labels and entry fields
labels_and_entries = [
    ("LOOKUP TYPE", 14),
    ("TYPE DESCRIPTION", 15),
    ("ENABLED FLAG", 16)
]


entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def insert():
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                        'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                        'Database=InfraDB1;'
                        'Trusted_Connection=yes;')
        connection.autocommit = True

        # Get the current date and time as a string
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Assuming username is passed as a command-line argument or an empty string if not provided
        username = sys.argv[1] if len(sys.argv) > 1 else ''

        # Use a tuple to unpack the entry fields for the SQL query
        query_params = tuple(entry.get() for entry in entry_fields)

        # Add current_date and username to the tuple for query_params
        query_params += (current_date, username, current_date, username)

        # Use parameterized query to avoid SQL injection and handle date conversion
        connection.execute("""
            INSERT INTO Lookup_Type1 
            (LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG, 
            CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, query_params)

        info_label_invent = ttk.Label(app, text="DATA ADDED SUCCESSFULLY", foreground="GREEN")
        info_label_invent.place(relx=0.1, rely=0.90)  # Adjusted y-position+
        reset()

    except pyodbc.Error as ex:
        if 'Violation of UNIQUE KEY constraint' in str(ex):
            print("DATA ALREADY EXISTS")
            info_label_item = ttk.Label(app, text="DATA ALREADY EXISTS!!!", foreground="RED")
            info_label_item.place(relx=0.1, rely=0.90)
        else:
            print("CONNECTION FAILED", ex)

def reset():
    # Reset all entry fields to empty strings
    for entry in entry_fields:
        entry.delete(0, tk.END)


def cancel():
    app.destroy()

# Create a new frame for the buttons
button_frame = tk.Frame(app)
button_frame.place(relx=0.1, rely=0.8, relwidth=0.8)

# Function to create bold font
def get_bold_font():
    return font.Font(weight="bold")

# Create buttons with bold text
insert_button = tk.Button(button_frame, text="ADD", command=insert,
                          foreground="black", font=font.Font(size=10, weight="bold"), width=7, height=1, background="#e0e0e0")
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="CLEAR", command=reset,
                         foreground="black", font=font.Font(size=10, weight="bold"), width=7, height=1, background="#e0e0e0")
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="CANCEL", command=cancel,
                          foreground="black", font=font.Font(size=10, weight="bold"), width=7, height=1, background="#e0e0e0")
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)



app.mainloop()
