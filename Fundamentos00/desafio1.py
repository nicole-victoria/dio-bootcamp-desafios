# Desafio 1: Criar um sistema bancário com as operações sacar, depositar e visualizar extrato

# Desafio 2: Modularizar as opções, criando funções e criar mais duas funções: criar usuário e criar conta corrente
def saque(saldo, valor, historico, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        historico += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Seu saldo atual é de R$ {saldo:.2f}\n")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, historico, numero_saques


def deposito(saldo, valor, historico):
    if valor > 0:
        saldo += valor
        historico += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Opa! Não é possível depositar esse valor")

    return saldo, historico


def extrato(saldo, historico):
    print("\n================ EXTRATO ================")
    print(historico if historico else "Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================\n")


menu = """
===== MENU =====
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
=> """

saldo = 0
limite = 500
historico = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saldo, historico = deposito(saldo, valor, historico)
        print(f"Seu saldo é de {saldo}\n")
        extrato(saldo, historico)

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        saldo, historico, numero_saques = saque(
            saldo, valor, historico, limite, numero_saques, LIMITE_SAQUES
        )
        print(f"Seu saldo é de {saldo}\n")
        extrato(saldo, historico)


    elif opcao == "3":
        extrato(saldo, historico)

    elif opcao == "4":
        print("Saindo... Obrigado por usar nosso sistema!")
        break

    else:
        print("Operação inválida, tente novamente.")