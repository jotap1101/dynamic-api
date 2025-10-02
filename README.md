# Dynamic API - API REST Universal com Django

Uma API REST em Django que fornece um **endpoint universal** para operações CRUD em múltiplos bancos de dados e modelos. A inovação principal é o roteamento baseado em parâmetros de consulta: `/api/v1/?db=db1&table=product` acessa dinamicamente qualquer modelo em qualquer banco de dados sem endpoints codificados.

## Arquitetura

### Estrutura de Bancos de Dados

```
├── default db (db.sqlite3) - Tabelas Django auth/admin + modelo User customizado
├── db1 (db1.sqlite3) - Products & Categories (domínio e-commerce)
├── db2 (db2.sqlite3) - Animals, Species & Breeds (domínio veterinário)
└── db3 (db3.sqlite3) - Movies & Genres (domínio entretenimento)
```

### Principais Características

- **Endpoint Universal**: Um único endpoint para todas as operações CRUD
- **Roteamento Dinâmico**: Acesso aos modelos via parâmetros de query
- **Multi-Database**: Cada contexto de domínio em seu próprio banco de dados
- **Autenticação JWT**: Tokens de acesso e refresh para segurança
- **Documentação OpenAPI**: Swagger UI e ReDoc integrados

## Requisitos

- Python 3.12+
- Django 5.2.6
- Django REST Framework 3.16.1
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/jotap1101/dynamic-api.git
cd dynamic-api
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

```bash
# Crie um arquivo .env na raiz do projeto
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Opcional: Configure bancos de dados específicos
DB1_ENGINE=django.db.backends.postgresql
DB1_NAME=nome_db1
# ... outras configurações de banco
```

## Configuração

1. Execute as migrações em ordem:

```bash
# Primeiro o banco default (auth, admin, etc)
python3 manage.py migrate

# Depois cada banco de domínio específico
python3 manage.py migrate app1 --database=db1
python3 manage.py migrate app2 --database=db2
python3 manage.py migrate app3 --database=db3
```

2. Crie um superusuário:

```bash
python manage.py createsuperuser
```

3. Popular bancos com dados de teste (opcional):

```bash
python scripts/populate_databases.py
```

## Executando o Projeto

1. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

2. Acesse:

- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- Documentação: http://localhost:8000/api/schema/swagger-ui/

## Usando a API

### Autenticação

1. Obtenha os tokens:

```bash
curl -X POST http://localhost:8000/api/v1/token/ \
    -H "Content-Type: application/json" \
    -d '{"username":"seu-usuario","password":"sua-senha"}'
```

2. Use o token de acesso:

```bash
curl -H "Authorization: Bearer <access_token>" \
    "http://localhost:8000/api/v1/?db=db1&table=product"
```

### Exemplos de Requisições

#### Listar Produtos (db1)

```bash
GET /api/v1/?db=db1&table=product
```

#### Criar Animal (db2)

```bash
POST /api/v1/?db=db2&table=animal
Content-Type: application/json

{
    "name": "Rex",
    "age": 3,
    "breed": "uuid-da-raça"
}
```

#### Obter Filme (db3)

```bash
GET /api/v1/123/?db=db3&table=movie
```

## Documentação da API

- **OpenAPI Schema**: http://localhost:8000/api/schema/
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
