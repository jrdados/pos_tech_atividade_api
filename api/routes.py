import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any, List

router = APIRouter(prefix="/api/v1")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "books.csv")

try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    df = None
    print("Erro ao carregar CSV:", e)


def _require_df() -> pd.DataFrame:
    if df is None:
        raise HTTPException(status_code=500, detail="CSV não carregado. Verifique data/books.csv")
    return df


@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Verifica se a API está no ar e se o CSV foi carregado com sucesso.",
)
def health() -> Dict[str, Any]:
    _require_df()
    return {"status": "ok"}


@router.get(
    "/books",
    tags=["Books"],
    summary="Listar livros",
    description=(
        "Lista livros com filtros opcionais por categoria, rating e preço máximo. "
        "Use `limit` para controlar o tamanho da resposta (evita travar o Swagger)."
    ),
)
def get_books(
    category: Optional[str] = None,
    rating: Optional[int] = None,
    max_price: Optional[float] = None,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    data = _require_df()
    filtered = data.copy()

    if category:
        filtered = filtered[filtered["category"] == category]

    if rating is not None:
        filtered = filtered[filtered["rating"] == rating]

    if max_price is not None:
        filtered = filtered[filtered["price"] <= max_price]

    return filtered.head(limit).to_dict(orient="records")


@router.get(
    "/stats/overview",
    tags=["Stats"],
    summary="Estatísticas gerais",
    description="Retorna total de livros, preço médio e distribuição de ratings da coleção.",
)
def stats_overview() -> Dict[str, Any]:
    data = _require_df()

    total_books = int(len(data))
    avg_price = float(data["price"].mean())

    rating_counts = data["rating"].value_counts(dropna=False).sort_index().to_dict()
    # Se existir NaN, vira -1 (opcional; útil pra debug)
    rating_distribution = {int(k) if pd.notna(k) else -1: int(v) for k, v in rating_counts.items()}

    return {
        "total_books": total_books,
        "avg_price": avg_price,
        "rating_distribution": rating_distribution,
    }


@router.get(
    "/stats/categories",
    tags=["Stats"],
    summary="Estatísticas por categoria",
    description="Retorna quantidade e estatísticas de preço (média, mínimo, máximo) para cada categoria.",
)
def stats_categories() -> List[Dict[str, Any]]:
    data = _require_df()

    grouped = (
        data.groupby("category")
        .agg(
            total_books=("title", "count"),
            avg_price=("price", "mean"),
            min_price=("price", "min"),
            max_price=("price", "max"),
        )
        .reset_index()
        .sort_values("total_books", ascending=False)
    )

    result: List[Dict[str, Any]] = []
    for _, row in grouped.iterrows():
        result.append(
            {
                "category": str(row["category"]),
                "total_books": int(row["total_books"]),
                "avg_price": float(row["avg_price"]),
                "min_price": float(row["min_price"]),
                "max_price": float(row["max_price"]),
            }
        )

    return result


@router.get(
    "/books/top-rated",
    tags=["Books"],
    summary="Top-rated",
    description="Lista livros com maior rating. Em caso de empate, ordena por preço (mais barato primeiro).",
)
def top_rated(limit: int = 20) -> List[Dict[str, Any]]:
    data = _require_df()

    filtered = data.sort_values(["rating", "price"], ascending=[False, True]).head(limit)
    return filtered.to_dict(orient="records")


@router.get(
    "/books/price-range",
    tags=["Books"],
    summary="Filtrar por faixa de preço",
    description=(
        "Filtra livros dentro de uma faixa de preço específica usando `min` e `max`. "
        "Inclui filtros bônus opcionais por categoria e rating."
    ),
)
def books_price_range(
    min: float,
    max: float,
    category: Optional[str] = None,
    rating: Optional[int] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    data = _require_df()

    filtered = data[(data["price"] >= min) & (data["price"] <= max)]

    if category:
        filtered = filtered[filtered["category"] == category]

    if rating is not None:
        filtered = filtered[filtered["rating"] == rating]

    filtered = filtered.sort_values("price", ascending=True).head(limit)
    return filtered.to_dict(orient="records")
