# API Consulta Dados Embrapa

Projeto para entrega do Tech Challenge do primeiro módulo da Pós em Machine Learning Engineering.

## Arquitetura do Projeto

![Arquitetura do Projeto](arquiteturatechchallenge.png)

## Como Executar o Projeto

### 1. Inicialize e Ative o Ambiente Virtual

    ```bash
    python3 -m venv venv
    # Para Windows
    venv\Scripts\activate
    # Para Linux
    source venv/bin/activate
    ```

### 2. Instale as Dependências do Projeto

    ```bash
    pip install -r requirements.txt
    ```

### 3. Gere as Chaves Assimétricas

Para a autenticação usando JWT com chaves assimétricas, você precisa gerar um par de chaves RSA (privada e pública). Use os comandos abaixo:

    ```bash
    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in private_key.pem -out public_key.pem
    ```

### 4. Testar se as Chaves Estão Funcionando

Certifique-se de que os arquivos `private_key.pem` e `public_key.pem` estão no diretório `src` onde seus arquivos de código estão localizados. Você pode adicionar uma pequena função de teste no seu código para verificar se as chaves estão sendo carregadas corretamente.

### 5. Rode o Código para Realizar o Web Scraping

    ```bash
    python3 src/scraper.py
    ```

### 6. Inicialize a API

    ```bash
    uvicorn src.main:app --reload
    ```

### 7. Testando a API com Postman

#### Gerar um Token JWT:

1. Abra o Postman.
2. Crie uma nova requisição HTTP.
3. Configure a requisição:
   - Método: `POST`
   - URL: `http://127.0.0.1:8000/token`
   - Adicione um cabeçalho (Header):
     - Key: `accept`
     - Value: `application/json`
4. Envie a requisição.
5. Você deve receber uma resposta com um token JWT, semelhante a:
   ```json
   {
     "access_token": "SEU_TOKEN_JWT_GERADO",
     "token_type": "bearer"
   }
   ```
6. Copie o valor de `access_token`.

#### Usar o Token para Acessar um Endpoint Protegido:

1. Crie uma nova requisição HTTP no Postman.
2. Configure a requisição:
   - Método: `GET`
   - URL: `http://127.0.0.1:8000/api/productions`
   - Adicione os cabeçalhos (Headers):
     - Key: `accept`
     - Value: `application/json`
     - Key: `Authorization`
     - Value: `Bearer SEU_TOKEN_JWT_GERADO`
       - Substitua `SEU_TOKEN_JWT_GERADO` pelo token que você copiou anteriormente.

3. Envie a requisição.

4. Você deve receber uma resposta semelhante a:

   ```json
   {
     "message": "Hello user"
   }
   ```
