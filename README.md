 Sistema Bancário Orientado a Objetos (POO)Este é um sistema bancário simples refatorado para utilizar o paradigma de Programação Orientada a Objetos (POO) em Python.

As funções originais foram convertidas em classes para organizar melhor o código, utilizando Herança para definir diferentes tipos de Contas e Clientes.

 Menu de OperaçõesO sistema permite as seguintes ações:[d] Depositar[s] Sacar (Sujeito a limites diários e por transação)[e] Extrato (Visualiza saldo e histórico de movimentações)[nu] Novo Usuário (Cadastra um cliente Pessoa Física)[nc] Nova Conta (Cria uma Conta Corrente e vincula a um cliente)[lc] Listar Contas (Exibe todas as contas cadastradas)[q] Sair

 Estrutura do Projeto (Classes Principais)O sistema é construído sobre as seguintes classes principais:1.
 
 ClientesClasseDescriçãoRelaçãoClienteClasse base para todos os usuários. Gerencia suas contas e delega as transações.É pai de PessoaFisica.
 PessoaFisicaRepresenta o cliente com informações de registro (Nome, CPF, Data de Nascimento).

Herda de Cliente.2. ContasClasseDescriçãoRelaçãoContaClasse base que armazena o saldo, número da agência e histórico. Define as operações básicas.

É pai de ContaCorrente.ContaCorrenteImplementa as regras específicas do desafio: limite de R$ 500 por saque e máximo de 3 saques diários.Herda de Conta.
HistoricoResponsável por manter o registro detalhado de todas as operações (Deposito e Saque).Composição (Faz parte da Conta).

TransaçõesClasseDescriçãoRelaçãoTransacaoClasse Abstrata que define o padrão (interface) para todas as movimentações financeiras.
 É pai de Deposito e Saque.Deposito / SaqueImplementam a lógica específica de cada tipo de movimentação, registrando-a na conta e no histórico.Herdam de Transacao.

 ▶️ Como UsarSalve o código em um arquivo chamado sistema_bancario.py.Execute no terminal:Bashpython sistema_bancario.py

Siga as opções do menu para criar um novo usuário ([nu]) e uma nova conta ([nc]) antes de realizar depósitos ([d]) e saques ([s]).
