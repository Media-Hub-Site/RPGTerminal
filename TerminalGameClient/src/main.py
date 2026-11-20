from utils.console import install_rich_print

# install rich print globally so existing `print()` calls are rendered with rich
install_rich_print()

from core.menu_log import Juego

# ALL
if __name__ == "__main__":
    Juego()