# Sistema de Gestão - Indústrias Wayne

<div align="center">
  <img src="./frontend/img/Logo Industrias Wayne.png" alt="Logo Indústrias Wayne" width="400"/>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=yellow" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/Flask-2.2%2B-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange?logo=html5" alt="Frontend">
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green" alt="Licença MIT">
</p>

<p align="center">
  <strong>Status do Projeto:</strong> Concluído ✔️
</p>

<p align="center">
  Um protótipo funcional de uma aplicação web full stack desenvolvida para as Indústrias Wayne, com o objetivo de otimizar processos internos e a segurança de Gotham City.
</p>

<p align="center">
 <a href="#sobre-o-projeto">Sobre</a> •
 <a href="#funcionalidades">Funcionalidades</a> •
 <a href="#tecnologias-utilizadas">Tecnologias</a> •
 <a href="#instalação-e-execução">Instalação</a> • 
 <a href="#credenciais-de-teste">Uso</a> •
 <a href="#endpoints-da-api">API</a> •
 <a href="#licença">Licença</a>
</p>

-----

### 📖 **Sobre o Projeto**

Este projeto foi desenvolvido como uma solução tecnológica para atender às necessidades específicas das Indústrias Wayne. Trata-se de uma plataforma robusta que centraliza o gerenciamento de recursos internos e o controle de acesso às instalações, com um dashboard visualmente atraente para monitoramento de dados relevantes.

-----

### ✨ **Funcionalidades**

  - **Sistema de Gerenciamento de Segurança:**

      - Controle de acesso a áreas restritas para usuários autorizados.
      - Autenticação via Token JWT (JSON Web Token).
      - Autorização baseada em 3 níveis de permissão: `funcionário`, `gerente` e `administrador de segurança`.

  - **Gestão de Recursos:**

      - Interface para gerenciar inventário de equipamentos, veículos e dispositivos.
      - Operações de CRUD (Criar, Ler, Atualizar, Deletar) para os recursos, com permissões atreladas aos papéis dos usuários.

  - **Dashboard de Visualização:**

      - Painel de controle dinâmico que exibe dados sobre os recursos cadastrados.
      - Gráficos interativos para uma análise visual rápida e eficiente.

-----

### 🛠️ **Tecnologias Utilizadas**

O projeto foi construído utilizando as seguintes tecnologias:

  - **Backend:**

      - **Python 3.9+**
      - **Flask:** Microframework web para a construção da API RESTful.
      - **Flask-SQLAlchemy:** ORM para interação com o banco de dados.
      - **Flask-CORS:** Para permitir a comunicação entre o frontend e o backend.
      - **PyJWT:** Para geração e validação dos tokens de autenticação.
      - **Werkzeug:** Para hashing seguro de senhas.

  - **Frontend:**

      - **HTML5**
      - **CSS3**
      - **JavaScript (ES6+)**
      - **Chart.js:** Biblioteca para a criação dos gráficos do dashboard.

  - **Banco de Dados:**

      - **SQLite 3:** Banco de dados relacional baseado em arquivo, ideal para desenvolvimento e prototipagem.

-----

### 📁 **Estrutura de Pastas**

O projeto está organizado da seguinte forma:

```
/industrias_wayne
|
|-- /backend
|   |-- /app            # Contém a lógica principal da aplicação Flask
|   |-- /instance       # Onde o banco de dados é criado
|   |-- /venv           # Ambiente virtual do Python
|   `-- run.py          # Script para iniciar o servidor
|
|-- /frontend
|   |-- /css
|   |-- /img
|   `-- /js
|
`-- README.md
```

-----

### 🚀 **Instalação e Execução**

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

#### **Pré-requisitos**

Antes de começar, você precisará ter o [**Python 3.9**](https://www.python.org/downloads/) ou superior instalado.

#### **1. Clone o Repositório**

Se você estivesse baixando de um repositório Git (como o GitHub), usaria o comando abaixo. Como você já tem os arquivos, pode pular para o próximo passo.

```bash
git clone https://github.com/seu-usuario/industrias_wayne.git
cd industrias_wayne
```

#### **2. Configuração do Backend**

Todos os comandos a seguir devem ser executados a partir da pasta `/backend`.

```bash
cd backend
```

**a) Crie e ative o ambiente virtual:**

Um ambiente virtual isola as dependências do projeto.

```bash
# Cria o ambiente
python -m venv venv

