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
import tkinter.ttk as ttk
import webbrowser
import platform
import subprocess
import os
import pathlib
#from reportlab.pdfgen import canvas
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

upper_frame =  tk.Frame(root)
upper_frame.pack(side='top',fill='y')

input_frame = tk.Frame(upper_frame)
input_frame.pack(side="left",fill='x')

display_frame = tk.Frame(upper_frame)
display_frame.pack(side='right',fill='x')

attachment_tree = ttk.Treeview(display_frame)
attachment_tree.pack(side='top',fill='y',expand=True)
attachment_tree["columns"] = ("column1","column2")
attachment_tree.heading("column1", text="History")
attachment_tree.heading("column2", text="Attachments")
attachment_tree.column('#0',width=1,stretch=True)
attachment_tree.column('column1',width=300,stretch=True)
attachment_tree.column('column2',width=200,stretch=True)
#attachment_tree.insert("",'end',values=("1",'Test'))

input_frame_uname = tk.Frame(input_frame)
input_frame_uname.pack(side='top',fill='y')
# Create username label and entry field
username_label = ttk.Label(input_frame_uname, text="Username:    ")
username_label.pack(side='left',fill='y')

username_entry = ttk.Entry(input_frame_uname)
username_entry.insert(0,'gawaisanjit@gmail.com')
username_entry.pack(side='right',fill='y')

input_frame_pass = tk.Frame(input_frame)
input_frame_pass.pack(side='top',fill='y')
# Create password label and entry field
password_label = ttk.Label(input_frame_pass, text="Password:     ")
password_label.pack(side='left',fill='y')

password_entry = ttk.Entry(input_frame_pass, show="*")  # Hide password characters
password_entry.insert(0,'feun xsng mwjh dzxc')
password_entry.pack(side = 'right', fill='y')

# Create login button
login_button = ttk.Button(input_frame, text="Login", command=lambda: check_login(username_entry.get(), password_entry.get()))
login_button.pack(side='top', fill='y')




tooltip = ttk.Label(input_frame, text="Body")
tooltip.pack(side='top', fill='y',expand=True)

# Define error message label (optional)
error_label = ttk.Label(input_frame, text="", foreground="red")  # Initially empty, red for errors
error_label.pack(side='top', fill='y')

message_label = ttk.Label(input_frame, text="", foreground="blue")  # Initially empty, blue for errors
message_label.pack(side='top', fill='y')



update_queue = queue.Queue()



tree = ttk.Treeview(root)

def open_attachment(item_id):
    print("Opening the attachment: ",item_id)
    item_values = attachment_tree.item(item_id)['values']
    splitvals = item_values[0].split("=")
    if len(splitvals)> 1:
        filename = "downloads/"+splitvals[1]
        filename = os.path.abspath(filename)
        filename = pathlib.Path(filename).as_uri()
        print("File=",filename)
        webbrowser.open(filename, new=0, autoraise=True) 
    pass
def popup(event):
    item_id = attachment_tree.identify("item", event.x, event.y)
    # Access data here based on item_id
    item_values = attachment_tree.item(item_id)['values']
    print("Popup item_values:=",item_values)
    if item_values[0].startswith('File:='):
        menu = tk.Menu(attachment_tree, tearoff=0)
        menu.add_command(label="Open", command=lambda: open_attachment(item_id))
        menu.add_command(label="View", command=lambda: open_attachment(item_id))
        menu.post(event.x_root, event.y_root)
        
attachment_tree.bind("<Button-3>", popup) 


def on_selection_change(event):
    selected_item = tree.item(tree.focus())["values"]  # Get selected item text
    # Perform actions based on selected item
    print("Selected item:", selected_item)
    #text = selected_item[2].replace('][]',']\n[')
    children_ids = attachment_tree.get_children()
    for child_id in children_ids:
        attachment_tree.delete(child_id)
    lines = selected_item[2].split('|')
    body = ''
    print("No of lines:=",len(lines))
    for line in lines:
        if ".zip" not in  line and "https://drive.google" not in line:
            body+=line
            body += '|'
    #multiline_text = body.replace('|','\n')
            
            #attachment_tree.delete(0, tk.END)
            attachment_tree.insert("",'end',values=(line,''))
    #message_label.config(text=body)
    #Read the attachment file names and display in the 
    attachments = selected_item[6].split('|')
    if len(attachments) > 0:
        for filename in attachments:
            print("Mail attachment file:=",filename)
            if len(filename.strip()) >0:
                attachment_tree.insert("",'end',values=("File:="+filename,''))
tree.bind("<<TreeviewSelect>>", on_selection_change)

gdrive_downloader.init_gdrive()
frame1 = tk.Frame(root)
frame1.pack(padx=pad_x,pady=pad_y)
def win_open_dicom_viewer(scan_file):
    print("Opening scan file(windows)...",scan_file)
    pyautogui.hotkey("win")  # Open Run dialog
    time.sleep(1)
    pyautogui.write("Radiant DICOM Viewer")
    pyautogui.press("enter")  # Open Notepad
    time.sleep(1)  # Wait for Notepad to open
    pyautogui.hotkey("alt","n")
    time.sleep(1)  # Wait for Notepad to open
    pyautogui.hotkey("enter")
    time.sleep(1)  # Wait for Notepad to open
    pyautogui.hotkey("ctrl","o")  # Open file dialog
    #pyautogui.write("c:\\users\\admin\\gmail_downloader\\downloads\\")
    pyautogui.write(scan_file[0])
    pyautogui.write(scan_file)
    pyautogui.press("enter")  # Open the file
    print("Setting up augnito ui")
    time.sleep(1)  # Wait for Notepad to open
    webbrowser.open("web.augnito.ai", new=0, autoraise=True) 
    pass
