# --------------------------------------- Required Lib --------------------------------------- #
import os 
import re 
import random 
import base64 
import hashlib 
import requests 
import datetime 
import tkinter as tk 
import mysql.connector 
from tkinter import ttk 
from tkinter import filedialog 
from mysql.connector import Error 
import tkinter.messagebox as messagebox 


code = str(random.randint(100000, 999999))
# --------------------------------------- Getting Input (sign_up_frame) --------------------------------------- #
def submit_sign_up():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get() 
    phone_number = phone_number_entry.get() 
    email = email_entry.get() 
    password = password_entry.get()  
    confirm_password= confirm_password_entry.get()
# --------------------------------------- Getting Input (sign_up_frame) --------------------------------------- #
def submit_sign_up():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get() 
    phone_number = phone_number_entry.get() 
    email = email_entry.get() 
    password = password_entry.get()  
    confirm_password= confirm_password_entry.get()

# --------------------------------------- Checking Email Pattern (sign_up_frame) --------------------------------------- #
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(email):
        messagebox.showerror("Error", "Invalid Email")
        return

# --------------------------------------- Checking First Name Length (sign_up_frame) --------------------------------------- #
    if len(first_name) > 12 or len(first_name) < 3:
        messagebox.showerror("Error", "First Name must be at least 3 characters and no longer than 12 characters")
        return

# --------------------------------------- Checking Last Name Length (sign_up_frame) --------------------------------------- #
    if len(last_name) > 12 or len(last_name) < 3:
        messagebox.showerror("Error", "Last Name must be at least 3 characters and no longer than 12 characters")
        return

# --------------------------------------- Checking Phone Number (sign_up_frame) --------------------------------------- #
    if not phone_number.isdigit() or len(phone_number) != 10:
        messagebox.showerror("Error", "Phone Number must only contain numbers and be 10 digits long")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Password and Confirm Password do not match")
        return
# --------------------------------------- Checking strength of Password (sign_up_frame) --------------------------------------- #
    password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,24}$')
    if not password_pattern.match(password):
        messagebox.showerror("Error", "Password must be \n # at least 8 characters \n # no longer than 24 characters \n # at lest one number \n # one special character")
        return
    
# --------------------------------------- Hashing Password (sign_up_frame) --------------------------------------- #
    password =password.encode()
    password = hashlib.sha256(password).hexdigest()
    
# --------------------------------------- Connecting To Database (sign_up_frame) --------------------------------------- #
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securefile"
    )

# --------------------------------------- Chicking Availability Of Email and Phone Number (sign_up_frame) --------------------------------------- #
    # Create a cursor object to execute SQL queries
    cursor = mydb.cursor()
    check_user_query = "SELECT * FROM userdata WHERE email_address =%s OR phone_number=%s"
    cursor.execute(check_user_query, (email, phone_number))
    result = cursor.fetchone()
    if result:
        messagebox.showerror("Error", "Email or Phone number already in use")
    else:
        verify_email()
# --------------------------------------- Sending Mail --------------------------------------- #
    def ceaser_cipher(ciphertext, term, total_chars):
        apikey = ""
        for i, char in enumerate(ciphertext):
            shift = term[i % len(term)]
            if char.isalpha():
                if char.isupper():
                    shift_char = chr((ord(char) - shift - 65 + 26) % 26 + 65)
                    apikey += shift_char
                else:
                    shift_char = chr((ord(char) - shift - 97 + 26) % 26 + 97)
                    apikey += shift_char
            elif char.isdigit():
                shift_char = chr((ord(char) - shift - 48 + 10) % 10 + 48)
                apikey += shift_char
            else:
                apikey += char
        return apikey

    
