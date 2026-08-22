import os
import subprocess

def create_desktop_shortcut():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    target_bat = os.path.join(project_dir, "iniciar_studio.bat")
    icon_path = os.path.join(project_dir, "icon.ico")
    
    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Desktop = [Environment]::GetFolderPath('Desktop')
    $ShortcutPath = Join-Path $Desktop 'Parser Trajetoria Studio.lnk'
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = '{target_bat}'
    $Shortcut.WorkingDirectory = '{project_dir}'
    $Shortcut.IconLocation = '{icon_path},0'
    $Shortcut.Description = 'Parser Trajetoria Studio'
    $Shortcut.Save()
    Write-Host "[OK] Atalho criado com sucesso em: $ShortcutPath"
    """
    
    result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"[ERRO] {result.stderr.strip()}")

if __name__ == "__main__":
    create_desktop_shortcut()

