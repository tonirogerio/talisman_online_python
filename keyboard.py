import ctypes
from ctypes.wintypes import HWND, WPARAM, LPARAM

# Constantes de mensagens para eventos de teclado
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# Mapeamento de teclas para Virtual-Key Codes (VK)
VK_CODES = {
    **{str(i): 0x30 + i for i in range(10)},  # Teclas numéricas 0-9
    **{chr(i): i for i in range(0x41, 0x5A + 1)},  # Letras A-Z
    **{f"F{i}": 0x70 + (i - 1) for i in range(1, 13)},  # Teclas F1-F12
    "ALT": 0x12,
    "SHIFT": 0x10,
    "CTRL": 0x11,
    "ENTER": 0x0D,
    "BACKSPACE": 0x08,
    "SPACE": 0x20,
    "TAB": 0x09,
    "ESC": 0x1B,
}

# Carregar a biblioteca user32.dll
user32 = ctypes.windll.user32


def send(hwnd: int, command: str):
    vk_code = VK_CODES.get(command.upper())
    if vk_code is None:
        raise ValueError(f"Tecla '{command}' não é suportada ou inválida.")

    # Envia as mensagens WM_KEYDOWN e WM_KEYUP
    user32.SendMessageW(HWND(hwnd), WM_KEYDOWN, WPARAM(vk_code), LPARAM(0))
    user32.SendMessageW(HWND(hwnd), WM_KEYUP, WPARAM(vk_code), LPARAM(0))

