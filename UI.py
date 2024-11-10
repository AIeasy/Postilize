import tkinter as tk
from tkinter import ttk, messagebox
import json

class InstagramMockUI:
    def __init__(self, master):
        self.master = master
        master.title("Instagram Mock UI")
        master.geometry("300x400")
        
        self.login_frame = ttk.Frame(master, padding="10")
        self.message_frame = ttk.Frame(master, padding="10")
        
        self.create_login_screen()
        self.create_message_form()
        
        self.show_login_screen()

    def create_login_screen(self):
        ttk.Label(self.login_frame, text="Instagram", font=("Arial", 20)).pack(pady=10)
        
        ttk.Label(self.login_frame, text="Username").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        ttk.Label(self.login_frame, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(self.login_frame, text="Log In", command=self.login).pack(pady=10)
        ttk.Button(self.login_frame, text="Load JSON for Login", command=self.load_json).pack(pady=5)

    def create_message_form(self):
        ttk.Label(self.message_frame, text="Send Message", font=("Arial", 16)).pack(pady=10)
        
        ttk.Label(self.message_frame, text="Recipient Username").pack(pady=5)
        self.recipient_entry = ttk.Entry(self.message_frame)
        self.recipient_entry.pack(pady=5)
        
        ttk.Label(self.message_frame, text="Message").pack(pady=5)
        self.message_text = tk.Text(self.message_frame, height=5)
        self.message_text.pack(pady=5)
        
        ttk.Button(self.message_frame, text="Send", command=self.send_message).pack(pady=10)

    def show_login_screen(self):
        self.message_frame.pack_forget()
        self.login_frame.pack()

    def show_message_form(self):
        self.login_frame.pack_forget()
        self.message_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Here you would typically verify the credentials
        # For this mock-up, we'll just check if fields are not empty
        if username and password:
            self.show_message_form()
        else:
            messagebox.showerror("Error", "Please enter both username and password")

    def load_json(self):
        # In a real application, you'd load this from a file or API
        json_data = json.dumps({"username": "demo_user", "password": "demo_pass"})
        data = json.loads(json_data)
        
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, data["username"])
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, data["password"])

    def send_message(self):
        recipient = self.recipient_entry.get()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if recipient and message:
            messagebox.showinfo("Success", f"Message sent to {recipient}")
            self.recipient_entry.delete(0, tk.END)
            self.message_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please enter both recipient and message")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramMockUI(root)
    root.mainloop()