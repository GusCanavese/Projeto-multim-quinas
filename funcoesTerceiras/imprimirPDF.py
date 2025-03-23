import win32print
import win32api

def imprimirPdf(caminho):
    impressora = win32print.GetDefaultPrinter()
    print(impressora)
    win32api.ShellExecute(0, "print", caminho, impressora, ".", 0)
    print(caminho)