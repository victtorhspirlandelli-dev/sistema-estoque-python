import json
from datetime import datetime

historico = []
5
try:
    with open("estoque.json", "r") as f:
        estoque = json.load(f)
except FileNotFoundError:
    estoque = {}



while True:
    print("\n" + "="*30)
    print("   SISTEMA DE ESTOQUE")
    print("="*30)


    print("1 - Adicionar produto")
    print("2 - Remover produto")
    print("3 - Ver estoque")
    print("4 - Vender produto")
    print("5 - Ver histórico")
    print("6 - Sair")
    

    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input("Nome do produto: ").strip().lower()
        quantidade = int(input("Quantidade: "))

        estoque[nome] = quantidade
        print("Produto adicionado!")

    elif opcao == "2":
        nome = input("Produto para remover: ")
        
        if nome in estoque:
            del estoque[nome]
            print("Produto removido!")
        else:
            print("Produto não encontrado")

    elif opcao == "3":
         if not estoque:
            print("Estoque vazio!")
         else:
            for produto, qtd in estoque.items():
                if qtd <= 5:
                    print(produto, "-", qtd, "⚠️ BAIXO")
                else:
                    print(produto, "-", qtd)
    
    elif opcao == "4":
        nome = input("Produto: ")
        quantidade = int(input("Quantidade: "))
        
        if nome in estoque:
            if estoque[nome] >= quantidade:
                estoque[nome] -= quantidade
                data = datetime.now().strftime("%d/%m/%Y %H:%M")
                historico.append(f"{data} - Venda: {nome} - {quantidade}")
                print("Venda realizada!")
            else:
                print("Estoque insuficiente")
        else:
            print("Produto não encontrado")
    
    elif opcao == "5":
        for item in historico:
            print(item)

    
    elif opcao == "6":
        print("Saindo...")
        with open("estoque.json", "w") as f:
            json.dump(estoque, f)
        break

    else:
        print("Opção inválida")            