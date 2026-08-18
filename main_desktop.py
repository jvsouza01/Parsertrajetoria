import os
import sys
import time
import webbrowser
import threading
from app import app

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception as e:
        print(f"[Aviso] Nao foi possivel abrir o navegador automaticamente: {e}")

if __name__ == '__main__':
    port = 5000
    print("\n" + "="*60)
    print("   PARSER TRAJETORIA STUDIO - EXECUTAVEL LOCAL")
    print("="*60)
    print(f"\n -> Servidor ativo em: http://127.0.0.1:{port}")
    print(" -> Seu navegador padrao abrira automaticamente.")
    print(" -> Para encerrar o programa, basta fechar esta janela.\n")
    print("="*60 + "\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='127.0.0.1', port=port, debug=False)
