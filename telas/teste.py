import customtkinter as ctk

# Inicialização da janela
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1200x500")
app.title("Nota Fiscal")

# Função auxiliar para criar labels + entry
def criar_label_entry(texto, relx, rely, width=150):
    label = ctk.CTkLabel(app, text=texto)
    label.place(relx=relx, rely=rely, anchor="w")
    entry = ctk.CTkEntry(app, width=width)
    entry.place(relx=relx, rely=rely + 0.05, anchor="w")
    return entry

# Identificação
criar_label_entry("Número da Nota", 0.02, 0.05)
criar_label_entry("Série", 0.2, 0.05, width=50)
criar_label_entry("Modelo", 0.3, 0.05, width=60)
criar_label_entry("Chave NF-e", 0.4, 0.05, width=350)

# Destinatário
criar_label_entry("Razão Social", 0.02, 0.18, width=500)
criar_label_entry("CNPJ", 0.6, 0.18, width=180)

# Emitente
criar_label_entry("Razão Social", 0.02, 0.3, width=500)
alterar_btn = ctk.CTkButton(app, text="Alterar", width=60, height=24)
alterar_btn.place(relx=0.43, rely=0.305)

criar_label_entry("CPF/CNPJ", 0.6, 0.3, width=180)

# Informações
status_label = ctk.CTkLabel(app, text="Status")
status_label.place(relx=0.8, rely=0.05, anchor="w")
status_entry = ctk.CTkEntry(app, width=150, placeholder_text="Digitação")
status_entry.place(relx=0.8, rely=0.1, anchor="w")

criar_label_entry("Data Documento", 0.8, 0.18)
criar_label_entry("Data Entrada", 0.8, 0.26)
criar_label_entry("Hora da Entrada/Saída", 0.8, 0.34)
criar_label_entry("Data de criação", 0.8, 0.42)
criar_label_entry("Data de confirmação", 0.8, 0.5)

# Finalidade e Situação
finalidade_label = ctk.CTkLabel(app, text="Finalidade")
finalidade_label.place(relx=0.8, rely=0.58, anchor="w")
finalidade_combo = ctk.CTkComboBox(app, values=["Normal"])
finalidade_combo.place(relx=0.8, rely=0.63, anchor="w")

situacao_label = ctk.CTkLabel(app, text="Situação")
situacao_label.place(relx=0.8, rely=0.7, anchor="w")
situacao_combo = ctk.CTkComboBox(app, values=["Normal"])
situacao_combo.place(relx=0.8, rely=0.75, anchor="w")

# CFOP e Natureza da Operação
criar_label_entry("CFOP", 0.02, 0.42, width=100)
criar_label_entry("Natureza da Operação", 0.12, 0.42, width=400)

# Pedido de Compra Vinculado
criar_label_entry("Pedido de Compra Vinculado", 0.55, 0.42, width=200)

# Mercadoria
check = ctk.CTkCheckBox(app, text="Movimentação Física")
check.place(relx=0.02, rely=0.58)

# Dados de transporte
modal_label = ctk.CTkLabel(app, text="Modalidade do Frete")
modal_label.place(relx=0.25, rely=0.58, anchor="w")
modal_combo = ctk.CTkComboBox(app, values=["Contratação do Frete por conta do Destinatário"])
modal_combo.place(relx=0.25, rely=0.63)

detalhar_label = ctk.CTkLabel(app, text="Detalhar Transporte")
detalhar_label.place(relx=0.55, rely=0.58)
detalhar_nao = ctk.CTkRadioButton(app, text="Não")
detalhar_nao.place(relx=0.55, rely=0.63)
detalhar_sim = ctk.CTkRadioButton(app, text="Sim")
detalhar_sim.place(relx=0.6, rely=0.63)

# Pagamento
forma_label = ctk.CTkLabel(app, text="Forma de Pagamento")
forma_label.place(relx=0.7, rely=0.58)
forma_combo = ctk.CTkComboBox(app, values=["À Vista"])
forma_combo.place(relx=0.7, rely=0.63)

app.mainloop()
