# import json
# import random
# import threading
# import time
# import tkinter as tk
# from tkinter import Text, Scrollbar, Entry, Listbox, Button, END, messagebox, Toplevel
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# import interface
#
# def load_login_list():
#     try:
#         with open("login_list.json", "r") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return []
#
# def save_login_list(login_list):
#     with open("login_list.json", "w") as file:
#         json.dump(login_list, file)
#
# class Main:
#     def __init__(self, root):
#         self.secondary_interface = None
#         self.root = root
#         root.title("Spotify Automation")
#
#
#         self.create_login_ui()
#         self.create_automation_ui()
#         self.create_log_ui()
#         self.create_buttons()
#
#         self.driver = None
#         self.running_thread = None
#         self.show_password = False
#
#         # Tenta carregar as credenciais salvas
#         self.load_credentials()
#
#         # Carrega os logins cadastrados a partir do JSON
#         self.login_list = load_login_list()
#
#         # Limpe os campos ao iniciar o aplicativo
#         self.clear_fields()
#
#     def create_login_ui(self):
#         login_frame = tk.Frame(self.root)
#         login_frame.pack(pady=10)
#         tk.Label(login_frame, text="Email:").grid(row=0, column=0, sticky="e")
#         self.entry_email = tk.Entry(login_frame)
#         self.entry_email.grid(row=0, column=1, padx=10, pady=5)
#         tk.Label(login_frame, text="Senha:").grid(row=1, column=0, sticky="e")
#         self.entry_senha = Entry(login_frame, show='*')
#         self.entry_senha.grid(row=1, column=1, padx=10, pady=5)
#         self.show_password_var = tk.IntVar()
#         self.show_password_checkbox = tk.Checkbutton(login_frame, text="Mostrar Senha", variable=self.show_password_var, command=self.toggle_password)
#         self.show_password_checkbox.grid(row=2, column=1, padx=10, pady=5)
#
#     def create_automation_ui(self):
#         tk.Label(self.root, text="Nome do Cantor:").pack()
#         self.entry_cantor = tk.Entry(self.root)
#         self.entry_cantor.pack()
#
#     def create_log_ui(self):
#         log_frame = tk.Frame(self.root)
#         log_frame.pack(pady=10)
#         tk.Label(log_frame, text="Log:").grid(row=0, column=0, sticky="w")
#         self.log_text = Text(log_frame, height=10, width=40)
#         self.log_text.grid(row=1, column=0)
#         self.scrollbar = Scrollbar(log_frame, command=self.log_text.yview)
#         self.scrollbar.grid(row=1, column=1, sticky="nsew")
#         self.log_text.config(yscrollcommand=self.scrollbar.set)
#         self.log_text.tag_configure("error", foreground="red")
#
#     def create_buttons(self):
#         button_frame = tk.Frame(self.root)
#         button_frame.pack(pady=10)
#         tk.Button(button_frame, text="Iniciar", command=self.start).pack(side="left", padx=10)
#         tk.Button(button_frame, text="Cadastrar Conta do Spotify", command=self.mudar_interface).pack(side="left", padx=10)
#         tk.Button(button_frame, text="Logins Cadastrados", command=self.show_login_list).pack(side="left", padx=10)
#         tk.Button(button_frame, text="Limpar Campos", command=self.clear_fields).pack(side="left", padx=10)
#
#     def toggle_password(self):
#         self.show_password = bool(self.show_password_var.get())
#         if self.show_password:
#             self.entry_senha.config(show="")
#         else:
#             self.entry_senha.config(show="*")
#
#     def clear_fields(self):
#         self.entry_email.delete(0, tk.END)
#         self.entry_senha.delete(0, tk.END)
#         self.entry_cantor.delete(0, tk.END)
#
#     def start(self):
#         if self.campos_de_login_preenchidos():
#             if self.running_thread is None or not self.running_thread.is_alive():
#                 self.running_thread = threading.Thread(target=self.run_automation)
#                 self.running_thread.start()
#         else:
#             messagebox.showerror("Erro", "Por favor, preencha os campos de login e senha.")
#
#     def run_automation(self):
#         self.login_sptfy = self.entry_email.get()
#         self.senha_sptfy = self.entry_senha.get()
#         self.buscar_cantor = self.entry_cantor.get()
#
#         try:
#             self.driver = webdriver.Chrome()
#             self.driver.get("https://open.spotify.com/intl-pt")
#
#             self.entrando_pag_login()
#             self.fazendo_login()
#             self.buscando_cantor()
#             self.clicando_no_cantor()
#             self.pagina_do_cantor("/intl-pt/artist/", "/discography/all")
#
#             self.log("Automação concluída com sucesso.")
#         except Exception as e:
#             self.log("Erro durante a automação:", "error")
#             self.log(str(e), "error")
#
#     def entrando_pag_login(self):
#         self.log("Entrando na página de login...")
#         botao_entrar = self.driver.find_element(By.XPATH, "//button[@data-testid='login-button']")
#         botao_entrar.click()
#         time.sleep(3)
#
#     def fazendo_login(self):
#         self.log("Fazendo login...")
#         campo_email = self.driver.find_element(By.XPATH, "//input[@id='login-username']")
#         campo_senha = self.driver.find_element(By.XPATH, "//input[@id='login-password']")
#         botao_entrar = self.driver.find_element(By.XPATH, "//button[@data-testid='login-button']")
#
#         campo_email.clear()
#         self.digite_como_uma_pessoa(self.login_sptfy, campo_email)
#         time.sleep(2)
#
#         campo_senha.clear()
#         self.digite_como_uma_pessoa(self.senha_sptfy, campo_senha)
#         time.sleep(3)
#
#         botao_entrar.click()
#         time.sleep(10)
#
#     def buscando_cantor(self):
#         self.log(f"Buscando o cantor {self.buscar_cantor}...")
#         botao_buscar = self.driver.find_element(By.XPATH, "//a[@href='/search']")
#         botao_buscar.click()
#         time.sleep(5)
#
#         caixa_de_busca = self.driver.find_element(By.XPATH, "//input[@data-testid='search-input']")
#         self.digite_como_uma_pessoa(self.buscar_cantor, caixa_de_busca)
#         time.sleep(3)
#
#     def clicando_no_cantor(self):
#         self.log(f"Clicando no cantor {self.buscar_cantor}...")
#         clicando_cantor = self.driver.find_element(By.XPATH, "//div[@data-testid='herocard-click-handler']")
#         clicando_cantor.click()
#         time.sleep(10)
#
#     def pagina_do_cantor(self, classe, texto):
#         self.log(f"Acessando página do cantor {self.buscar_cantor}...")
#         elemento_mostrar_tudo = self.driver.find_element(By.XPATH,
#                                                          f"//a[contains(@href, '{classe}') and contains(., '{texto}')]")
#         try:
#             elemento_mostrar_tudo.click()
#         except Exception as e:
#             self.log(f"Erro ao acessar a página do cantor: {str(e)}", "error")
#
#     def log(self, message, tag=None):
#         self.log_text.insert(tk.END, message + "\n", tag)
#         self.log_text.see(tk.END)
#
#     @staticmethod
#     def digite_como_uma_pessoa(frase, campo_input_unico):
#         print("Digitando...")
#         for letra in frase:
#             campo_input_unico.send_keys(letra)
#             time.sleep(random.randint(1, 5) / 30)
#
#     def load_credentials(self):
#         try:
#             # Tenta carregar as credenciais salvas no arquivo credenciais.json
#             with open("credenciais.json", "r") as file:
#                 credentials = json.load(file)
#                 self.entry_email.insert(0, credentials["email"])
#                 self.entry_senha.insert(0, credentials["senha"])
#         except FileNotFoundError:
#             pass  # Se o arquivo não existir, não faz nada
#
#     def show_login_list(self):
#         if not self.login_list:
#             messagebox.showinfo("Logins Cadastrados", "Nenhum login cadastrado.")
#             return
#
#         # Abre uma nova janela para mostrar os logins cadastrados em forma de lista
#         login_list_window = Toplevel(self.root)
#         login_list_window.title("Logins Cadastrados")
#         login_list_window.geometry("400x200")
#
#         listbox = Listbox(login_list_window, selectmode=tk.SINGLE)
#         for login in self.login_list:
#             listbox.insert(END, f"Login: {login['email']}")
#
#         listbox.pack()
#
#         # Adicione um botão "Selecionar"
#         select_button = Button(login_list_window, text="Selecionar",
#                                command=lambda: self.select_login(login_list_window, listbox))
#         select_button.pack()
#
#     def select_login(self, login_list_window, listbox):
#         selected_index = listbox.curselection()
#         if selected_index:
#             selected_index = int(selected_index[0])
#             selected_login = self.login_list[selected_index]
#             email = selected_login['email']
#             senha = selected_login['senha']
#
#             # Preencha os campos de email e senha com o login selecionado
#             self.entry_email.delete(0, tk.END)
#             self.entry_email.insert(0, email)
#             self.entry_senha.delete(0, tk.END)
#             self.entry_senha.insert(0, senha)
#
#             # Feche a janela de seleção
#             login_list_window.destroy()
#
#     def edit_interface(self):
#         edit_interface_window = Toplevel(self.root)
#         edit_interface_window.title("Login Manager")
#         edit_interface_window.geometry("400x200")
#
#         self.login_list = load_login_list()
#
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.label_email = tk.Label(self.root, text="Email:")
#         self.label_email.pack()
#
#         self.entry_email = tk.Entry(self.root)
#         self.entry_email.pack()
#
#         self.label_senha = tk.Label(self.root, text="Senha:")
#         self.label_senha.pack()
#
#         self.entry_senha = tk.Entry(self.root, show='*')
#         self.entry_senha.pack()
#
#         self.button_add = tk.Button(self.root, text="Adicionar", command=self.add_login)
#         self.button_add.pack()
#
#         self.button_show = tk.Button(self.root, text="Mostrar Logins", command=self.show_login_list)
#         self.button_show.pack()
#
#     def add_login(self):
#         email = self.entry_email.get()
#         senha = self.entry_senha.get()
#
#         if not email or not senha:
#             messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
#             return
#
#         # Verifica se o login já existe
#         for login in self.login_list:
#             if login["email"] == email:
#                 messagebox.showerror("Erro", "Login já cadastrado.")
#                 return
#
#         self.login_list.append({"email": email, "senha": senha})
#         save_login_list(self.login_list)
#         self.entry_email.delete(0, tk.END)
#         self.entry_senha.delete(0, tk.END)
#
#     def show_login_list(self):
#         def edit_login():
#             selected_index = listbox.curselection()[0]
#             selected_login = self.login_list[selected_index]
#
#             def save_changes():
#                 selected_login["email"] = entry_email.get()
#                 selected_login["senha"] = entry_senha.get()
#                 save_login_list(self.login_list)
#                 edit_login_window.destroy()
#                 listbox.delete(selected_index)
#                 listbox.insert(selected_index, f"Login: {selected_login['email']}")
#
#             def cancel_changes():
#                 edit_login_window.destroy()
#
#             edit_login_window = tk.Toplevel(self.root)
#             edit_login_window.title("Editar Login")
#             edit_login_window.geometry("400x200")
#
#             entry_email = tk.Entry(edit_login_window)
#             entry_email.insert(0, selected_login["email"])
#             entry_email.pack()
#
#             entry_senha = tk.Entry(edit_login_window, show='*')
#             entry_senha.insert(0, selected_login["senha"])
#             entry_senha.pack()
#
#             save_button = tk.Button(edit_login_window, text="Salvar", command=save_changes)
#             save_button.pack()
#
#             cancel_button = tk.Button(edit_login_window, text="Cancelar", command=cancel_changes)
#             cancel_button.pack()
#
#         def delete_login():
#             selected_index = listbox.curselection()[0]
#             self.login_list.pop(selected_index)
#             save_login_list(self.login_list)
#             listbox.delete(selected_index)
#
#         show_login_list_window = tk.Toplevel(self.root)
#         show_login_list_window.title("Lista de Logins")
#         show_login_list_window.geometry("400x400")
#
#         listbox = tk.Listbox(show_login_list_window)
#         for login in self.login_list:
#             listbox.insert(tk.END, f"Login: {login['email']}")
#         listbox.pack()
#
#         button_edit = tk.Button(show_login_list_window, text="Editar", command=edit_login)
#         button_edit.pack()
#
#         button_delete = tk.Button(show_login_list_window, text="Excluir", command=delete_login)
#         button_delete.pack()
#
#         close_button = tk.Button(show_login_list_window, text="Fechar", command=show_login_list_window.destroy)
#         close_button.pack()
#
#     def mudar_interface(self):
#         self.secondary_interface = Toplevel(self.root)
#         interface.InterfaceManager(self.secondary_interface)
#         self.root.withdraw()
#
#     def campos_de_login_preenchidos(self):
#         email = self.entry_email.get()
#         senha = self.entry_senha.get()
#         return email and senha
#
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = Main(root)
#     root.mainloop()
