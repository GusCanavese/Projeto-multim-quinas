import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import datetime
from telas.telaProdutos import telaProdutos
from componentes import criarLabelEntry, criarLabelComboBox, criarLabelLateralEntry, criarLabelLateralComboBox, criaFrame, criaBotao
from telas.telaTransporte import telaTransporte

def telaRegistroCredito(self, dadosNota):
    self.dadosNotaPegar=[]
    frame = criaFrame(self, 0.5, 0.5, 0.94, 0.9)
    
    # variaveis
    variavelNumeroDaNota = ctk.StringVar()
    variavelChaveDaNota = ctk.StringVar()
    variavelSerieDaNota = ctk.StringVar()
    variavelRazaoSocialEmitente = ctk.StringVar()
    variavelCNPJRazaoSocialEmitente = ctk.StringVar()
    variavelRazaoSocialRemetente = ctk.StringVar()
    variavelCNPJRazaoSocialRemetente = ctk.StringVar()
    variavelDataDocumento = ctk.StringVar()
    variavelDataEntrada = ctk.StringVar()
    variavelDataCriacao = ctk.StringVar()



    # formatação de datas e campos
    tirarPrefixoDaNota = dadosNota["NFe"]["infNFe"]["Id"]
    tirarPrefixoDaNota = tirarPrefixoDaNota[3:]

    dataCriacao = dadosNota["NFe"]["infNFe"]["ide"]["dhEmi"]["#text"]
    dataCriacao = dataCriacao.split("T")[0]
    dataCriacao = datetime.strptime(dataCriacao, "%Y-%m-%d")
    dataCriacao = dataCriacao.strftime("%d/%m/%Y")

    dataEntrada = dadosNota["NFe"]["infNFe"]["ide"]["dhSaiEnt"]["#text"]
    dataEntrada = dataEntrada.split("T")[0]
    dataEntrada = datetime.strptime(dataEntrada, "%Y-%m-%d")
    dataEntrada = dataEntrada.strftime("%d/%m/%Y")

    dataDocumento = dadosNota["NFe"]["infNFe"]["ide"]["dhEmi"]["#text"]
    dataDocumento = dataDocumento.split("T")[0]
    dataDocumento = datetime.strptime(dataDocumento, "%Y-%m-%d")
    dataDocumento = dataDocumento.strftime("%d/%m/%Y")




    variavelNumeroDaNota.set(dadosNota["NFe"]["infNFe"]["ide"]["nNF"]["#text"])
    variavelSerieDaNota.set(dadosNota["NFe"]["infNFe"]["ide"]["serie"]["#text"])
    variavelChaveDaNota.set(tirarPrefixoDaNota)
    variavelRazaoSocialEmitente.set(dadosNota["NFe"]["infNFe"]["emit"]["xNome"]["#text"])
    variavelCNPJRazaoSocialEmitente.set(dadosNota["NFe"]["infNFe"]["emit"]["CNPJ"]["#text"])
    variavelRazaoSocialRemetente.set(dadosNota["NFe"]["infNFe"]["dest"]["xNome"]["#text"])
    variavelCNPJRazaoSocialRemetente.set(dadosNota["NFe"]["infNFe"]["dest"]["xNome"]["#text"])
    variavelDataDocumento.set(dataDocumento)
    variavelDataEntrada.set(dataEntrada)
    variavelDataCriacao.set(dataCriacao)

    

    # opções listas
    opcoesSituacao = ["Normal", "Extemporâneo"]
    opcoesFinalidade = ["Normal", "complementar", "Ajuste"]
    opcoesPagamento = ["À vista", "À prazo", "Outros"]
    opcoesTransporte = [ "Contratação do Frete por conta do Remetente (CIF)","Contratação do Frete por conta do Destinatário (FOB)","Contratação do Frete por conta de Terceiros","Transporte Próprio por conta do Remetente","Transporte Próprio por conta do Destinatário","Sem Ocorrência de Transporte"]




    criarLabelEntry(frame, "Número da NF", 0.1, 0.05, 0.07, variavelNumeroDaNota)
    criarLabelEntry(frame, "Série", 0.2, 0.05, 0.07, variavelSerieDaNota)
    criarLabelEntry(frame, "Chave da NF", 0.3, 0.05, 0.3, variavelChaveDaNota)

    destinatario = ctk.CTkLabel(frame, text="Destinatário----------")
    destinatario.place(relx=0.1, rely=0.15)
    criarLabelEntry(frame, "Razão social", 0.1, 0.20, 0.3, variavelRazaoSocialRemetente)
    criarLabelEntry(frame, "CNPJ", 0.45, 0.20, 0.15, variavelCNPJRazaoSocialRemetente)

    emitente = ctk.CTkLabel(frame, text="Emitente----------")
    emitente.place(relx=0.1, rely=0.3)
    criarLabelEntry(frame, "Razão social", 0.1, 0.35, 0.3, variavelRazaoSocialEmitente)
    criarLabelEntry(frame, "CNPJ", 0.45, 0.35, 0.15, variavelCNPJRazaoSocialEmitente)

    criarLabelLateralEntry(frame, "Status",             0.75, 0.09, 0.1, None)
    criarLabelLateralEntry(frame, "Data documento",     0.75, 0.14, 0.1, variavelDataDocumento)
    criarLabelLateralEntry(frame, "Data entrada",       0.75, 0.19, 0.1, variavelDataEntrada)
    criarLabelLateralEntry(frame, "Hora entrada/saída", 0.75, 0.24, 0.1, None)
    criarLabelLateralEntry(frame, "Data criação",       0.75, 0.29, 0.1, variavelDataCriacao)
    criarLabelLateralEntry(frame, "Data confirmação",   0.75, 0.34, 0.1, None)
    criarLabelLateralComboBox(frame, "Data finalidade", 0.75, 0.39, 0.1, opcoesFinalidade)
    criarLabelLateralComboBox(frame, "Data situação",   0.75, 0.44, 0.1, opcoesSituacao)

    criarLabelEntry(frame, "CFOP", 0.1, 0.49, 0.07, None)
    criarLabelEntry(frame, "Natureza da Operação", 0.2, 0.49, 0.4, None)

    
    transporte = ctk.CTkLabel(frame, text="Transporte----------")
    transporte.place(relx=0.1, rely=0.59)
    self.modalidadeDoFrete = criarLabelComboBox(frame, "Modalidade do frete", 0.1, 0.64, 0.27, opcoesTransporte)
    criarLabelComboBox(frame, "Forma de pagamento", 0.4, 0.64, 0.2, opcoesPagamento)

    criaBotao(frame, "Próximo - Tela de Produtos", 0.25, 0.94, 0.15, lambda:telaProdutos(self, dadosNota)).place(anchor="nw")
    criaBotao(frame, "Voltar", 0.05, 0.94, 0.15, lambda: frame.destroy()).place(anchor="nw")

