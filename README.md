# EduControl - Sistema de Frequência Escolar

**Plataforma profissional para gestão de frequência e acompanhamento acadêmico**

## 🏢 Visão Geral

O EduControl é uma solução empresarial completa para instituições de ensino que precisam de controle rigoroso de frequência, relatórios detalhados e acompanhamento em tempo real do desempenho acadêmico dos alunos.

## ⚡ Características Principais

### 🎯 **Interface Profissional**
- Design moderno e responsivo baseado em padrões corporativos
- Dashboard intuitivo com navegação simplificada
- Componentes visuais profissionais (tabelas, gráficos, badges)
- Experiência otimizada para desktop e mobile

### 📊 **Analytics Avançados**
- Relatórios em tempo real com métricas de performance
- Identificação automática de alunos em risco
- Estatísticas visuais com barras de progresso


### 🔧 **Funcionalidades Técnicas**
- API REST robusta com documentação automática
- Banco de dados SQLite com relacionamentos otimizados
- Validação de dados com Pydantic
- Arquitetura modular e escalável

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# Clone ou baixe o projeto
cd sistema_frequencia

# Instale as dependências
pip install -r requirements.txt
```

### Execução
```bash
# Inicie o servidor
python main.py

# O sistema estará disponível em:
# Interface Web: http://127.0.0.1:8001
# API Docs: http://127.0.0.1:8001/docs
```

## 📋 Guia de Uso

### 1. **Configuração Inicial**
- Acesse a interface web
- Crie turmas através do painel "Gerenciar Turmas"
- Cadastre alunos associando-os às turmas criadas

### 2. **Controle de Frequência**
- Selecione a turma ativa
- Inicie uma nova sessão de aula
- Registre a frequência dos alunos (Presente/Falta/Justificado)

### 3. **Relatórios e Analytics**
- Visualize estatísticas em tempo real
- Identifique alunos com frequência abaixo de 75%


## 🛠️ Arquitetura Técnica

```
EduControl/
├── app/                    # Backend (FastAPI)
│   ├── database.py        # Modelos de dados (SQLAlchemy)
│   ├── schemas.py         # Validação (Pydantic)
│   ├── routes/api.py      # Endpoints REST
│   └── services/          # Lógica de negócio
├── static/                # Frontend Assets
│   ├── style.css         # Estilos principais
│   ├── dashboard.css     # Componentes profissionais
│   └── app.js            # Lógica de interface
├── templates/
│   └── index.html        # Interface principal
├── data/                 # Banco SQLite + Exports
└── main.py              # Servidor principal
```

## 📈 Demonstração e Testes

### Dados de Exemplo
```bash
# Popule o sistema com dados de demonstração
python demo_data.py
```

### Testes Automatizados
```bash
# Execute testes de funcionalidade
python test_sistema.py
```

## 🔌 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/turmas/` | Criar nova turma |
| `GET` | `/api/v1/turmas/` | Listar todas as turmas |
| `POST` | `/api/v1/alunos/` | Cadastrar aluno |
| `GET` | `/api/v1/turmas/{id}/alunos/` | Listar alunos da turma |
| `POST` | `/api/v1/sessoes/` | Criar sessão de aula |
| `POST` | `/api/v1/frequencias/lote/` | Registrar frequências |
| `GET` | `/api/v1/relatorio/turma/{id}` | Relatório da turma |


## 💼 Casos de Uso Empresariais

- **Escolas Particulares**: Controle rigoroso de frequência para compliance
- **Universidades**: Acompanhamento de presença em disciplinas
- **Cursos Técnicos**: Relatórios para órgãos reguladores
- **Treinamentos Corporativos**: Controle de participação em capacitações

## 🔒 Segurança e Compliance

- Validação de dados em todas as camadas
- Logs de auditoria para rastreabilidade
- Backup automático do banco de dados
- Conformidade com LGPD para dados educacionais

## 📞 Suporte Técnico

Para suporte técnico ou customizações empresariais:
- Documentação completa: `/docs` endpoint
- Logs do sistema: Disponíveis no console
- Testes automatizados: `python test_sistema.py`

---

**EduControl** - Transformando a gestão educacional através da tecnologia.