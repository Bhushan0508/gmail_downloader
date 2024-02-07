import tkinter as tk
from tkinter import ttk  # Import additional widgets for improved styling
import imaplib
import email
import datetime
from googleapiclient.discovery import build
import re
import threading
import time
import queue
import os
import gdrive_downloader
import pyautogui
import time
#from datetime import datetime, timedelta

# Replace with your downloaded credentials JSON file path
CREDENTIALS_FILE = 'credentials.json'

# Define scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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

tooltip = ttk.Label(root, text="Body")
tooltip.pack(padx=pad_x, pady=pad_y)

# Define error message label (optional)
error_label = ttk.Label(root, text="", foreground="red")  # Initially empty, red for errors
error_label.pack(padx=pad_x, pady=pad_y)

message_label = ttk.Label(root, text="", foreground="blue")  # Initially empty, blue for errors
message_label.pack(padx=pad_x, pady=pad_y)



update_queue = queue.Queue()



tree = ttk.Treeview(root)
gdrive_downloader.init_gdrive()
frame1 = tk.Frame(root)
frame1.pack(padx=pad_x,pady=pad_y)
def open_dicom_viewer(scan_file):
    pyautogui.hotkey("win")  # Open Run dialog
    time.sleep(1)
    pyautogui.write("terminator")
    pyautogui.press("enter")  # Open Notepad
    time.sleep(1)  # Wait for Notepad to open
    #pyautogui.hotkey("ctrl", "o")  # Open file dialog
    pyautogui.write("bhushan")
    pyautogui.press("enter")  # Open the file
    pass
def open_scan(tree):
    print("opening scan...")
    selected_item_id = tree.focus()
    print(selected_item_id)
    if selected_item_id != '':
        selected_item = tree.item(selected_item_id)
        print(selected_item)
        open_dicom_viewer(selected_item['values'][3])
    pass


def show_tooltip(event):
    str_row = tree.identify_row(event.y)
    #rowindex = int(str_row.replace('I',' '))
    print('row:=',str_row,'type:=',type(str_row))
    str_column = tree.identify_column(event.x)
    print('str_column:=',str_column)
    for item_id in tree.get_children():
        if str_row == item_id:
            print("item_id:=",item_id)
            item_data = tree.item(item_id)["values"]
            text =item_data[2]# tree.item(item, "values")[2]  # Retrieve text from relevant column
            tooltip.config(text=text)
            #tooltip.place(x=event.x + 10, y=event.y + 10)

tree.bind("<Enter>", show_tooltip)
tree.bind("<Leave>", lambda _: tooltip.pack_forget())


open_button = ttk.Button(frame1,text="open",command=lambda: open_scan(tree))
open_button.pack(side='left',fill="x")

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
        #print(part)
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append(filename)
    #print(attachments)
    return attachments

def extract_drive_links(email_content):
    print('Extracting drive links')
    drive_links = []
    for part in email_content.walk():
        if part.get_content_type() == 'text/plain':  # Text content
            text = part.get_payload(decode=True).decode('utf-8')
            print(text)
            drive_link_match = re.search(r"https://drive.google.com/file/d/(.+?)/", text)
            if drive_link_match:
                drive_links.append(drive_link_match.group(0))   
    return drive_links
def get_body(email_message):
    print('Getting Body...')
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':  # Text content
            text = part.get_payload(decode=True).decode('utf-8')
            lines = text.splitlines()
            output=''
            for line in lines:
                output += '['+line+']'
            return output
    return "No Body"
    pass
def get_zip_filename(email_message):
    print("Getting ZIP File Name")
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':  # Text content
            text = part.get_payload(decode=True).decode('utf-8')
            #print(text)
            lines = text.splitlines()
            for line in lines:
                if '.ZIP' in line.upper():
                    print("Zip filename found:--",line)
                    return line.strip()


def clear_treeview(tree):
    if len(tree.get_children())>0:
        tree.delete(*tree.get_children())

class MultilineCell(tk.Frame):
    def __init__(self, master, text):
        super().__init__(master)
        self.text = tk.Text(self, wrap="word")
        self.text.insert("1.0", text)
        self.text.pack()
        
