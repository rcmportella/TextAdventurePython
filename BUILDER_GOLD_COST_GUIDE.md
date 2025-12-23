# Como Usar Gold Cost no Adventure Builder

## Visão Geral

O Adventure Builder agora suporta a definição de **custo de ouro** (gold cost) para nodes! Isso permite criar situações onde o jogador precisa pagar ouro para entrar em determinados locais.

## Como Adicionar Gold Cost

### Ao Criar um Novo Node

Quando você criar um novo node, após adicionar monstros, tesouros e armadilhas, o builder perguntará:

```
Add gold cost to enter this node? (y/n):
```

Se você responder `y`, poderá definir o custo:

```
--- Set Gold Cost ---
This is the amount of gold that will be deducted when the player enters this node.
Useful for: tolls, shop purchases, bribes, entry fees, etc.
Gold cost [0]: 30
✓ Gold cost set to 30 gp
```

### Ao Editar um Node Existente

1. No menu principal, escolha `3. Edit Current Adventure`
2. Escolha `2. Edit Node`
3. Selecione o node que deseja editar
4. No menu de edição, escolha `7. Gold cost`

Você verá as opções:
```
Current gold cost: 0
1. Set gold cost
2. Remove gold cost
Choice:
```

- **Opção 1**: Define ou altera o custo de ouro
- **Opção 2**: Remove o custo de ouro (volta para 0)

## Exemplo Prático

### Cenário: Ponte com Pedágio

Vamos criar um node onde o jogador precisa pagar 30 moedas de ouro para atravessar uma ponte:

1. **Criar o node:**
   ```
   Node ID: toll_bridge
   Title: A Ponte do Troll
   Description: Um enorme troll bloqueia a ponte. "30 moedas de ouro para passar!" ele exige.
   ```

2. **Quando perguntado sobre gold cost:**
   ```
   Add gold cost to enter this node? (y/n): y
   Gold cost [0]: 30
   ✓ Gold cost set to 30 gp
   ```

3. **Adicionar choices:**
   ```
   Choice text: Atravessar a ponte
   Target node ID: other_side
   ```

### O Que Acontece no Jogo

Quando o jogador escolher atravessar a ponte:
- 30 moedas de ouro serão automaticamente deduzidas
- Uma mensagem aparecerá: "You pay 30 gold to enter. (Remaining: X gp)"
- Se o jogador não tiver ouro suficiente, verá: "WARNING: You don't have enough gold! (X/30 gp needed)"
- O jogador pode continuar mesmo sem ouro suficiente (você pode adicionar requirements para impedir isso)

## Ideias de Uso

### 1. Loja
```
Node: merchant_shop_purchase
Title: Comprar Espada Mágica
Description: O mercador aceita sua oferta. Você compra a espada mágica!
Gold cost: 100
Treasure: ["Magic Sword +1"]
```

### 2. Suborno
```
Node: bribe_guards
Title: Subornar os Guardas
Description: Você oferece ouro aos guardas. Eles aceitam e deixam você passar.
Gold cost: 50
```

### 3. Entrada em Local Exclusivo
```
Node: noble_district
Title: Distrito Nobre
Description: Você paga a taxa de entrada no distrito nobre da cidade.
Gold cost: 25
```

### 4. Serviço de Transporte
```
Node: ferry_ride
Title: Travessia de Balsa
Description: O barqueiro o leva para o outro lado do rio.
Gold cost: 10
```

## Combinando com Tesouros

Certifique-se de que o jogador possa encontrar ouro antes de chegar aos nodes com custo! Adicione tesouros com ouro:

```
Treasure: ["50 gold pieces", "Potion of Healing"]
```

Quando o jogador coletar este tesouro, receberá automaticamente o ouro e poderá usá-lo para pagar pedágios e compras.

## Visualizando Gold Cost

No menu `4. View Adventure Structure`, você verá o gold_cost de cada node listado na estrutura, facilitando o planejamento e balanceamento da sua aventura.

## Dicas

1. **Balanceamento**: Certifique-se de que o jogador possa ganhar ouro suficiente para pagar os custos necessários
2. **Opções alternativas**: Considere oferecer caminhos alternativos para jogadores sem ouro
3. **Avisos antecipados**: Mencione os custos na descrição de nodes anteriores
4. **Valores realistas**: Use valores que façam sentido para a economia da sua aventura

## Exemplo Completo

Veja o arquivo `adventures/toll_bridge_example.json` para uma aventura completa demonstrando o sistema de gold cost em ação!

---

**Aproveite o novo sistema de ouro para criar aventuras mais ricas e com mais opções estratégicas para os jogadores!** 💰
