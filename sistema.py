from memoriaprincipal import MemoriaPrincipal
from cache import Cache
from produto import Produto

class SistemaDeInventario:
    def __init__(self, estoque):
        self.estoque_objeto = estoque
        self.memoria_principal = MemoriaPrincipal(estoque)
        self.caches = [Cache() for _ in range(3)]  # Três processadores
    
    def ler(self, processador_id, endereco):
        cache = self.caches[processador_id]
        tag = endereco
        
        linha = cache.encontrar_linha(tag)
        
        if linha:
            if linha.estado == 'I':
                print(f"Read Falha de leitura (Inválido) no processador {processador_id}")
                linha_compartilhada = self.verificar_cache_exclusiva(tag)
                if linha_compartilhada:
                    print(f"Processador {processador_id} obtém a linha de outro processador em estado Exclusivo ou Modificado")
                    linha_compartilhada.estado = 'S'  # Atualiza estado para Compartilhado
                    linha = cache.substituir_linha(tag, linha_compartilhada.dados, self.memoria_principal)
                    linha.estado = 'S'  # Atualiza estado para Compartilhado
                else:
                    data = self.memoria_principal.ler(endereco)
                    linha = cache.substituir_linha(tag, data, self.memoria_principal)
                    linha.estado = 'S'  # Compartilhado
            else:
                print(f"Read Hit - Acerto de leitura no processador {processador_id}")
            return linha.dados
        else:
            linha_compartilhada = self.verificar_cache_exclusiva(tag)
            if linha_compartilhada:
                print(f"Read Miss - Processador {processador_id} obtém a linha de outro processador em estado Exclusivo ou Modificado")
                linha_compartilhada.estado = 'S'  # Atualiza estado para Compartilhado
                linha = cache.substituir_linha(tag, linha_compartilhada.dados, self.memoria_principal)
                linha.estado = 'S'  # Atualiza estado para Compartilhado
            else:
                data = self.memoria_principal.ler(endereco)
                linha = cache.substituir_linha(tag, data, self.memoria_principal)
                linha.estado = 'E'  # Exclusivo
            
            if linha:
                print(f"Read Miss - Leitura bem-sucedida após atualização no processador {processador_id}")
                return linha.dados
            else:
                print(f"Falha de leitura persistente no processador {processador_id}")
                return None
    
    def escrever(self, processador_id, endereco, nome = None, quantidade = None, preco_compra= None, preco_venda= None, local= None):
        
        cache = self.caches[processador_id]
        tag = endereco
        linha = cache.encontrar_linha(tag)
        
        if linha:
            if linha.estado == 'M':
                # Write Hit (WH) - Linha já está modificada
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Mantém o estado como Modificado
                produto = linha.dados
            elif linha.estado == 'S':
                # Write Hit (WH) - Linha está compartilhada
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Atualiza para Modificado
                self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
                produto = linha.dados
            elif linha.estado == 'E':
                # Write Hit (WH) - Linha está exclusiva
                print(f"WH (write hit) no processador {processador_id}")
                linha.estado = 'M'  # Atualiza para Modificado
                produto = linha.dados
            elif linha.estado == 'I':
                # Write Miss (WM) - Linha encontrada mas invalida
                print(f"WM (write miss) no processador {processador_id}")
                produto = self.memoria_principal.ler(endereco)
                
            
            self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
            
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
                
        else:
            
            print(f"WM (write miss) no processador {processador_id}")
            produto = self.memoria_principal.ler(endereco)
            
            if produto :
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
            else:
                produto = Produto(tag, nome, quantidade, preco_compra, preco_venda, local)
                
        linha = cache.substituir_linha(tag, produto, self.memoria_principal)   
        linha.estado = 'M' 
        self.invalidar_outras_caches(processador_id, tag)  # Invalida outras caches
        
        # Imprima os detalhes atualizados do produto
        produto_atualizado = self.memoria_principal.ler(endereco)
        if produto_atualizado:
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
            print(f"Produto atualizado: ID: {endereco}, Nome: {produto_atualizado.nome}, Quantidade: {produto_atualizado.quantidade}, Preço de Compra: {produto_atualizado.preco_compra}, Preço de Venda: {produto_atualizado.preco_venda}, Local: {produto_atualizado.local}")
        else:
            print(f"Produto novo: ID: {endereco}, Nome: {produto.nome}, Quantidade: {produto.quantidade}, Preço de Compra: {produto.preco_compra}, Preço de Venda: {produto.preco_venda}, Local: {produto.local}")
    
    def verificar_cache_exclusiva(self, tag):
        """
        Verifica se a linha está em outra cache em estado Exclusivo ('E').
        Retorna a linha se encontrada, caso contrário, retorna None.
        """
        for cache in self.caches:
            linha = cache.encontrar_linha(tag)
            if linha and linha.estado == 'E':
                return linha
            if linha and linha.estado == 'M':
                self.memoria_principal.escrever(linha.tag, linha.dados.nome, linha.dados.quantidade, linha.dados.preco_compra, linha.dados.preco_venda, linha.dados.local)
                print(f"Atualizando memória principal com a linha de tag {linha.tag}")
                return linha
            if linha and linha.estado == 'S':
                return linha
        return None

    def invalidar_outras_caches(self, processador_id, tag):
        for i, cache in enumerate(self.caches):
            if i != processador_id:
                linha = cache.encontrar_linha(tag)
                if linha:
                    linha.estado = 'I'
