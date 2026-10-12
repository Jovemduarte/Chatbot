import threading
import customtkinter as ctk
from tkinter import scrolledtext
from dotenv import load_dotenv
from google import genai

load_dotenv()

cliente = genai.Client()

print("Chatbot iniciado (Digite 'sair' para encerrar )")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Meu Chatbot")
janela.geometry("500x600")

chat = ctk.CTkTextbox(janela, wrap="word", font=("Segoe UI", 14), state="disabled")
chat.pack(padx=10, pady=10, fill="both", expand=True)

rodape = ctk.CTkFrame(janela, fg_color="transparent")
rodape.pack(padx=10, pady=(0, 10), fill="x")

entrada = ctk.CTkEntry(rodape, placeholder_text="Digite sua mensagem...", height=40, font=("Segoe UI", 14))
entrada.pack(side="left", fill="x", expand=True)


def escrever(texto):
    chat.configure(state="normal")
    chat.insert(ctk.END, texto + "\n\n")
    chat.configure(state="disabled")
    chat.see(ctk.END)
def pedir_resposta(pergunta):
    try:
        resposta = cliente.models.generate_content(
            model="gemini-3.8-flash",
            contents=pergunta
        )
        texto = resposta.text
    except Exception as e:
        texto = (f"Erro ao conectar a API: {e}")

    janela.after(0, lambda: escrever("Bot: " + texto))
    janela.after(0, lambda: botao.configure(state="normal"))

def enviar(event=None):
    pergunta = entrada.get().strip()
    if not pergunta:
        return

    entrada.delete(0, ctk.END)
    escrever("Você: " + pergunta)
    botao.configure(state="disabled")

    threading.Thread(target=pedir_resposta, args=(pergunta,), daemon=True).start()

botao = ctk.CTkButton(rodape, text="Enviar", command=enviar, width=80, height=40)
botao.pack(side="right", padx=(8, 0))

entrada.bind("<Return>", enviar)
entrada.focus()


escrever("Bot: Olá! Pode me perguntar o que quiser.")

janela.mainloop()





