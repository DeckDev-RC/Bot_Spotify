import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for Windows GUI applications

# Dependencies (adicionar outras dependências se necessário)
options = {
    "build_exe": {
        "includes": ["tkinter", "selenium"],  # Adicione os módulos que você precisa
    }
}

executables = [
    Executable("main.py", base=base, icon="icon.ico"),  # Substitua "main.py" pelo nome do seu script principal
]

setup(
    name="SpotifyAutomation",
    version="1.0",
    description="Descrição do seu aplicativo",
    options=options,
    executables=executables
)
