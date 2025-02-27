# Desafio 1: Criar um sistema bancário com as operações sacar, depositar e visualizar extrato

# Desafio 2: Modularizar as opções, criando funções e criar mais duas funções: criar usuário e criar conta corrente
def saque(*, saldo, valor, historico, limite, numero_saques, limite_saques):
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


def deposito(saldo, valor, historico, /):
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


def criar_usuario(usuarios):
    cpf = input("Informe o CPF(Somente número)")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n!!! Já existe um usuário com esse CPF !!! ")
        return

    nome = input("Digite o nome: ")
    data_nasc = input("Informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("Informe seu endereço: ")
    usuarios.append({"nome": nome, "data_nascimento": data_nasc, "endereco": endereco, "cpf":cpf})

    print("||| Usuário criado com sucesso |||")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtro = [usuarios for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtro[0] if usuarios_filtro else None

def criar_conta(agencia, numero, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero, "usuario4": usuario}
    print("\n !!! Usuário não encontrado")


menu = """
===== MENU =====
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar usuario
[5] Criar conta
[6] Sair
=> """

usuarios = []
contas =[]
saldo = 0
limite = 500
historico = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "001"

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saldo, historico = deposito(saldo, valor, historico)
        extrato(saldo, historico)

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        saldo, historico, numero_saques = saque(
            saldo =saldo, valor=valor, historico=historico, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES
        )
        extrato(saldo, historico)


    elif opcao == "3":
        extrato(saldo, historico)
    
    elif opcao == "4":
        criar_usuario(usuarios)
    
    elif opcao == "5":
        numero_conta = len(contas) +1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)

        if contas:
            contas.append(conta)


    elif opcao == "6":
        print("Saindo... Obrigado por usar nosso sistema!")
        break

    else:
        print("Operação inválida, tente novamente.")