# Ativa o ambiente (o comando varia conforme o sistema operacional)

# No Windows (Command Prompt - cmd.exe):
venv\Scripts\activate

# No Windows (PowerShell):
# (Primeiro, pode ser necessário rodar: Set-ExecutionPolicy Unrestricted -Scope Process)
.\venv\Scripts\Activate.ps1

# No macOS/Linux:
source venv/bin/activate
```

**b) Instale as dependências:**

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias de uma vez.

```bash
pip install Flask Flask-SQLAlchemy PyJWT Werkzeug Flask-Cors
```

#### **3. Inicialização do Banco de Dados**

Este comando único irá criar o arquivo do banco de dados e popular a tabela de usuários com dados de teste.

```bash
# Diga ao Flask qual é o arquivo principal da aplicação
# No Windows:
set FLASK_APP=run.py
# No macOS/Linux:
export FLASK_APP=run.py

# Execute o comando personalizado para criar o banco de dados e os usuários
flask create-users
```

#### **4. Executando a Aplicação**

**a) Inicie o servidor backend:**

```bash
flask run
```

O servidor estará rodando em `http://127.0.0.1:5000`. **Deixe este terminal aberto.**

**b) Abra o frontend no navegador:**

Navegue até a pasta `/frontend` e abra o arquivo `index.html` diretamente no seu navegador de preferência (Google Chrome, Firefox, etc.).

-----

### 🔑 **Credenciais de Teste**

Use os seguintes usuários para testar os diferentes níveis de acesso da plataforma:

| Papel                     | Usuário  | Senha      | Permissões                                      |
| ------------------------- | :------- | :--------- | :---------------------------------------------- |
| **Administrador Segurança** | `bruce`  | `gotham`   | Acesso total (CRUD completo).                   |
| **Gerente** | `lucius` | `fox`      | Pode criar e editar, mas não excluir recursos. |
| **Gerente** | `barbara`| `gordon`   | Pode criar e editar, mas não excluir recursos. |
| **Funcionário** | `alfred` | `pennyworth` | Apenas visualização.                            |
| **Funcionário** | `tim`    | `drake`    | Apenas visualização.                            |
| **Funcionário** | `selina` | `kyle`     | Apenas visualização.                            |

-----

### 🔌 **Endpoints da API**

A API RESTful segue os seguintes endpoints. Todas as rotas (exceto `/api/login`) requerem um token JWT enviado no cabeçalho `x-access-token`.

| Método   | Endpoint             | Proteção                                 | Descrição                                         |
| :------- | :------------------- | :--------------------------------------- | :------------------------------------------------ |
| `POST`   | `/api/login`         | Nenhuma                                  | Autentica um usuário e retorna um token JWT.        |
| `GET`    | `/api/recursos`      | Token Obrigatório                        | Retorna a lista de todos os recursos.             |
| `POST`   | `/api/recursos`      | Token + `gerente` ou `admin_seguranca`   | Cria um novo recurso.                             |
| `PUT`    | `/api/recursos/<id>` | Token + `gerente` ou `admin_seguranca`   | Atualiza um recurso existente.                    |
| `DELETE` | `/api/recursos/<id>` | Token + `admin_seguranca`                | Deleta um recurso.                                |
| `GET`    | `/api/dashboard`     | Token Obrigatório                        | Retorna dados agregados para os gráficos.         |

-----

### ⚖️ **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Você pode criar um arquivo LICENSE com o texto da licença MIT, se desejar).

-----

<p align="center">
Feito com 🦇 e muita tecnologia pelas Indústrias Wayne.
</p\>