def mac_import_in_horos_database(scan_file):
    print("Opening scan file(MacOS)...",scan_file)
    print(f'Importing the zip file{scan_file} to the horos database')
    subprocess.run(["osascript", "-e", f"tell application \"Horos\" \n open \"/downloads/{scan_file}\"\n end tell"])
    webbrowser.open("web.augnito.ai", new=0, autoraise=True) 
    
def open_scan(tree):
    print("opening scan...")
    selected_item_id = tree.focus()
    print(selected_item_id)
    if selected_item_id != '':
        selected_item = tree.item(selected_item_id)
        print(selected_item)
        
        if platform.system() == "Windows":
            print("Windows detected")
            win_open_dicom_viewer(selected_item['values'][3])
        elif platform.system() == "Darwin":
            print("Mac OS X detected")
            mac_import_in_horos_database(selected_item['values'][3])
        else:
            print(f"Other OS: {platform.system()}")
        
        
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
            #message_label.config(text=text)
            #root.update()
            
            
            #tooltip.place(x=event.x + 10, y=event.y + 10)
#ToolTip(tree, msg="MyTool tip")
#tree.bind("<Enter>", show_tooltip)
#tree.bind("<Leave>", lambda _: message_label.pack_forget())


open_button = ttk.Button(input_frame,text="open",command=lambda: open_scan(tree))
open_button.pack(side='top',fill="y")

def check_logout(login_button,logout_button):
    login_button.config(state=tk.NORMAL)
    #logout_button.config(state=tk.DISABLED)
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
def download_attachment_file(filename,part):
    if filename:
        attachment_data = part.get_payload(decode=True)

        # Save attachment
        with open("downloads/"+filename, "wb") as f:
            f.write(attachment_data)
        print(f"Attachment '{filename}' downloaded successfully!")

    
def get_attachments(email_message):
    attachments=''
    for part in email_message.walk():
        #print(part)
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        download_attachment_file(filename,part)
        if filename:
            attachments+=filename
            attachments+='|'
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
                output += line+'|'
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
            tree.insert("", tk.END, values=(sender, subject,body,zipfilename,"Calculating...",drive_file_id,attachments))
def update_row(item_id, new_values):
    tree.item(item_id, values=new_values)
                
def check_file_exists(filename,drive_file_id,item_id,item_values):
    downloads_path = os.path.expanduser("downloads")
    file_path = os.path.join(downloads_path, filename)
    if os.path.exists(file_path):
        print("The file({}) exists in the Downloads folder.",filename)
        #set the status to downloaded
        item_values[4] = "Downloaded."
        update_row(item_id,item_values)
        return True
    else:
        print("The file does not exist in the Downloads folder.")
        print('Downloading the file...',filename)
        #set the status to downloading
        item_values[4] = "Downloading started."
        update_row(item_id,item_values)
        gdrive_downloader.download(drive_file_id,filename)
        #set status to downloaded Dome
        item_values[4] = "Downloading completed."
        update_row(item_id,item_values)
        return False
    pass
def check_download(tree):
    print("Checking if files are downloaded...")
    for item_id in tree.get_children():
        item_data = tree.item(item_id)["values"]
        print(item_data)
        print('Downloaded File Name:-',item_data[3])
        result = check_file_exists(item_data[3],item_data[5],item_id,item_data)
        if result == False:
            print('Start Downloading file')
        
def background_task(queue,server, tree,username,password):
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
            print('Sleeping for seconds:=',five_min_delta.total_seconds())
            time.sleep(five_min_delta.total_seconds())
            print('wakingup the background task....')
        except Exception as e:
            print("Error:=",e)
            print('Starting the background task again..')
            threading.Thread(target=check_login, args=(username,password)).start()
            print('exiitng the current thread...')
            break

def update_treeview(tree):
    #print("updating tree view...")
    if not update_queue.empty():
        item_id, item_text = update_queue.get()
        tree.insert("", tk.END, values=(item_id, item_text))
    root.after(100, update_treeview,tree)  # Check for updates again after 100ms
def update_ui_on_login(server,username,password):
    error_label.config(text="Login Successful")
    
    tree.pack(fill=tk.BOTH, expand=True)
    tree["columns"] = ("column1", "column2","column3","column4",'column5',"column6","column7")
    tree.heading("column1", text="Sender")
    tree.heading("column2", text="Subject")
    tree.heading("column3",text="Body")
    tree.heading("column4",text="Attachments")
    tree.heading("column5",text="Status")
    tree.heading("column6",text="Drive ID")
    tree.heading("column7",text="History")
    tree.column('#0',width=1,stretch=True)
    tree.column('column1',minwidth=1,stretch=True)
    tree.column('column2',minwidth=100,stretch=True)
    tree.column('column3',minwidth=100,stretch=True,anchor='center')
    tree.column('column4',minwidth=100,stretch=True)
    tree.column('column5',minwidth=100,stretch=True)
    tree.column('column6',minwidth=100,stretch=True)
    tree.column('column7',width=10)
    threading.Thread(target=background_task, args=(update_queue,server,tree,username,password)).start()
    
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
        
        # Insert items with multiple columns
        #tree.insert("", tk.END, values=("Item 1", "Value A"))
        #tree.insert("", tk.END, values=("Item 2", "Value B"))
        #populate_email(server,tree)
        root.after(0,lambda: update_ui_on_login(server,username,password))
        
        

    else:
        error_label.config(text="Invalid username or password")



# Start the event loop
update_treeview(tree)
root.mainloop()