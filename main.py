# -*- coding: utf-8 -*-
"""
RPGTerminal - Juego RPG por turnos para la terminal
Integrado en el conglomerado MediaHub
"""
import sys
import os
import traceback


def _ensure_windows_console():
    """
    Si el ejecutable fue lanzado desde MediaHub Launcher con DETACHED_PROCESS
    (sin consola asociada), crea una nueva ventana de consola interactiva
    y reconecta stdin/stdout/stderr en UTF-8 con soporte ANSI.
    """
    if sys.platform != "win32":
        return

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32

        # Si no hay consola asociada (ej. lanzado con DETACHED_PROCESS), asignar una nueva
        if kernel32.GetConsoleWindow() == 0:
            if kernel32.AllocConsole():
                # Reconectar descriptores estándar a la nueva consola
                sys.stdin = open("CONIN$", "r", encoding="utf-8", errors="replace")
                sys.stdout = open("CONOUT$", "w", encoding="utf-8", errors="replace")
                sys.stderr = open("CONOUT$", "w", encoding="utf-8", errors="replace")

        # Configurar título de ventana y codificación UTF-8 (65001)
        kernel32.SetConsoleTitleW("RPG Terminal - MediaHub Edition")
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)

        # Ajustar dimensiones de ventana y búfer a un tamaño amplio (120 columnas x 34 filas)
        # para que los gráficos Rich, galerías de personajes y barras de combate no desborden
        try:
            os.system("mode con: cols=120 lines=34 >nul 2>&1")
        except Exception:
            pass

        # Si tenemos ventana de consola de Windows, intentar maximizarla o ajustarla
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            try:
                user32 = ctypes.windll.user32
                SW_MAXIMIZE = 3
                user32.ShowWindow(hwnd, SW_MAXIMIZE)
            except Exception:
                pass

        # Habilitar secuencias ANSI / VT100 (colores Rich y Asciimatics)
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if handle and handle != -1:
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

        # Reconfigurar flujos a UTF-8 si corresponde
        for stream in (sys.stdout, sys.stderr, sys.stdin):
            if stream and hasattr(stream, "reconfigure"):
                try:
                    stream.reconfigure(encoding="utf-8", errors="replace")
                except Exception:
                    pass
    except Exception:
        pass


# Inicializar consola ANTES de importar Rich o Asciimatics
_ensure_windows_console()

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
    except Exception as e:
        print(f"\n[Error inesperado en RPG Terminal]: {e}")
        traceback.print_exc()
        try:
            input("\nPresiona Enter para cerrar...")
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
