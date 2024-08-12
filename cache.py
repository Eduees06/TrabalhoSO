class LinhaCache:
    def __init__(self):
        self.tag = None
        self.data = None
        self.estado = 'I'  # Inválido por padrão

class Cache:
    def __init__(self, tamanho=5):
        self.linhas = [LinhaCache() for _ in range(tamanho)]
    
    def encontrar_linha(self, tag):
        for linha in self.linhas:
            if linha.tag == tag:
                return linha
        return None
    
    def substituir_linha(self, tag, data):
        #FIFO
        self.linhas.pop(0)
        nova_linha = LinhaCache()
        nova_linha.tag = tag
        nova_linha.data = data
        nova_linha.estado = 'E'  # Exclusivo
        self.linhas.append(nova_linha)
        return nova_linha
    
    def imprimir(self, num):
        print("Memória Cache " + str(num) +": ")
        for i, linha in enumerate(self.linhas):
            estado = linha.estado
            print(f"Linha {i}: Tag = {linha.tag}, Dados = {linha.data}, Estado = {estado}")