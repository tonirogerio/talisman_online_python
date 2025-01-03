import ctypes
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM

# Constantes das mensagens
WM_SETCURSOR = 0x0020
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

HTCLIENT = 1  # Hit-test no cliente da janela
MK_LBUTTON = 0x0001  # Botão esquerdo pressionado
MK_RBUTTON = 0x0002  # Botão direito pressionado

# Carregando a biblioteca user32.dll
user32 = ctypes.windll.user32


# Função para criar o LPARAM com as coordenadas
def make_lparam(x: int, y: int) -> LPARAM:
    return LPARAM(y << 16 | x & 0xFFFF)


# Funções para cliques de mouse
def left(hwnd: int, x: int, y: int):
    """Simula um clique com o botão esquerdo do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONDOWN, WPARAM(MK_LBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_LBUTTONUP, WPARAM(0), make_lparam(x, y))


def right(hwnd: int, x: int, y: int):
    """Simula um clique com o botão direito do mouse."""
    user32.SendMessageW(HWND(hwnd), WM_SETCURSOR, WPARAM(hwnd), LPARAM(HTCLIENT | (WM_MOUSEMOVE << 16)))
    user32.SendMessageW(HWND(hwnd), WM_MOUSEMOVE, WPARAM(0), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONDOWN, WPARAM(MK_RBUTTON), make_lparam(x, y))
    user32.SendMessageW(HWND(hwnd), WM_RBUTTONUP, WPARAM(0), make_lparam(x, y))


# Função para mover o mouse com PostMessage
def move(hwnd: int, x: int, y: int):
    """
    Move fisicamente o cursor do mouse para uma posição específica dentro da janela alvo.

    Args:
        hwnd (int): Handle da janela onde o movimento será calculado.
        x (int): Coordenada X relativa à janela.
        y (int): Coordenada Y relativa à janela.
    """
    # Obter a posição absoluta da janela na tela
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(HWND(hwnd), ctypes.byref(rect))
    window_x, window_y = rect.left, rect.top

    # Converter coordenadas relativas à janela em coordenadas absolutas
    absolute_x = window_x + x
    absolute_y = window_y + y

    # Mover o cursor fisicamente para as coordenadas absolutas
    user32.SetCursorPos(absolute_x, absolute_y)



"""
import mouse

hwnd = 0x000E0398
xPos, yPos = 75, 75

mouse.left(hwnd, xPos, yPos)
"""