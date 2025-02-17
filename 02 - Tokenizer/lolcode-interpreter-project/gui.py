import tkinter as tk
from tkinter import *
from tkinter import filedialog, font, ttk
from lolcode_lexer import *
from lolcode_parser import *

# Global Variables
fileLoaded = False
filePath = ""

submitInput = False
userInput = ""

# Fonts
defaultFont = ("Microsoft YaHei UI", 8, "normal")
titleFont = ("Microsoft YaHei UI", 12, "bold") 
textEditorFont = ("Courier New", 11, "normal")
contentFont = ("Courier New", 10, "normal")

# GUI Functions
def insert_spaces(event):
    textEditor.insert(tk.INSERT, " " * 4)
    return 'break'

# Redirect printing messages from console into the gui
class RedirectToLabel:
    def __init__(self, label, update_function):
        self.label = label
        self.update_function = update_function

    def write(self, message):
        if message.strip():  # To avoid printing empty lines
            current_text = self.label.cget("text")
            new_text = current_text + "\n" + message.strip()  # Append new message
            self.update_function(new_text)  # Update label with accumulated text

    def flush(self):
        pass  # No need to handle flushing


# Program Functions
def open_file():
    global fileLoaded, filePath, characters
    filePath = filedialog.askopenfilename(title="Open File", filetypes=[("All files", "*.*")])
    if filePath:
        clear_table()
        fileLoaded = True
        filepathText.config(state=tk.NORMAL)
        filepathText.delete("1.0","end")
        filepathText.insert(tk.END, filePath)
        filepathText.config(state=tk.DISABLED)
        print("File opened.")
        
        with open(filePath, "r") as file:
            characters = file.read()
            textEditor.config(state=tk.NORMAL)
            textEditor.delete("1.0", "end")
            textEditor.insert("1.0", characters)
        # textEditor.config(state=tk.DISABLED)      # allow/deny text editing

def save_file():
    if filePath:
        with open(filePath, "w") as file:
            file.write(textEditor.get("1.0", "end-1c"))
        print("File saved successfully!")
    else:
        print("No file loaded to save.")

def exec_lolcode():
    statusLabel.config(text="")  # Clear current content in the label

    global characters
    characters = textEditor.get("1.0", "end-1c")
    if not characters:
        print("Error: No text in the editor to execute.")
        return
    tokens = lolcode_lex(characters)

    for row in lexemeTable.get_children():
        lexemeTable.delete(row)
    for token, tag in tokens:
        lexemeTable.insert("", "end", values=(token, tag))

    # REPLACE WITH 'KEYWORD'
    for i in range(len(tokens)):
        token = tokens[i]

        if token[1] not in (STRING, INTEGER, FLOAT, BOOLEAN, IDENTIFIER, NOOB, LITERAL_TYPE):
            token_update = (token[0], 'Reserved', token[1])
            tokens[i] = token_update

    env = generate_symtab(tokens)

    for row in symbolTable.get_children():
        symbolTable.delete(row)
    for identifier in env:
        symbolTable.insert("", "end", values=(identifier, env[identifier]))

def clear_table():
    for row in lexemeTable.get_children():
        lexemeTable.delete(row)
    for row in symbolTable.get_children():
        symbolTable.delete(row)

def get_input():
    global submitInput, userInput, submitFlag
    submitFlag.set(1)
    userInput = consoleInput.get(1.0, 'end').strip()
    submitInput = True
    consoleInput.delete(1.0, 'end')


# -----------------------------------------------------

root = tk.Tk()
root.title("LOLCODE Interpreter")

submitFlag = IntVar()

windowWidth = 1450
windowHeight = 800

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

positionTop = int((screenHeight - windowHeight) / 2)
positionLeft = int((screenWidth - windowWidth) / 2)

root.geometry(f'{windowWidth}x{windowHeight}+{positionLeft}+{positionTop}')
root.minsize(windowWidth, windowHeight)

font.nametofont("TkDefaultFont").configure(family=defaultFont[0], size=defaultFont[1])

topFrame = tk.Frame(root)
bottomFrame = tk.Frame(root)

# --------------------- Top Frame ---------------------
# Text Editor
textEditorFrame = tk.Frame(topFrame, width=400)
openfileUI = tk.Frame(textEditorFrame)
filepathText = tk.Text(openfileUI, height=1, width=45)
openfileButton = tk.Button(openfileUI, text="Open", command=open_file)
savefileButton = tk.Button(openfileUI, text="Save", command=save_file)
filepathText.configure(state=tk.DISABLED)

textEditFrame = tk.Frame(textEditorFrame)
textEditor = tk.Text(textEditFrame, height=10, width=60, wrap='none', font=textEditorFont)

textEditorvsb = ttk.Scrollbar(textEditFrame, orient="vertical", command=textEditor.yview)
textEditor.configure(yscrollcommand=textEditorvsb.set)
textEditorvsb.pack(side=tk.RIGHT, fill=tk.Y)

