import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def executar_automação():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        return

    
    root.destroy()

    
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://github.com/login")

    
    driver.find_element(By.ID, "login_field").send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(senha)
    driver.find_element(By.NAME, "commit").click()


    driver.switch_to.new_window('tab')
    driver.get("https://github.com")

root = tk.Tk()
root.title("Automação GitHub")
root.geometry("300x200")

# Campo Usuário
label_usuario = tk.Label(root, text="Usuário / E-mail:")
label_usuario.pack(pady=(15, 2))
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack(pady=2)

# Campo Senha
label_senha = tk.Label(root, text="Senha:")
label_senha.pack(pady=(10, 2))
entry_senha = tk.Entry(root, show="*", width=30)
entry_senha.pack(pady=2)

# Botão para Iniciar
btn_iniciar = tk.Button(root, text="Fazer Login", command=executar_automação, bg="#002f70", fg="white", font=("Arial", 10, "bold"))
btn_iniciar.pack(pady=15)

root.mainloop()