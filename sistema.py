from memoriaprincipal import MemoriaPrincipal
from cache import Cache

class SistemaDeInventario:
    def __init__(self, estoque):
        self.memoria_principal = MemoriaPrincipal(estoque)
        self.caches = [Cache() for _ in range(3)]  # Três processadores
    
    def ler(self, processador_id, endereco):
        cache = self.caches[processador_id]
        tag = endereco
        
        linha = cache.encontrar_linha(tag)
        if linha:
            if linha.estado == 'I':
                print(f"Falha de leitura (Inválido) no processador {processador_id}")
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data)
                linha.estado = 'E'
            else:
                print(f"Acerto de leitura no processador {processador_id}")
            return linha.data
        else:
            print(f"Falha de leitura no processador {processador_id}")
            data = self.memoria_principal.ler(endereco)
            linha = cache.substituir_linha(tag, data)
            return data
    
    def escrever(self, processador_id, endereco, valor):
        cache = self.caches[processador_id]
        tag = endereco
        
        linha = cache.encontrar_linha(tag)
        if linha:
            if linha.estado == 'I':
                print(f"Falha de escrita (Inválido) no processador {processador_id}")
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data)
                linha.estado = 'M'
            else:
                print(f"Acerto de escrita no processador {processador_id}")
                linha.estado = 'M'
        else:
            print(f"Falha de escrita no processador {processador_id}")
            data = self.memoria_principal.ler(endereco)
            linha = cache.substituir_linha(tag, data)
            linha.estado = 'M'
        
        linha.data = valor
        self.memoria_principal.escrever(endereco, nome=None, quantidade=valor)