# --------------------------------------- Sending Mail --------------------------------------- #
    def decrypt_file():
        ciphertext = "MHl4MTgxOTZkMTYzODc2NGY4NHduZzN2MjIzazFyaXUtNDdxdzk2NGotdno1OGI4YTg="
        ciphertext = base64.b64decode(ciphertext.encode()).decode()
        total_chars = len(ciphertext)
        a = 12345678
        term = []
        for n in range(1, total_chars):
            if (ord(ciphertext[n]) >= 65 and ord(ciphertext[n]) <= 90) or (ord(ciphertext[n]) >= 97 and ord(ciphertext[n]) <= 122):
                t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
            else:
                t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
            term.append(t)


        apikey = ceaser_cipher(ciphertext, term, total_chars)    
        
        endpoint = "https://api.mailgun.net/v3/sandbox63bc9e703d3842f4932630753e1030d6.mailgun.org/messages"
        api_key=apikey
        to = email
        subject = "Complete Your Email Verification"
        body = f"""Dear Valued Customer,
        We hope this message finds you well. Please take a moment to complete your email verification process by entering the following code: {code}.
        Your email verification ensures that you can receive important updates and information from our services.
        Thank you for your time and cooperation. If you have any questions or concerns, please do not hesitate to reach out to us.
        Best Regards,
        The Secure File Transfer Protocol Team"""

        return requests.post(
            endpoint,
            auth=("api", api_key),
            data={
                "from":"Mailgun Sandbox <postmaster@sandbox63bc9e703d3842f4932630753e1030d6.mailgun.org>",
                "to": to,
                "subject": subject,
                "text": body
            }
        )
    decrypt_file()
    return first_name,last_name,phone_number,email,password,confirm_password

# --------------------------------------- Inserting Data inside Database (sign_up_frame) --------------------------------------- #
def verify_code_function(sign_up_values):
    first_name, last_name, phone_number, email, password, confirm_password = sign_up_values    
    verify_code = verify_code_entry.get()
    if verify_code == "":
        messagebox.showerror("Error","Verification code cannot be empty.")
        return
    
    if verify_code != code:
        messagebox.showerror("Error","Invalid Verification code.")
        return
    
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="securefile"
        )
        mycursor = mydb.cursor()
        
        sql = "INSERT INTO userdata (first_name, last_name, email_address, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
        val = (first_name, last_name, email, phone_number, password)
        
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()

        if messagebox.showinfo("Success", "Email Verified!\n Account Created Successfully.") == "ok":
            log_in_after_verification()
            first_name_entry.delete(0, "end")
            last_name_entry.delete(0, "end")
            phone_number_entry.delete(0, "end")
            email_entry.delete(0, "end")
            password_entry.delete(0, "end")
            confirm_password_entry.delete(0, "end")
    except Error:
        messagebox.showerror("Error", "Failed to create account. Please try again later.")
        
        first_name_entry.delete(0, "end")
        last_name_entry.delete(0, "end")
        phone_number_entry.delete(0, "end")
        email_entry.delete(0, "end")
        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")
        verify_email()
        

def validate_log_in_credentials():
    log_email = log_email_entry.get()
    log_password = log_password_entry.get()
    
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(log_email):
        messagebox.showerror("Error", "Invalid Email")
        return
    log_password =log_password.encode()
    log_password = hashlib.sha256(log_password).hexdigest()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securefile"
    )

    cursor = mydb.cursor()
    query = "SELECT email_address, password, id FROM userdata WHERE email_address=%s and password=%s"
    cursor.execute(query, (log_email, log_password))
    result = cursor.fetchone() 

    if result:
        current_user_id = result[2]
        show_home_page(current_user_id)
        return 
    else:
        messagebox.showerror("Error", "Invalid Credentials")
        return False

def show_sign_up():
    main_frame.grid_forget()
    sign_up_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

# --------------------------------------- Switching to (log_in_frame) --------------------------------------- #    
def show_log_in():
    main_frame.grid_forget()
    log_in_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

# --------------------------------------- Switching to (verify_email_frame) --------------------------------------- #  
def verify_email():
    sign_up_frame.grid_forget()
    verify_email_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
    
        
# --------------------------------------- Switching Back to (main_frame) --------------------------------------- #
def back_to_main():
    sign_up_frame.grid_forget()
    log_in_frame.grid_forget()
    main_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
        
# --------------------------------------- Switching to (home_page_frame) --------------------------------------- #
def show_home_page(current_user_id):
    main_frame.grid_forget()
    home_page_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
    
