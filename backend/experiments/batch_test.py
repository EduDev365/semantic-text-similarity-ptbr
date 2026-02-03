from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer, util

def main():
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"

    # base do projeto (backend/)
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)

    output_file = DATA_DIR / "results_multilingual_batch.csv"

    pairs = [
        ("PARAFRASE_FORTE", "O gato dorme no sofá.", "O felino está dormindo no sofá."),
        ("PARAFRASE_FORTE", "A reunião foi cancelada por falta de participantes.", "O encontro foi cancelado porque ninguém apareceu."),
        ("PARAFRASE_FORTE", "Preciso enviar o relatório até amanhã.", "Tenho que mandar o relatório até o dia seguinte."),
        ("PARAFRASE_FORTE", "O sistema apresentou falhas após a atualização.", "Depois do update, o sistema começou a falhar."),
        ("PARAFRASE_FORTE", "Ela comprou um carro novo na semana passada.", "Na semana passada, ela adquiriu um automóvel novo."),

        ("PARAFRASE_MEDIA", "O aluno estudou bastante para a prova.", "O estudante se preparou muito para o exame."),
        ("PARAFRASE_MEDIA", "O aplicativo ficou lento depois da última versão.", "Após a última versão, o app passou a ter desempenho ruim."),
        ("PARAFRASE_MEDIA", "A empresa reduziu custos para aumentar o lucro.", "Para lucrar mais, a organização diminuiu despesas."),
        ("PARAFRASE_MEDIA", "O servidor caiu durante o pico de acesso.", "Em horário de maior tráfego, o servidor ficou fora do ar."),
        ("PARAFRASE_MEDIA", "O cliente solicitou mudanças no requisito.", "O usuário pediu alterações na especificação."),

        ("MESMO_TEMA", "Embeddings representam textos como vetores numéricos.", "Modelos de linguagem podem transformar frases em vetores."),
        ("MESMO_TEMA", "Cosine similarity mede o ângulo entre dois vetores.", "A similaridade do cosseno compara vetores pelo ângulo."),
        ("MESMO_TEMA", "Transformers melhoraram tarefas de NLP nos últimos anos.", "Arquiteturas baseadas em atenção revolucionaram o processamento de linguagem."),
        ("MESMO_TEMA", "Testes automatizados ajudam a evitar regressões.", "Escrever testes permite detectar erros após mudanças no código."),
        ("MESMO_TEMA", "Requisitos bem definidos reduzem retrabalho.", "Uma boa especificação de requisitos diminui mudanças futuras."),

        ("DIFERENTES", "Redes neurais são usadas para reconhecimento de padrões.", "O time ganhou o campeonato depois dos pênaltis."),
        ("DIFERENTES", "A análise de requisitos é essencial em projetos de software.", "A receita leva farinha, ovos e leite."),
        ("DIFERENTES", "O banco de dados relacional usa tabelas e chaves.", "A praia estava cheia no feriado."),
        ("DIFERENTES", "O algoritmo de busca encontra caminhos em grafos.", "Comprei uma bicicleta para passear no parque."),
        ("DIFERENTES", "A biblioteca pandas facilita análise de dados.", "Meu cachorro gosta de correr atrás da bola."),

        ("CONTRADITORIOS", "O projeto foi concluído antes do prazo.", "O projeto atrasou e não foi entregue no prazo."),
        ("CONTRADITORIOS", "O sistema está funcionando corretamente.", "O sistema está com problemas e falhando."),
        ("CONTRADITORIOS", "A internet está rápida hoje.", "A internet está muito lenta hoje."),
        ("CONTRADITORIOS", "O usuário aprovou a interface.", "O usuário rejeitou a interface."),
        ("CONTRADITORIOS", "A aplicação ficou mais rápida após otimização.", "A aplicação ficou mais lenta após a otimização."),
    ]

    print(f"Carregando modelo: {model_name}")
    model = SentenceTransformer(model_name)

    rows = []
    for idx, (categoria, a, b) in enumerate(pairs, start=1):
        emb_a = model.encode(a, convert_to_tensor=True)
        emb_b = model.encode(b, convert_to_tensor=True)
        score = util.cos_sim(emb_a, emb_b).item() * 100

        rows.append({
            "id": idx,
            "categoria": categoria,
            "texto_a": a,
            "texto_b": b,
            "similaridade_percent": round(score, 2),
        })

        print(f"[{idx:02d}] {categoria:<15} -> {score:.2f}%")

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding="utf-8")

    print("\n✅ Batch concluído!")
    print(f"Arquivo gerado: {output_file}")
    print(f"Média: {df['similaridade_percent'].mean():.2f}%")
    print(f"Mínimo: {df['similaridade_percent'].min():.2f}%")
    print(f"Máximo: {df['similaridade_percent'].max():.2f}%")

if __name__ == "__main__":
    main()
