import customtkinter as ctk

def aplicar_maiusculo_em_todos_entries(widget_raiz):
    for widget in widget_raiz.winfo_children():
        # Se for CTkEntry, aplica o trace
        if isinstance(widget, ctk.CTkEntry):
            var = widget.cget("textvariable")
            if not var:
                var = ctk.StringVar()
                widget.configure(textvariable=var)
            # Adiciona trace para converter em maiúsculas
            var.trace_add("write", lambda *args, v=var: v.set(v.get().upper()))
        
        # Chamada recursiva para frames internos
        aplicar_maiusculo_em_todos_entries(widget)
