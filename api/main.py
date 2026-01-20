from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Books to Scrape - Public API",
    version="1.0.0",
    description=(
        "API pública para consulta e insights de livros extraídos do site books.toscrape.com.\n\n"
        "Inclui:\n"
        "- Listagem e filtros de livros\n"
        "- Health check\n"
        "- Estatísticas gerais e por categoria\n"
        "- Top-rated e filtro por faixa de preço\n"
    ),
)

app.include_router(router)


