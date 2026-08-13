import json
import requests
import sys

JSON_PATH = "output/questoes_payload_api.json"
URL = "http://localhost:8080/api/admin/ingestao/questoes"

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

token = sys.argv[1]
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {token}"
}

print(f"Testando envio item a item (Total: {len(questoes)})...")

sucessos = 0
duplicados = 0
erros = 0

for i, q in enumerate(questoes):
    payload = [q]
    resp = requests.post(URL, json=payload, headers=headers)
    if resp.status_code in [200, 201]:
        sucessos += 1
        print(f"[{i+1}/{len(questoes)}] [SUCESSO] Item {q['idOrigem']} salvo com sucesso!")
    elif resp.status_code == 409:
        duplicados += 1
        print(f"[{i+1}/{len(questoes)}] [DUPLICADO] Item {q['idOrigem']} ja existe no banco.")
    else:
        erros += 1
        print(f"[{i+1}/{len(questoes)}] [ERRO] Item {q['idOrigem']}: {resp.status_code} - {resp.text}")

print("\n=== RESUMO DO ENVIO ===")
print(f"Novas questoes salvas: {sucessos}")
print(f"Questoes ja existentes (duplicadas): {duplicados}")
print(f"Erros: {erros}")