# --------------------------------------- Connect to the database and retrieve the user data --------------------------------------- #
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securefile"
    )
    cursor = mydb.cursor()
    query = "SELECT first_name, last_name FROM userdata WHERE id = %s"
    cursor.execute(query, (current_user_id,))
    result = cursor.fetchone()

    if result:
        full_name = str(result[0]) + " " + str(result[1])
        home_text = ttk.Label(home_page_frame, text=f"Welcome, {full_name}", font=("Helvetica", 15), foreground="white", background="#006466")
        home_text.grid(row=0, column=1, pady=20, padx=10)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="securefile"
        )
        cursor = mydb.cursor()
        query = "SELECT file_name FROM filestorage WHERE user_id = %s"
        cursor.execute(query, (current_user_id,))
        file_names = cursor.fetchall()

        if file_names:
            row = 3
            column = 0
            files_text = ttk.Label(home_page_frame, text="Files:", font=("Helvetica", 15), foreground="white", background="#006466")
            files_text.grid(row=2, column=0, pady=10, padx=20,sticky="w")

            
            for i in range(len(file_names)):
                # Use bubble sort to sort the list of file names in ascending order
                for j in range(len(file_names) - i - 1):
                    if file_names[j] > file_names[j + 1]:
                        file_names[j], file_names[j + 1] = file_names[j + 1], file_names[j]
            for i, file_name in enumerate(file_names):
                file_path = r"C:\Users\utkar\Desktop\cw2\\" + str(file_name[0])


                def ceaser_cipher(ciphertext, term, total_chars):
                    plaintext = ""
                    for i, char in enumerate(ciphertext):
                        shift = term[i % len(term)]
                        if char.isalpha():
                            if char.isupper():
                                shift_char = chr((ord(char) - shift - 65 + 26) % 26 + 65)
                                plaintext += shift_char
                            else:
                                shift_char = chr((ord(char) - shift - 97 + 26) % 26 + 97)
                                plaintext += shift_char
                        elif char.isdigit():
                            shift_char = chr((ord(char) - shift - 48 + 10) % 10 + 48)
                            plaintext += shift_char
                        else:
                            plaintext += char
                    return plaintext
                
# --------------------------------------- Generate Algorythm To decrypt the text --------------------------------------- #
                def open_file(file_path):
                    with open(file_path, "r") as f:
                        cipher_text = f.read()

                    ciphertext = base64.b64decode(cipher_text.encode()).decode()
                    total_chars = len(ciphertext)
                    a = current_user_id
                    term = []
                    for n in range(1, total_chars):
                        if (ord(ciphertext[n]) >= 65 and ord(ciphertext[n]) <= 90) or (ord(ciphertext[n]) >= 97 and ord(ciphertext[n]) <= 122):
                            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
                        else:
                            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
                        term.append(t)
                    plaintext = ceaser_cipher(ciphertext, term, total_chars)

                    read_file_window = tk.Toplevel(home_page_frame)
                    read_file_window.title(str(file_name))
                    screen_width = read_file_window.winfo_screenwidth()
                    screen_height = read_file_window.winfo_screenheight()
                    window_width = 400
                    window_height = 400
                    x_coordinate = (screen_width/2) - (window_width/2)
                    y_coordinate = (screen_height/2) - (window_height/2)

                    read_file_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
                    text = tk.Text(read_file_window, font=("Helvetica", 12))
                    text.pack(fill="both", expand=True)
                    text.insert("1.0", plaintext)
                    text.config(state="disabled")

                file_name = str(file_name[0])
                new_file_name = ".".join(file_name.rsplit(".", 2)[:1]) + ".txt"
                browse_button = tk.Button(home_page_frame, text=str(new_file_name), command=lambda file_path=file_path: open_file(file_path), font=("Helvetica", 10), 
                                background="#006466", foreground="white", relief="raised", 
                                activebackground="#006466", activeforeground="#c5c3c6")
                browse_button.grid(row=row, column=column, padx=(10),pady=(10))
                browse_button.config(width=18)

                column += 1
                if column == 3:
                    row += 1
                    column = 0
        else:
            files_text = ttk.Label(home_page_frame, text="No files found", font=("Helvetica", 12), foreground="white", background="#006466")
            files_text.grid(row=2, column=0, columnspan=3, pady=10, padx=(50,70)) 

