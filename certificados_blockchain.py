import hashlib
import time
import json

class CertificateBlock:
    def __init__(self, index, previous_hash, timestamp, certificate_data, nonce=0, hash_value=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.certificate_data = certificate_data
        self.nonce = nonce
        self.hash = hash_value or self.calculate_hash()

    def calculate_hash(self):
        cert_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.certificate_data, sort_keys=True)}{self.nonce}"
        return hashlib.sha256(cert_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "certificate_data": self.certificate_data,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data):
        return CertificateBlock(
            index=data["index"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            certificate_data=data["certificate_data"],
            nonce=data.get("nonce", 0),
            hash_value=data.get("hash")
        )

class CertificateBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return CertificateBlock(0, "0", time.time(), {
            "nombre_estudiante": "GENESIS",
            "curso": "GENESIS",
            "fecha_emision": "GENESIS",
            "institucion": "GENESIS",
            "id_certificado": "GENESIS",
            "calificacion": "GENESIS",
            "duracion": "GENESIS",
            "email": "GENESIS",
            "anulado": False
        })

    def get_latest_block(self):
        return self.chain[-1]

    def add_certificate(self, certificate_data):
        # Asegura el campo "anulado" en todos los certificados nuevos
        certificate_data["anulado"] = False
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
            if block.certificate_data.get("id_certificado") == id_certificado:
                return block
        return None

    def anular_certificado(self, id_certificado):
        block = self.find_certificate(id_certificado)
        if block and not block.certificate_data.get("anulado", False):
            block.certificate_data["anulado"] = True
            return True
        return False

    def export_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([block.to_dict() for block in self.chain], f, ensure_ascii=False, indent=4)

    def import_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            chain_data = json.load(f)
            self.chain = [CertificateBlock.from_dict(block) for block in chain_data]