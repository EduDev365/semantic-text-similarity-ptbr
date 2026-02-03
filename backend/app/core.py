from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sentence_transformers import SentenceTransformer, util


@dataclass(frozen=True)
class AppPaths:
    base_dir: Path
    data_dir: Path
    reports_dir: Path
    history_csv: Path
    batch_csv: Path


def get_paths() -> AppPaths:
    # base_dir = backend/
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    reports_dir = base_dir / "reports"

    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    return AppPaths(
        base_dir=base_dir,
        data_dir=data_dir,
        reports_dir=reports_dir,
        history_csv=data_dir / "history.csv",
        batch_csv=data_dir / "results_multilingual_batch.csv",
    )


MODELS: Dict[str, str] = {
    "Multilingual (final)": "paraphrase-multilingual-MiniLM-L12-v2",
    "Baseline (comparação)": "all-MiniLM-L6-v2",
}


def load_model(model_label: str) -> SentenceTransformer:
    model_name = MODELS[model_label]
    return SentenceTransformer(model_name)


def cosine_similarity(model: SentenceTransformer, text_a: str, text_b: str) -> float:
    emb_a = model.encode(text_a, convert_to_tensor=True)
    emb_b = model.encode(text_b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())


def classify(score: float) -> str:

    if score >= 0.70:
        return "alta"
    elif score >= 0.50:
        return "moderada"
    elif score >= 0.30:
        return "baixa-moderada"
    else:
        return "baixa"


def append_history(
    paths: AppPaths,
    model_label: str,
    text_a: str,
    text_b: str,
    score: float,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = [
        "timestamp",
        "model_label",
        "model_name",
        "text_a",
        "text_b",
        "similarity",
        "percent",
        "classificacao",
    ]
    row = [
        now,
        model_label,
        MODELS[model_label],
        text_a,
        text_b,
        f"{score:.6f}",
        f"{score * 100:.2f}",
        classify(score),
    ]

    file_exists = paths.history_csv.exists()
    with open(paths.history_csv, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(header)
        w.writerow(row)


def read_history(paths: AppPaths) -> pd.DataFrame:
    if not paths.history_csv.exists():
        return pd.DataFrame(
            columns=[
                "timestamp",
                "model_label",
                "model_name",
                "text_a",
                "text_b",
                "similarity",
                "percent",
                "classificacao",
            ]
        )
    df = pd.read_csv(paths.history_csv)
    # garantir tipos
    if "similarity" in df.columns:
        df["similarity"] = pd.to_numeric(df["similarity"], errors="coerce")
    if "percent" in df.columns:
        df["percent"] = pd.to_numeric(df["percent"], errors="coerce")
    return df


def reports_available(paths: AppPaths) -> Dict[str, Path]:
    # mostra o que existir
    wanted = {
        "Boxplot (batch)": paths.reports_dir / "boxplot_batch.png",
        "Boxplot por categoria": paths.reports_dir / "boxplot_categoria.png",
        "Scatter (batch)": paths.reports_dir / "scatter_batch.png",
        "Boxplot (baseline vs multi)": paths.reports_dir / "boxplot.png",
        "Scatter (baseline vs multi)": paths.reports_dir / "scatter.png",
    }
    return {k: v for k, v in wanted.items() if v.exists()}


def load_batch(paths: AppPaths) -> Tuple[pd.DataFrame, str]:
    if not paths.batch_csv.exists():
        return pd.DataFrame(), f"Não encontrei o arquivo {paths.batch_csv.name} em data/."
    df = pd.read_csv(paths.batch_csv)
    if "similaridade_percent" in df.columns:
        df["similaridade_percent"] = pd.to_numeric(df["similaridade_percent"], errors="coerce")
    return df, ""
