import tkinter as tk
from tkinter import messagebox
from estoque import Estoque
from sistema import SistemaDeInventario

class InventarioGUI:
    def __init__(self, root, estoque):
        self.root = root
        self.sistema = SistemaDeInventario(estoque)
        self.create_widgets()
    
    def create_widgets(self):
        self.root.title("Sistema de Inventário")

        # Frame para o Processador
        processador_frame = tk.Frame(self.root)
        processador_frame.pack(pady=10)
        
        tk.Label(processador_frame, text="Escolha o Processador (0, 1, 2):").pack(side=tk.LEFT)
        self.processador_id = tk.IntVar(value=0)
        tk.Spinbox(processador_frame, from_=0, to=2, textvariable=self.processador_id, width=5).pack(side=tk.LEFT)
        
        # Frame para as Operações
        operacao_frame = tk.Frame(self.root)
        operacao_frame.pack(pady=10)

        tk.Button(operacao_frame, text="Leitura", command=self.ler).pack(side=tk.LEFT, padx=5)
        tk.Button(operacao_frame, text="Escrita", command=self.escrever).pack(side=tk.LEFT, padx=5)
        tk.Button(operacao_frame, text="Imprimir Memória Principal", command=self.imprimir_memoria_principal).pack(side=tk.LEFT, padx=5)
        tk.Button(operacao_frame, text="Imprimir Caches", command=self.imprimir_caches).pack(side=tk.LEFT, padx=5)
        tk.Button(operacao_frame, text="Sair", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def ler(self):
        processador_id = self.processador_id.get()
        endereco = self.solicitar_endereco()

        if endereco is None:
            return
        
        estado_anterior = self.sistema.caches[processador_id].encontrar_linha(endereco)
        produto = self.sistema.ler(processador_id, endereco)
        estado_atual = self.sistema.caches[processador_id].encontrar_linha(endereco)
        
        if produto:
            messagebox.showinfo("Leitura", f"Produto lido: {produto}")
            if estado_anterior is None:
                messagebox.showinfo("Read Miss", "Ocorreu um read miss.")
            else:
                messagebox.showinfo("Read Hit", "Ocorreu um read hit.")
        else:
            messagebox.showwarning("Leitura", "Produto não encontrado.")

    def escrever(self):
        processador_id = self.processador_id.get()
        endereco = self.solicitar_endereco()

        if endereco is None:
            return

        estado_anterior = self.sistema.caches[processador_id].encontrar_linha(endereco)
        nome, quantidade, preco_compra, preco_venda, local = self.solicitar_dados_produto()
        
        self.sistema.escrever(processador_id, endereco, nome=nome, quantidade=quantidade, preco_compra=preco_compra, preco_venda=preco_venda, local=local)
        estado_atual = self.sistema.caches[processador_id].encontrar_linha(endereco)
        
        if estado_anterior is None:
            messagebox.showinfo("Write Miss", "Ocorreu um write miss.")
        else:
            messagebox.showinfo("Write Hit", "Ocorreu um write hit.")
        messagebox.showinfo("Escrita", f"Produto ID {endereco} atualizado com sucesso.")

    def solicitar_endereco(self):
        endereco = tk.simpledialog.askinteger("ID do Produto", "Digite o ID do produto (0-49):")
        if endereco is None or endereco < 0 or endereco >= 50:
            messagebox.showwarning("Entrada inválida", "ID do produto fora do intervalo válido (0-49).")
            return None
        return endereco

    def solicitar_dados_produto(self):
        nome = tk.simpledialog.askstring("Nome do Produto", "Digite o novo nome (ou pressione Enter para não alterar):")
        quantidade = tk.simpledialog.askinteger("Quantidade", "Digite a nova quantidade (ou pressione Enter para não alterar):")
        preco_compra = tk.simpledialog.askfloat("Preço de Compra", "Digite o novo preço de compra (ou pressione Enter para não alterar):")
        preco_venda = tk.simpledialog.askfloat("Preço de Venda", "Digite o novo preço de venda (ou pressione Enter para não alterar):")
        local = tk.simpledialog.askstring("Local", "Digite o novo local (ou pressione Enter para não alterar):")
        return nome, quantidade, preco_compra, preco_venda, local
    
    def imprimir_memoria_principal(self):
        self.sistema.memoria_principal.imprimir()

    def imprimir_caches(self):
        processador_id = self.processador_id.get()
        messagebox.showinfo(f"Cache do Processador {processador_id}", f"{self.sistema.caches[processador_id].imprimir()}")

def main():
    print("Deseja iniciar com o estoque vazio ou importar de um arquivo?")
    print("1 - Iniciar com estoque vazio")
    print("2 - Importar do arquivo 'estoque.txt'")
    
    escolha = int(input())
    if escolha == 1:
        print("Digite o nome do novo arquivo de estoque (ex: 'novo_estoque.txt'):")
        arquivo = input().strip()
        criar_estoque_com_valores_none(arquivo)
        print(f"Estoque iniciado com valores 'None'. Arquivo criado: {arquivo}")
    
    elif escolha == 2:
        arquivo = "estoque.txt"
        print("Estoque importado do arquivo 'estoque.txt'.")
    
    else:
        print("Opção inválida. O programa será encerrado.")
        return

    estoque = Estoque(arquivo)
    
    root = tk.Tk()
    app = InventarioGUI(root, estoque)
    root.mainloop()

def criar_estoque_com_valores_none(arquivo, num_produtos=50):
    with open(arquivo, 'w') as f:
        for i in range(num_produtos):
            nome = "None"
            quantidade = 0
            preco_compra = 0
            preco_venda = 0
            local = "None"
            f.write(f"{nome},{quantidade},{preco_compra},{preco_venda},{local}\n")

if __name__ == "__main__":
    main()
