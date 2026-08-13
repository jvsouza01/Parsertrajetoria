import json
import requests
import sys
import os

JSON_PATH = os.path.join("output", "questoes_payload_api.json")
URL = "http://localhost:8080/api/admin/ingestao/questoes"

if not os.path.exists(JSON_PATH):
    print(f"[ERRO] Arquivo {JSON_PATH} nao encontrado. Execute o parser primeiro.")
    sys.exit(1)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

print(f"[INFO] Carregadas {len(questoes)} questoes para envio...")

headers = {
    'Content-Type': 'application/json'
}

token = os.getenv("ADMIN_TOKEN")
if len(sys.argv) > 1:
    token = sys.argv[1]

if token:
    headers['Authorization'] = f"Bearer {token}"
    print("[AUTH] Utilizando token de autenticacao fornecido.")
else:
    print("[WARN] Nenhum token fornecido.")

try:
    response = requests.post(URL, json=questoes, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"[SUCESSO] {len(questoes)} questoes salvas e classificadas por IA com sucesso!")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception:
            print(response.text)
    else:
        print(f"[ERRO] Erro ao enviar. Status: {response.status_code}")
        print(f"Resposta da API: {response.text}")

except Exception as e:
    print(f"[ERRO] Erro de conexao com a API ({URL}): {e}")
