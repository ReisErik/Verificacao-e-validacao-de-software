# Resumo do Projeto

# Sistema de Gamificação de Hábitos

Este projeto consiste em um sistema de gamificação voltado ao incentivo da criação e manutenção de hábitos por meio de desafios personalizados.

Os usuários podem criar desafios individuais para acompanhar seu próprio progresso ou convidar amigos para participar em desafios colaborativos e competições.

O sistema conta com um mecanismo de recompensas baseado na dificuldade do desafio. O cálculo de XP considera fatores como meta, duração e tipo do desafio, buscando equilibrar a progressão e evitar recompensas desproporcionais ou inflacionadas.

Além das funcionalidades de negócio, o projeto prioriza a qualidade e a confiabilidade do software por meio da implementação de uma ampla suíte de testes automatizados, com alta cobertura de código e foco na validação das principais regras de negócio e fluxos da aplicação.

# Instalação e execução do projeto

## Pré-requisitos

Certifique-se de ter instalado:

* Python 3.11 ou superior
* Git
* Node.js e npm (caso utilize o frontend)

---

## 1. Clone o repositório

```bash
git clone https://github.com/ReisErik/Verificacao-e-validacao-de-software.git
cd verificacao-e-validacao-de-software
```

---

## 2. Crie um ambiente virtual

```bash
cd backend
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instale as dependências do backend

```bash
pip install -r requirements.txt
```

---

## 4. Execute a API

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```
http://127.0.0.1:8000
```

E a documentação automática da API poderá ser acessada em:

```
http://127.0.0.1:8000/docs
```

---

## 5. Executando os testes

Para executar todos os testes:

```bash
pytest
```

Para visualizar a cobertura de testes:

```bash
pytest --cov=app
```

Ou gerar um relatório HTML:

```bash
pytest --cov=app --cov-report=html
```

O relatório será criado na pasta `htmlcov/`.

---

# Frontend

Entre na pasta do frontend:

```bash
cd frontend
cd gym
```

Instale as dependências:

```bash
npm install
```

Execute o projeto:

```bash
npm run dev
```

Por padrão, ele ficará disponível em:

```
http://localhost:5173
```

---

# Estrutura do projeto

```
app/
 ├── routes/
 ├── services/
 ├── models/
 ├── schemas/
 ├── database/
 ├── core/
 └── tests/

frontend/
 ├── components/
 ├── pages/
 ├── services/
 └── schemas/
```

---

# Observações

* Sempre ative o ambiente virtual antes de executar o backend.
* Caso novas dependências sejam adicionadas, atualize o arquivo `requirements.txt` para manter o ambiente reproduzível.
* Recomenda-se utilizar a documentação em `/docs` para testar rapidamente os endpoints da API durante o desenvolvimento.
