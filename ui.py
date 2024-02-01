import tkinter as tk
from tkinter import ttk  # Import additional widgets for improved styling
import imaplib
import email
import datetime

scan_senders=["dhanvantarict@gmail.com","hr.ctscan@gmail.com"]

# Define window size and padding
window_width = 300
window_height = 900
pad_x = 10
pad_y = 5

# Create the main window
root = tk.Tk()
root.title("Login")
root.geometry(f"{window_width}x{window_height}")  # Set window size

# Create logo (optional)
logo_image = tk.PhotoImage(file="logo2.png")  # Replace with your logo image path
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(pady=pad_y)  # Add padding above and below

# Create username label and entry field
username_label = ttk.Label(root, text="Username:")
username_label.pack(padx=pad_x, pady=pad_y)

username_entry = ttk.Entry(root)
username_entry.insert(0,'gawaisanjit@gmail.com')
username_entry.pack(padx=pad_x, pady=pad_y)

# Create password label and entry field
password_label = ttk.Label(root, text="Password:")
password_label.pack(padx=pad_x, pady=pad_y)

password_entry = ttk.Entry(root, show="*")  # Hide password characters
password_entry.insert(0,'feun xsng mwjh dzxc')
password_entry.pack(padx=pad_x, pady=pad_y)

# Create login button
login_button = ttk.Button(root, text="Login", command=lambda: check_login(username_entry.get(), password_entry.get()))
login_button.pack(padx=pad_x, pady=pad_y)

# Define error message label (optional)
error_label = ttk.Label(root, text="", foreground="red")  # Initially empty, red for errors
error_label.pack(padx=pad_x, pady=pad_y)
def check_logout(login_button,logout_button):
    login_button.config(state=tk.NORMAL)
    logout_button.config(state=tk.DISABLED)
    pass
def check_login_credentials(server,username,app_password):
    try:
        
        server.login(username, app_password)
        return 1
    except Exception as e :
        print(e)
        return -1
        pass
    pass
def get_attachments(email_message):
    attachments=[]
    for part in email_message.walk():
        print(part.get_filename())
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append(filename)
    print(attachments)
    return attachments
def populate_email(server,tree):
    server.select("INBOX")
    # Get today's date in UTC
    today = datetime.datetime.now(datetime.timezone.utc).date()
    today_str = today.strftime("%d-%b-%Y")  # Adjust format as needed

    # Search emails from today backwards
    search_criteria = "(SINCE {})".format(today_str)
    result, data = server.search(None, search_criteria)
    uids = data[0].split()

    # Process each email
    for uid in uids[::-1]:  # Reverse order for backward iteration
        _, data = server.fetch(uid, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        #print(email_message)
        # Extract relevant information (e.g., headers, body)
        sender = email_message["From"]
        email_address = email.utils.parseaddr(sender)[1]
        if email_address in scan_senders:
            
            subject = email_message["Subject"]
            print("From:", sender )
            print("Subject:", subject)
            tree.insert("", tk.END, values=(sender, subject))
            attachments = get_attachments(email_message)
            print(attachments)
            
def check_login(username, password):
    # Replace with your actual authentication logic
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    status = check_login_credentials(server,username,password)
    if status == 1:
        print("Login successful!")
        logout_button = ttk.Button(root, text="Logout", command=lambda: check_logout(login_button,logout_button))
        logout_button.pack(padx=pad_x, pady=pad_y)
        login_button.config(state=tk.DISABLED)
        #root.destroy()  # Close the window on successful login
        error_label.config(text="Login Successful")
        tree = ttk.Treeview(root)
        tree.pack(fill=tk.BOTH, expand=True)
        tree["columns"] = ("column1", "column2","column3","column4")
        tree.heading("column1", text="Sender")
        tree.heading("column2", text="Subject")
        tree.heading("column3",text="Attachments")
        tree.heading("column4",text="Status")
        tree.column('#0',width=1)
        tree.column('column1',width=100)
        tree.column('column2',width=100)

        # Insert items with multiple columns
        #tree.insert("", tk.END, values=("Item 1", "Value A"))
        #tree.insert("", tk.END, values=("Item 2", "Value B"))
        populate_email(server,tree)
        
        

    else:
        error_label.config(text="Invalid username or password")

# Start the event loop
root.mainloop()