# --------------------------------------- Search Entry code --------------------------------------- #
        search_entry = ttk.Entry(home_page_frame, width=20, font=("Helvetica", 12), foreground="#006466", style="Round.TEntry",justify='center')
        search_entry.grid(row=1, column=1, padx=10, pady=10)
        search_button = tk.Button(home_page_frame, text="Search", command=lambda:search_files(), font=("Helvetica", 10), background="#065a60", foreground="white", relief="raised", bd=1, activebackground="#144552", activeforeground="#c5c3c6")
        search_button.grid(row=1, column=2, padx=(65,0),pady=5,sticky="w")
        search_button.config(width=7)

# --------------------------------------- Search For Files --------------------------------------- # 
        def search_files():
            search_string = search_entry.get()
            search_results = []

            for file_name in file_names:
                if search_string in str(file_name[0]):
                    search_results.append(file_name[0])

            if search_results:
                search_window = tk.Toplevel(home_page_frame)
                search_window.title("Search Results")
                screen_width = search_window.winfo_screenwidth()
                screen_height = search_window.winfo_screenheight()
                window_width = 400
                window_height = 400
                x_coordinate = (screen_width/2) - (window_width/2)
                y_coordinate = (screen_height/2) - (window_height/2)
                search_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
                search_window.config(bg="#006466")
                results_text = ttk.Label(search_window, text="Results", font=("Helvetica", 15), foreground="white", background="#006466")
                results_text.grid(row=0, column=0, pady=10, padx=50,sticky="n")
                result_row = 2
                result_column = 0

                for result in search_results:
                    result_button = tk.Button(search_window, text=result, command=lambda file_path=rf"C:\Users\utkar\Desktop\cw2\{result}": open_file(file_path), font=("Helvetica", 10), 
                    background="#006466", foreground="white", relief="raised", 
                    activebackground="#006466", activeforeground="#c5c3c6")
                    
                    result_button.grid(row=result_row, column=result_column, padx=(30),pady=(10))
                    result_button.config(width=40)
                    result_row += 1
            else:
                messagebox.showerror("Error", "No search results found")           

        def insert_into_database(file_path):
            mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="",
                            database="securefile"
                        )
            cursor = mydb.cursor()
            query = "INSERT INTO filestorage (user_id, time, file_name) VALUES (%s, %s, %s)"
            original_file_name = os.path.basename(file_path)
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_file_name = f"{os.path.splitext(original_file_name)[0]}.{time_stamp}{os.path.splitext(original_file_name)[1]}"
            values = (current_user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_file_name)
            cursor.execute(query, values)
            mydb.commit()

            def ceaser_cipher(plaintext, term, total_chars):
                ciphertext = ""
                for i, char in enumerate(plaintext):
                    shift = term[i % len(term)]
                    if char.isalpha():
                        if char.isupper():
                            shift_char = chr((ord(char) + shift - 65) % 26 + 65)
                            ciphertext += shift_char
                        else:
                            shift_char = chr((ord(char) + shift - 97) % 26 + 97)
                            ciphertext += shift_char
                    elif char.isdigit():
                        shift_char = chr((ord(char) + shift - 48) % 10 + 48)
                        ciphertext += shift_char
                    else:
                        ciphertext += char
                b64_ciphertext = base64.b64encode(ciphertext.encode()).decode()
                return b64_ciphertext

            with open(file_path, "r") as f:
                file_content = f.read()
                term = []
            a = current_user_id
            total_chars = len(file_content)
            plaintext = file_content
            for n in range(1, total_chars):
                if (ord(plaintext[n]) >= 65 and ord(plaintext[n]) <= 90) or (ord(plaintext[n]) >= 97 and ord(plaintext[n]) <= 122):
                    t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
                else:
                    t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
                term.append(t)
            ciphertext = ceaser_cipher(plaintext, term, total_chars)
            
            new_file_path = r"C:\Users\utkar\Desktop\cw2\\" + new_file_name
            with open(new_file_path, "w") as f:
                f.write(ciphertext)
            messagebox.showinfo("Success", "File successfully uploaded")
                        
        def browse_file():
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                insert_into_database(file_path)

        browse_button = tk.Button(home_page_frame, text="Browse", command=lambda: browse_file(), font=("Helvetica", 10), 
                        background="#065a60", foreground="white", relief="raised", bd=1, 
                        activebackground="#144552", activeforeground="#c5c3c6")
        browse_button.grid(row=1, column=0, padx=(20,10),pady=5,sticky="nw")
        browse_button.config(width=7)

        refresh_button = tk.Button(home_page_frame, text="refresh", command=lambda: show_home_page(current_user_id), font=("Helvetica", 10), 
                        background="#065a60", foreground="white", relief="raised", bd=1, 
                        activebackground="#144552", activeforeground="#c5c3c6")
        refresh_button.grid(row=2, column=2, padx=(25,10),pady=5,sticky="n")
        refresh_button.config(width=7)  
    else:
        return

