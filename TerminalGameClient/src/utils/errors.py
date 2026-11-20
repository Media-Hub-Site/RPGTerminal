from utils.common import time
from utils.console import console

def error():
    try:
        from core import UI_MAP
        UI_MAP['error']()
    except Exception:
        pass
    console.rule()
    console.print("[red]Acción no válida, por favor intente nuevamente[/red]")
    time.sleep(1)

def valueError(e):
    try:
        from core import UI_MAP
        UI_MAP['error']()
    except Exception:
        pass
    console.print(f"\n[green]ValueError: {e}[/green]")
    console.print("[red]Valor inválido, ingresa nuevamente[/red]")
    time.sleep(2)

ERRORS = {
    'ERROR': error,
    'VALUEERROR': valueError,
}
