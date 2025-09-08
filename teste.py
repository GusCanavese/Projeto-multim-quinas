from brazilfiscalreport.danfe import Danfe

xml_path = r"C:\ACBrMonitorPLUS\Logs\31250900995044000107550010000000021468373645-nfe.xml"  # <-- ajuste aqui
with open(xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

danfe = Danfe(xml=xml_content)
danfe.output("danfe.pdf")  # cria danfe.pdf na mesma pasta onde rodar o script




# import os, time

# # Preencha estes campos:
# CHAVE = "31250900995044000107550010000000011834442342"  # chave a cancelar (a do erro)
# CNPJ  = "00995044000107"                               # CNPJ do emitente (só dígitos)
# JUST  = "Cancelamento por duplicidade em homologacao." # ≥ 15 caracteres

# CMD_DIR = r"NotaFiscal/EnviarComando"
# RSP_DIR = r"NotaFiscal/ReceberComando"
# os.makedirs(CMD_DIR, exist_ok=True)
# os.makedirs(RSP_DIR, exist_ok=True)

# cmd_path  = os.path.join(CMD_DIR,  "cancelar.txt")
# resp_path = os.path.join(RSP_DIR, "cancelar-resp.txt")
# try:
#     if os.path.exists(resp_path):
#         os.remove(resp_path)
# except Exception:
#     pass

# # Envia o evento 110111 para a SEFAZ via ACBr Monitor
# with open(cmd_path, "w", encoding="utf-8", newline="\r\n") as f:
#     f.write(f'NFe.CancelarNFe("{CHAVE}","{JUST}","{CNPJ}")')

# # Aguarda a resposta do ACBr (até 120s)
# t0 = time.time()
# while time.time() - t0 < 120:
#     if os.path.exists(resp_path):
#         with open(resp_path, "r", encoding="utf-8", errors="ignore") as f:
#             print(f.read())
#         break
#     time.sleep(0.2)
# else:
#     print("Timeout aguardando resposta do ACBr.")