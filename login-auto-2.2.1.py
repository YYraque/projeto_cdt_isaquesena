import sys
import os
import time
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Variavel global para controlar o tema
modo_escuro = False

def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro

    if modo_escuro:
        bg_geral = "#1e1e1e"
        fg_texto = "#ffffff"
        entry_bg = "#2d2d2d"
        entry_fg = "#ffffff"
        btn_tema_txt = "☀️ Modo Claro"
    else:
        bg_geral = "#f0f0f0"
        fg_texto = "#000000"
        entry_bg = "#ffffff"
        entry_fg = "#000000"
        btn_tema_txt = "🌙 Modo Escuro"

    # Atualiza cores dos elementos da interface
    root.config(bg=bg_geral)
    label_usuario.config(bg=bg_geral, fg=fg_texto)
    entry_usuario.config(bg=entry_bg, fg=entry_fg, insertbackground=fg_texto)
    
    label_senha.config(bg=bg_geral, fg=fg_texto)
    entry_senha.config(bg=entry_bg, fg=entry_fg, insertbackground=fg_texto)
    
    btn_tema.config(text=btn_tema_txt, bg="#4a4a4a" if modo_escuro else "#e0e0e0", fg=fg_texto)


def executar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        return

    # Oculta a janela da interface gráfica durante a automação
    root.withdraw()

    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # Configuração do ChromeDriver gerenciado automaticamente
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        wait = WebDriverWait(driver, 15)

        # Realizar Login no GitHub
        driver.get("https://github.com/login")
        
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "login_field")))
        campo_usuario.send_keys(usuario)
        
        driver.find_element(By.ID, "password").send_keys(senha)
        driver.find_element(By.NAME, "commit").click()

        # Aguarda a confirmação de login
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header, .AppHeader")))
        
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o login:\n{str(e)}")
    finally:
        root.destroy()


# --- Interface Gráfica (Tkinter) ---
root = tk.Tk()
root.title("Automação GitHub - Login")
root.geometry("320x280")
root.config(bg="#f0f0f0")

# Botão Alternar Tema (Claro / Escuro)
btn_tema = tk.Button(
    root, 
    text="🌙 Modo Escuro", 
    command=alternar_tema, 
    bg="#e0e0e0", 
    fg="#000000", 
    bd=1, 
    relief="solid"
)
btn_tema.pack(anchor="ne", padx=10, pady=10)

# Campo Usuário
label_usuario = tk.Label(root, text="Usuário / E-mail:", bg="#f0f0f0", fg="#000000")
label_usuario.pack(pady=(5, 2))
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack(pady=2)

# Campo Senha
label_senha = tk.Label(root, text="Senha:", bg="#f0f0f0", fg="#000000")
label_senha.pack(pady=(10, 2))
entry_senha = tk.Entry(root, show="*", width=30)
entry_senha.pack(pady=2)

# Botão Fazer Login
btn_iniciar = tk.Button(
    root, 
    text="Fazer Login", 
    command=executar_login, 
    bg="#002f70", 
    fg="white", 
    font=("Arial", 10, "bold")
)
btn_iniciar.pack(pady=20)

root.mainloop()