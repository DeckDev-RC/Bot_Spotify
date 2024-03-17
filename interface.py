import tkinter as tk
from tkinter import messagebox
import json
import telainicial


def load_login_list():
    try:
        with open("login_list.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_login_list(login_list):
    with open("login_list.json", "w") as file:
        json.dump(login_list, file)


class InterfaceManager:
    def __init__(self, root):
        self.button_show = None
        self.button_add = None
        self.entry_senha = None
        self.label_senha = None
        self.entry_email = None
        self.label_email = None
        self.root = root
        self.root.title("Login Manager")
        self.root.geometry("400x300")

        self.login_list = load_login_list()

        self.create_widgets()

    def create_widgets(self):
        self.label_email = tk.Label(self.root, text="Email:")
        self.label_email.pack()

        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        self.label_senha = tk.Label(self.root, text="Senha:")
        self.label_senha.pack()

        self.entry_senha = tk.Entry(self.root, show='*')
        self.entry_senha.pack()

        self.button_add = tk.Button(self.root, text="Adicionar", command=self.add_login)
        self.button_add.pack()

        self.button_show = tk.Button(self.root, text="Mostrar Logins", command=self.show_login_list)
        self.button_show.pack()

        self.button_show = tk.Button(self.root, text="Tela Inicial", command=self.close_secondary_interface)
        self.button_show.pack()

    def add_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Verifica se o login já existe
        for login in self.login_list:
            if login["email"] == email:
                messagebox.showerror("Erro", "Login já cadastrado.")
                return

        self.login_list.append({"email": email, "senha": senha})
        save_login_list(self.login_list)
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

    def show_login_list(self):
        def edit_login():
            selected_index = listbox.curselection()[0]

            if selected_index < len(self.login_list):
                selected_login = self.login_list[selected_index]

                if isinstance(selected_login, dict):
                    def save_changes():
                        if isinstance(selected_login, dict) and "email" in selected_login and "senha" in selected_login:
                            selected_login["email"] = entry_email.get()
                            selected_login["senha"] = entry_senha.get()
                            save_login_list(self.login_list)
                            edit_login_window.destroy()
                            listbox.delete(selected_index)
                            listbox.insert(selected_index, f"Login: {selected_login['email']}")
                        else:
                            # Lida com o caso em que selected_login não é um dicionário válido
                            messagebox.showerror("Erro", "O login selecionado não é válido.")

                    def cancel_changes():
                        edit_login_window.destroy()

                    edit_login_window = tk.Toplevel(self.root)
                    edit_login_window.title("Editar Login")
                    edit_login_window.geometry("400x200")

                    entry_email = tk.Entry(edit_login_window)
                    entry_email.insert(0, selected_login.get("email", ""))
                    entry_email.pack()

                    entry_senha = tk.Entry(edit_login_window, show='*')
                    entry_senha.insert(0, selected_login.get("senha", ""))
                    entry_senha.pack()

                    save_button = tk.Button(edit_login_window, text="Salvar", command=save_changes)
                    save_button.pack()

                    cancel_button = tk.Button(edit_login_window, text="Cancelar", command=cancel_changes)
                    cancel_button.pack()

        def delete_login():
            selected_index = listbox.curselection()[0]
            self.login_list.pop(selected_index)
            save_login_list(self.login_list)
            listbox.delete(selected_index)

        show_login_list_window = tk.Toplevel(self.root)
        show_login_list_window.title("Lista de Logins")
        show_login_list_window.geometry("400x400")

        listbox = tk.Listbox(show_login_list_window)
        for login in self.login_list:
            listbox.insert(tk.END, f"Login: {login['email']}")
        listbox.pack()

        button_edit = tk.Button(show_login_list_window, text="Editar", command=edit_login)
        button_edit.pack()

        button_delete = tk.Button(show_login_list_window, text="Excluir", command=delete_login)
        button_delete.pack()

        close_button = tk.Button(show_login_list_window, text="Fechar", command=show_login_list_window.destroy)
        close_button.pack()

    def close_secondary_interface(self):
        self.root.withdraw()  # Oculta a janela secundária
        main_app = telainicial.Main(tk.Tk())  # Cria uma nova instância da classe Main


if __name__ == "__main__":
    root = tk.Tk()
    main = InterfaceManager(root)
    root.mainloop()
