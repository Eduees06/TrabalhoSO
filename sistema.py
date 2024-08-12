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
                # Verificar se a linha está em outra cache com estado 'E'
                linha_compartilhada = self.verificar_cache_exclusiva(tag)
                if linha_compartilhada:
                    print(f"Processador {processador_id} obtém a linha de outro processador em estado Exclusivo")
                    linha_compartilhada.estado = 'S'  # Altera o estado da linha na outra cache para 'S'
                    linha = cache.substituir_linha(tag, linha_compartilhada.data)
                    linha.estado = 'S'  # Altera o estado da linha na cache atual para 'S'
                else:
                    # Caso contrário, ler da memória principal
                    data = self.memoria_principal.ler(endereco)
                    linha = cache.substituir_linha(tag, data)
                    linha.estado = 'E'  # Exclusivo
            else:
                print(f"Acerto de leitura no processador {processador_id}")
            return linha.data
        else:
            print(f"Falha de leitura no processador {processador_id}")
            # Verificar se a linha está em outra cache com estado 'E'
            linha_compartilhada = self.verificar_cache_exclusiva(tag)
            if linha_compartilhada:
                print(f"Processador {processador_id} obtém a linha de outro processador em estado Exclusivo")
                linha_compartilhada.estado = 'S'  # Altera o estado da linha na outra cache para 'S'
                linha = cache.substituir_linha(tag, linha_compartilhada.data)
                linha.estado = 'S'  # Altera o estado da linha na cache atual para 'S'
            else:
                # Caso contrário, ler da memória principal
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data)
                linha.estado = 'E'  # Exclusivo
            return linha.data
    
    def escrever(self, processador_id, endereco, valor):
        cache = self.caches[processador_id]
        tag = endereco
        
        linha = cache.encontrar_linha(tag)
        if linha:
            if linha.estado in ['I', 'S']:
                print(f"Falha de escrita no processador {processador_id}")
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data)
                linha.estado = 'M'
                self.invalidar_outras_caches(processador_id, tag)
            else:
                print(f"Acerto de escrita no processador {processador_id}")
                linha.estado = 'M'
        else:
            print(f"Falha de escrita no processador {processador_id}")
            data = self.memoria_principal.ler(endereco)
            linha = cache.substituir_linha(tag, data)
            linha.estado = 'M'
            self.invalidar_outras_caches(processador_id, tag)
        
        linha.data = valor
        self.memoria_principal.escrever(endereco, nome=None, quantidade=valor)
    
    def verificar_cache_exclusiva(self, tag):
        """
        Verifica se a linha está em outra cache em estado Exclusivo ('E').
        Retorna a linha se encontrada, caso contrário, retorna None.
        """
        for cache in self.caches:
            linha = cache.encontrar_linha(tag)
            if linha and linha.estado == 'E':
                return linha
        return None

    def invalidar_outras_caches(self, processador_id, tag):
        for i, cache in enumerate(self.caches):
            if i != processador_id:
                linha = cache.encontrar_linha(tag)
                if linha:
                    linha.estado = 'I'