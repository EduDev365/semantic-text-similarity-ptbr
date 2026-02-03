# Semantic Text Similarity (PT-BR)

A lightweight NLP system for measuring semantic similarity between Portuguese texts using sentence embeddings and cosine similarity.  
Includes a Streamlit web interface and CLI support.

---

## Descrição (Português)

Um sistema leve de NLP para medir a similaridade semântica entre textos em português usando embeddings de sentenças e similaridade do cosseno.  
Inclui uma interface web em Streamlit e suporte via linha de comando (CLI).

O sistema é capaz de identificar similaridade semântica mesmo quando os textos não são literalmente iguais.

---

## Features

- Semantic similarity using embeddings and cosine similarity  
- Multilingual pre-trained model with good performance for PT-BR  
- Streamlit interface with:
  - text comparison
  - private session history
  - CSV export
  - session analytics
- Command-line interface (CLI)
- Experimental scripts and reports for academic reproducibility

---

## Funcionalidades (Português)

- Similaridade semântica usando embeddings e similaridade do cosseno  
- Modelo multilíngue pré-treinado com bom desempenho em PT-BR  
- Interface Streamlit com:
  - comparação de textos
  - histórico privado por sessão
  - exportação em CSV
  - análises estatísticas da sessão
- Interface via linha de comando (CLI)
- Scripts experimentais e relatórios para reprodutibilidade acadêmica

---

## Note on Contradictory Texts

Texts with opposite meanings may present moderate similarity scores, as they share similar semantic contexts.

For example, sentences about the same topic with different opinions may generate close embeddings.

---

## Observação sobre Textos Contraditórios

Textos com significados opostos podem apresentar similaridade moderada, pois compartilham contexto semântico semelhante.

Por exemplo, frases sobre o mesmo tema, mesmo com opiniões diferentes, tendem a gerar embeddings próximos.

---

## Project Structure

```txt
backend/
  app/           # Streamlit application
  cli/           # Command-line scripts
  core.py        # Core functions (model, similarity, classification)
  data/          # CSV files
  experiments/   # Experimental scripts
  reports/       # Plots and reports
```

---

## Estrutura do Projeto (Português)

```txt
backend/
  app/           # Aplicação Streamlit
  cli/           # Scripts de linha de comando
  core.py        # Funções centrais (modelo, similaridade, classificação)
  data/          # Arquivos CSV
  experiments/   # Scripts experimentais
  reports/       # Gráficos e relatórios
```

---

## Requirements

- Python 3.10+ (recommended)
- Dependencies are listed in `requirements.txt`

---

## Requisitos (Português)

- Python 3.10+ (recomendado)
- Dependências listadas em `requirements.txt`

---

## Run Locally (Streamlit)

### 1) Create a virtual environment

```bash
python -m venv .venv
```

### 2) Activate the environment

**Windows (PowerShell)**

```bash
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Start the application

```bash
streamlit run backend/app/Home.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

---

## Execução Local (Português)

### 1) Criar ambiente virtual

```bash
python -m venv .venv
```

### 2) Ativar o ambiente

**Windows**

```bash
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Executar o sistema

```bash
streamlit run backend/app/Home.py
```

Abra o endereço exibido no terminal (geralmente http://localhost:8501).

---

## CLI Usage

Run the CLI script to generate results in CSV format:

```bash
python backend/cli/main.py
```

Outputs are saved under `backend/data/`.

---

## Uso via Terminal (Português)

Execute o script CLI para gerar resultados em CSV:

```bash
python backend/cli/main.py
```

Os resultados são salvos em `backend/data/`.

---

## Similarity Classes

| Class         | Score |
|---------------|--------|
| High          | ≥ 0.70 |
| Moderate      | ≥ 0.50 |
| Low-Moderate  | ≥ 0.30 |
| Low           | < 0.30 |

---

## Classificação de Similaridade (Português)

| Classe         | Score |
|----------------|--------|
| Alta           | ≥ 0.70 |
| Moderada       | ≥ 0.50 |
| Baixa-Moderada | ≥ 0.30 |
| Baixa          | < 0.30 |

---

## Academic Context

This repository is part of an undergraduate thesis in Software Engineering focused on semantic text similarity for PT-BR.

---

## Contexto Acadêmico (Português)

Este repositório faz parte de um Trabalho de Conclusão de Curso em Engenharia de Software, com foco em similaridade semântica para textos em português.

---

## License

MIT License.
