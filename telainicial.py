import json
import threading
import tkinter as tk
from tkinter import Entry, Text, Scrollbar, Listbox, Button, END, messagebox, Toplevel

# Assuming these modules exist in your project
import interface
from estetica import ativar_modo_noturno
from script import Automation

# Constants for file paths
LOGIN_LIST_FILE = "login_list.json"

# Error messages
ERROR_MESSAGE_FIELDS = "Por favor, preencha todos os campos."
ERROR_MESSAGE_LOGIN = "Por favor, preencha os campos de login e senha."


def load_login_list():
    try:
        with open(LOGIN_LIST_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_login_list(login_list):
    with open(LOGIN_LIST_FILE, "w") as file:
        json.dump(login_list, file)


def show_error(message):
    messagebox.showerror("Erro", message)


class Main:
    def __init__(self, root):
        self.secondary_interface = None
        self.running_thread = None
        self.scrollbar = None
        self.log_text = None
        self.entry_cantor = None
        self.entry_senha = None
        self.show_password_checkbox = None
        self.show_password_var = None
        self.entry_email = None
        self.root = root
        self.root.title("Spotify Automation")

        self.modo_noturno_ativo = False
        self.show_password = False
        self.login_list = load_login_list()

        self.create_login_ui()
        self.create_automation_ui()
        self.create_log_ui()
        self.create_buttons()

        self.clear_fields()

    def create_login_ui(self):
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=10)
        tk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky="e")
        self.entry_email = tk.Entry(login_frame)
        self.entry_email.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(login_frame, text="Senha:").grid(row=1, column=0, sticky="e")
        self.entry_senha = Entry(login_frame, show='*')
        self.entry_senha.grid(row=1, column=1, padx=10, pady=5)
        self.show_password_var = tk.IntVar()
        self.show_password_checkbox = tk.Checkbutton(login_frame, text="Mostrar Senha", variable=self.show_password_var,
                                                     command=self.toggle_password)
        self.show_password_checkbox.grid(row=2, column=1, padx=10, pady=5)

    def create_automation_ui(self):
        tk.Label(self.root, text="Nome do Cantor:").pack()
        self.entry_cantor = tk.Entry(self.root)
        self.entry_cantor.pack()

    def create_log_ui(self):
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10)
        tk.Label(log_frame, text="Log:").grid(row=0, column=0, sticky="w")
        self.log_text = Text(log_frame, height=10, width=40)
        self.log_text.grid(row=1, column=0)
        self.scrollbar = Scrollbar(log_frame, command=self.log_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="nsew")
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        self.log_text.tag_configure("error", foreground="red")

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Iniciar", command=self.start, width=10).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cadastrar Conta do Spotify", command=self.mudar_interface, width=20).pack(
            side="left",
            padx=10)
        tk.Button(button_frame, text="Logins Cadastrados", command=self.show_login_list, width=15).pack(side="left",
                                                                                                        padx=10)
        tk.Button(button_frame, text="Limpar Campos", command=self.clear_fields, width=15).pack(side="left", padx=10)

        # Botão para ativar/desativar o modo noturno
        tk.Button(button_frame, text="Modo Noturno", command=self.ativar_modo_noturno, width=15).pack(side="left",
                                                                                                      padx=10)

    def toggle_password(self):
        self.show_password = bool(self.show_password_var.get())
        if self.show_password:
            self.entry_senha.config(show="")
        else:
            self.entry_senha.config(show="*")

    def clear_fields(self):
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_cantor.delete(0, tk.END)

    def start(self):
        if self.campos_de_login_preenchidos():
            if not self.is_thread_running():
                self.start_automation_thread()
        else:
            show_error(ERROR_MESSAGE_LOGIN)

    def is_thread_running(self):
        return self.running_thread is not None and self.running_thread.is_alive()

    def start_automation_thread(self):
        self.running_thread = threading.Thread(target=self.start_automation)
        self.running_thread.start()

    def start_automation(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        cantor = self.entry_cantor.get()

        if not all([email, senha, cantor]):
            show_error(ERROR_MESSAGE_FIELDS)
            return

        self.log("Iniciando automação...")
        automation = Automation(email, senha, cantor, log_function=self.log)
        automation.run()
        self.clear_fields()

    def log(self, message, tag=None):
        self.display_log_message(message, tag)

    def display_log_message(self, message, tag=None):
        if tag == "error":
            self.log_text.insert(tk.END, message + "\n", "error")
        else:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def campos_de_login_preenchidos(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        return email and senha

    def show_login_list(self):
        if not self.login_list:
            messagebox.showinfo("Logins Cadastrados", "Nenhum login cadastrado.")
            return

        # Abre uma nova janela para mostrar os logins cadastrados em forma de lista
        login_list_window = Toplevel(self.root)
        login_list_window.title("Logins Cadastrados")
        login_list_window.geometry("400x200")

        listbox = Listbox(login_list_window, selectmode=tk.SINGLE)
        for login in self.login_list:
            listbox.insert(END, f"Login: {login['email']}")

        listbox.pack()

        # Adicione um botão "Selecionar"
        select_button = Button(login_list_window, text="Selecionar",
                               command=lambda: self.select_login(login_list_window, listbox))
        select_button.pack()

    def select_login(self, login_list_window, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_login = self.login_list[selected_index]
            email = selected_login['email']
            senha = selected_login['senha']

            # Preencha os campos de email e senha com o login selecionado
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, email)
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.insert(0, senha)

            # Feche a janela de seleção
            login_list_window.destroy()

    def mudar_interface(self):
        if self.secondary_interface:
            self.secondary_interface.withdraw()
            self.secondary_interface.protocol("WM_DELETE_WINDOW", self.mostrar_janela_principal)
            self.secondary_interface.deiconify()
        else:
            self.secondary_interface = Toplevel(self.root)
            interface.InterfaceManager(self.secondary_interface)
            self.secondary_interface.protocol("WM_DELETE_WINDOW", self.mostrar_janela_principal)
            self.root.withdraw()

    def mostrar_janela_principal(self):
        if self.secondary_interface:
            self.secondary_interface.destroy()
            self.secondary_interface = None

        self.root.deiconify()

    def ativar_modo_noturno(self):
        self.modo_noturno_ativo = ativar_modo_noturno(self.root, self.modo_noturno_ativo)


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()
