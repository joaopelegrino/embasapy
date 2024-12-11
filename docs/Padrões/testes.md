# Padrões de Teste - EMBASA

## 1. Estrutura de Testes

### 1.1 Organização de Diretórios
```
tests/
├── unit/                    # Testes unitários
│   ├── test_core/          # Testes dos módulos core
│   └── test_api/           # Testes da API
├── integration/            # Testes de integração
│   └── test_api/          # Testes E2E da API
└── conftest.py            # Fixtures compartilhadas
```

### 1.2 Tipos de Teste
- **Testes Unitários**: Testam componentes isoladamente
- **Testes de Integração**: Testam interações entre componentes
- **Testes E2E**: Testam fluxos completos da API

## 2. Metas de Cobertura

### 2.1 Metas por Módulo
- Core Modules: 95%
  - config.py: 95%
  - security.py: 95%
- API Endpoints: 90%
  - routes: 90%
- Overall: 90%

### 2.2 Relatórios de Cobertura
```bash
# Gerar relatório de cobertura
pytest --cov=app --cov-report=html

# Verificar no browser
open coverage_html/index.html
```

## 3. Padrões de Mocking

### 3.1 Quando Usar Mocks
- Chamadas externas (APIs, banco de dados)
- Operações custosas
- Comportamentos não determinísticos

### 3.2 Exemplos de Mocking
```python
# Mock de resposta externa
@pytest.fixture
def mock_external_api(mocker):
    return mocker.patch("app.services.external.api_call")

# Mock de configuração
@pytest.fixture
def mock_settings(mocker):
    return mocker.patch("app.core.config.Settings")
```

## 4. Padrões de Fixtures

### 4.1 Fixtures Globais (conftest.py)
- test_settings: Configurações de teste
- client: Cliente de teste da API
- test_headers: Headers padrão
- api_base_url: URL base da API

### 4.2 Fixtures Específicas
```python
@pytest.fixture
def valid_api_key():
    return "test_key"

@pytest.fixture
def invalid_api_key():
    return "invalid_key"
```

## 5. Boas Práticas

### 5.1 Nomenclatura
- Arquivos: `test_*.py`
- Funções: `test_*`
- Classes: `Test*`
- Fixtures: nome descritivo do que fornecem

### 5.2 Organização de Testes
- Um arquivo por módulo
- Testes agrupados por funcionalidade
- Descrições claras nos docstrings

### 5.3 Assertions
- Use mensagens descritivas
- Verifique todos os aspectos relevantes
- Evite múltiplos asserts quando possível

## 6. Execução de Testes

### 6.1 Comandos Básicos
```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app

# Executar testes específicos
pytest tests/unit/test_core/
```

### 6.2 Marcadores
```python
@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass
```

## 7. CI/CD

### 7.1 GitHub Actions
- Executa testes em cada PR
- Verifica cobertura mínima
- Gera relatórios de teste

### 7.2 Ambiente de Teste
- Variáveis de ambiente específicas
- Banco de dados de teste
- Mocks de serviços externos