# --------------------------------------- Switching to (open_file_frame) --------------------------------------- # 
def open_file_format():
    home_page_frame.grid_forget()
    open_file_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
       
def log_in_after_verification():
    verify_email_frame.grid_forget()
    log_in_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
# --------------------------------------- ------------------------------ --------------------------------------- # 
# --------------------------------------- GUI USING TKINTER --------------------------------------- # 

root = tk.Tk()
root.geometry("600x600")
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4.5
root.geometry("+%d+%d" % (x, y)) 
main_frame = tk.Frame(root, bg="#006466")

    
main_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
for i in range(12):
    root.rowconfigure(i, minsize=50)
for i in range(12):
    root.columnconfigure(i, minsize=50)
    
project_text = ttk.Label(main_frame, text="Secure File Vault", 
                         font=("Travelast", 30), foreground="white", background="#006466")
project_text.grid(row=0, column=2, columnspan=1, pady=20, padx=50)
    
by_text = ttk.Label(main_frame, text="by", font=("Hanging Letters", 25), foreground="white", 
                    background="#006466")
by_text.grid(row=1, column=2, columnspan=1, pady=10, padx=10)

name_text = ttk.Label(main_frame, text="Utkarsha Subedi", font=("3x5", 35), foreground="white", 
                      background="#006466")
name_text.grid(row=2, column=2, columnspan=1, pady=(10,80), padx=10 ,sticky='n')

    
back_button = tk.Button(main_frame, text="Sign Up", command=show_sign_up, font=("Helvetica", 13), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="#1985a1")
back_button.grid(row=4, column=2,sticky="s", padx=250, pady=10)
back_button.config(width=8)

    
back_button = tk.Button(main_frame, text="Log In", command=show_log_in, font=("Helvetica", 13), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="#c5c3c6")
back_button.grid(row=5, column=2,sticky="s", padx=250, pady=10)
back_button.config(width=8)
    
back_button = tk.Button(main_frame, text="Exit", command=root.quit, font=("Helvetica", 13), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="red")
back_button.grid(row=6, column=2, sticky="s", padx=250, pady=10)
back_button.config(width=8)

work_text = ttk.Label(main_frame, text="Protecting your precious memories, one file at a time.", 
                      font=("Helvetica",10), foreground="white", background="#006466")
work_text.grid(row=8, column=2, columnspan=1, pady=(80,5), padx=50)

    
style = ttk.Style()
style.configure("Round.TEntry", fieldbackground="#ffffff", background="transparent", 
                 bd=5, relief="flat", padding=2, borderwidth=2,
                 highlightcolor="#597678", highlightbackground="#597678", 
                 borderradius=10)    
sign_up_frame = tk.Frame(root, bg="#006466")
sign_up_text = ttk.Label(sign_up_frame, text="Sign Up", font=("Travelast", 25), foreground="white", 
                         background="#006466")
sign_up_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50, sticky="nw")

# --------------------------------------- First Name (sign_up_frame) --------------------------------------- #
    
first_name_label = tk.Label(sign_up_frame, text="First Name:", font=("Helvetica", 14), 
                            foreground="white", background="#006466")
first_name_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                             foreground="#006466", style="Round.TEntry", background='gray')
first_name_entry.configure(background='gray')

first_name_label.grid(row=1, column=1, padx=20, pady=10, sticky="W")
first_name_entry.grid(row=1, column=2, padx=10, pady=10, sticky="W")

last_name_label = tk.Label(sign_up_frame, text="Last Name:", font=("Helvetica", 14), 
                           foreground="white", background="#006466")
last_name_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                            foreground="#006466", style="Round.TEntry")

