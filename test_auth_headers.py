import requests
import json

URL = "http://localhost:8080/api/admin/ingestao/questoes"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwY2FkODZkNzY5ZmFkZTViODkxNmQ5Y2U1MDc0YzgyMGYwNjdkNTIiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiam_Do28gdml0aG9yIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0tyak83cG1LTkhLXzNrN0JUdXljcEc1MC04ZUVQcElBSDVRMTNvR1VFYVgwWmcycEY1PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3RyYWpldG9yaWEtMjg1ZDQiLCJhdWQiOiJ0cmFqZXRvcmlhLTI4NWQ0IiwiYXV0aF90aW1lIjoxNzg2MzIxNjI2LCJ1c2VyX2lkIjoicVdIRThpTmxYZU1pdEU1YjlXQjJ3d1A1bjlSMiIsInN1YiI6InFXSEU4aU5sWGVNaXRFNWI5V0Iyd3dQNW45UjIiLCJpYXQiOjE3ODYzMzA2OTYsImV4cCI6MTc4NjMzNDI5NiwiZW1haWwiOiJqb2Fvdml0aG9yNjUwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEwNzQ5NDc0ODQ0MTY0NjU2MDMzIl0sImVtYWlsIjpbImpvYW92aXRob3I2NTBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.tRAwOGjS1bfIzqwDp8bdzki7yqXxJjHAF9P6Z2tjTRZhEOpucKpGNZyPF2QQ9okP8UAy1ARzKx3glX5-HsBGgX1WnZQFBSS0PRFlyGYYStdS9SQh6rBAwH8CGao3o-dSvV9ydg6vtL2fI5jUWU5WLkqcbKQCNighhb-II864Ut2xyzhxOeAspkQkXKZMpfZZIVio7EVzffV21MdZ3HvEKNNp0iTMpCrqtiwrjXqXggz4NT1uhlSTrlEaG9UCWiCV4RR3s51IcSReEai9sHD0L0aUub6aB3Knr0-KgJXDdtDn5J17UF1R3raI3TWiUiqoV3PBosmWVnoeALL34F"

q = json.load(open('output/questoes_payload_api.json', encoding='utf-8'))[0]

tests = [
    ("Bearer prefix", {'Authorization': f'Bearer {TOKEN}'}),
    ("No Bearer prefix", {'Authorization': TOKEN}),
    ("Token header", {'token': TOKEN}),
    ("X-Auth-Token", {'X-Auth-Token': TOKEN}),
]

for name, h in tests:
    h['Content-Type'] = 'application/json'
    r = requests.post(URL, json=[q], headers=h)
    print(f"[{name}] Status: {r.status_code} | Body: {r.text[:150]}")
