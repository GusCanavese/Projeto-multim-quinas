import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
import requests
from funcoesTerceiras.registraClienteNoBanco import registraClienteNoBanco
from funcoesTerceiras.buscarCnpj import buscar_cnpj
from componentes import criaFrameJanela, criaFrameJanela, criarLabelEntry, criaBotao, criaBotaoPequeno, criarLabelComboBox
from funcoesTerceiras.maiusculo import aplicar_maiusculo_em_todos_entries

def telaCadastroClientes(self, ehClienteFiscal):
    frame  = criaFrameJanela(self, 0.5, 0.5, 1, 1, self.corFundo)
    bairro = ctk.StringVar()
    rua    = ctk.StringVar()
    cidade = ctk.StringVar()
    estado = ctk.StringVar()

    self.textoCadastro = ctk.CTkLabel(frame, width=950, height=0, text="Cadastrar cliente", font=("Century Gothic bold", 30))
    self.textoCadastro.place(relx=0.5, rely=0.08, anchor="center")
    

    #nome
    self.nomeCliente = criarLabelEntry(frame, "Nome *", 0.15, 0.15, 0.30, None)
    self.cpf = criarLabelEntry(frame, "CPF *", 0.15, 0.25, 0.30, None)
    self.cnpj = criarLabelEntry(frame, "CNPJ", 0.15, 0.35, 0.30, None)
    self.botaoBuscaCNPJ = criaBotaoPequeno(frame, "Buscar CNPJ", 0.40, 0.404, 0.1, lambda: buscaCnpj(self.cnpj.get()))
    self.IEcliente = criarLabelEntry(frame, "Inscrição Estadual", 0.15, 0.45, 0.30, None)
    self.RGcliente = criarLabelEntry(frame, "Insira o RG", 0.15, 0.55, 0.15, None)
    self.telefoneCliente = criarLabelEntry(frame, "Telefone", 0.31, 0.55, 0.14, None)

    self.CEPcliente    = criarLabelEntry(frame, "CEP", 0.45+0.05, 0.15, 0.10, None)
    self.botaoBuscaCEP = criaBotaoPequeno(frame, "Buscar CEP", 0.628, 0.204, 0.06, lambda: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))
    self.rua = criarLabelEntry(frame, "Rua *", 0.67, 0.15, 0.18, rua)

    self.bairroCliente = criarLabelEntry(frame, "Bairro *", 0.50, 0.25, 0.20, bairro)
    self.numeroCliente = criarLabelEntry(frame, "Número *", 0.71, 0.25, 0.14, None)

    self.cidadeCliente = criarLabelEntry(frame, "Cidade *", 0.50, 0.35, 0.24, cidade)
    self.estadoCliente = criarLabelEntry(frame, "Estado *", 0.75, 0.35, 0.10, estado)

    self.referencia    = criarLabelEntry(frame, "Referência ", 0.50, 0.45, 0.35, None)

    self.CEPcliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))
    self.CEPcliente.bind("<Tab>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()) if self.CEPcliente.get().strip() else None)
    self.numeroCliente.bind("<Return>", lambda event: buscaCep(self.CEPcliente.get(), self.numeroCliente.get()))
    self.cnpj.bind("<Return>", lambda event: buscaCnpj(self.cnpj.get()))

    def buscaCep(cep, numero):
        cep_limpo = ''.join(filter(str.isdigit, cep))
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            if "erro" in dados:
                messagebox.showerror("Erro", "CEP não encontrado.")
            else:
                bairro.set(dados.get("bairro", ""))
                rua.set(dados.get("logradouro", ""))
                cidade.set(dados.get("localidade", ""))
                estado.set(dados.get("uf", ""))
        else:
            messagebox.showerror("Erro", "Falha na consulta do CEP.")

    def _set_entry(entry, value):
        entry.delete(0, "end")
        entry.insert(0, value or "")

    def buscaCnpj(cnpj):
        try:
            dados = buscar_cnpj(cnpj)
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return
        except requests.RequestException:
            messagebox.showerror("Erro", "Falha na consulta do CNPJ.")
            return

        _set_entry(self.nomeCliente, dados.get("nome"))
        _set_entry(self.telefoneCliente, dados.get("telefone"))
        _set_entry(self.CEPcliente, dados.get("cep"))
        _set_entry(self.rua, dados.get("rua"))
        _set_entry(self.numeroCliente, dados.get("numero"))
        _set_entry(self.bairroCliente, dados.get("bairro"))
        bairro.set(dados.get("bairro", ""))
        rua.set(dados.get("rua", ""))
        cidade.set(dados.get("cidade", ""))
        estado.set(dados.get("estado", ""))

    # ================ Botões =====================#

    criaBotao(frame, "◀️ Voltar", 0.29, 0.80, 0.20, lambda:frame.destroy())
    criaBotao(frame, "Cadastrar", 0.66, 0.80, 0.20, lambda:registraClienteNoBanco(self, frame, ehClienteFiscal))
    aplicar_maiusculo_em_todos_entries(self)
