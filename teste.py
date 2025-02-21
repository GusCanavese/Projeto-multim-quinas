import requests
import customtkinter as ctk

# Função para buscar o CEP e preencher os campos
def buscar_cep():
    cep = entry_cep.get()
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            
            # Preenchendo os campos automaticamente
            entry_cidade.delete(0, ctk.END)
            entry_estado.delete(0, ctk.END)
            entry_bairro.delete(0, ctk.END)
            entry_endereco.delete(0, ctk.END)

            entry_cidade.insert(0, dados.get('city', ''))
            entry_estado.insert(0, dados.get('state', ''))
            entry_bairro.insert(0, dados.get('district', ''))
            entry_endereco.insert(0, dados.get('address', ''))
        else:
            label_status.configure(text="CEP não encontrado!", text_color="red")
    except requests.RequestException:
        label_status.configure(text="Erro na requisição!", text_color="red")

# Configuração da janela
ctk.set_appearance_mode("dark")  # Modo escuro
root = ctk.CTk()
root.title("Busca de CEP")
root.geometry("400x400")

# Entrada do CEP
ctk.CTkLabel(root, text="Digite o CEP:", font=("Arial", 14)).pack(pady=5)
entry_cep = ctk.CTkEntry(root, width=200)
entry_cep.pack(pady=5)

# Botão de busca
botao_buscar = ctk.CTkButton(root, text="Buscar", command=buscar_cep)
botao_buscar.pack(pady=10)

# Status de busca
label_status = ctk.CTkLabel(root, text="", font=("Arial", 12))
label_status.pack(pady=5)

# Campos de preenchimento automático
ctk.CTkLabel(root, text="Cidade:", font=("Arial", 12)).pack()
entry_cidade = ctk.CTkEntry(root, width=250)
entry_cidade.pack(pady=5)

ctk.CTkLabel(root, text="Estado:", font=("Arial", 12)).pack()
entry_estado = ctk.CTkEntry(root, width=250)
entry_estado.pack(pady=5)

ctk.CTkLabel(root, text="Bairro:", font=("Arial", 12)).pack()
entry_bairro = ctk.CTkEntry(root, width=250)
entry_bairro.pack(pady=5)

ctk.CTkLabel(root, text="Endereço:", font=("Arial", 12)).pack()
entry_endereco = ctk.CTkEntry(root, width=250)
entry_endereco.pack(pady=5)

# Iniciar loop da interface
root.mainloop()
