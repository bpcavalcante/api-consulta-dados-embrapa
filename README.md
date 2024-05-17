# api-consulta-dados-embrapa

Projeto para entrega do Tech Challenge do primeiro módulo da Pós em Machine Learning Engineering

## Arquitetura do Projeto

![arquiteturatechchallenge](https://github.com/bpcavalcante/api-consulta-dados-embrapa/assets/69259703/992b1cf2-8cac-407f-bad6-cd38ba7a764a)

## Como executar o projeto

1. Inicialize e ative o ambiente virtual:

    ```bash
    python3 -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux
    source venv/bin/activate
    ```

2. Instale as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

3. Rode o código para realizar o web scraping:

    ```bash
    python3 src/scraper.py
    ```

4. Inicialize a API

    ```bash
    uvicorn src.main:app --reload
    ```
