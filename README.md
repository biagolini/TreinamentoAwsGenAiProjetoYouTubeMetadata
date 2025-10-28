# YouTube Metadata Automation with AWS Bedrock

Este projeto automatiza a geração e aplicação de metadados otimizados para vídeos do YouTube usando AWS Bedrock para análise de documentação técnica e criação de conteúdo multilíngue.

## Visão Geral do Projeto

O sistema integra AWS Bedrock, YouTube Data API e Google Cloud para automatizar completamente a criação de metadados de vídeos baseados em documentação técnica AWS, oferecendo:

- **Geração automática** de títulos, descrições e tags otimizadas para SEO
- **Suporte multilíngue** com traduções para 8 idiomas
- **Processamento flexível** de arquivos PDF e TXT
- **Agendamento inteligente** de publicações
- **Validação completa** de recursos antes do processamento

---

## Fluxo de Trabalho Automatizado

### 1. Preparação (`01_videos_table.py`)
- Gera tabela inicial com vídeos do YouTube
- Cria CSV para edição manual com nomes de arquivos
- Suporte a tipos de arquivo (PDF/TXT)

### 2. Validação (`02_validate_files.py`)
- Verifica correspondências entre vídeos e arquivos
- Valida existência no S3 e YouTube
- Suporte a múltiplos formatos de arquivo

### 3. Geração de Metadados (`03_generate_metadata.py`)
- Processa documentação com AWS Bedrock
- Gera metadados otimizados e multilíngues
- Configuração flexível de agendamento

### 4. Aplicação no YouTube (`04_update_youtube.py`)
- Aplica metadados aos vídeos automaticamente
- Autenticação inteligente (reutiliza tokens)
- Suporte completo a localizações

---

## Estrutura do Repositório

```
.
├── 01_videos_table.py          # Geração da tabela inicial
├── 01_videos_table.md          # Documentação do passo 1
├── 02_validate_files.py        # Validação de recursos
├── 02_validate_files.md        # Documentação do passo 2
├── 03_generate_metadata.py     # Geração com Bedrock
├── 03_generate_metadata.md     # Documentação do passo 3
├── 04_update_youtube.py        # Aplicação no YouTube
├── 04_update_youtube.md        # Documentação do passo 4
├── prompt/                     # Prompts otimizados para Bedrock
│   ├── prompt.txt    # Prompt principal
│   └── README.md              # Instruções de configuração
├── YouTube_Data/              # Dados gerados e processados
│   ├── videos_table.csv       # Tabela editável de vídeos
│   └── generated_metadata.json # Metadados gerados
├── .env                       # Variáveis de ambiente
├── requirements.txt           # Dependências Python
├── client_secret.json         # Credenciais OAuth Google
└── README.md                  # Este arquivo
```

---

## Tipos de Arquivo Suportados

### PDF (Recomendado para Qualidade)
- **Uso**: Documentação oficial AWS, guias técnicos detalhados
- **Vantagens**: Formatação preservada, imagens, tabelas, conteúdo completo
- **Desvantagens**: Processamento mais lento (60-120s), maior uso de tokens
- **Ideal para**: Conteúdo complexo que requer máxima qualidade

### TXT (Recomendado para Velocidade)
- **Uso**: Resumos, notas simplificadas, conteúdo textual puro
- **Vantagens**: Processamento rápido (30-60s), menor uso de tokens, menos timeouts
- **Desvantagens**: Sem formatação, apenas texto puro
- **Ideal para**: Conteúdo simples ou quando velocidade é prioridade

---

## Configuração Inicial

### 1. Pré-requisitos
- Python 3.8+
- Conta AWS com acesso ao Bedrock
- Canal ativo no YouTube
- Conta Google Cloud Platform

### 2. Ambiente Virtual e Dependências

#### Criar e Ativar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No macOS/Linux:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate
```

#### Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração de Variáveis de Ambiente

#### Criar arquivo .env
Crie um arquivo `.env` na raiz do projeto com suas credenciais:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=sua_access_key_aqui
AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
AWS_DEFAULT_REGION=us-east-1

# S3 Configuration
S3_BUCKET_NAME=seu-bucket-name

# Bedrock Configuration
BEDROCK_PROMPT_ARN=arn:aws:bedrock:us-east-1:account:prompt/ID
```

