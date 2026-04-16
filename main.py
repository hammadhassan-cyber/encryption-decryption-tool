from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import base64
root = Tk()
root.title("Encryption and Decryption Tool")
root.geometry("600x408")
root.resizable(False, False)

# ==================== Creating Functions ===================
selected_file = None
def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = bytearray(file.read())

        for i in range(len(data)):
            data[i] = (data[i] + key) % 256

        output_path = file_path + ".enc"

        with open(output_path, "wb") as file:
            file.write(data)

        messagebox.showinfo("Success", f"File encrypted:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = bytearray(file.read())

        for i in range(len(data)):
            data[i] = (data[i] - key) % 256

        name = file_path[:-4]  # remove .enc
        output_path = name.replace(".", "_decrypted.", 1)

        with open(output_path, "wb") as file:
            file.write(data)

        messagebox.showinfo("Success", f"File decrypted:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def encrypt_data_function(text, key):
    data = bytearray(text.encode("utf-8"))

    for i in range(len(data)):
        data[i] = (data[i] + key) % 256

    # Convert to Base64 (ASCII only)
    encrypted = base64.b64encode(data).decode("utf-8")

    return encrypted

def encrypt_button_func():
    try:
        text = input_entry.get("1.0", END).strip()

        # If text exists then encrypt text
        if text != "":
            key_input = simpledialog.askinteger("Key", "Enter your encryption key: ")
            encrypted = encrypt_data_function(text, key_input)

            output_entry.delete("1.0", END)
            output_entry.insert(END, encrypted)
            return

        # If no text then ask for file
        file_path = filedialog.askopenfilename(
            title="Select File to Encrypt"
        )

        if file_path:
            key_input = simpledialog.askinteger("Key", "Enter your encryption key: ")
            encrypt_file(file_path, key_input)

    except:
        messagebox.showwarning("Error", "Invalid Input...")


def decrypt_data_function(text, key):
    data = bytearray(base64.b64decode(text))

    # Reverse encryption
    for i in range(len(data)):
        data[i] = (data[i] - key) % 256

    # Convert back to string
    return data.decode("utf-8")
    
def decrypt_button_func():
    try:
        text = input_entry.get("1.0", END).strip()

        # If text exists then decrypt text
        if text != "":
            key = simpledialog.askinteger("Key", "Enter decryption key")
            decrypted = decrypt_data_function(text, key)

            output_entry.delete("1.0", END)
            output_entry.insert(END, decrypted)
            return

        # Otherwise decrypt file
        file_path = filedialog.askopenfilename(
            title="Select Encrypted File",
            filetypes=[("Encrypted Files", "*.enc")]
        )

        if file_path:
            key = simpledialog.askinteger("Key", "Enter decryption key")
            decrypt_file(file_path, key)

    except:
        messagebox.showerror("Error", "Invalid Input")

def save_into_file():
    encrypted_data = output_entry.get("1.0", END)

    if encrypted_data == "":
        messagebox.showwarning("Warning", "File is empty!")
        return
    
    file = filedialog.asksaveasfile(defaultextension=".txt")
    if file:
        file.write(encrypted_data)
        file.close()
        messagebox.showinfo("Success", "File saved successfully!")

def load_file_data():
    global selected_file
    try:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        selected_file = file_path

        # If text file then show content
        if file_path.endswith(".txt"):
            with open(file_path, "r") as file:
                data = file.read()
                input_entry.delete("1.0", END)
                input_entry.insert(END, data)
        else:
            # For images/docs, just show file info
            input_entry.delete("1.0", END)
            # input_entry.insert(END, f"Selected File:\n{file_path}\n\n(Click Encrypt to process file)")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    input_entry.delete(1.0, END)
    output_entry.delete(1.0, END)

def exit_program():
    root.quit()

# =================== Main Heading Frame ====================
main_frame = Frame(root, bg="darkslategrey", relief=GROOVE, bd=4)
main_frame.grid(padx=1, pady=1)

main_heading = Label(main_frame, text="Encryption and Decryption Tool", font="Times 20 bold"
                     , bg="lightgrey", fg="black")
main_heading.grid(padx=1, pady=1, ipadx=100, ipady=5)


# =================== Creating Input label and entries ===================
encryption_frame = Frame(root, bg="darkslategrey", relief=RIDGE, bd=0)
encryption_frame.grid(row=1, padx=1, pady=1)
# -------------------------------- # ----------------------------------- #

input_frame = Frame(encryption_frame, bg="darkslategrey", relief=SUNKEN, bd=0)
input_frame.grid(padx=1, pady=1)

input_label = Label(input_frame, text="Your input text here...", font="Times 15",
                    bg="lightgrey", fg="black")
input_label.grid(row=0, padx=2, pady=2, ipadx=207)

input_entry = Text(input_frame, font="Calibri 12", width=73, height=5)
input_entry.grid(row=1, padx=2, pady=2, ipadx=2)
# input_entry.insert(1.0, "Write your text here...")

# =================== Creating Output label and entries ===================
decryption_frame = Frame(root, bg="darkslategrey", relief=RIDGE, bd=0)
decryption_frame.grid(row=2, padx=1, pady=1)
# -------------------------------- # ----------------------------------- #

output_frame = Frame(decryption_frame, bg="darkslategrey", relief=SUNKEN, bd=0)
output_frame.grid(padx=1, pady=1)

output_label = Label(output_frame, text="Your Output here...", font="Times 15",
                    bg="lightgrey", fg="black")
output_label.grid(row=0, padx=2, pady=2, ipadx=217)

output_entry = Text(output_frame, font="Calibri 12", width=73, height=5)
output_entry.grid(row=1, padx=2, pady=2, ipadx=2)
output_entry.insert(1.0, "Your output text here...")

# =========================== Creating Buttons ===========================
buttons_frame = Frame(root, bg="darkslategrey", relief=GROOVE, bd=0)
buttons_frame.grid(row=3, padx=1, pady=1, ipadx=0, ipady=1)
# -------------------------------- # ----------------------------------- #

encrypt_btn = Button(buttons_frame, text="Encrypt Data/File", font="Times 13", bg="darkslategray", fg="white", 
                     command=encrypt_button_func)
encrypt_btn.grid(row=0, column=0, ipadx=12, padx=3)

file_save_btn = Button(buttons_frame, text="Save Output", font="Times 13", bg="darkslategray", fg="white", 
                       command=save_into_file)
file_save_btn.grid(row=0, column=1, ipadx=26, padx=3)

decrypt_btn = Button(buttons_frame, text="Decrypt Data/File", font="Times 13", bg="darkslategray", fg="white",
                     command=decrypt_button_func)
decrypt_btn.grid(row=1, column=0, ipadx=11, padx=3)

load_file_btn = Button(buttons_frame, text="Load Output", font="Times 13", bg="darkslategray", fg="white", 
                       command=load_file_data)
load_file_btn.grid(row=0, column=2, ipadx=30, padx=3)

load_file_btn = Button(buttons_frame, text="Clear Fields", font="Times 13", bg="darkslategray", fg="white", 
                       command=clear_fields)
load_file_btn.grid(row=1, column=1, ipadx=25, padx=3)

load_file_btn = Button(buttons_frame, text="Exit Tool", font="Times 13", bg="darkslategray", fg="white", 
                       command=exit_program)
load_file_btn.grid(row=1, column=2, ipadx=40, padx=3)

root.mainloop()
