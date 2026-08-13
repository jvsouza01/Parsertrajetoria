import json
import requests

JSON_PATH = "output/questoes_payload_api.json"
URL = "http://localhost:8080/api/admin/ingestao/questoes"

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    questoes = json.load(f)

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwY2FkODZkNzY5ZmFkZTViODkxNmQ5Y2U1MDc0YzgyMGYwNjdkNTIiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiam_Do28gdml0aG9yIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tyak83cG1LTkhLXzNrN0JUdXljcEc1MC04ZUVQcElBSDVRMTNvR1VFYVgwWmcycEY1PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3RyYWpldG9yaWEtMjg1ZDQiLCJhdWQiOiJ0cmFqZXRvcmlhLTI4NWQ0IiwiYXV0aF90aW1lIjoxNzg2MzIxNjI2LCJ1c2VyX2lkIjoicVdIRThpTmxYZU1pdEU1YjlXQjJ3d1A1bjlSMiIsInN1YiI6InFXSEU4aU5sWGVNaXRFNWI5V0Iyd3dQNW45UjIiLCJpYXQiOjE3ODYzMjU4OTAsImV4cCI6MTc4NjMyOTQ5MCwiZW1haWwiOiJqb2Fvdml0aG9yNjUwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEwNzQ5NDc0ODQ0MTY0NjU2MDMzIl0sImVtYWlsIjpbImpvYW92aXRob3I2NTBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.fJORn2t_JGJqnCz-CadhOpS5wVPK3ye3gKiq23cIxSF5Mez_aZFqErTm3a8yyl-3EMgFv-2haP2rklrI8g_zNjYS1lOcAEtz-kABqhlNsOWnsQND4lpgvHF1fzj6WX8BAb-paJKYcwEqoxw8AY4VVBg1CmTjzWuD7uljTeSzXC0lw_e0w-V-OhWlOFDUHh2ra6WbqoBBEl2DW4kdt2hpKAZWLOUjngGP0ResSSoayZFee8Y-TC7KMhWd_ddRPcHOkIRBaROl-oQfJTCjDhIYG2jfA7H16edC7L0DZqVog_iMcL9ia5qGHl5YbiceFMMSMZdX3T5agu-b_GRztDvzDQ"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {token}"
}

# Pegar item 30 (indice 29) que falhava por causa da materia 'Historia'
item = questoes[29]
item['materiaNome'] = 'Linguagens' # Mudar temporariamente para testar se salva

r = requests.post(URL, json=[item], headers=headers)
print(f"Status: {r.status_code}")
print(f"Body: {r.text[:300]}")