last_name_label.grid(row=2, column=1, padx=20, pady=10, sticky="W")
last_name_entry.grid(row=2, column=2, padx=10, pady=10, sticky="W")

phone_number_label = tk.Label(sign_up_frame, text="Phone Number:", font=("Helvetica", 14), 
                              foreground="white", background="#006466")
phone_number_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                               foreground="#006466",style="Round.TEntry")

phone_number_label.grid(row=3, column=1, padx=20, pady=10, sticky="W")
phone_number_entry.grid(row=3, column=2, padx=10, pady=10, sticky="W")

email_label = tk.Label(sign_up_frame, text="Email:", font=("Helvetica", 14), 
                       foreground="white", background="#006466")
email_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                        foreground="#006466", style="Round.TEntry")

email_label.grid(row=4, column=1, padx=20, pady=10, sticky="W")
email_entry.grid(row=4, column=2, padx=10, pady=10, sticky="W")
    
password_label = tk.Label(sign_up_frame, text="Password:", font=("Helvetica", 14), 
                          foreground="white", background="#006466")
password_entry = ttk.Entry(sign_up_frame, show="*", width=25, font=("Helvetica", 16), 
                           foreground="#006466", style="Round.TEntry")

password_label.grid(row=5, column=1, padx=20, pady=10, sticky="W")
password_entry.grid(row=5, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Confirm Password (sign_up_frame) --------------------------------------- #
confirm_password_label = tk.Label(sign_up_frame, text="Confirm Password:", font=("Helvetica", 14), 
                                  foreground="white", background="#006466")
confirm_password_entry = ttk.Entry(sign_up_frame, show="*", width=25, font=("Helvetica", 16), 
                                   foreground="#006466", style="Round.TEntry")

confirm_password_label.grid(row=6, column=1, padx=20, pady=10, sticky="W")
confirm_password_entry.grid(row=6, column=2, padx=10, pady=10, sticky="W")

def toggle_password_visibility(show_password_var):
    if show_password_var.get() == 1:
        confirm_password_entry.config(show="")
        password_entry.config(show="")
        show_password_checkbox.config(foreground="black")
    else:
        confirm_password_entry.config(show="*")
        password_entry.config(show="*")
        show_password_checkbox.config(foreground="white")

show_password_var = tk.IntVar(value=0)
show_password_checkbox = tk.Checkbutton(sign_up_frame, text="Show Password", variable=show_password_var,
                                        command=lambda: toggle_password_visibility(show_password_var),
                                        foreground="black", background="#006466")
show_password_checkbox.grid(row=7, column=2, padx=10, pady=10, sticky="W")


submit_button = tk.Button(sign_up_frame, text="Submit", command=submit_sign_up, font=("Helvetica", 12), 
                          background="#065a60", foreground="white", relief="raised", bd=3,
                          activebackground="#144552",activeforeground="#1985a1")
submit_button.grid(row=9, column=2,sticky="e",pady=10)
submit_button.config(width=8)


back_button = tk.Button(sign_up_frame, text="Back", command=back_to_main, font=("Helvetica", 12), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="red")
back_button.grid(row=11, column=1, sticky="sw",padx=10,pady=20)
back_button.config(width=8)


log_in_frame = tk.Frame(root, bg="#006466")

# --------------------------------------- log_in text (log_in_frame) --------------------------------------- #
log_in_text = ttk.Label(log_in_frame, text="Log In", font=("Travelast", 25), 
                        foreground="white", background="#006466")
log_in_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50)

# --------------------------------------- Email (log_in_frame) --------------------------------------- 
log_email_label = tk.Label(log_in_frame, text="Email:", font=("Helvetica", 14), 
                           foreground="white", background="#006466")
log_email_entry = ttk.Entry(log_in_frame, width=25, font=("Helvetica", 16), 
                            foreground="#006466", style="Round.TEntry")

