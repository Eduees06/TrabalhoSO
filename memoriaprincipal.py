from estoque import Estoque

class MemoriaPrincipal:
    def __init__(self, estoque):
        estoque = Estoque()
        self.data = estoque
    
    def ler(self, endereco):
        produto = self.data.ler_produto(endereco)
        return produto if produto else None
    
    def escrever(self, endereco, nome=None, quantidade=None, preco_compra=None, preco_venda=None, local=None):
        self.data.escrever_produto(endereco, nome=nome, quantidade=quantidade, preco_compra=preco_compra, preco_venda=preco_venda, local=local)
        
    def imprimir(self):
        print("Memória Principal:")
        for id, produto in self.data.produtos.items():
            print(f"ID: {produto.id}, Nome: {produto.nome}, Quantidade: {produto.quantidade}, Preço de Compra: {produto.preco_compra}, Preço de Venda: {produto.preco_venda}, Local: {produto.local}")