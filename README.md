# 🎬 Letterboxd Movie Analytics: ETL e DataViz

## 📊 Visão Geral do Projeto

Este projeto demonstra o ciclo completo de *Data Analytics*, desde a extração de dados brutos até a criação de um dashboard interativo no Power BI. O objetivo é analisar o consumo cinematográfico pessoal, enriquecendo dados da plataforma Letterboxd com informações detalhadas da API do TMDB (The Movie Database).

### Tecnologias Utilizadas

| Categoria | Tecnologia | Uso no Projeto |
| :--- | :--- | :--- |
| **Linguagem** | Python | Script para ETL (Extração, Transformação e Carga). |
| **Bibliotecas** | Pandas, `tmdbsimple`, `python-dotenv`, `tqdm` | Manipulação de dados, conexão com API, gerenciamento seguro de chaves e barras de progresso. |
| **Visualização** | Power BI | Criação do dashboard interativo e cálculo de métricas (DAX). |
| **Fonte de Dados** | Letterboxd (.csv) e TMDB (API) | Dados de entrada (watched/watchlist) e enriquecimento de metadados (gênero, bilheteria, elenco). |

-----

## ✨ Análise e Visualização

O dashboard no Power BI Desktop fornece *insights* sobre as tendências e preferências pessoais de consumo de filmes.

**[(https://app.powerbi.com/view?r=eyJrIjoiYjVkNWIxYmQtZWUxMC00MThlLTg2MzctODc0MmQ4OGNmMTJkIiwidCI6ImUyOTgzNTliLTliNTQtNDVjMC05YmI3LTY5MDkxM2IzNGNmOCJ9&pageName=6eecf3dadab2641d77a8)]**
*(Clique para interagir com o dashboard publicado na web)*

### Principais Análises e Métricas:

  * **Tendência de Notas:** Comparação da minha Nota Pessoal vs. Nota Média da Comunidade (TMDB).
  * **Análise de Gênero e País:** Visualização dos gêneros mais assistidos e mapa interativo das origens de produção dos filmes.
  * **Análise de Elenco/Direção:** Classificação dos atores e diretores mais frequentes na lista.
  * **Métricas Financeiras:** Cálculo do **Lucro Total** (Bilheteria - Orçamento) por título, utilizando métricas DAX.
  * **Usabilidade:** Implementação de Tooltips de Página dinâmicas para exibir informações e o pôster do filme ao passar o mouse.

-----

## ⚙️ Guia de Uso (ETL com Python)

Este guia explica como executar o script Python para enriquecer seus próprios dados do Letterboxd.

### 1\. Pré-requisitos

Você precisa ter o **Python (3.x)** e as seguintes bibliotecas instaladas:

```bash
pip install pandas tmdbsimple tqdm python-dotenv
```

### 2\. Configuração da API Key (Segurança)

Por segurança, este projeto utiliza variáveis de ambiente para a chave da API do TMDB.

1.  Obtenha sua chave da API do TMDB [(https://www.themoviedb.org/settings/api)].

2.  Crie um arquivo chamado `.env` na mesma pasta do script Python.

3.  Dentro do arquivo `.env`, adicione sua chave no seguinte formato:

    ```env
    # Arquivo .env
    TMDB_API_KEY=SUA_CHAVE_DE_32_CARACTERES
    ```

### 3\. Obtenção dos Dados do Letterboxd

1.  Exporte seus dados do Letterboxd (Configurações \> Exportar Dados).
2.  Descompacte o arquivo e coloque os arquivos **`watched.csv`** e **`watchlist.csv`**  na mesma pasta do script.

### 4\. Execução do Script

Execute o script principal no seu terminal:

```bash
python enriquecimento_letterboxd_tmdb.py
```

O script irá:

1.  Ler o `watched.csv` e `watchlist.csv`.
2.  Fazer requisições ao TMDB (com pausas para respeitar o limite da API).
3.  Gerar dois novos arquivos: **`watched_enriquecido.csv`** e **`watchlist_enriquecida.csv`**.

### 5\. Importação no Power BI

Os arquivos enriquecidos estarão prontos para serem importados no Power BI Desktop. Utilize o Power Query para fazer o *Append* (Anexar) das duas tabelas, criando uma tabela principal para a análise.

-----

## 🤝 Contribuições

Sinta-se à vontade para fazer *fork* e adaptar este projeto para suas próprias análises\! Sugestões e *pull requests* são bem-vindas.

-----

## **Desenvolvido por: [Marco Túlio Ribeiro]**