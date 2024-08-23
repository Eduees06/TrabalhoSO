class Produto:
    def __init__(self, id, nome, quantidade, preco_compra, preco_venda, local):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.local = local
            
    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Quantidade: {self.quantidade}, Preço de Compra: {self.preco_compra}, Preço de Venda: {self.preco_venda}, Local: {self.local}"