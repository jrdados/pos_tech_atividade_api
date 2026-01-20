# Tech Challenge – Books to Scrape API

Projeto desenvolvido para o Tech Challenge da Pós Tech – FIAP, com foco em Machine Learning Engineering. O objetivo é construir um pipeline completo de dados, desde a extração via web scraping até a disponibilização dos dados por meio de uma API REST, pronta para consumo por aplicações e modelos de Machine Learning.

## Objetivo do Projeto
- Realizar web scraping do site https://books.toscrape.com/
- Extrair, tratar e estruturar dados de livros
- Persistir os dados em formato CSV
- Disponibilizar os dados através de uma API pública
- Fornecer endpoints de consulta e insights
- Documentar a API automaticamente com Swagger

## Arquitetura
Pipeline implementado:
Web Scraping → Processamento → CSV → API FastAPI → Consumo

Descrição das etapas:
- Ingestão: coleta de dados via scraping
- Processamento: limpeza, normalização e estruturação
- Persistência: armazenamento em arquivo CSV
- Serviço: API REST para consulta e estatísticas
- Consumo: aplicações, análises e modelos de ML

## Estrutura do Projeto
pos_tech_atividade_api/
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── lib/
│   ├── scraper.py
│   └── parser.py
├── include/
│   └── constants.py
├── scripts/
│   └── run_scraping.py
├── data/
│   └── books.csv
├── venv/
├── requirements.txt
└── README.md

## Web Scraping
O processo de scraping coleta todos os livros disponíveis no site books.toscrape.com, extraindo:
- Título
- Preço
- Rating
- Disponibilidade
- Categoria
- URL da imagem
- URL do livro

Execução do scraping (com o venv ativo):
python scripts/run_scraping.py

O arquivo books.csv será gerado na pasta data/.

## API REST (FastAPI)
A API foi desenvolvida utilizando FastAPI, com documentação automática via Swagger.

Tecnologias:
- Python
- FastAPI
- Uvicorn
- Pandas

## Como Executar a API
1. Ativar o ambiente virtual:
venv\Scripts\activate
2. Subir a API:
uvicorn api.main:app --reload
3. Acessar a documentação:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

Health Check
GET /api/v1/health
Verifica se a API está ativa e se o CSV foi carregado corretamente.

Listagem de Livros
GET /api/v1/books
Parâmetros:
- category (opcional)
- rating (opcional)
- max_price (opcional)
- limit (opcional, padrão = 20)
Exemplos:
- /api/v1/books?limit=5
- /api/v1/books?category=Poetry&limit=10
- /api/v1/books?rating=5

Estatísticas Gerais
GET /api/v1/stats/overview
Retorna total de livros, preço médio e distribuição de ratings.

Estatísticas por Categoria
GET /api/v1/stats/categories
Retorna quantidade de livros por categoria e estatísticas de preço (médio, mínimo e máximo).

Livros Mais Bem Avaliados
GET /api/v1/books/top-rated
Parâmetros:
- limit (opcional)
Exemplo:
- /api/v1/books/top-rated?limit=10

Filtro por Faixa de Preço
GET /api/v1/books/price-range
Parâmetros:
- min (obrigatório)
- max (obrigatório)
- category (opcional)
- rating (opcional)
- limit (opcional)
Exemplo:
- /api/v1/books/price-range?min=10&max=20&limit=5

## Documentação Automática (Swagger)
A API possui documentação automática gerada pelo FastAPI, acessível em /docs (Swagger UI) e /redoc (ReDoc). A documentação permite visualizar e testar todos os endpoints diretamente no navegador.

## Boas Práticas Implementadas
- Código modular e organizado
- Separação clara entre scraping, processamento e API
- Uso de ambiente virtual
- Health check para monitoramento
- Limitação de payload para performance
- Endpoints de insights
- Documentação automática
- Estrutura preparada para integração com Machine Learning

## Possíveis Evoluções
- Deploy em nuvem (Render, Fly.io, Heroku)
- Persistência em banco de dados
- Autenticação e autorização
- Paginação e ordenação avançadas
- Cache de respostas
- Integração com modelos de ML
- Monitoramento e métricas

## Autor
Projeto desenvolvido para o Tech Challenge – Pós Tech FIAP
Aluno: Anderson Carneiro

