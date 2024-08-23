from collections import deque

class Linha:
    def __init__(self):
        self.tag = None
        self.dados = None
        self.estado = 'I'  # Inicialmente Inválido

class Cache:
    def __init__(self):
        self.linhas = [Linha() for _ in range(5)]  # 5 linhas de cache
        self.fila_fifo = deque()  # Fila FIFO para rastrear a ordem das linhas
        
    def encontrar_linha(self, tag):
        for linha in self.linhas:
            if linha.tag == tag:
                return linha
        return None
    
    def substituir_linha(self, tag, dados, memoria_principal):
        linha = self.encontrar_linha(None)  # Encontrar uma linha vazia
        if linha is None:
            if len(self.fila_fifo) == 0:
                print("Erro: A fila FIFO está vazia. Não há linhas para substituir.")
                return None
            
            linha = self.fila_fifo.popleft()  # Remove a linha mais antiga da fila FIFO
            
            # Atualiza a memória principal se a linha estava modificada
            if linha.estado == 'M':
                print(f"Atualizando memória principal com a linha de tag {linha.tag}")
                memoria_principal.escrever(linha.tag, linha.dados.nome, linha.dados.quantidade, linha.dados.preco_compra, linha.dados.preco_venda, linha.dados.local)
        
        if linha:
            linha.tag = tag
            linha.dados = dados
            linha.estado = 'S'  # Atualiza o estado para Compartilhado ou conforme necessário
            self.fila_fifo.append(linha)  # Adiciona a linha à fila FIFO após a substituição
        return linha
    

    def imprimir(self):
        print("Memória Cache:")
        for i, linha in enumerate(self.linhas):
            print(f"Linha {i}: Tag = {linha.tag}, Dados = {linha.dados}, Estado = {linha.estado}")