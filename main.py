from estoque import Estoque
from sistema import SistemaDeInventario

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
    sistema = SistemaDeInventario(estoque)
    
    while True:
        print("Escolha um processador (0, 1, 2) :")
        try:
            processador_id = int(input())
            if processador_id not in [0, 1, 2]:
                print("ID do processador inválido. Por favor, escolha 0, 1 ou 2.")
                continue
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            continue
        
        print("=" * 100)
        print("Escolha uma operação:")
        print("1 - Leitura: Ler as informações de um produto do estoque")
        print("2 - Escrita: Adicionar ou Atualizar informações de um produto no estoque")
        print("3 - Imprimir Memória Principal: Exibir todos os produtos na memória principal")
        print("4 - Imprimir Caches: Exibir o conteúdo das caches dos processadores")
        print("5 - Testar Sistema: Executar cenários de teste")
        print("6 - Sair: Encerrar o programa")
        print("=" * 100)
        
        try:
            operacao = int(input())
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            continue
        
        if operacao in [1, 2]:
            try:
                print("Digite o ID do produto (0-49):")
                endereco = int(input())
                if endereco < 0 or endereco >= 50:
                    print("ID do produto fora do intervalo válido (0-49).")
                    continue
                
                if operacao == 1:
                    produto = sistema.ler(processador_id, endereco)
                    if produto is not None:
                        print(f"Produto lido: {produto}")
                    else:
                        print("Produto não encontrado.")
                elif operacao == 2:
                    print("Digite a nova quantidade (ou pressione Enter para não alterar):")
                    quantidade_str = input().strip()
                    quantidade = int(quantidade_str) if quantidade_str != "" else None
                    
                    print("Digite o novo nome (ou pressione Enter para não alterar):")
                    nome = input().strip()
                    if nome == "":
                        nome = None
                    
                    print("Digite o novo preço de compra (ou pressione Enter para não alterar):")
                    preco_compra_str = input().strip()
                    preco_compra = float(preco_compra_str) if preco_compra_str != "" else None
                    
                    print("Digite o novo preço de venda (ou pressione Enter para não alterar):")
                    preco_venda_str = input().strip()
                    preco_venda = float(preco_venda_str) if preco_venda_str != "" else None
                    
                    print("Digite o novo local (ou pressione Enter para não alterar):")
                    local = input().strip()
                    if local == "":
                        local = None
                    
                    produto_existente = sistema.memoria_principal.ler(endereco)
                    
                    if produto_existente is not None:
                        sistema.escrever(processador_id, endereco, nome=nome, quantidade=quantidade, preco_compra=preco_compra, preco_venda=preco_venda, local=local)
                        print(f"Produto ID {endereco} atualizado com sucesso.")
                    else:
                        # Verifica se todos os campos obrigatórios foram fornecidos para criação
                        if nome and quantidade is not None and preco_compra is not None and preco_venda is not None and local:
                            sistema.escrever(processador_id, endereco, nome=nome, quantidade=quantidade, preco_compra=preco_compra, preco_venda=preco_venda, local=local)
                            print(f"Produto ID {endereco} criado com sucesso.")
                        else:
                            print("Não foi possível criar o produto. Todos os campos devem ser fornecidos.")
            
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
        
        elif operacao == 3:
            sistema.memoria_principal.imprimir()
        
        elif operacao == 4:
            if processador_id in [0, 1, 2]:
                print(f"Cache do Processador {processador_id}:")
                sistema.caches[processador_id].imprimir()
            else:
                print("ID do processador inválido.")
        
        elif operacao == 5:
            testar_sistema(arquivo)
        
        elif operacao == 6:
            break
        
        else:
            print("Operação inválida.")

