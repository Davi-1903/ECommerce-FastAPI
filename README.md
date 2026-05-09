# ECommerce

**CRUD** com `FastAPI` e `MySQL`.

## Como executar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Davi-1903/ECommerce-FastAPI.git
   ```

2. **Acesse o diretório do projeto:**

   ```bash
   cd ECommerce-FastAPI
   ```

3. **Crie um arquivo `.env` com as variáveis de ambiente:**

   ```env
   DATABASE_URI=mysql+pymysql://root:<SENHA>@localhost:<PORTA>/db_ecommerce
   ```

4. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Execute a aplicação:**

   ```bash
   uvicorn main:app --reload
   ```

> [!TIP]
> Use ambiente virtual 🙃
