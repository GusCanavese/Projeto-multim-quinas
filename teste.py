import requests
import customtkinter as ctk
import db

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







# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Conectar ao MySQL


# Função para buscar produto no banco de dados
def buscar_produto():
    termo = entry_busca.get()
    
    if not termo.strip():
        resultado_label.configure(text="Digite um nome ou código!")
        return

    query = "SELECT id, nome, preco FROM produtos WHERE nome LIKE %s OR id = %s"
    db.cursor.execute(query, (f"%{termo}%", termo if termo.isdigit() else None))

    resultados = db.cursor.fetchall()

    if resultados:
        texto_resultado = "\n".join([f"ID: {r[0]} | Nome: {r[1]} | Preço: R$ {r[2]:.2f}" for r in resultados])
    else:
        texto_resultado = "Produto não encontrado."

    resultado_label.configure(text=texto_resultado)

# Criar a Janela Principal
janela = ctk.CTk()
janela.geometry("500x400")
janela.title("Busca de Produtos")

# Campo de Busca
entry_busca = ctk.CTkEntry(janela, placeholder_text="Digite um nome ou código")
entry_busca.pack(pady=20)

# Botão de Buscar
botao_buscar = ctk.CTkButton(janela, text="Buscar", command=buscar_produto)
botao_buscar.pack()

# Label para Mostrar Resultados
resultado_label = ctk.CTkLabel(janela, text="")
resultado_label.pack(pady=20)

# Rodar a aplicação
janela.mainloop()