def populate_email(server,tree):
    server.select("INBOX")
    # Get today's date in UTC
    today = datetime.datetime.now(datetime.timezone.utc).date()
    today_str = today.strftime("%d-%b-%Y")  # Adjust format as needed

    # Search emails from today backwards
    search_criteria = "(SINCE {})".format(today_str)
    result, data = server.search(None, search_criteria)
    uids = data[0].split()
    print('Clearing the List View...')
    root.after(0, clear_treeview(tree))    
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
            
            attachments = get_attachments(email_message)
            drivelinks = extract_drive_links(email_message)
            print("Attachments:-",attachments)
            print("Drive Links:-",drivelinks)
            zipfilename = get_zip_filename(email_message)
            body = get_body(email_message)
            #bodycell = MultilineCell(tree,body)
            #download_image = tk.PhotoImage(file="download_icon.png")
            drive_file_id = ''
            if len(drivelinks) > 0: 
                drive_file_id = re.search(r"/file/d/(.*?)/", drivelinks[0]).group(1)
            tree.insert("", tk.END, values=(sender, subject,body,zipfilename,"Calculating...",drive_file_id))
            
def check_file_exists(filename,drive_file_id):
    downloads_path = os.path.expanduser("downloads")
    file_path = os.path.join(downloads_path, filename)
    if os.path.exists(file_path):
        print("The file({}) exists in the Downloads folder.",filename)
        return True
    else:
        print("The file does not exist in the Downloads folder.")
        print('Downloading the file...',filename)
        gdrive_downloader.download(drive_file_id,filename)
        return False
    pass
def check_download(tree):
    print("Checking if files are downloaded...")
    for item_id in tree.get_children():
        item_data = tree.item(item_id)["values"]
        print(item_data)
        print('Downloaded File Name:-',item_data[3])
        result = check_file_exists(item_data[3],item_data[5])
        if result == False:
            print('Start Downloading file')
        
def background_task(queue,server, tree):
    #for i in range(5):
    #    time.sleep(1)  # Simulate some work
    #    queue.put((i, f"Item {i}"))  # Add items to the queue
    print('starting email scanning ...')
    while True:
        try:
            message_label.config(text="Scanning emails...")
        
            populate_email(server, tree)
            
            root.after(0,check_download(tree))

            current_time = datetime.datetime.now()
            five_min_delta = datetime.timedelta(minutes=5)
            next_scan_time = current_time+five_min_delta
            print('next scan will start at ',next_scan_time)
            time.sleep(600)
        except Exception as e:
            print('Starting the background task again..')
            threading.Thread(target=background_task, args=(queue,server,tree,)).start()
            print('exiitng the current thread...')
            break

def update_treeview(tree):
    #print("updating tree view...")
    if not update_queue.empty():
        item_id, item_text = update_queue.get()
        tree.insert("", tk.END, values=(item_id, item_text))
    root.after(100, update_treeview,tree)  # Check for updates again after 100ms

def check_login(username, password):
    # Replace with your actual authentication logic
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    status = check_login_credentials(server,username,password)
    if status == 1:
        print("Login successful!")
        #logout_button = ttk.Button(root, text="Logout", command=lambda: check_logout(login_button,logout_button))
        #logout_button.pack(padx=pad_x, pady=pad_y)
        #login_button.config(state=tk.DISABLED)
        #root.destroy()  # Close the window on successful login
        error_label.config(text="Login Successful")
        
        tree.pack(fill=tk.BOTH, expand=True)
        tree["columns"] = ("column1", "column2","column3","column4",'column5',"column6")
        tree.heading("column1", text="Sender")
        tree.heading("column2", text="Subject")
        tree.heading("column3",text="Body")
        tree.heading("column4",text="Attachments")
        tree.heading("column5",text="Status")
        tree.heading("column6",text="Drive ID")
        tree.column('#0',width=1,stretch=True)
        tree.column('column1',minwidth=1,stretch=True)
        tree.column('column2',minwidth=100,stretch=True)
        tree.column('column3',minwidth=100,stretch=True,anchor='center')
        tree.column('column4',minwidth=100,stretch=True)
        tree.column('column5',minwidth=100,stretch=True)
        tree.column('column6',minwidth=100,stretch=True)
        # Insert items with multiple columns
        #tree.insert("", tk.END, values=("Item 1", "Value A"))
        #tree.insert("", tk.END, values=("Item 2", "Value B"))
        #populate_email(server,tree)
        threading.Thread(target=background_task, args=(update_queue,server,tree,)).start()
        
        

    else:
        error_label.config(text="Invalid username or password")



# Start the event loop
update_treeview(tree)
root.mainloop()