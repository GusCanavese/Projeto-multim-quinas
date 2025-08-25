from brazilfiscalreport.danfe import Danfe

xml_path = r"C:\ACBrMonitorPLUS\Logs\31250800995044000107550010000000011575708674-nfe.xml"  # <-- ajuste aqui
with open(xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

danfe = Danfe(xml=xml_content)
danfe.output("danfe.pdf")  # cria danfe.pdf na mesma pasta onde rodar o script