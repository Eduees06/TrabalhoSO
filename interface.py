import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from estoque import Estoque
from sistema import SistemaDeInventario
from main import testar_sistema

class SistemaGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Sistema de Inventário")
        self.sistema = None 
        self.ultima_leitura = None
        self.iniciar_tela_inicial()

    def iniciar_tela_inicial(self):
        self.frame_inicial = tk.Frame(self.root)
        self.frame_inicial.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(self.frame_inicial, text="Sistema de Inventário", font=("Arial", 24))
        titulo.pack(pady=20)

        btn_novo_estoque = tk.Button(self.frame_inicial, text="Iniciar com Estoque Vazio", command=self.tela_novo_estoque)
        btn_novo_estoque.pack(pady=10)

        btn_importar_estoque = tk.Button(self.frame_inicial, text="Importar Estoque do Arquivo", command=self.importar_estoque)
        btn_importar_estoque.pack(pady=10)

    def mostrar_interface_operacoes(self):
        if hasattr(self, 'frame_inicial'):
            self.frame_inicial.pack_forget()
        if hasattr(self, 'frame_novo_estoque'):
            self.frame_novo_estoque.pack_forget()

        self.frame_operacoes = tk.Frame(self.root)
        self.frame_operacoes.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(self.frame_operacoes, text="Operações de Estoque", font=("Arial", 24))
        titulo.pack(pady=20)

        btn_ler_produto = tk.Button(self.frame_operacoes, text="Ler Produto", command=self.ler_produto)
        btn_ler_produto.pack(pady=10)

        btn_escrever_produto = tk.Button(self.frame_operacoes, text="Escrever Produto", command=self.escrever_produto)
        btn_escrever_produto.pack(pady=10)

        btn_imprimir_memoria = tk.Button(self.frame_operacoes, text="Imprimir Memória", command=self.imprimir_memoria)
        btn_imprimir_memoria.pack(pady=10)

        btn_imprimir_caches = tk.Button(self.frame_operacoes, text="Imprimir Caches", command=self.imprimir_caches)
        btn_imprimir_caches.pack(pady=10)

        btn_teste = tk.Button(self.frame_operacoes, text="Testar Sistema", command=self.testar_sistema)
        btn_teste.pack(pady=10)

        btn_voltar = tk.Button(self.frame_operacoes, text="Voltar", command=self.voltar_para_inicial)
        btn_voltar.pack(pady=10)

    def tela_novo_estoque(self):
        self.frame_inicial.pack_forget()
        self.frame_novo_estoque = tk.Frame(self.root)
        self.frame_novo_estoque.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(self.frame_novo_estoque, text="Novo Estoque", font=("Arial", 24))
        titulo.pack(pady=20)

        lbl_arquivo = tk.Label(self.frame_novo_estoque, text="Digite o nome do novo arquivo de estoque:")
        lbl_arquivo.pack(pady=10)

        self.entry_arquivo = tk.Entry(self.frame_novo_estoque)
        self.entry_arquivo.pack(pady=10)

        btn_criar = tk.Button(self.frame_novo_estoque, text="Criar Estoque", command=self.criar_novo_estoque)
        btn_criar.pack(pady=10)

        btn_voltar = tk.Button(self.frame_novo_estoque, text="Voltar", command=self.voltar_para_inicial)
        btn_voltar.pack(pady=10)

    def importar_estoque(self):
        arquivo = "estoque.txt"  # Nome do arquivo a ser importado
        self.sistema = SistemaDeInventario(Estoque(arquivo))
        messagebox.showinfo("Importar Estoque", f"Estoque '{arquivo}' importado com sucesso!")
        self.mostrar_interface_operacoes()

    def criar_novo_estoque(self):
        arquivo = self.entry_arquivo.get().strip()
        if arquivo:
            criar_estoque_com_valores_none(arquivo)
            self.sistema = SistemaDeInventario(Estoque(arquivo))
            messagebox.showinfo("Sucesso", f"Estoque iniciado com valores 'None'. Arquivo criado: {arquivo}")
            self.mostrar_interface_operacoes()
        else:
            messagebox.showerror("Erro", "Por favor, insira um nome de arquivo válido.")

    def voltar_para_inicial(self):
        if hasattr(self, 'frame_operacoes'):
            self.frame_operacoes.pack_forget()
        self.iniciar_tela_inicial()

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
        
        cache_hit_antes = any(self.sistema.caches[i].encontrar_linha(endereco) is not None for i in range(len(self.sistema.caches)))

        produto = self.sistema.ler(processador_id, endereco)
        
        if cache_hit_antes:
            messagebox.showinfo("Read Hit", f"Leitura bem-sucedida na cache {processador_id} (Read Hit).")
        else:
            messagebox.showinfo("Read Miss", f"Produto não estava na cache {processador_id} (Read Miss).")

        if produto is not None:
            messagebox.showinfo("Produto", f"Produto lido: {produto}")

        else:
            messagebox.showinfo("Produto", "Produto não encontrado.")
            self.ultima_leitura = None

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
        
        cache_hit_antes = any(self.sistema.caches[i].encontrar_linha(endereco) is not None for i in range(len(self.sistema.caches)))

        self.sistema.escrever(processador_id, endereco, nome=nome, quantidade=int(quantidade), preco_compra=float(preco_compra), preco_venda=float(preco_venda), local=local)
        
        if cache_hit_antes:
            messagebox.showinfo("Write Hit", f"Escrita bem-sucedida na cache {processador_id} (Write Hit).")
        else:
            messagebox.showinfo("Write Miss", f"Produto não estava na cache {processador_id} (Write Miss).")

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
            cache = self.sistema.caches[processador_id]
            cache.imprimir()
        else:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")

    def testar_sistema(self):
        # Supondo que o sistema tenha um atributo para acessar o estoque
        if self.sistema and hasattr(self.sistema, 'estoque_objeto'):  # Substitua 'estoque_objeto' pelo nome correto
            arquivo_estoque = self.sistema.estoque_objeto.arquivo  # Acesse o arquivo do estoque através do objeto
            teste = testar_sistema(arquivo_estoque)
        
            if teste == 9:
                messagebox.showinfo("Passou no teste!", "O sistema passou nos 9 testes!")
            else:
                messagebox.showinfo("Não passou.", f"O sistema não passou em todos os testes. {teste}/9 testes.")

        else:
            messagebox.showwarning("Aviso", "Por favor, inicie o estoque antes.")
    
    def solicitar_processador(self):
        processador_id = simpledialog.askinteger("Processador", "Digite o ID do processador (0, 1 ou 2):")
        if processador_id is None or processador_id not in [0, 1, 2]:
            messagebox.showwarning("Aviso", "Por favor, insira um ID de processador válido (0, 1 ou 2).")
            return None
        return processador_id

    def solicitar_endereco(self):
        endereco = simpledialog.askinteger("Endereço", "Digite o endereço do produto:")
        if endereco is None or endereco < 0:
            messagebox.showwarning("Aviso", "Por favor, insira um endereço válido (número inteiro positivo).")
            return None
        return endereco

    def solicitar_input(self, label, valor_atual=""):
        return simpledialog.askstring(label, f"{label}:", initialvalue=valor_atual)

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

