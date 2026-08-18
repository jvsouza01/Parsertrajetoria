$outputDir = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$pyContent = [System.IO.File]::ReadAllText("C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\generate_pmba_soldado_2019.py", [System.Text.Encoding]::UTF8)

# Extract texto_verissimo
$tvStart = $pyContent.IndexOf('texto_verissimo = """') + 'texto_verissimo = """'.Length
$tvEnd = $pyContent.IndexOf('"""', $tvStart)
$textoVerissimo = $pyContent.Substring($tvStart, $tvEnd - $tvStart).Trim()
$textoVerissimoJson = $textoVerissimo | ConvertTo-Json

# Extract questoes
$startIdx = $pyContent.IndexOf("questoes = [")
$endIdx = $pyContent.IndexOf("payload_api = []")
$rawSub = $pyContent.Substring($startIdx + "questoes = ".Length, $endIdx - ($startIdx + "questoes = ".Length)).Trim()

$lines = $rawSub -split "`r?`n"
$cleanedLines = @()
foreach ($l in $lines) {
    $trimmed = $l.Trim()
    if (-not ($trimmed.StartsWith("#"))) {
        $cleanedLines += $l
    }
}
$jsonStr = ($cleanedLines -join "`n") `
    -replace 'True', 'true' `
    -replace 'False', 'false' `
    -replace 'None', 'null' `
    -replace '\(', '[' `
    -replace '\)', ']' `
    -replace 'texto_verissimo', $textoVerissimoJson

$questoes = $jsonStr | ConvertFrom-Json

$banca = "IBFC"
$orgao = "Polícia Militar da Bahia - PMBA"
$cargo = "Aluno Soldado da PM - Caderno 01"
$ano = 2019
$fonte = "CONCURSO"

$payloadApi = @()

foreach ($q in $questoes) {
    $posStr = "{0:D2}" -f $q.pos
    $idOrigem = "PMBA_SOLDADO_2019_Q$posStr"
    
    $dif = $q.dif
    if ($dif -eq "MEDIO") {
        $dif = "MODERADO"
    }

    $enunciadoFinal = $q.enunc
    if ($q.base -and -not [string]::IsNullOrWhiteSpace($q.base)) {
        $enunciadoFinal = "$($q.base)`n`n$($q.enunc)"
    }

    $altsList = @()
    foreach ($alt in $q.alts) {
        $letra = $alt[0]
        $texto = $alt[1]
        $isCorreta = ($q.gab -ne "*" -and $letra -eq $q.gab)
        $altsList += [PSCustomObject]@{
            letra = $letra
            texto = $texto
            correta = $isCorreta
        }
    }

    $dto = [PSCustomObject]@{
        idOrigem = $idOrigem
        fonte = $fonte
        banca = $banca
        orgao = $orgao
        cargo = $cargo
        ano = $ano
        materiaNome = $q.materia
        dificuldade = $dif
        enunciado = $enunciadoFinal
        imagemUrl = $null
        alternativas = $altsList
    }
    $payloadApi += $dto
}

$outFile = Join-Path $outputDir "pmba_soldado_2019_payload_api.json"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$jsonText = $payloadApi | ConvertTo-Json -Depth 10

[System.IO.File]::WriteAllText($outFile, $jsonText, $utf8NoBom)

Write-Host "Processamento concluído com sucesso!"
Write-Host "Total de questões processadas: $($payloadApi.Count)"
Write-Host "Salvo em: $outFile"