#### Carregar Variáveis (Opcional)
O projeto pode usar python-dotenv para carregar automaticamente as variáveis do .env:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Configuração AWS
- Credenciais AWS já configuradas via arquivo .env
- Crie bucket S3 para armazenar documentação
- Configure prompt no AWS Bedrock Prompt Manager

### 5. Configuração Google/YouTube
- Configure OAuth 2.0 no Google Cloud Console
- Baixe `client_secret.json`
- Habilite YouTube Data API v3

### 5. Configuração do Prompt
- Use arquivos da pasta `prompt/` para configurar no AWS Bedrock
- Atualize ARN do prompt nos scripts

---

## Como Usar

### Passo 1: Gerar Tabela Inicial
```bash
python 01_videos_table.py
```
- Gera `YouTube_Data/videos_table.csv`
- Edite manualmente: nomes de arquivos e tipos (pdf/txt)

### Passo 2: Validar Recursos
```bash
python 02_validate_files.py
```
- Verifica se arquivos existem no S3
- Confirma vídeos no YouTube
- Deve mostrar "✅ Todos os arquivos estão disponíveis!"

### Passo 3: Gerar Metadados
```bash
python 03_generate_metadata.py
```
- Processa arquivos com AWS Bedrock
- Gera `YouTube_Data/generated_metadata.json`
- Configure datas de agendamento no script

### Passo 4: Aplicar no YouTube
```bash
python 04_update_youtube.py
```
- Aplica metadados aos vídeos
- Configura agendamento de publicação
- Adiciona localizações multilíngues

---

## Configurações Avançadas

### Agendamento de Publicações
```python
# Em 03_generate_metadata.py
START_DATE = "2025-11-15"  # Data inicial
INTERVAL_DAYS = 7          # Intervalo (1=diário, 7=semanal)
```

### Configuração de Bucket S3
```python
# Nos scripts 02 e 03
S3_BUCKET = "seu-bucket-name"
```

### Configuração do Prompt
```python
# Em 03_generate_metadata.py
PROMPT_ARN = "arn:aws:bedrock:region:account:prompt/ID"
```

---

## Recursos Principais

### 🤖 Geração Inteligente com IA
- AWS Bedrock para processamento de linguagem natural
- Prompts otimizados para conteúdo técnico AWS
- Análise contextual de documentação

### 🌍 Suporte Multilíngue
- Traduções automáticas para 8 idiomas
- Adaptação cultural para diferentes mercados
- Manutenção de precisão técnica

### 📊 Otimização SEO
- Títulos otimizados (60 caracteres)
- Descrições estruturadas (1000-1500 caracteres)
- Tags relevantes e diversificadas

### ⚡ Processamento Flexível
- Suporte a PDF e TXT
- Processamento incremental
- Recuperação automática de falhas

### 🔐 Autenticação Inteligente
- Reutilização de tokens válidos
- Renovação automática quando necessário
- Tratamento robusto de erros

---

## Monitoramento e Logs

### Logs Detalhados
- Progresso em tempo real
- Métricas de performance (latência, tokens)
- Identificação clara de erros

### Validação Contínua
- Verificação de recursos antes do processamento
- Validação de datas de agendamento
- Confirmação de aplicação de metadados

---

## Solução de Problemas

### PDFs Grandes/Complexos
- **Problema**: Timeout ou alta latência
- **Solução**: Converter para TXT ou dividir em partes menores

### Erros de Autenticação
- **Problema**: Token inválido ou expirado
- **Solução**: Script renova automaticamente, ou delete `token.json`

### Arquivos Não Encontrados
- **Problema**: Arquivo não existe no S3
- **Solução**: Verifique nomes e extensões no CSV

### Falhas do Bedrock
- **Problema**: Limite de tokens ou timeout
- **Solução**: Use TXT em vez de PDF para arquivos grandes

---

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs ou melhorias
- Criar pull requests com novos recursos
- Forkar o repositório para suas próprias soluções

---

## Licença e Disclaimer

Este projeto é open-source e disponível sob a Licença MIT. Você é livre para copiar, modificar e usar o projeto como desejar. No entanto, qualquer responsabilidade pelo uso do código é exclusivamente sua. Use por sua própria conta e risco.

Use responsavelmente e siga os [Termos de Serviço da API do YouTube](https://developers.google.com/youtube/terms) e [Termos de Uso do AWS Bedrock](https://aws.amazon.com/service-terms/).
