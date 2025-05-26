# Book API com Monitoramento

***Autor**: Giovanny Oliveira*

## Descrição
API REST para gerenciamento de livros com monitoramento usando Prometheus e Grafana.

## Pré-requisitos
- Docker Desktop
- Git

## Instalação e Execução

1. Clone o repositório:
```bash
git clone https://github.com/DoutorK/bookAPI.git
cd bookAPI
```

2. Inicie os containers:
```bash
docker-compose up -d
```

## Endpoints Disponíveis

### API (http://localhost:8000)
- `GET /books` - Lista todos os livros
- `GET /books/{id}` - Busca um livro específico
- `POST /books` - Adiciona um novo livro
- `GET /health` - Status da API
- `GET /metrics` - Métricas Prometheus

### Exemplo de POST:
```json
{
    "id": 1,
    "title": "Dom Casmurro",
    "author": "Machado de Assis"
}
```

## Monitoramento

### Prometheus (http://localhost:9090)
- Dashboard com métricas da API
- Scraping a cada 15 segundos

### Grafana (http://localhost:3000)
- **Login**: admin
- **Senha**: admin
- Dashboard pré-configurado com:
  - Status codes das requisições
  - Latência por endpoint
  - Total de requisições

## Estrutura do Projeto
```
bookAPI/
├── book_api.py         # Lógica da API
├── main.py            # Entrada da aplicação
├── Dockerfile         # Configuração do container da API
├── docker-compose.yml # Orquestração dos serviços
├── requirements.txt   # Dependências Python
├── prometheus/        # Configurações Prometheus
└── grafana/          # Configurações Grafana
```

## Stack Tecnológica
- FastAPI
- Prometheus
- Grafana
- Docker

## Métricas Disponíveis
- `books_total`: Contador de livros cadastrados
- `books_requests_total`: Contador de requisições por endpoint
- `books_gauge`: Número atual de livros no sistema
- Métricas padrão do FastAPI

## Troubleshooting
Se o Docker não iniciar, tente:
```bash
docker-compose down
docker-compose up -d --build
```

## Contribuição
1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nome`)
3. Commit suas mudanças (`git commit -m 'Adicionando feature'`)
4. Push para a branch (`git push origin feature/nome`)
5. Abra um Pull Request

---
Desenvolvido com ❤️ usando FastAPI e Docker