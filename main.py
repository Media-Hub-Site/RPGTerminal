# -*- coding: utf-8 -*-
"""
RPGTerminal - Juego RPG por turnos para la terminal
Integrado en el conglomerado MediaHub
"""
import sys
import os

# Configuración de codificación UTF-8 para consola en Windows
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul 2>&1")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Asegurar rutas de importación tanto en desarrollo como en ejecutable empaquetado (PyInstaller)
current_dir = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    base_dir = getattr(sys, "_MEIPASS", current_dir)
else:
    base_dir = current_dir

src_dir = os.path.join(base_dir, "TerminalGameClient", "src")
if os.path.isdir(src_dir) and src_dir not in sys.path:
    sys.path.insert(0, src_dir)
elif base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from utils.console import install_rich_print
install_rich_print()

from core.menu_log import Juego

def main():
    try:
        Juego()
    except (KeyboardInterrupt, SystemExit):
        print("\n\nSaliendo de RPG Terminal. ¡Hasta la próxima!")
        sys.exit(0)

if __name__ == "__main__":
    main()
