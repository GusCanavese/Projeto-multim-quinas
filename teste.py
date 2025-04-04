import tkinter as tk
from tkcalendar import DateEntry

root = tk.Tk()
root.title("Filtrar por Período")

# Label e DatePicker para a Data Inicial
tk.Label(root, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
datePickerInicio = DateEntry(root, width=12, background="darkblue", foreground="white", date_pattern="dd/MM/yyyy")
datePickerInicio.grid(row=0, column=1, padx=5, pady=5)

# Label e DatePicker para a Data Final
tk.Label(root, text="Data Final:").grid(row=1, column=0, padx=5, pady=5)
datePickerFim = DateEntry(root, width=12, background="darkblue", foreground="white", date_pattern="dd/MM/yyyy")
datePickerFim.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()