import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from estoque import Estoque
from sistema import SistemaDeInventario
from main import testar_sistema

class SistemaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventário")
        
        self.label_intro = tk.Label(root, text="Deseja iniciar com o estoque vazio ou importar de um arquivo?")
        self.label_intro.pack()
        
        self.btn_estoque_vazio = tk.Button(root, text="Iniciar com estoque vazio", command=self.iniciar_estoque_vazio)
        self.btn_estoque_vazio.pack()
        
        self.btn_importar_estoque = tk.Button(root, text="Importar do arquivo 'estoque.txt'", command=self.importar_estoque)
        self.btn_importar_estoque.pack()
        
        self.label_op = tk.Label(root, text="Escolha uma operação:")
        self.label_op.pack()
        
        self.frame_op = tk.Frame(root)
        self.frame_op.pack()
        
        self.btn_ler = tk.Button(self.frame_op, text="Ler Produto", command=self.ler_produto)
        self.btn_ler.grid(row=0, column=0)
        
        self.btn_escrever = tk.Button(self.frame_op, text="Escrever Produto", command=self.escrever_produto)
        self.btn_escrever.grid(row=0, column=1)
        
        self.btn_imprimir_memoria = tk.Button(self.frame_op, text="Imprimir Memória", command=self.imprimir_memoria)
        self.btn_imprimir_memoria.grid(row=1, column=0)
        
        self.btn_imprimir_caches = tk.Button(self.frame_op, text="Imprimir Caches", command=self.imprimir_caches)
        self.btn_imprimir_caches.grid(row=1, column=1)
        
        self.btn_testar_sistema = tk.Button(self.frame_op, text="Testar Sistema", command=self.testar_sistema)
        self.btn_testar_sistema.grid(row=2, column=0)
        
        self.btn_sair = tk.Button(self.frame_op, text="Sair", command=root.quit)
        self.btn_sair.grid(row=2, column=1)
        
        self.estoque = None
        self.sistema = None
    
    def iniciar_estoque_vazio(self):
        self.estoque = Estoque("novo_estoque.txt")
        criar_estoque_com_valores_none("novo_estoque.txt")
        self.sistema = SistemaDeInventario(self.estoque)
        messagebox.showinfo("Informação", "Estoque iniciado com valores 'None'.")
    
    def importar_estoque(self):
        self.estoque = Estoque("estoque.txt")
        self.sistema = SistemaDeInventario(self.estoque)
        messagebox.showinfo("Informação", "Estoque importado do arquivo 'estoque.txt'.")
    
    def ler_produto(self):
        if not self.sistema:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
            return
        
        processador_id = self.solicitar_processador()
        if processador_id is None:
            return
        
        endereco = self.solicitar_endereco()
        if endereco is None:
            return
        
        produto = self.sistema.ler(processador_id, endereco)
        if produto is not None:
            messagebox.showinfo("Produto", f"Produto lido: {produto}")
        else:
            messagebox.showinfo("Produto", "Produto não encontrado.")
    
    def escrever_produto(self):
        if not self.sistema:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
            return
        
        processador_id = self.solicitar_processador()
        if processador_id is None:
            return
        
        endereco = self.solicitar_endereco()
        if endereco is None:
            return
        
        produto_existente = self.sistema.memoria_principal.ler(endereco)
        
        nome = self.solicitar_input("Nome do produto", produto_existente.nome if produto_existente else "")
        quantidade = self.solicitar_input("Quantidade do produto", produto_existente.quantidade if produto_existente else "")
        preco_compra = self.solicitar_input("Preço de compra", produto_existente.preco_compra if produto_existente else "")
        preco_venda = self.solicitar_input("Preço de venda", produto_existente.preco_venda if produto_existente else "")
        local = self.solicitar_input("Localização", produto_existente.local if produto_existente else "")
        
        self.sistema.escrever(processador_id, endereco, nome=nome, quantidade=int(quantidade), preco_compra=float(preco_compra), preco_venda=float(preco_venda), local=local)
        messagebox.showinfo("Produto", f"Produto ID {endereco} atualizado com sucesso.")
    
    def imprimir_memoria(self):
        if self.sistema:
            self.sistema.memoria_principal.imprimir()
        else:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
    
    def imprimir_caches(self):
        processador_id = self.solicitar_processador()
        if processador_id is None:
            return
        
        if self.sistema:
            self.sistema.caches[processador_id].imprimir()
        else:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
    
    def testar_sistema(self):
        if self.estoque:
            testar_sistema(self.estoque.arquivo)
        else:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
    
    def solicitar_processador(self):
        processador_id = self.solicitar_input("Escolha um processador (0, 1, 2)")
        if processador_id is None:
            return None
        try:
            processador_id = int(processador_id)
            if processador_id not in [0, 1, 2]:
                messagebox.showerror("Erro", "ID do processador inválido. Por favor, escolha 0, 1 ou 2.")
                return None
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Por favor, digite um número inteiro.")
            return None
        return processador_id
    
    def solicitar_endereco(self):
        endereco = self.solicitar_input("Digite o ID do produto (0-49)")
        if endereco is None:
            return None
        try:
            endereco = int(endereco)
            if endereco < 0 or endereco >= 50:
                messagebox.showerror("Erro", "ID do produto fora do intervalo válido (0-49).")
                return None
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida. Por favor, digite um número inteiro.")
            return None
        return endereco
    
    def solicitar_input(self, mensagem, valor_default=""):
        return simpledialog.askstring("Input", mensagem, initialvalue=valor_default)

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
    root = tk.Tk()
    app = SistemaGUI(root)
    root.mainloop()
