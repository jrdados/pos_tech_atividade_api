from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes import router

app = FastAPI(
    title="Books to Scrape - Public API",
    version="1.0.0",
    description="API pública para consulta e insights de livros extraídos do books.toscrape.com.",
)

app.include_router(router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
