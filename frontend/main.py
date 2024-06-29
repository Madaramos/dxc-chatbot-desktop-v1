import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import fitz
import os

# Set API URL
api_url = 'http://localhost:5000'
token = None
username = None

class DXCApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DXC Application")
        self.geometry("1200x800")

        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()
        self.upload_frame = self.create_upload_frame()
        self.chatbot_frame = self.create_chatbot_frame()

        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.tkraise()

    def create_login_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        # Title
        ctk.CTkLabel(frame, text="WELCOME BACK!", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.25, rely=0.1, anchor='w')

        # Username Entry
        ctk.CTkLabel(frame, text="Username", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.25, anchor='w')
        self.login_username_entry = ctk.CTkEntry(frame, width=300)
        self.login_username_entry.place(relx=0.25, rely=0.3, anchor='w')

        # Password Entry
        ctk.CTkLabel(frame, text="Password", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.4, anchor='w')
        self.login_password_entry = ctk.CTkEntry(frame, show="*", width=300)
        self.login_password_entry.place(relx=0.25, rely=0.45, anchor='w')

        # Logo
        logo_img = ctk.CTkImage(light_image=Image.open("D:/DXC-flask/frontend/assets/logo.jpg"), size=(450, 150))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="", fg_color='white')
        logo_label.place(relx=0.55, rely=0.4, anchor='w')

        # Sign In Button
        ctk.CTkButton(frame, text="Sign In", command=self.login, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20).place(relx=0.25, rely=0.55, anchor='w')

        # Register Label
        register_label = ctk.CTkLabel(frame, text="Don’t have an account? Sign up", font=("Helvetica", 12), text_color="#1E90FF", cursor="hand2", fg_color='white')
        register_label.place(relx=0.25, rely=0.65, anchor='w')
        register_label.bind("<Button-1>", lambda e: self.show_frame(self.register_frame))

        return frame


    def create_register_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        # Title
        ctk.CTkLabel(frame, text="CREATE ACCOUNT", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.25, rely=0.1, anchor='w')

        # Username Entry
        ctk.CTkLabel(frame, text="Username", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.25, anchor='w')
        self.reg_username_entry = ctk.CTkEntry(frame, width=300)
        self.reg_username_entry.place(relx=0.25, rely=0.3, anchor='w')

        # Password Entry
        ctk.CTkLabel(frame, text="Password", font=("Helvetica", 14), fg_color='white', text_color='black').place(relx=0.25, rely=0.4, anchor='w')
        self.reg_password_entry = ctk.CTkEntry(frame, show="*", width=300)
        self.reg_password_entry.place(relx=0.25, rely=0.45, anchor='w')

        # Logo
        logo_img = ctk.CTkImage(light_image=Image.open("D:/DXC-flask/frontend/assets/logo.jpg"), size=(450, 150))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="", fg_color='white')
        logo_label.place(relx=0.55, rely=0.4, anchor='w')

        # Register Button
        ctk.CTkButton(frame, text="Sign up", command=self.register, fg_color="#6A0DAD", hover_color="#8A2BE2", corner_radius=20).place(relx=0.25, rely=0.55, anchor='w')

        # Back to Login Label
        back_to_login_label = ctk.CTkLabel(frame, text="Back to Login", font=("Helvetica", 12), text_color="#1E90FF", cursor="hand2", fg_color='white')
        back_to_login_label.place(relx=0.25, rely=0.65, anchor='w')
        back_to_login_label.bind("<Button-1>", lambda e: self.show_frame(self.login_frame))

        return frame


    def create_upload_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        ctk.CTkLabel(frame, text="Upload and View PDF", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.5, rely=0.05, anchor='center')

        # Buttons
        ctk.CTkButton(frame, text="Upload PDF", command=self.upload_pdf, fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=20).place(relx=0.1, rely=0.2, anchor='w')
        ctk.CTkButton(frame, text="Chatbot", command=lambda: self.show_frame(self.chatbot_frame), fg_color="#32CD32", hover_color="#2E8B57", corner_radius=20).place(relx=0.1, rely=0.3, anchor='w')
        ctk.CTkButton(frame, text="Logout", command=lambda: self.show_frame(self.login_frame), fg_color="#FF4500", hover_color="#FF6347", corner_radius=20).place(relx=0.1, rely=0.4, anchor='w')

        # PDF Listbox
        self.pdf_listbox = tk.Listbox(frame, width=20, height=10, selectmode=tk.SINGLE)
        self.pdf_listbox.place(relx=0.15, rely=0.45, anchor='n')
        self.pdf_listbox.bind("<<ListboxSelect>>", self.display_selected_pdf)

        # PDF Viewer
        self.pdf_viewer_frame = tk.Frame(frame, bg="black", bd=1)
        self.pdf_viewer_frame.place(relx=0.6, rely=0.2, anchor='n', width=500, height=600)
        
        self.pdf_image_label = ctk.CTkLabel(self.pdf_viewer_frame, text="", fg_color='white', text_color='black')
        self.pdf_image_label.pack(fill="both", expand=True)

        # Navigation Buttons
        self.prev_page_button = ctk.CTkButton(frame, text="Previous Page", command=self.previous_page, fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=20)
        self.prev_page_button.place(relx=0.5, rely=0.85, anchor='center')
        self.next_page_button = ctk.CTkButton(frame, text="Next Page", command=self.next_page, fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=20)
        self.next_page_button.place(relx=0.65, rely=0.85, anchor='center')

        return frame

    def create_chatbot_frame(self):
        frame = ctk.CTkFrame(self, fg_color='white')
        frame.place(relwidth=1, relheight=1)

        ctk.CTkLabel(frame, text="Chatbot", font=("Helvetica", 24, "bold"), fg_color='white', text_color='black').place(relx=0.5, rely=0.1, anchor='center')

        self.chatbot_text = ctk.CTkTextbox(frame, width=800, height=500, border_width=1, border_color="black",)
        self.chatbot_text.place(relx=0.5, rely=0.45, anchor='center')

        self.chatbot_entry = ctk.CTkEntry(frame, width=600)
        self.chatbot_entry.place(relx=0.5, rely=0.8, anchor='center')

        ctk.CTkButton(frame, text="Send", command=self.send_query, fg_color="#1E90FF", hover_color="#1C86EE").place(relx=0.90, rely=0.8, anchor='center')
        ctk.CTkButton(frame, text="Back", command=lambda: self.show_frame(self.upload_frame), fg_color="#32CD32", hover_color="#2E8B57").place(relx=0.10, rely=0.8, anchor='center')

        return frame

    def login(self):
        global token, username
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        data = {"username": username, "password": password}
        
        try:
            response = requests.post(f'{api_url}/auth/login', json=data)
            if response.status_code == 200:
                token = response.json().get('token')
                messagebox.showinfo("Success", "Logged in successfully")
                self.load_user_pdfs()
                self.show_frame(self.upload_frame)
            else:
                messagebox.showerror("Error", response.json().get('message', 'Invalid credentials'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def register(self):
        global username
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        data = {"username": username, "password": password}
        
        try:
            response = requests.post(f'{api_url}/auth/register', json=data)
            if response.status_code == 201:
                messagebox.showinfo("Success", "User registered successfully")
                self.show_frame(self.login_frame)
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error registering user'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        try:
            files = {'file': open(file_path, 'rb')}
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f'{api_url}/file/upload', files=files, headers=headers)
            
            if response.status_code == 201:
                messagebox.showinfo("Success", "File uploaded and processed successfully")
                self.load_user_pdfs()
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error uploading file'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

    def load_user_pdfs(self):
        self.pdf_listbox.delete(0, tk.END)
        user_folder = os.path.join(r'D:\DXC-flask\flask2\uploads', username)
        if os.path.exists(user_folder):
            for filename in os.listdir(user_folder):
                if filename.endswith('.pdf'):
                    self.pdf_listbox.insert(tk.END, filename)
        else:
            messagebox.showerror("Error", "User folder does not exist.")

    def display_selected_pdf(self, event):
        try:
            selected_index = self.pdf_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "No PDF selected.")
                return
            selected_file = self.pdf_listbox.get(selected_index)
            file_path = os.path.join(r'D:\DXC-flask\flask2\uploads', username, selected_file)
            self.display_pdf(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def display_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            self.page_count = len(doc)
            self.current_page = 0
            self.pdf_pages = []
            for i in range(self.page_count):
                page = doc.load_page(i)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                self.pdf_pages.append(img)
            self.show_page(self.current_page)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def show_page(self, page_number):
        img = self.pdf_pages[page_number]
        img_tk = ImageTk.PhotoImage(img)
        self.pdf_image_label.configure(image=img_tk)
        self.pdf_image_label.image = img_tk

    def next_page(self):
        if self.current_page < self.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def send_query(self):
        query = self.chatbot_entry.get()
        headers = {'Authorization': f'Bearer {token}'}
        data = {'query': query}
        
        try:
            response = requests.post(f'{api_url}/query/query', json=data, headers=headers)
            if response.status_code == 200:
                result = response.json().get('response')
                self.chatbot_text.configure(state='normal')
                self.chatbot_text.insert(ctk.END, "You: " + query + "\n")
                self.chatbot_text.insert(ctk.END, "Bot: " + result + "\n\n")
                self.chatbot_text.configure(state='disabled')
                self.chatbot_entry.delete(0, ctk.END)
                self.chatbot_text.configure("user", foreground="blue")
                self.chatbot_text.configure("bot", foreground="green")
            else:
                messagebox.showerror("Error", response.json().get('message', 'Error processing query'))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = DXCApp()
    app.mainloop()

