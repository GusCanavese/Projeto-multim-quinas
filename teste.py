from brazilfiscalreport.danfe import Danfe

xml_path = r"C:\ACBrMonitorPLUS\Logs\\31250900995044000107650010000000081749370328-nfe.xml"
with open(xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

danfe = Danfe(xml=xml_content)
danfe.output("danfe.pdf")