import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

# ==============================================================================
# CLASSES ABSTRATAS E DE TRANSAÇÃO
# ==============================================================================

class Cliente:
    """Classe base para o cliente do sistema bancário."""
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação (depósito ou saque) na conta do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self._contas.append(conta)

class PessoaFisica(Cliente):
    """Representa um cliente Pessoa Física, herda de Cliente."""
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome

class Conta:
    """Classe base para contas bancárias."""
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de classe para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """Método para realizar saques na conta."""
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n===== Saque realizado com sucesso! =====")
            return True
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

    def depositar(self, valor):
        """Método para realizar depósitos na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n==== Depósito realizado com sucesso! ====")
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False
        return True

class ContaCorrente(Conta):
    """Representa uma Conta Corrente, herda de Conta."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para incluir limites da Conta Corrente."""
        numero_saques = len(
            [
                transacao for transacao in self.historico.transacoes 
                if transacao["tipo"] == Saque.__name__
            ]
        )
        
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! Valor excede o limite de R$ 500.00. @@@")
            return False
        
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido (3). @@@")
            return False
        
        else:
            return super().sacar(valor)

    def __str__(self):
        """Representação em string da Conta Corrente."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    """Classe para registrar e exibir o histórico de transações da conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        """Gera um relatório do histórico, opcionalmente filtrando por tipo."""
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class Transacao(ABC):
    """Classe Abstrata base para todas as transações."""
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    """Representa uma transação de saque, herda de Transacao."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra o saque na conta e no histórico."""
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    """Representa uma transação de depósito, herda de Transacao."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra o depósito na conta e no histórico."""
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# ==============================================================================
# FUNÇÕES DE INTERAÇÃO E AUXILIARES
# ==============================================================================

def menu():
    """Exibe o menu e recebe a opção do usuário."""
    menu_texto = """\n
    __________MENU____________
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    -> """
    return input(textwrap.dedent(menu_texto))

def filtrar_cliente(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def filtrar_conta(numero_conta, contas):
    """Busca uma conta na lista pelo número."""
    contas_filtradas = [conta for conta in contas if conta.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def recuperar_conta_cliente(cliente):
    """Permite ao cliente selecionar uma de suas contas."""
    if not cliente._contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # Implementação simples para selecionar a primeira conta (para este desafio)
    print("\nContas disponíveis:")
    for i, conta in enumerate(cliente._contas):
        print(f"{i+1}: Agência {conta.agencia} / Conta {conta.numero}")

    # No sistema final, o usuário escolheria uma conta
    try:
        if len(cliente._contas) == 1:
            print("Selecionando a única conta disponível...")
            return cliente._contas[0]
        else:
             # Para simplificar, vou selecionar a primeira conta se houver mais de uma
            opcao = input("Digite o número da conta para operar: ")
            try:
                num_conta_selecionada = int(opcao)
                conta_selecionada = filtrar_conta(num_conta_selecionada, cliente._contas)
                if conta_selecionada:
                    return conta_selecionada
                else:
                    print("\n@@@ Número de conta inválido. @@@")
                    return None
            except ValueError:
                print("\n@@@ Entrada inválida. @@@")
                return None
            
    except IndexError:
        print("\n@@@ Opção inválida. @@@")
        return None
    except Exception:
        print("\n@@@ Ocorreu um erro ao selecionar a conta. @@@")
        return None

def depositar(clientes):
    """Função para realizar a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    """Função para realizar a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    """Função para exibir o extrato bancário."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n======= EXTRATO =======")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in conta.historico.gerar_relatorio():
            extrato += f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f} ({transacao['data']})\n"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================")

def criar_usuario(clientes):
    """Função para criar um novo usuário (cliente)."""
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n==== Usuário criado com sucesso! ====")

def criar_conta(numero_conta, clientes, contas):
    """Função para criar uma nova conta corrente e vinculá-la a um cliente."""
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Usuário não encontrado! Criação de conta encerrada. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n==== Conta criada com sucesso! ====")

def listar_contas(contas):
    """Função para listar todas as contas cadastradas."""
    if not contas:
        print("\nNão há contas cadastradas.")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    print("==================================================")

# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

def main():
    """Função principal do sistema bancário."""
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_usuario(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()