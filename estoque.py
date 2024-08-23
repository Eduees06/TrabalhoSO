from produto import Produto

class Estoque:
    def __init__(self, arquivo):
        self.arquivo = arquivo
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
    
    def ler_produto(self, endereco):
        return self.produtos[endereco] if endereco in self.produtos else None
    
    def escrever_produto(self, id, nome=None, quantidade=None, preco_compra=None, preco_venda=None, local=None):
        
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
        print(f"Posição {id} atualizado na memória principal: {produto}")
        
        # Atualiza a linha específica no arquivo
        self.atualizar_linha_no_arquivo(id, produto)

    def atualizar_linha_no_arquivo(self, id, produto):
        linhas = []
        with open(self.arquivo, 'r') as f:
            linhas = f.readlines()

        if id < len(linhas):
            # Substitui a linha específica pelo produto atualizado
            linhas[id] = f"{produto.nome},{produto.quantidade},{produto.preco_compra},{produto.preco_venda},{produto.local}\n"
        else:
            # Adiciona nova linha se o ID for novo
            linhas.append(f"{produto.nome},{produto.quantidade},{produto.preco_compra},{produto.preco_venda},{produto.local}\n")

        with open(self.arquivo, 'w') as f:
            f.writelines(linhas)
