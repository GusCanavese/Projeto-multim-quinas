import sys
import os

def resource_path(relative_path):
    """Pega o caminho absoluto, considerando se está rodando com PyInstaller ou não"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extrai os arquivos temporariamente nesta pasta
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
