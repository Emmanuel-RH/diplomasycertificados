import hashlib
import time

class CertificateBlock:
    def __init__(self, index, previous_hash, timestamp, certificate_data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.certificate_data = certificate_data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        cert_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.certificate_data}{self.nonce}"
        return hashlib.sha256(cert_string.encode()).hexdigest()

class CertificateBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return CertificateBlock(0, "0", time.time(), {
            "nombre_estudiante": "GENESIS",
            "curso": "GENESIS",
            "fecha_emision": "GENESIS",
            "institucion": "GENESIS",
            "id_certificado": "GENESIS"
        })

    def get_latest_block(self):
        return self.chain[-1]

    def add_certificate(self, certificate_data):
        latest_block = self.get_latest_block()
        new_block = CertificateBlock(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            certificate_data=certificate_data
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                print(f"El hash del bloque {i} es inválido")
                return False
            if current.previous_hash != previous.hash:
                print(f"El hash anterior del bloque {i} no coincide")
                return False
        return True

    def find_certificate(self, id_certificado):
        for block in self.chain:
            if block.certificate_data["id_certificado"] == id_certificado:
                return block
        return None

if __name__ == "__main__":
    # Crear la blockchain de certificados
    blockchain = CertificateBlockchain()

    # Emitir un certificado de ejemplo
    certificado1 = {
        "nombre_estudiante": "Emmanuel Rodríguez",
        "curso": "Python Básico",
        "fecha_emision": "2025-06-22",
        "institucion": "Universidad Ejemplo",
        "id_certificado": "CERT-0001"
    }
    blockchain.add_certificate(certificado1)

    certificado2 = {
        "nombre_estudiante": "Laura Méndez",
        "curso": "Introducción a Blockchain",
        "fecha_emision": "2025-06-22",
        "institucion": "Instituto Digital",
        "id_certificado": "CERT-0002"
    }
    blockchain.add_certificate(certificado2)

    # Listar certificados
    print("Certificados en la blockchain:")
    for block in blockchain.chain:
        print(f"Índice: {block.index}")
        print(f"Datos del certificado: {block.certificate_data}")
        print(f"Hash: {block.hash}")
        print(f"Hash anterior: {block.previous_hash}")
        print("-" * 40)

    # Verificar la cadena
    print("¿La cadena es válida?", blockchain.is_chain_valid())

    # Buscar y verificar un certificado
    id_a_buscar = "CERT-0002"
    block = blockchain.find_certificate(id_a_buscar)
    if block:
        print(f"Certificado encontrado: {block.certificate_data}")
    else:
        print("Certificado no encontrado.")