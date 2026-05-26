# ECommerce

**CRUD** com `FastAPI` e `MySQL`.

## Como executar

1. **Clone o repositório e acesse o repositório:**

   ```bash
   git clone https://github.com/Davi-1903/ECommerce-FastAPI.git
   cd ECommerce-FastAPI
   ```

2. **Crie um arquivo `.env` com as variáveis de ambiente:**

   ```.env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=db_ecommerce
   DB_USER=root
   DB_PASSWORD=<SENHA>
   ```

3. **Instale as dependências:**

   ```bash
   uv sync
   # ----------- ou -----------
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**

   ```bash
   uvicorn app:app --reload
   ```

> [!TIP]
> Use ambiente virtual 🙃
