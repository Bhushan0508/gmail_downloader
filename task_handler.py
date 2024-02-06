import tkinter as tk
from tkinter import ttk
import threading
import queue
import time

def background_task(queue):
    for i in range(5):
        time.sleep(1)  # Simulate some work
        queue.put((i, f"Item {i}"))  # Add items to the queue

def update_treeview():
    print("updating tree view...")
    if not update_queue.empty():
        item_id, item_text = update_queue.get()
        tree.insert("", tk.END, values=(item_id, item_text))
    root.after(100, update_treeview)  # Check for updates again after 100ms

root = tk.Tk()
tree = ttk.Treeview(root, columns=("id", "text"))
tree.pack()

update_queue = queue.Queue()

# Start background thread
threading.Thread(target=background_task, args=(update_queue,)).start()

# Schedule updates in the main thread
update_treeview()

root.mainloop()