textEditorhsb = ttk.Scrollbar(textEditFrame, orient="horizontal", command=textEditor.xview)
textEditor.configure(xscrollcommand=textEditorhsb.set)
textEditorhsb.pack(side=tk.BOTTOM, fill=tk.X)

filepathText.pack(side=tk.LEFT, fill=tk.X, expand=True)
openfileButton.pack(side=tk.LEFT, fill=tk.X, expand=False)
savefileButton.pack(side=tk.LEFT, fill=tk.X, expand=False)
openfileUI.pack(side=tk.TOP, fill=tk.X, expand=False)
textEditor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

textEditFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
textEditorFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure("Custom.Treeview", font=contentFont)

# Lexemes Table
lexemeFrame = tk.Frame(topFrame, width=300)
lexemeTableLabel = tk.Label(lexemeFrame, text="Lexemes", font=titleFont)

lexemeTableFrame = tk.Frame(lexemeFrame, width=300)

lexemeTable = ttk.Treeview(lexemeTableFrame, columns=("lexeme", "classification"), show='headings', style="Custom.Treeview")
lexemeTable.heading("lexeme", text="Lexeme")
lexemeTable.heading("classification", text="Classification")

lexemeTable.column("lexeme", anchor="center", width=200)
lexemeTable.column("classification", anchor="center", width=200)

lexemevsb = ttk.Scrollbar(lexemeTableFrame, orient="vertical", command=lexemeTable.yview)
lexemeTable.configure(yscrollcommand=lexemevsb.set)
lexemevsb.pack(side=tk.RIGHT, fill=tk.Y)

lexemeTableLabel.pack(side=tk.TOP)
lexemeTable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
lexemeTableFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

lexemeFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Symbol Table
symbolFrame = tk.Frame(topFrame, width=300)
symbolTableLabel = tk.Label(symbolFrame, text="Symbol Table", font=titleFont)

symbolTableFrame = tk.Frame(symbolFrame, width=300)

symbolTable = ttk.Treeview(symbolTableFrame, columns=("identifier", "value"), show='headings', style="Custom.Treeview")
symbolTable.heading("identifier", text="Identifier")
symbolTable.heading("value", text="Value")

symbolTable.column("identifier", anchor="center", width=200)
symbolTable.column("value", anchor="center", width=200)

symbolvsb = ttk.Scrollbar(symbolTableFrame, orient="vertical", command=symbolTable.yview)
symbolTable.configure(yscrollcommand=symbolvsb.set)
symbolvsb.pack(side=tk.RIGHT, fill=tk.Y)

symbolTableLabel.pack(side=tk.TOP)
symbolTable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
symbolTableFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

symbolFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# ------------------- Bottom Frame --------------------
executeButton = tk.Button(bottomFrame, text="EXECUTE", font=titleFont, command=exec_lolcode)
executeButton.pack(side=tk.TOP, fill=tk.X)

panedWindow = tk.PanedWindow(bottomFrame, orient=tk.HORIZONTAL, sashwidth=0)
panedWindow.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

statusPanel = tk.Frame(panedWindow, width=800, bg='#FFFFFF')
statusCanvas = tk.Canvas(statusPanel, bg='#FFFFFF', height=150)
statusScrollbar = tk.Scrollbar(statusPanel, orient="vertical", command=statusCanvas.yview)
statusCanvas.configure(yscrollcommand=statusScrollbar.set)

statusFrame = tk.Frame(statusCanvas, bg='#FFFFFF')
statusLabel = tk.Label(
    statusFrame,
    text="Welcome to LOLCODE Interpreter!", 
    font=("Microsoft YaHei UI", 10, "bold"),  
    bg="#FFFFFF",
    anchor="nw",
    justify="left",
    padx=10  
)

statusLabel.pack(side=tk.TOP, anchor="w")

statusCanvas.create_window((0, 0), window=statusFrame, anchor="nw")
statusCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
statusScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

statusFrame.update_idletasks()
statusCanvas.config(scrollregion=statusCanvas.bbox("all"))

statusPanel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
panedWindow.add(statusPanel)

inputPanel = tk.Frame(panedWindow, width=200, bg='#FFFFFF')
inputPanel.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

submitButton = tk.Button(inputPanel, text="Submit Input", font=titleFont, command=get_input)
submitButton.pack(side=tk.TOP, fill=tk.X)

consoleInput = tk.Text(inputPanel, height=4, wrap="word", font=textEditorFont)
consoleInput.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

panedWindow.add(inputPanel)
panedWindow.paneconfigure(statusPanel, minsize=1000)
panedWindow.paneconfigure(inputPanel, minsize=0)

topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
bottomFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Function to Update the Status Label
def update_status(message):
    statusLabel.config(text=message)
    statusFrame.update_idletasks()
    statusCanvas.config(scrollregion=statusCanvas.bbox("all"))

# Redirect stdout to the statusLabel
sys.stdout = RedirectToLabel(statusLabel, update_status)

# Event Binds
textEditor.bind("<Tab>", insert_spaces)

root.mainloop()