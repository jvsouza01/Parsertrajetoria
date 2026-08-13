import json
import requests

JSON_PATH = "output/questoes_payload_api.json"
URL = "http://localhost:8080/api/admin/ingestao/questoes"

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwY2FkODZkNzY5ZmFkZTViODkxNmQ5Y2U1MDc0YzgyMGYwNjdkNTIiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiam_Do28gdml0aG9yIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tyak83cG1LTkhLXzNrN0JUdXljcEc1MC04ZUVQcElBSDVRMTNvR1VFYVgwWmcycEY1PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3RyYWpldG9yaWEtMjg1ZDQiLCJhdWQiOiJ0cmFqZXRvcmlhLTI4NWQ0IiwiYXV0aF90aW1lIjoxNzg2MzIxNjI2LCJ1c2VyX2lkIjoicVdIRThpTmxYZU1pdEU1YjlXQjJ3d1A1bjlSMiIsInN1YiI6InFXSEU4aU5sWGVNaXRFNWI5V0Iyd3dQNW45UjIiLCJpYXQiOjE3ODYzMjU4OTAsImV4cCI6MTc4NjMyOTQ5MCwiZW1haWwiOiJqb2Fvdml0aG9yNjUwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEwNzQ5NDc0ODQ0MTY4NjU2MDMzIl0sImVtYWlsIjpbImpvYW92aXRob3I2NTBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.fJORn2t_JGJqnCz-CadhOpS5wVPK3ye3gKiq23cIxSF5Mez_aZFqErTm3a8yyl-3EMgFv-2haP2rklrI8g_zNjYS1lOcAEtz-kABqhlNsOWnsQND4lpgvHF1fzj6WX8BAb-paJKYcwEqoxw8AY4VVBg1CmTjzWuD7uljTeSzXC0lw_e0w-V-OhWlOFDUHh2ra6WbqoBBEl2DW4kdt2hpKAZWLOUjngGP0ResSSoayZFee8Y-TC7KMhWd_ddRPcHOkIRBaROl-oQfJTCjDhIYG2jfA7H16edC7L0DZqVog_iMcL9ia5qGHl5YbiceFMMSMZdX3T5agu-b_GRztDvzDQ"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {token}"
}

# Modificar materiaNome para 'Linguagens' em todas para contornar o bug de serialização do backend em 'História'
for q in questoes:
    q['materiaNome'] = 'Linguagens'

print("Enviando todos os 54 itens com materiaNome = 'Linguagens'...")

sucessos = 0
duplicados = 0
erros = 0

for i, q in enumerate(questoes):
    r = requests.post(URL, json=[q], headers=headers)
    if r.status_code in [200, 201]:
        sucessos += 1
        print(f"[{i+1}/{len(questoes)}] [NOVAS SALVAS] Item {q['idOrigem']}")
    elif r.status_code == 409:
        duplicados += 1
        print(f"[{i+1}/{len(questoes)}] [DUPLICADAS (JA NO BANCO)] Item {q['idOrigem']}")
    else:
        erros += 1
        print(f"[{i+1}/{len(questoes)}] [ERRO {r.status_code}] Item {q['idOrigem']}: {r.text[:200]}")

print(f"\n=== RESULTADO FINAL ===")
print(f"Novas questoes salvas agora: {sucessos}")
print(f"Questoes ja no banco (duplicadas): {duplicados}")
print(f"Erros restantes: {erros}")
print(f"TOTAL NO BANCO POSTGRESQL: {sucessos + duplicados} / {len(questoes)}")
