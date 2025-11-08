import tkinter as tk
from tkinter import messagebox
import time
import threading
import sys

class VirusSimulador:
    def __init__(self):
        self.senha_correta = "12345"
        self.abas_abertas = 0
        self.max_abas = 50
        self.janelas = []

    def bloquear_fechamento(self, janela):
        messagebox.showwarning("BLOQUEADO", "Sistema comprometido! Use a senha na janela principal.")

    def criar_janela_alarme(self):
        self.root = tk.Tk()
        self.root.title("🚨 ALERTA CRÍTICO DO SISTEMA 🚨")
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.attributes('-fullscreen', True)  # TELA CHEIA

        # Mensagem alarmante
        label = tk.Label(self.root,
                         text="⚠️  VÍRUS DETECTADO NO SISTEMA  ⚠️\n\n"
                              "SEU COMPUTADOR ESTÁ COMPROMETIDO!\n"
                              "Todos os arquivos estão sendo criptografados...\n"
                              "Todas as janelas estão BLOQUEADAS!\n\n"
                              "DIGITE A SENHA PARA INTERROMPER:",
                         font=('Arial', 16, 'bold'),
                         fg='red',
                         bg='black',
                         justify='center')
        label.pack(pady=50)

        # Campo de senha
        self.senha_entry = tk.Entry(self.root, show='*', font=('Arial', 18), width=20)
        self.senha_entry.pack(pady=20)
        self.senha_entry.focus()

        # Botão de verificação
        def verificar_senha():
            if self.senha_entry.get() == self.senha_correta:
                self.fechar_tudo()
            else:
                messagebox.showerror("ERRO", "SENHA INCORRETA! O sistema continua comprometido.")

        btn = tk.Button(self.root,
                        text="TENTAR INTERROMPER INFECÇÃO",
                        command=verificar_senha,
                        font=('Arial', 12, 'bold'),
                        bg='red',
                        fg='white',
                        width=25,
                        height=2)
        btn.pack(pady=20)

        # Bind Enter para verificar senha
        self.senha_entry.bind('<Return>', lambda e: verificar_senha())

        # Bloquear fechamento
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.bloquear_fechamento(self.root))

        # Desabilitar Alt+F4, Alt+Tab, etc
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Alt-Tab>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')

        self.root.mainloop()

    def fechar_tudo(self):
        """Fecha todas as janelas quando a senha estiver correta"""
        for janela in self.janelas:
            try:
                janela.destroy()
            except:
                pass
        self.root.quit()
        sys.exit()

    def abrir_abas(self):
        for i in range(self.max_abas):
            self.abas_abertas += 1
            threading.Thread(target=self.criar_janela_aba, args=(i + 1,), daemon=True).start()
            time.sleep(0.4)  # Intervalo rápido entre abas

    def criar_janela_aba(self, numero):
        janela = tk.Toplevel()
        janela.title(f"🚨 ALERTA DE SEGURANÇA {numero} 🚨")
        janela.geometry("500x150")
        janela.attributes('-topmost', True)

        # Configurações para dificultar fechamento
        janela.attributes('-toolwindow', False)
        janela.resizable(False, False)

        label = tk.Label(janela,
                         text=f"PROCESSO SUSPEITO DETECTADO #{numero}\n\n"
                              "Esta janela está BLOQUEADA!\n"
                              "Use a senha na janela principal para fechar.",
                         font=('Arial', 12, 'bold'),
                         fg='white',
                         bg='red',
                         justify='center')
        label.pack(expand=True, fill='both')

        # Bloquear completamente o fechamento
        def tentar_fechar():
            messagebox.showwarning("JANELA BLOQUEADA",
                                   "Não é possível fechar esta janela!\n"
                                   "O sistema está comprometido.\n"
                                   "Use a senha na janela principal.")

        janela.protocol("WM_DELETE_WINDOW", tentar_fechar)
        janela.bind('<Alt-F4>', lambda e: 'break')
        janela.bind('<Escape>', lambda e: 'break')

        # Adicionar à lista de janelas para fechar depois
        self.janelas.append(janela)

        # Manter a janela aberta
        janela.mainloop()

# Executar o simulador
if __name__ == "__main__":
    # Executar o "vírus" (sem persistência)
    virus = VirusSimulador()

    # Iniciar abertura de abas em thread separada
    threading.Thread(target=virus.abrir_abas, daemon=True).start()

    # Mostrar janela principal de alarme
    virus.criar_janela_alarme()
