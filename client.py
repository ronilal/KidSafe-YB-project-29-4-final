import sys


import tkinter as tk
import pickle
import hashlib
import socket
from tcp_by_size import recv_by_size, send_with_size
from queue import Queue
import threading
import time
#from PIL import Image
import re
#import numpy as np
import pickle
import secrets
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import customtkinter as ctk

IP ='10.68.121.254'
PORT = 5551
key =0

class App(ctk.CTk):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

        self.geometry('500x800')
        self.title("Login/Signup System")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.login_frame = self.create_login_frame()
        self.signup_frame = self.create_signup_frame()
        self.confirmation_frame = self.create_confirmation_frame()
        self.unconfirmation_frame = self.create_unconfirmation_frame()
        self.parent_selection_frame = self.create_parent_selection_frame()

        self.show_login_frame()

    def on_closing(self):
        self.exitReq()
        self.quit()
        self.destroy()
        sys.exit()

    def create_login_frame(self):
        frame = ctk.CTkFrame(self)

        main_label = ctk.CTkLabel(
            master=frame,
            text='System Login',
            font=('Aharoni', 30),
            text_color='light gray'
        )
        main_label.pack(pady=(20, 0))

        username_label = ctk.CTkLabel(frame, text="Username:")
        username_label.pack(pady=(10, 5))

        self.username_entry = ctk.CTkEntry(frame, placeholder_text='username')
        self.username_entry.pack(pady=(0, 10))

        password_label = ctk.CTkLabel(frame, text="Password:")
        password_label.pack(pady=(5, 5))

        self.password_entry = ctk.CTkEntry(frame, show="*", placeholder_text='password')
        self.password_entry.pack(pady=(0, 20))

        login_button = ctk.CTkButton(frame, text="Login", command=self.login)
        login_button.pack()

        checkBox = ctk.CTkCheckBox(frame, text='Remember Me')
        checkBox.pack(pady=10)

        signUp_label = ctk.CTkLabel(frame, text='Dont have an account?')
        signUp_label.pack()

        signUp_button = ctk.CTkButton(frame, text='Sign Up', width=40, height=20, command=self.show_signup_frame)
        signUp_button.pack()

        return frame

    def create_signup_frame(self):
        frame = ctk.CTkFrame(self)

        main_label = ctk.CTkLabel(
            master=frame,
            text='Sign Up',
            font=('Aharoni', 30),
            text_color='light gray'
        )
        main_label.pack(pady=(20, 0))

        username_label = ctk.CTkLabel(frame, text="Username:")
        username_label.pack(pady=(10, 5))
        self.username_entry_su = ctk.CTkEntry(frame, placeholder_text='Enter username')
        self.username_entry_su.pack(pady=(0, 10))

        email_label = ctk.CTkLabel(frame, text="Email:")
        email_label.pack(pady=(5, 5))
        self.email_entry_su = ctk.CTkEntry(frame, placeholder_text='Enter email')
        self.email_entry_su.pack(pady=(0, 10))

        password_label = ctk.CTkLabel(frame, text="Password:")
        password_label.pack(pady=(5, 5))
        self.password_entry_su = ctk.CTkEntry(frame, show="*", placeholder_text='Enter password')
        self.password_entry_su.pack(pady=(0, 10))

        confirm_password_label = ctk.CTkLabel(frame, text="Confirm Password:")
        confirm_password_label.pack(pady=(5, 5))
        self.confirm_password_entry_su = ctk.CTkEntry(frame, show="*", placeholder_text='Confirm password')
        self.confirm_password_entry_su.pack(pady=(0, 10))

        # Add a label for the account type switch
        account_type_label = ctk.CTkLabel(frame, text="Account Type:")
        account_type_label.pack(pady=(5, 5))

        # Create a frame to hold the switch and labels
        switch_frame = ctk.CTkFrame(frame, fg_color="transparent")
        switch_frame.pack(pady=(0, 10))

        # Child label
        child_label = ctk.CTkLabel(switch_frame, text="Child")
        child_label.pack(side=tk.LEFT, padx=(0, 10))

        # Add the switch for account type selection
        self.account_type_switch = ctk.CTkSwitch(
            switch_frame,
            text=""
        )
        self.account_type_switch.pack(side=tk.LEFT)

        # Parent label
        parent_label = ctk.CTkLabel(switch_frame, text="Parent")
        parent_label.pack(side=tk.LEFT, padx=(10, 0))

        dob_label = ctk.CTkLabel(frame, text="Date of Birth:")
        dob_label.pack(pady=(5, 5))
        self.dob_entry = ctk.CTkEntry(frame, placeholder_text='YYYY-MM-DD')
        self.dob_entry.pack(pady=(0, 10))

        signup_button = ctk.CTkButton(frame, text="Sign Up", command=self.signup)
        signup_button.pack(pady=(0, 10))

        terms_checkbox = ctk.CTkCheckBox(frame, text='I agree to the Terms and Conditions')
        terms_checkbox.pack(pady=10)

        login_label = ctk.CTkLabel(frame, text='Already have an account?')
        login_label.pack()

        login_button = ctk.CTkButton(frame, text='Log In', command=self.show_login_frame, width=40, height=20)
        login_button.pack()

        return frame

    def create_confirmation_frame(self):
        confirmation_frame = ctk.CTkFrame(self)
        main_label = ctk.CTkLabel(
            master=confirmation_frame,
            text='Sign Up',
            font=('Aharoni', 30),
            text_color='light gray'
        )
        main_label.pack(pady=(20, 0))

        message = "The action is confirmed!"
        color = "green"

        confirmation_label = ctk.CTkLabel(confirmation_frame, text=message, font=("Helvetica", 16), text_color=color)
        confirmation_label.pack(pady=20)

        # Button to go back to the main frame
        back_button = ctk.CTkButton(confirmation_frame, text="Back to Main", command=self.show_login_frame)
        back_button.pack(pady=10)
        return confirmation_frame

    def create_unconfirmation_frame(self):
        unconfirmation_frame = ctk.CTkFrame(self)
        main_label = ctk.CTkLabel(
            master=unconfirmation_frame,
            text='Sign Up',
            font=('Aharoni', 30),
            text_color='light gray'
        )
        main_label.pack(pady=(20, 0))

        message = "The action is not confirmed."
        color = "red"

        unconfirmation_label = ctk.CTkLabel(unconfirmation_frame, text=message, font=("Helvetica", 16), text_color=color)
        unconfirmation_label.pack(pady=20)

        # Button to go back to the main frame
        back_button = ctk.CTkButton(unconfirmation_frame, text="Back to Main", command=self.show_login_frame)
        back_button.pack(pady=10)
        return unconfirmation_frame

    def create_parent_selection_frame(self):
        """Create the parent selection frame for child accounts"""
        frame = ctk.CTkFrame(self)

        main_label = ctk.CTkLabel(
            master=frame,
            text='Select a Parent',
            font=('Aharoni', 30),
            text_color='light gray'
        )
        main_label.pack(pady=(20, 0))

        instruction_label = ctk.CTkLabel(
            frame,
            text="Please select a parent account to connect with:",
            font=("Helvetica", 14)
        )
        instruction_label.pack(pady=(10, 10))

        # Frame to hold the parent list
        parents_frame = ctk.CTkFrame(frame)
        parents_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create a scrollable frame for the parents list
        self.parents_scrollable = ctk.CTkScrollableFrame(parents_frame, height=200)
        self.parents_scrollable.pack(fill="both", expand=True)

        # Variable to store the selected parent
        self.selected_parent = tk.StringVar()

        # Button to connect with selected parent
        connect_button = ctk.CTkButton(
            frame,
            text="Connect with Parent",
            command=self.link_with_parent
        )
        connect_button.pack(pady=(10, 20))

        # Button to skip (for testing or special cases)
        skip_button = ctk.CTkButton(
            frame,
            text="Skip for now",
            command=self.skip_parent_selection,
            fg_color="gray",
            hover_color="#555555"
        )
        skip_button.pack(pady=(0, 20))

        return frame

    def populate_parent_list(self, parents):
        """Populate the parent selection list with available parents"""
        # Clear existing widgets
        for widget in self.parents_scrollable.winfo_children():
            widget.destroy()

        # Add radio buttons for each parent
        if not parents:
            no_parents_label = ctk.CTkLabel(
                self.parents_scrollable,
                text="No parent accounts found. Please skip for now.",
                text_color="orange"
            )
            no_parents_label.pack(pady=10)
            return

        for parent in parents:
            parent_radio = ctk.CTkRadioButton(
                self.parents_scrollable,
                text=f"{parent}",
                variable=self.selected_parent,
                value=parent
            )
            parent_radio.pack(anchor="w", pady=5, padx=10)

    def show_confirmation_frame(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack_forget()  # Add this line
        self.unconfirmation_frame.pack_forget()  # Add this line
        self.parent_selection_frame.pack_forget()
        self.confirmation_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_unconfirmation_frame(self):
        self.signup_frame.pack_forget()
        self.confirmation_frame.pack_forget()  # Add this line
        self.login_frame.pack_forget()  # Add this line
        self.parent_selection_frame.pack_forget()
        self.unconfirmation_frame.pack(pady=20, padx=20, fill="both", expand=True)
    def show_login_frame(self):
        self.signup_frame.pack_forget()
        self.confirmation_frame.pack_forget()  # Add this line
        self.unconfirmation_frame.pack_forget()  # Add this line
        self.parent_selection_frame.pack_forget()
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_signup_frame(self):
        self.login_frame.pack_forget()
        self.confirmation_frame.pack_forget()  # Add this line
        self.unconfirmation_frame.pack_forget()  # Add this line
        self.parent_selection_frame.pack_forget()
        self.signup_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_parent_selection_frame(self):
        self.login_frame.pack_forget()
        self.confirmation_frame.pack_forget()
        self.unconfirmation_frame.pack_forget()
        self.signup_frame.pack_forget()

        # Request parent list from server
        self.get_parents_list()

        self.parent_selection_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def get_parents_list(self):
        """Request list of parent accounts from server"""
        request = {
            "code": "get_parents"
        }
        data = pickle.dumps(request)
        data = AESenc(data)
        send_with_size(self.sock, data)

        # Receive response from server
        encrypted_data = recv_by_size(self.sock, return_type='byte')
        decrypted_data = AESdec(encrypted_data)
        response = pickle.loads(decrypted_data)

        if response['status'] == True:
            self.populate_parent_list(response['parents'])
        else:
            print(response['massage'])
            self.populate_parent_list([])  # Empty list if error

    def link_with_parent(self):
        """Send request to link child with selected parent"""
        selected_parent = self.selected_parent.get()

        if not selected_parent:
            # Show error if no parent selected
            error_label = ctk.CTkLabel(
                self.parent_selection_frame,
                text="Please select a parent or skip for now",
                text_color="red"
            )
            error_label.pack(pady=5)
            return

        # Send link request to server
        request = {
            "code": "link_parent",
            "child_username": self.username,
            "parent_username": selected_parent
        }

        data = pickle.dumps(request)
        data = AESenc(data)
        send_with_size(self.sock, data)

        # Receive confirmation from server
        encrypted_data = recv_by_size(self.sock, return_type='byte')
        decrypted_data = AESdec(encrypted_data)
        response = pickle.loads(decrypted_data)

        if response['status'] == True:
            self.show_confirmation_frame()
        else:
            self.show_unconfirmation_frame()

    def skip_parent_selection(self):
        """Skip the parent selection process"""
        self.show_confirmation_frame()

    def signup(self):
        self.username = self.username_entry_su.get()
        self.password = self.password_entry_su.get()
        self.confirm_password = self.confirm_password_entry_su.get()
        self.email = self.email_entry_su.get()
        self.dob = self.dob_entry.get()
        if self.account_type_switch.get():
            self.role = 'Parent'
        else:
            self.role = 'Child'

        if not self.username or not self.password or not self.email:
            self.show_unconfirmation_frame()
            return


        if self.password != self.confirm_password:
            self.show_unconfirmation_frame()
            return

            # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            self.show_unconfirmation_frame()
            return

        # Date validation
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, self.dob):
            self.show_unconfirmation_frame()
            return


        else:
            self.signupReq(self.username, self.password, self.email, self.role)
            encrypted_data = recv_by_size(self.sock, return_type='byte')  # Receive encrypted message from client
            decrypted_data = AESdec(encrypted_data)  # Decrypt the message
            server_msg = pickle.loads(decrypted_data)  # load the pickle file to dict
            if server_msg['status'] == True:
                self.show_confirmation_frame()
                if self.role == 'Child':
                    self.show_parent_selection_frame()
            else:
                self.show_unconfirmation_frame()

    def login(self):
        global key
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        self.loginReq(self.username, password)
        server_msg_encrypted = recv_by_size(self.sock, return_type='byte')  # Receive encrypted message from client
        server_msg = AESdec(server_msg_encrypted)  # Decrypt the message
        server_msg = pickle.loads(server_msg)  # load the pickle file to dict
        if server_msg['status'] == True:
            if server_msg['role'] == 'Parent':
                # מעבר לממשק הורה
                self.withdraw()  # הסתרת חלון הנוכחי
                from Parent_Dashboard import ParentDashboard
                parent_app = ParentDashboard(self.sock, self.username, key)
                parent_app.mainloop()
            else:
                # מעבר לממשק ילד או התנהגות אחרת
                self.show_confirmation_frame()

        else:
            self.show_unconfirmation_frame()

    def generate_random_key(length):
        return secrets.token_bytes(length)

    def RSA(self):
        public_key1 = self.generate_random_key(16)
        public_key2 = recv_by_size(self.sock)

    def signupReq(self, username, password, email, role):
        login_dict = {
            "code": 'signup',
            "user": username,
            "password": password,
            "email": email,
            "role": role
        }
        data = pickle.dumps(login_dict)
        data = AESenc(data)
        send_with_size(self.sock, data)
        return
    def loginReq(self, username, password):
        login_dict = {
            "code": 'login',
            "user": username,
            "password": password
        }
        data = pickle.dumps(login_dict)
        data = AESenc(data)
        send_with_size(self.sock, data)
        return

    def exitReq(self):
        global key
        login_dict = {
            "code": 'exit',
        }
        data = pickle.dumps(login_dict)
        data = AESenc(data,key)
        send_with_size(self.sock, data)
        return



