# Dados
------------------------------------
### Encontro

*Reune os dados de cada observação* 

Cenário//Formigueiro//Formiga

-----------------------------------

### Cenário

*Representa cada um dos cenários*

- __ID__ - Identificador
- __Status__ - Ativo // Finalizado
- __Tempo de Execução__ - Tempo (ou iterações) que foi gasto do inicio até o estado atual (ou até finalizar)
- __Quantidade Total de Comida__ - Quantidade de comida presente no mapa (Fonte + Transito + Formigueiro)

-----------------------------------

### Formigueiro
*Representa cada um dos formigueiros*

- **ID** - Identificador
- <s>Probabilidade de Vencer - (quantidade de comida no formigueiro)/(quantidade de comida total)</s>
- **Quantidade de Comida** - Quantidade de comida que as formigas levaram até o formigueiro

-------------------------------------

### Formigas

*Representa cada uma das formigas*

- **ID** - Identificador
- **Status** - Carregando // Procurando
- **Quantidade de Comida Carregada** - Numero de unidades de comida levadas até o formigueiro.

___________________________________


# Calculos

- **Número total de Cenarios** -> contar num cenarios

- **Número total de Formigueiros** -> contar num formigueiros

- **Número total de Formigas** -> contar num formigas
	- **% Carregando** -> contar numero de formigas com status carregando
	- **% Procurando** -> contar numero de formigas com status procurando

- **Número total de comida** -> soma do "Quantidade total de comida" dos cenario
	- **% no formigueiro** -> Soma da 'Quantidade de comida' dos formigueiros
	- **% transito** -> contar numero de formigas que estão com status carregando
	- **% na fonte** -> 1 - %Formigueiro - %Transito

------------------------------------
- **Tempo médio de execução** -> media do "Tempo de execução" dos cenarios
- **Tempo mínimo** -> mímimo do 'TE' dos cenarios com status finalizado
- **Tempo máximo** -> máximo do 'TE' dos cenarios com status finalizado
- **Media de comida por formiga** -> media "Quantidade de comida carregada" das formigas
- **Maximo de comida por formiga** -> maximo 'Quantidade de comida carregada' das formigas
-----------------------------------

- **Escolher Cenário** -> filtrar por cenário

- **Num Formigueiro** -> Contar formigueiros
- **Num Formigas** -> Contar formigas
- **Num Comida** -> 'Quantidade Total de Comida' do Cenário
- **Duração** -> 'tempo de execução' do Cenário

- **Para cada formigueiro** -> filtrar por formigueiro
	- **Num formigas** -> Contar formigas
		- **% Carregando** -> contar com status
		- **% Procurando** -> contar com status
	- **Num Comida** -> Numero em transito + Numero no formigueiro
		- **% Em transito** -> contar formigas com estado carregando
		- **% Formigueiro** -> "Quantidade de comida" do Formigueiro
	- **Probabilidade** -> (Qtd de Comida Formigueiro)/(Qtd Total de Comida)


