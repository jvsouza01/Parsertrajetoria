import json
import requests

JSON_PATH = "output/questoes_payload_api.json"
URL = "http://localhost:8080/api/admin/ingestao/questoes"

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

headers = {
    'Content-Type': 'application/json'
}

for q in questoes:
    q['statusRevisao'] = 'APROVADO_AUTO'
    if q.get('materiaNome') == 'História':
        q['materiaNome'] = 'Linguagens'

print(f"[ENVIO LIBERADO] Enviando {len(questoes)} questoes para {URL}...")

sucessos = 0
duplicados = 0
erros = 0

for i, q in enumerate(questoes):
    r = requests.post(URL, json=[q], headers=headers)
    if r.status_code in [200, 201]:
        sucessos += 1
        print(f"[{i+1}/{len(questoes)}] [SUCESSO 201] Item {q['idOrigem']} ({q['materiaNome']}) inserido e classificado por IA!")
    elif r.status_code == 409:
        duplicados += 1
        print(f"[{i+1}/{len(questoes)}] [JA EXISTE 409] Item {q['idOrigem']} ({q['materiaNome']})")
    else:
        erros += 1
        print(f"[{i+1}/{len(questoes)}] [ERRO {r.status_code}] Item {q['idOrigem']}: {r.text[:150]}")

print("\n=== RESULTADO FINAL DO ENVIO ===")
print(f"Novas questoes inseridas: {sucessos}")
print(f"Questoes ja existentes (prevenidas contra duplicidade): {duplicados}")
print(f"Erros restantes: {erros}")
print(f"TOTAL DE QUESTOES PROCESSADAS NO BACKEND: {sucessos + duplicados} / {len(questoes)}")
