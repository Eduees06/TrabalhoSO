from estoque import Estoque
from sistema import SistemaDeInventario

def main():
    estoque = Estoque()
    sistema = SistemaDeInventario(estoque)
    
    while True:
        print("Escolha um processador (0, 1, 2) :")
        processador_id = int(input())
        
        if processador_id not in [0, 1, 2]:
            print("ID do processador inválido. Por favor, escolha 0, 1 ou 2.")
            continue
        
        print("=" * 100)
        print("Escolha uma operação:")
        print("1 - Leitura: Ler as informações de um produto do estoque")
        print("2 - Escrita: Adicionar ou Atualizar informações de um produto no estoque")
        print("3 - Imprimir Memória Principal: Exibir todos os produtos na memória principal")
        print("4 - Imprimir Caches: Exibir o conteúdo das caches dos processadores")
        print("5 - Sair: Encerrar o programa")
        print("=" * 100)
        
        operacao = int(input())
        
        if operacao in [1, 2]:
            print("Digite o ID do produto (0-49):")
            endereco = int(input())
            
            if operacao == 1:
                quantidade = sistema.ler(processador_id, endereco)
                produto = estoque.ler_produto(endereco)
                print(f"Produto lido: {produto}, Quantidade lida: {quantidade}")
            elif operacao == 2:
                print("Digite a nova quantidade:")
                quantidade = int(input())
                sistema.escrever(processador_id, endereco, quantidade)
                print(f"Nova quantidade do produto ID {endereco} atualizada para {quantidade}")
        
        elif operacao == 3:
            sistema.memoria_principal.imprimir()
        
        elif operacao == 4:
            print(f"Cache do Processador {processador_id}:")
            sistema.caches[processador_id].imprimir()
                
        elif operacao == 5:
            break
        
        else:
            print("Operação inválida.")

if __name__ == "__main__":
    main()