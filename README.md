# 🧩 8-Puzzle Solver & Visualizer

Este projeto implementa e compara diferentes algoritmos de busca de Inteligência Artificial para resolver o clássico **8-Puzzle** (Jogo dos 8). O projeto inclui métricas de desempenho detalhadas e uma visualização gráfica da solução utilizando **Pygame**.

## 🚀 Funcionalidades

* **Algoritmos Implementados:**
  * **BFS (Breadth-First Search):** Busca em Largura (Garante o caminho ótimo, mas alto custo de memória).
  * **A* (A-Star):** Busca Informada (Garante o caminho ótimo com alta eficiência usando custo real + heurística).
  * **Busca Gulosa (Greedy Search):** Busca Informada (Extremamente rápida, mas não garante o caminho mais curto).

* **Heurísticas Disponíveis:**
  1.  **Misplaced Tiles:** Contagem de peças fora do lugar.
  2.  **Manhattan Distance:** Soma das distâncias verticais e horizontais de cada peça até o alvo (Recomendada).
  3.  **Euclidean Distance:** Distância geométrica em linha reta.

* **Visualização:** Animação passo a passo do tabuleiro resolvendo o puzzle.
* **Métricas:** Exibe tempo de execução, número de nós explorados e profundidade da solução.

## 🛠️ Pré-requisitos

Para executar este projeto, você precisará ter o **Python 3.x** instalado. Além disso, o projeto utiliza a biblioteca `pygame` para a visualização gráfica.

Instale a dependência com o comando:

```bash
pip install pygame
```
## 📊 Comparativo de Desempenho Real

Os testes abaixo foram realizados utilizando um cenário de complexidade média (Solução em 8 passos).

**Cenário de Teste:** Profundidade 8

| Algoritmo | Heurística | Tempo (s) | Nós Explorados | Caminho Encontrado |
| :--- | :--- | :--- | :--- | :--- |
| **Busca Gulosa** | Manhattan | **0.0007s** 🏆 | **9** 🏆 | 8 passos |
| **Busca Gulosa** | Misplaced | 0.0007s | 11 | 8 passos |
| **A* (A-Star)** | Manhattan | 0.0011s | 14 | 8 passos |
| **A* (A-Star)** | Misplaced | 0.0009s | 21 | 8 passos |
| **BFS** | N/A | 0.0061s | 197 | 8 passos |

### 📌 Análise dos Resultados

1.  **Eficiência:** A **Busca Gulosa com Manhattan** foi a vencedora absoluta neste cenário, explorando apenas 9 nós para chegar ao objetivo.
2.  **Custo da Força Bruta:** A **BFS** (Busca em Largura) precisou explorar **197 nós** para encontrar a mesma solução que a Gulosa encontrou com 9, demonstrando a ineficiência de buscas não informadas.
3.  **Qualidade da Heurística:** Comparando dentro do A*, a heurística **Manhattan** se mostrou superior à Misplaced, reduzindo a exploração de 21 para 14 nós.
