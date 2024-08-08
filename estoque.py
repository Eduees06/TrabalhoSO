from produto import Produto

class Estoque:
    def __init__(self, arquivo='estoque.txt'):
        self.produtos = {}
        self.carregar_estoque(arquivo)
    
    def carregar_estoque(self, arquivo):
        with open(arquivo, 'r') as f:
            for idx, linha in enumerate(f):
                dados = linha.strip().split(',')
                if len(dados) == 5:  # Verifica se a linha tem 5 campos
                    nome = dados[0]
                    quantidade = int(dados[1])
                    preco_compra = float(dados[2])
                    preco_venda = float(dados[3])
                    local = dados[4]
                    produto = Produto(idx, nome, quantidade, preco_compra, preco_venda, local)
                    self.produtos[idx] = produto
                else:
                    print(f"Formato incorreto na linha {idx + 1}: {linha}")
    
    def ler_produto(self, id):
        return self.produtos.get(id)
    
    def escrever_produto(self, id, nome=None, quantidade=None, preco_compra=None, preco_venda=None, local=None):
        if id in self.produtos:
            produto = self.produtos[id]
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
            self.produtos[id] = produto
            print(f"Produto atualizado: {produto}")
        else:
            resposta = input(f"Produto com ID {id} não encontrado. Deseja criar um novo produto? (s/n): ").strip().lower()
            if resposta == 's':
                nome = input("Digite o nome do produto: ")
                quantidade = int(input("Digite a quantidade: "))
                preco_compra = float(input("Digite o preço de compra: "))
                preco_venda = float(input("Digite o preço de venda: "))
                local = input("Digite o local do estabelecimento: ")
                produto = Produto(id, nome, quantidade, preco_compra, preco_venda, local)
                self.produtos[id] = produto
                print(f"Produto criado: {produto}")