def testar_sistema(arquivo):
    teste = 0
    estoque = Estoque(arquivo)
    sistema = SistemaDeInventario(estoque)

    # Cenário 1: Leitura em Estado Exclusivo (E)
    print("Cenário 1: Leitura em Estado Exclusivo pelo Processador 0")
    sistema.ler(0, 0)
    estado1 = sistema.caches[0].encontrar_linha(0).estado
    sistema.ler(0, 0)
    estado2 = sistema.caches[0].encontrar_linha(0).estado
    if estado1 == estado2:
        print("Teste passou: Estado correto após leitura.")
        teste += 1
    else:
        print(f"Teste falhou: Estado incorreto ({estado}) após leitura.")
        
    # Cenário 2: Leitura em Estado Compartilhado (S)
    print("\nCenário 2: Leitura em Estado Compartilhado pelo Processador 1")
    sistema.ler(1, 0)
    estado_proc0 = sistema.caches[0].encontrar_linha(0).estado
    estado_proc1 = sistema.caches[1].encontrar_linha(0).estado
    if estado_proc0 == 'S' and estado_proc1 == 'S':
        print("Teste passou: Ambos os processadores têm o estado correto (Compartilhado).")
        teste += 1
    else:
        print(f"Teste falhou: Estados incorretos (Proc0: {estado_proc0}, Proc1: {estado_proc1}).")

    # Cenário 3: Leitura em Estado Modificado (M)
    print("\nCenário 3: Leitura em Estado Modificado pelo Processador 2")
    sistema.escrever(0, 0, "Arroz", 200, 3.5, 5.0, "Corredor 1")
    sistema.ler(2, 0)
    estado_proc0 = sistema.caches[0].encontrar_linha(0).estado
    estado_proc2 = sistema.caches[2].encontrar_linha(0).estado
    if estado_proc0 == 'S' and estado_proc2 == 'S':
        print("Teste passou: Estados corretos após leitura de dado modificado.")
        teste += 1
    else:
        print(f"Teste falhou: Estados incorretos (Proc0: {estado_proc0}, Proc2: {estado_proc2}).")

    # Cenário 4: Escrita em Estado Exclusivo (E)
    print("\nCenário 4: Escrita em Estado Exclusivo pelo Processador 0")
    sistema.escrever(0, 1, "Feijão", 100, 4.0, 6.0, "Corredor 1")
    estado = sistema.caches[0].encontrar_linha(1).estado
    if estado == 'M':
        print("Teste passou: Estado correto (Modificado) após escrita exclusiva.")
        teste += 1
    else:
        print(f"Teste falhou: Estado incorreto ({estado}) após escrita exclusiva.")

    # Cenário 5: Escrita em Estado Compartilhado (S)
    print("\nCenário 5: Escrita em Estado Compartilhado pelo Processador 1")
    sistema.ler(0, 3)
    sistema.ler(1, 3)
    sistema.escrever(1, 3, "Macarrão", 50, 2.0, 3.0, "Corredor 2")
    estado_proc1 = sistema.caches[1].encontrar_linha(3).estado
    estado_proc0 = sistema.caches[0].encontrar_linha(3).estado
    if estado_proc1 == 'M' and estado_proc0 == 'I':
        print("Teste passou: Estados corretos após escrita em dado compartilhado.")
        teste += 1
    else:
        print(f"Teste falhou: Estados incorretos (Proc1: {estado_proc1}, Proc0: {estado_proc0}).")

    # Cenário 6: Escrita em Estado Modificado (M)
    print("\nCenário 6: Escrita em Estado Modificado pelo Processador 0")
    sistema.escrever(1, 3, "Feijão", 150, 3.0, 4.5, "Corredor 3")
    estado = sistema.caches[1].encontrar_linha(3).estado
    if estado == 'M':
        print("Teste passou: Estado correto (Modificado) após escrita.")
        teste += 1
    else:
        print(f"Teste falhou: Estado incorreto ({estado}) após escrita.")

    # Cenário 7: Escrita com Estado Inválido (I)
    print("\nCenário 7: Escrita com Estado Inválido pelo Processador 1")
    sistema.ler(0, 3)
    sistema.ler(1, 3)
    sistema.escrever(0, 3, "Farinha", 80, 1.5, 2.5, "Corredor 4")
    estado_proc0 = sistema.caches[0].encontrar_linha(3).estado
    estado_proc1 = sistema.caches[1].encontrar_linha(3).estado
    if estado_proc0 == 'M' and estado_proc1 == 'I':
        print("Teste passou: Estado correto (Modificado) após escrita em dado inválido.")
        teste += 1
    else:
        print(f"Teste falhou: Estados incorretos (Proc0: {estado_proc0}, Proc1: {estado_proc1}).")

    print(f"{teste}/7 testes concluídos com sucesso.")
    

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