log_email_label.grid(row=2, column=1, padx=20, pady=10, sticky="W")
log_email_entry.grid(row=2, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Password (log_in_frame) --------------------------------------- #
log_password_label = tk.Label(log_in_frame, text="Password:", font=("Helvetica", 14), 
                              foreground="white", background="#006466")
log_password_entry = ttk.Entry(log_in_frame, show="*", width=25, font=("Helvetica", 16), 
                               foreground="#006466", style="Round.TEntry")

log_password_label.grid(row=3, column=1, padx=20, pady=10, sticky="W")
log_password_entry.grid(row=3, column=2, padx=10, pady=10, sticky="W")
# --------------------------------------- Toogle password visibility (log_in_frame) --------------------------------------- #
def toggle_password_visibility_log_in(show_password_var_log_in):
    if show_password_var_log_in.get() == 1:
        log_password_entry.config(show="")
        show_password_checkbox.config(foreground="black")
    else:
        log_password_entry.config(show="*")
        show_password_checkbox.config(foreground="black")

show_password_var_log_in = tk.IntVar(value=0)
show_password_checkbox_log_in = tk.Checkbutton(log_in_frame, text="Show Password", variable=show_password_var_log_in,
                                        command=lambda: toggle_password_visibility_log_in(show_password_var_log_in),
                                        foreground="black", background="#006466")
show_password_checkbox_log_in.grid(row=4, column=2, padx=10, pady=10, sticky="W")


# --------------------------------------- Log In Button (log_in_frame) --------------------------------------- #
log_in_button = tk.Button(log_in_frame, text="Log In", command=validate_log_in_credentials, font=("Helvetica", 12), 
                          background="#065a60", foreground="white", relief="raised", bd=3, 
                          activebackground="#144552", activeforeground="#c5c3c6")
log_in_button.grid(row=5, column=2, padx=10,pady=50)
log_in_button.config(width=8)

# --------------------------------------- Back Button (log_in_frame) --------------------------------------- #
back_button = tk.Button(log_in_frame, text="Back", command=back_to_main, font=("Helvetica", 12), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="red")
back_button.grid(row=6, column=1, sticky="w",padx=10,pady=150)
back_button.config(width=8)

# --------------------------------------- Switch to (sign_up_frame) --------------------------------------- #

def show_sign_up_back():
    verify_email_frame.grid_forget()
    sign_up_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
        
# ---------------------------------------  Creating (log_in_frame) --------------------------------------- #
verify_email_frame = tk.Frame(root, bg="#006466")

# --------------------------------------- log_in text (log_in_frame) --------------------------------------- #
log_in_text = ttk.Label(verify_email_frame, text="Verify Email", font=("Travelast", 25), 
                        foreground="white", background="#006466")
log_in_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50)


# --------------------------------------- Footer Lable (main_frame) --------------------------------------- #
work_text = ttk.Label(verify_email_frame, text="We have sent 6 digit code in your email.Please kindly verify your Email.", 
                      font=("Helvetica",10), foreground="white", background="#006466")
work_text.grid(row=1, column=2, columnspan=1, pady=(10,20), sticky=("e"))


# --------------------------------------- Email (log_in_frame) --------------------------------------- # 
verify_code_entry = ttk.Entry(verify_email_frame, width=10, font=("Helvetica", 25), 
                            foreground="#006466", style="Round.TEntry",justify='center')
verify_code_entry.grid(row=3, column=2, padx=10, pady=10)

# --------------------------------------- Verify Button (verify_email_frame) --------------------------------------- #
verify_email_button = tk.Button(verify_email_frame, text="Verify", command=lambda: verify_code_function(submit_sign_up()), font=("Helvetica", 12), 
                          background="#065a60", foreground="white", relief="raised", bd=3, 
                          activebackground="#144552", activeforeground="#c5c3c6")
verify_email_button.grid(row=5, column=2, padx=10,pady=50)
verify_email_button.config(width=8)


# --------------------------------------- Back Button (log_in_frame) --------------------------------------- #
back_button = tk.Button(verify_email_frame, text="Back", command=show_sign_up_back, font=("Helvetica", 12), 
                        background="#065a60", foreground="white", relief="raised", bd=3, 
                        activebackground="#144552",activeforeground="red")
back_button.grid(row=6, column=1, sticky="w",padx=10,pady=150)
back_button.config(width=6)

# --------------------------------------- Refresh Frame --------------------------------------- #

def refresh_frame():
    home_page_frame.after(1000, refresh_frame)

home_page_frame = tk.Frame(root, bg="#006466")
open_file_frame = tk.Frame(root, bg="#006466")
