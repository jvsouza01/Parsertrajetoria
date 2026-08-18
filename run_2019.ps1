$pyFile = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\generate_pmba_soldado_2019.py"
$outFile = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output\pmba_soldado_2019_payload_api.json"

# Search for python in system
$pyCandidate = (Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python", "C:\Python*", "C:\Program Files\Python*" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1).FullName

if ($pyCandidate) {
    Write-Host "Executando com Python $pyCandidate"
    & "$pyCandidate" "$pyFile"
} else {
    Write-Host "Python nao encontrado. Executando gerador nativo..."
}
