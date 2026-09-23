import sqlite3
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configurações globais do tema CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


def registrar_log_banco(usuario):
    try:
        conn = sqlite3.connect("historico_logins.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
        ''')
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO logins (usuario, data_hora)
            VALUES (?, ?)
        ''', (usuario, data_hora_atual))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro no banco: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


def fluxo_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        restaurar_botao_login()
        return

    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        wait = WebDriverWait(driver, 20)
        driver.get("https://github.com/login")
        
        campo_usuario = wait.until(EC.presence_of_element_located((By.ID, "login_field")))
        campo_usuario.send_keys(usuario)
        
        driver.find_element(By.ID, "password").send_keys(senha)
        driver.find_element(By.NAME, "commit").click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header, .AppHeader, div.AppHeader-user")))
        
        registrar_log_banco(usuario)
        messagebox.showinfo("Sucesso", "Login realizado e registrado com sucesso!")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante o login:\n{str(e)}")
        restaurar_botao_login()


def restaurar_botao_login():
    progress_bar.stop()
    progress_bar.pack_forget()
    btn_iniciar.configure(state="normal", text="Fazer Login")


def iniciar_thread_login(event=None):
    btn_iniciar.configure(state="disabled", text="Entrando...")
    progress_bar.pack(pady=10)
    progress_bar.start()
    threading.Thread(target=fluxo_login, daemon=True).start()


def alternar_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        btn_tema.configure(text="🌙 Modo Escuro")
    else:
        ctk.set_appearance_mode("Dark")
        btn_tema.configure(text="☀️ Modo Claro")


def abrir_janela_historico():
    janela_hist = ctk.CTkToplevel(root)
    janela_hist.title("Histórico de Logins")
    janela_hist.geometry("450x350")
    janela_hist.grab_set()  # Foca na janela secundária

    titulo = ctk.CTkLabel(janela_hist, text="Registros de Login", font=ctk.CTkFont(size=16, weight="bold"))
    titulo.pack(pady=10)

    # Caixa de texto rolável para exibir o histórico
    caixa_texto = ctk.CTkTextbox(janela_hist, width=400, height=250, corner_radius=10)
    caixa_texto.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        conn = sqlite3.connect("historico_logins.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, data_hora FROM logins ORDER BY id DESC")
        registros = cursor.fetchall()
        
        if not registros:
            caixa_texto.insert("end", "Nenhum log encontrado.")
        else:
            caixa_texto.insert("end", f"{'ID':<5} | {'Usuário':<20} | Data e Hora\n")
            caixa_texto.insert("end", "-" * 50 + "\n")
            for reg in registros:
                caixa_texto.insert("end", f"{reg[0]:<5} | {reg[1]:<20} | {reg[2]}\n")

        caixa_texto.configure(state="disabled")  # Apenas leitura
        conn.close()
    except sqlite3.Error as e:
        caixa_texto.insert("end", f"Erro ao carregar dados: {e}")


# --- Interface Principal ---
root = ctk.CTk()
root.title("Automação GitHub - Login")
root.geometry("380x420")
root.resizable(False, False)

# Botão de Tema
btn_tema = ctk.CTkButton(
    root, 
    text="☀️ Modo Claro" if ctk.get_appearance_mode() == "Dark" else "🌙 Modo Escuro", 
    command=alternar_tema,
    width=100,
    height=28,
    corner_radius=15,
    fg_color="transparent",
    border_width=1
)
btn_tema.pack(anchor="ne", padx=15, pady=15)

# Container central estilo Card
card_frame = ctk.CTkFrame(root, corner_radius=15)
card_frame.pack(padx=20, pady=5, fill="both", expand=True)

label_titulo = ctk.CTkLabel(card_frame, text="Acessar GitHub", font=ctk.CTkFont(size=18, weight="bold"))
label_titulo.pack(pady=(15, 10))

entry_usuario = ctk.CTkEntry(card_frame, placeholder_text="Usuário ou E-mail", width=250, corner_radius=10)
entry_usuario.pack(pady=8)

entry_senha = ctk.CTkEntry(card_frame, placeholder_text="Senha", show="*", width=250, corner_radius=10)
entry_senha.pack(pady=8)
entry_senha.bind("<Return>", iniciar_thread_login)

btn_iniciar = ctk.CTkButton(
    card_frame, 
    text="Fazer Login", 
    command=iniciar_thread_login,
    width=250,
    height=35,
    corner_radius=10,
    font=ctk.CTkFont(size=13, weight="bold")
)
btn_iniciar.pack(pady=12)

# Indicator de carregamento
progress_bar = ctk.CTkProgressBar(card_frame, width=250, mode="indeterminate")

btn_historico = ctk.CTkButton(
    card_frame, 
    text="📋 Ver Histórico", 
    command=abrir_janela_historico,
    fg_color="gray30",
    hover_color="gray20",
    width=250,
    height=30,
    corner_radius=10
)
btn_historico.pack(pady=(5, 15))

root.mainloop()