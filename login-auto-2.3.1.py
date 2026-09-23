import sys
import os
import time
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

modo_escuro = False

# --- Função para Criar e Salvar no Banco de Dados SQLite ---
def registrar_log_banco(usuario):
    # Cria (ou abre se já existir) o arquivo de banco de dados 'historico_logins.db'
    conn = sqlite3.connect("historico_logins.db")
    cursor = conn.cursor()

    # Cria a tabela caso ela ainda não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')

    # Obtém a data e hora atual no formato YYYY-MM-DD HH:MM:SS
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insere o registro de login
    cursor.execute('''
        INSERT INTO logins (usuario, data_hora)
        VALUES (?, ?)
    ''', (usuario, data_hora_atual))

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()


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

    root.withdraw()

    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        wait = WebDriverWait(driver, 15)

        driver.get("https://github.com/login")
        
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "login_field")))
        campo_usuario.send_keys(usuario)
        
        driver.find_element(By.ID, "password").send_keys(senha)
        driver.find_element(By.NAME, "commit").click()

        # Aguarda a confirmação de login
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header, .AppHeader")))
        
        # --- REGISTRA NO BANCO DE DADOS APÓS O LOGIN BEM-SUCEDIDO ---
        registrar_log_banco(usuario)
        
        messagebox.showinfo("Sucesso", "Login realizado e registrado no banco de dados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o login:\n{str(e)}")
    finally:
        root.destroy()


# --- Interface Gráfica (Tkinter) ---
root = tk.Tk()
root.title("Automação GitHub - Login")
root.geometry("320x280")
root.config(bg="#f0f0f0")

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

label_usuario = tk.Label(root, text="Usuário / E-mail:", bg="#f0f0f0", fg="#000000")
label_usuario.pack(pady=(5, 2))
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack(pady=2)

label_senha = tk.Label(root, text="Senha:", bg="#f0f0f0", fg="#000000")
label_senha.pack(pady=(10, 2))
entry_senha = tk.Entry(root, show="*", width=30)
entry_senha.pack(pady=2)

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