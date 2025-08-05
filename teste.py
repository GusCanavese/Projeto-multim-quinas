from cryptography.hazmat.primitives.serialization import pkcs12

with open(r"C:\Users\Gustavo\Desktop\Projeto-multim-quinas\arquivos\certificado.pfx", "rb") as f:
    data = f.read()

key, cert, ca = pkcs12.load_key_and_certificates(data, b"nutri@00995")
print(cert.subject)