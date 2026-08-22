import os
import sys
import time
import webbrowser
import threading
from app import app

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:5000")

if __name__ == '__main__':
    port = 5000
    print("\n" + "="*60)
    print(" [*] PARSER TRAJETORIA STUDIO - v2.0")
    print(" Interface visual para ingestao e extracao de provas")
    print("="*60)
    print(f"\n -> Abrindo o estudio no seu navegador em: http://localhost:{port}\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=port, debug=False)

