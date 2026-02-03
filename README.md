# Semantic Text Similarity (PT-BR)

A lightweight NLP system for measuring semantic similarity between Portuguese texts using sentence embeddings and cosine similarity.  
Includes a Streamlit web interface and CLI support.

---

## Descrição (Português)

Um sistema leve de NLP para medir a similaridade semântica entre textos em português usando embeddings de sentenças e similaridade do cosseno, com interface web em Streamlit e suporte via linha de comando.

---

## Features

- Semantic similarity with embeddings + cosine similarity
- Fixed multilingual model (PT-BR oriented)
- Streamlit interface with private session history
- CSV export and session analytics
- Command-line interface (CLI)
- Experimental and reporting scripts

---

## Estrutura do Projeto


backend/
  app/         # Aplicação Streamlit
  cli/         # Scripts CLI
  core.py      # Funções centrais
  data/        # Arquivos CSV
  experiments/ # Scripts experimentais
  reports/     # Gráficos e relatórios

  
Como Executar Localmente
1) Criar ambiente virtual
python -m venv .venv
Ativar:

Windows

.\.venv\Scripts\Activate.ps1
Linux/macOS

source .venv/bin/activate
2) Instalar dependências
pip install -r requirements.txt
3) Rodar o sistema
streamlit run backend/app/Home.py
Uso via Terminal (CLI)
python backend/cli/main.py
Os resultados são salvos em backend/data/.

Classificação de Similaridade
Alta: ≥ 0.70

Moderada: ≥ 0.50

Baixa-Moderada: ≥ 0.30

Baixa: < 0.30

Contexto Acadêmico
Projeto desenvolvido como Trabalho de Conclusão de Curso em Engenharia de Software.

Licença
MIT License.