import os
import json
import glob

files = sorted(glob.glob("payloadepdf/payload_*.json"))
print("=" * 100)
print(f"{'ARQUIVO':<50} | {'QTD':<5} | {'POSICOES':<22} | {'COM TEXTO BASE'}")
print("=" * 100)

for f in files:
    try:
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        
        posicoes = [q.get("posicao") for q in data if isinstance(q, dict) and "posicao" in q]
        com_tb = sum(1 for q in data if q.get("textoBase"))
        letras = set()
        for q in data:
            for alt in q.get("alternativas", []):
                letras.add(alt.get("letra"))
        
        if posicoes:
            pos_str = f"{min(posicoes)}..{max(posicoes)} ({len(posicoes)} un.)"
        else:
            pos_str = "0"
            
        print(f"{os.path.basename(f):<50} | {len(data):<5} | {pos_str:<22} | {com_tb} questoes (Letras: {sorted(list(letras))[:6]})")
    except Exception as e:
        print(f"{os.path.basename(f):<50} | ERRO: {e}")
print("=" * 100)
