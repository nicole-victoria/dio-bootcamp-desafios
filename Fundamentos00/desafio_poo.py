# Desafio 3 : recriar o desafio 2 a partir do paradigma de Orientação a objetos

from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap

#---------- classe Cliente e sua filha
class Cliente:
    def __init__(self, endereco):
        self.endereco =endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
#-------------- classe Conta e sua filha
class Conta():
    def __init__(self, numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "9999"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def cliente(self):
        return self._cliente
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor>saldo

        if excedeu_saldo:
            print("@@@@ Operação falhou! Saldo insuficiente...")
        elif not excedeu_saldo:
            self._saldo -= valor
            print("#### Saque realizado com sucesso!")
            return True
        else:
            print("@@@@ Valor informado inválido!")

        return False 
    
    def depositar(self, valor):
        if valor >0:
            self._saldo += valor
            print("#### Depósito realizado com sucesso!")
        else:
            print("@@@@ Valor informado inválido!") 
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]

        )
        excedeu_limite= valor > self.limite
        excedeu_saques = valor > self.limite_saques

        if excedeu_limite:
            print("@@@@ Operação falhou! Voce excedeu o limite de saque...")
        elif excedeu_saques:
            print("@@@@ Operação falhou! Voce excedeu o limite de saques...")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
        Agencia: {self.agencia}
        C/C: {self.numero}
        Titular:{self.cliente.nome}
        """

# -------- classe Historico
class Historico:
    def __init__(self):
        self._transacoes=[]
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

# --------- Interface transacao e suas implementações
class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# ----- função de menu
def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@@ Cliente não possui conta!")

        return
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@@ Cliente não encontrado!")
        return
    valor =float(input("Digite o valor: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@@ Cliente não encontrado!")
        return
    valor =float(input("Digite o valor: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@@ Cliente não encontrado!")
        return
    valor =float(input("Digite o valor: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=====================EXTRATO========================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}: R${transacao["valor"]:.2f}"
    print(extrato)
    print(f"\nSaldo: R${conta.saldo:.2f}")
    print("\n====================================================")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@@ Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    clientes.contas.append(conta)

    print("\n#### Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("="*10)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n@@@@ já existe cliente com esse cpf")
        return
    
    nome = input("Digite o nome: ")
    data_nasc = input("Informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("Informe seu endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nasc, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n#### Cliente criado com sucesso!")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)


        elif opcao == "3":
            exibir_extrato(clientes)
        
        elif opcao == "4":
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "5":
            criar_cliente(clientes)

        elif opcao== "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Saindo... Obrigado por usar nosso sistema!")
            break

        else:
            print("Operação inválida, tente novamente.")

main()