def close_window(window):
    # Call the quit() method to stop the main loop
    window.quit()

    # Destroy the window
    window.destroy()
def generate_random_key(length):
    return secrets.token_bytes(length)

def AESenc(data, k=None):
    global key
    if k is None:
        k = key
    print(f'AESenc using key {key}')
    iv = get_random_bytes(AES.block_size)  # Generate a random IV
    cipher = AES.new(k, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv + ciphertext  # Prepend IV to the ciphertext for later use in decryption

def AESdec(data, k=None):
    global key
    if k is None:
        k = key
    print(f'AESdec using key {key}')
    iv = data[:AES.block_size]  # Extract IV from the beginning of the ciphertext
    cipher = AES.new(k, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)
    return decrypted
def RSA(sock):
    global key
    public_key1 = int(recv_by_size(sock, return_type='byte').decode())
    public_key2 = int.from_bytes(generate_random_key(16), byteorder='big')
    send_with_size(sock, str(public_key2).encode())
    secret_key = int.from_bytes(generate_random_key(16), byteorder='big')
    p = pow(public_key2, secret_key, public_key1)
    b = int(recv_by_size(sock, return_type='byte').decode())
    send_with_size(sock, str(p).encode())
    a = pow(b,secret_key, public_key1)
    key = int_to_bytes(a)
    print(f"this is the key = {key}")

def int_to_bytes(x: int, length: int = None, byteorder: str = 'big') -> bytes:
    if length is None:
        length = (x.bit_length() + 7) // 8
    return x.to_bytes(length, byteorder)


def main(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    print("server connected")
    RSA(sock)
    app = App(sock)
    app.mainloop()

main(('10.0.0.16'),6122)



#if __name__ == '__main__':
 #   login_gui()

