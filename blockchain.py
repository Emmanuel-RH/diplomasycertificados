import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        # Crea el primer bloque de la cadena (bloque génesis)
        return Block(0, "0", time.time(), "Bloque Génesis")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            data=data
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

if __name__ == "__main__":
    mi_blockchain = Blockchain()
    mi_blockchain.add_block("Primer bloque después del génesis")
    mi_blockchain.add_block("Segundo bloque después del génesis")
    
    for block in mi_blockchain.chain:
        print(f"Índice: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Datos: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Hash anterior: {block.previous_hash}")
        print("-" * 40)
    
    print("¿La cadena es válida?", mi_blockchain.is_chain_valid())