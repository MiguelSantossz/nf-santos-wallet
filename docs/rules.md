NF SANTOS WALLET V2 - ESCOPO E REGRAS

FUNCIONALIDADES DO MVP:
- Registro de usuário
- Login de usuário
- Mostrar saldo em USD
- Depósito em USD
- Saque em USD
- Transferência em USD entre contas
- Histórico de transações
- Compra e venda de ações
- Mostrar ações compradas, quantidade, preço médio, valor investido, valor atual e percentual de valorização/desvalorização
- Mostrar patrimônio total líquido do usuário (saldo em caixa + valor atual das ações)

FORA DO ESCOPO DESTA VERSÃO:
- Transferência de ações entre contas
- Cálculo de impostos sobre ações
- Cálculo de dividendos
- Cálculo de juros
- Persistência em banco externo, API REST e Docker (ficam para etapas posteriores)

--------------------------------------------------
REGRAS DE NEGÓCIO E INVARIANTES
--------------------------------------------------

1. REGISTRO:
- Nome:
  * Mínimo de 2 caracteres e máximo de 32 caracteres.
  * Aceita letras (incluindo acentos) e espaços simples entre palavras; não aceita números ou símbolos.
- Username:
  * Mínimo de 4 caracteres e máximo de 16 caracteres.
  * Aceita apenas letras (incluindo acentos), números e underline (_).
  * Case-insensitive (ex.: "Miguel" e "MIGUEL" representam o mesmo username; normalizado em minúsculas para comparação/unicidade).
  * Não pode já existir no sistema.
- Senha:
  * Mínimo de 8 caracteres e máximo de 16 caracteres.
  * Deve conter pelo menos 1 letra maiúscula, 1 letra minúscula, 1 número e 1 símbolo.
  * Deve ser armazenada apenas como hash (nunca em texto puro).
- Atomicidade:
  * Se qualquer validação ou etapa do registro falhar, o processo é inteiramente cancelado e nenhum usuário é criado.

2. LOGIN:
- O usuário deve existir.
- A senha informada deve coincidir com o hash salvo no usuário.
- Se houver mais de 3 tentativas inválidas consecutivas para o mesmo usuário, o login fica bloqueado por 30 segundos.
- Durante o período de bloqueio, tentativas não são validadas e o sistema informa que a conta está temporariamente bloqueada.
- Quando um login é bem-sucedido, o contador de falhas consecutivas desse usuário é zerado.

3. MOSTRAR SALDO:
- Exibe o saldo atual em caixa do usuário em USD, formatado com 2 casas decimais.

4. DEPÓSITO:
- Valor deve ser informado/convertido como Decimal (nunca float).
- Valor deve ser maior que 0 (não pode ser 0 nem negativo).
- Máximo de 2 casas decimais.
- Atualiza o saldo para: saldo_anterior + valor_deposito.
- Registra o saldo após a operação e adiciona uma transação de depósito ao histórico (com data/hora em UTC e valor em USD).
- Se qualquer validação falhar, a operação é cancelada sem alterar saldo ou histórico.

5. SAQUE:
- Valor deve ser informado/convertido como Decimal (nunca float).
- Valor deve ser maior que 0 (não pode ser 0 nem negativo).
- Máximo de 2 casas decimais.
- Valor deve ser menor ou igual ao saldo disponível na carteira.
- Atualiza o saldo para: saldo_anterior - valor_saque.
- Registra o saldo após a operação e adiciona uma transação de saque ao histórico (com data/hora em UTC e valor em USD).
- Se qualquer validação falhar, a operação é cancelada sem alterar saldo ou histórico.

6. TRANSFERÊNCIA:
- Valor deve ser informado/convertido como Decimal (nunca float).
- Valor deve ser maior que 0 (não pode ser 0 nem negativo).
- Máximo de 2 casas decimais.
- Carteira de origem e carteira de destino devem existir.
- Remetente e destinatário não podem ser o mesmo usuário.
- Ambas as contas devem estar aptas para movimentação e o remetente deve ter saldo suficiente.
- Execução atômica: ou a transferência inteira ocorre, ou nada é alterado:
  * Debita o valor do remetente e registra o saldo após.
  * Credita o valor no destinatário e registra o saldo após.
  * Registra uma transação de saída no histórico do remetente e uma transação de entrada no histórico do destinatário (ambas com data/hora em UTC e valor em USD).

7. HISTÓRICO DE TRANSAÇÕES:
- Lista todas as transações da conta em ordem cronológica (ou conforme definido na exibição).
- Cada registro deve conter tipo da operação, valor formatado em USD, data e hora em UTC e saldo após a operação (quando aplicável).
- Deve incluir depósitos, saques, transferências, compras e vendas de ações.

8. AÇÕES (COMPRA, VENDA E PORTFÓLIO):
- O ativo/ação deve existir e possuir cotação válida em USD (via Decimal).
- Compra:
  * O usuário informa a quantidade de ações a comprar (valor positivo, com regra clara de casas decimais/inteiras).
  * Custo total = quantidade * preco_atual_acao.
  * O usuário deve ter saldo suficiente para cobrir o custo total.
  * Debita o custo total do saldo, registra o saldo após e adiciona a transação de compra ao histórico (com data/hora em UTC, ativo, quantidade e valor em USD).
  * Se o usuário já possuir posição naquela ação, soma a quantidade e atualiza o preço médio:
    preco_medio = ((qtd_anterior * preco_medio_anterior) + (qtd_comprada * preco_compra)) / (qtd_anterior + qtd_comprada).
  * Se não possuir posição, cria uma nova posição com a quantidade comprada, preço médio e data/hora da compra.
- Venda:
  * O usuário deve possuir a ação e ter quantidade suficiente disponível na posição (permite venda parcial ou total).
  * Valor da venda é calculado pelo preço atual da ação no mercado: valor_venda = quantidade_vendida * preco_atual_acao.