$pyFile = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\generate_pmba_soldado_2019.py"
$pyContent = [System.IO.File]::ReadAllText($pyFile, [System.Text.Encoding]::UTF8)

# Replace typographic quotes before ConvertFrom-Json
$pyContentClean = $pyContent.Replace([char]0x201C, "'").Replace([char]0x201D, "'").Replace('"', "'")

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
    -replace 'texto_verissimo', $textoVerissimoJson `
    -replace [char]0x201C, '\"' `
    -replace [char]0x201D, '\"' `
    -replace [char]0x2018, "'" `
    -replace [char]0x2019, "'"

# Replace inner unescaped double quotes in question strings
# Let's use PowerShell regex or execute via node / c#
$outputDir = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }
