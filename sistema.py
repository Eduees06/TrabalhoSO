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
                linha_compartilhada = self.verificar_cache_exclusiva(tag)
                if linha_compartilhada:
                    print(f"Processador {processador_id} obtém a linha de outro processador em estado Exclusivo")
                    linha_compartilhada.estado = 'S'  # Atualiza estado para Compartilhado
                    linha = cache.substituir_linha(tag, linha_compartilhada.dados, self.memoria_principal)
                    linha.estado = 'S'  # Atualiza estado para Compartilhado
                else:
                    data = self.memoria_principal.ler(endereco)
                    linha = cache.substituir_linha(tag, data, self.memoria_principal)
                    linha.estado = 'S'  # Compartilhado
            else:
                print(f"Acerto de leitura no processador {processador_id}")
            return linha.dados
        else:
            linha_compartilhada = self.verificar_cache_exclusiva(tag)
            if linha_compartilhada:
                print(f"Processador {processador_id} obtém a linha de outro processador em estado Exclusivo")
                linha_compartilhada.estado = 'S'  # Atualiza estado para Compartilhado
                linha = cache.substituir_linha(tag, linha_compartilhada.dados, self.memoria_principal)
                linha.estado = 'S'  # Atualiza estado para Compartilhado
            else:
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data, self.memoria_principal)
                linha.estado = 'E'  # Exclusivo
            
            if linha:
                print(f"Leitura bem-sucedida após atualização no processador {processador_id}")
                return linha.dados
            else:
                print(f"Falha de leitura persistente no processador {processador_id}")
                return None
    
    def escrever(self, processador_id, endereco, nome = None, quantidade = None, preco_compra= None, preco_venda= None, local= None):
        print(quantidade)
        cache = self.caches[processador_id]
        tag = endereco
        linha = cache.encontrar_linha(tag)
        
        if linha:
            if linha.estado == 'M':
                # Write Hit (WH) - Linha já está modificada
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Mantém o estado como Modificado
            elif linha.estado == 'S':
                # Write Hit (WH) - Linha está compartilhada
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Atualiza para Modificado
                self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
            elif linha.estado == 'E':
                # Write Hit (WH) - Linha está exclusiva
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Atualiza para Modificado
            elif linha.estado == 'I':
                # Write Miss (WM) - Linha não encontrada
                print(f"WM (write miss) no processador {processador_id}")
                produto = self.memoria_principal.ler(endereco)
                if nome is not None:
                    produto.nome = nome
                if quantidade is not None:
                    produto.quantidade = quantidade
                if preco_compra is not None:
                    produto.preco_compra = preco_compra
                if preco_venda is not None:
                    produto.preco_venda = preco_venda
                if local is not None:
                    produto.local = local            
                linha = cache.substituir_linha(tag, produto, self.memoria_principal)
                linha.estado = 'M'
                self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
        else:
            # Write Miss (WM) - Linha não encontrada na cache
            print(f"WM (write miss) no processador {processador_id}")
            produto = self.memoria_principal.ler(endereco)
            if nome is not None:
                produto.nome = nome
            if quantidade is not None:
                produto.quantidade = quantidade
            if preco_compra is not None:
                produto.preco_compra = preco_compra
            if preco_venda is not None:
                produto.preco_venda = preco_venda
            if local is not None:
                produto.local = local
            linha = cache.substituir_linha(tag, produto, self.memoria_principal)
            linha.estado = 'M'
            self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
        
        # Imprima os detalhes atualizados do produto
        produto_atualizado = self.memoria_principal.ler(endereco)
        if nome is not None:
            produto_atualizado.nome = nome
        if quantidade is not None:
            produto_atualizado.quantidade = quantidade
        if preco_compra is not None:
            produto_atualizado.preco_compra = preco_compra
        if preco_venda is not None:
            produto_atualizado.preco_venda = preco_venda
        if local is not None:
            produto_atualizado.local = local
        if produto_atualizado:
            print(f"Produto atualizado: ID: {endereco}, Nome: {produto_atualizado.nome}, Quantidade: {produto_atualizado.quantidade}, Preço de Compra: {produto_atualizado.preco_compra}, Preço de Venda: {produto_atualizado.preco_venda}, Local: {produto_atualizado.local}")
        else:
            print(f"Produto ID {endereco} não encontrado na memória principal.")
    
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
