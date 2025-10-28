# Configuração do Prompt no AWS Bedrock

## Arquivo do Prompt
Use o conteúdo do arquivo `prompt.txt` para criar/atualizar o prompt no AWS Bedrock Prompt Manager.

## Estratégia do Prompt

### Contexto do Projeto
- **PDFs**: Capítulos da documentação AWS
- **Vídeos**: Conteúdo gerado por IA do Google baseado nos PDFs
- **Desafio**: Criar metadados que sejam conectados ao PDF mas não muito específicos
- **Série**: Múltiplos vídeos cobrindo diferentes capítulos do mesmo serviço AWS

### Abordagem Balanceada
- ✅ **Conectado ao PDF**: Usa o tema e conceitos principais do documento
- ✅ **Visão Geral**: Foca em benefícios e conceitos de alto nível
- ✅ **Acessível**: Linguagem que não intimida iniciantes
- ✅ **Diferenciado**: Cada capítulo tem identidade própria na série
- ❌ **Não muito específico**: Evita detalhes que podem não aparecer no vídeo IA

## Configurações no Console AWS

### 1. Informações Básicas
- **Nome**: `youtube-metadata-generator-optimized`
- **Descrição**: `Gerador de metadados para vídeos AI baseados em documentação AWS`

### 2. Variáveis de Input
Configure estas 3 variáveis:

- `video_id` (tipo: text)
- `scheduled_date` (tipo: text)
- `reference_link` (tipo: text)

### 3. Configurações de Inferência
- **Modelo**: `amazon.nova-pro-v1:0`
- **Temperature**: `0.9`
- **Max Tokens**: `5120`
- **Top P**: `0.9`

### 4. Principais Características
- 🎯 **Foco em benefícios** em vez de detalhes técnicos
- 🌐 **Acessível para iniciantes** mas respeitoso com experts
- 📚 **Consciência de série** - diferencia capítulos
- 🤖 **Adaptado para IA** - considera interpretação do Google AI
- 🎬 **Engajamento prioritário** - por que assistir, não só o que aprender

## Como Usar
1. Copie o conteúdo de `prompt.txt`
2. Cole no campo de texto do prompt no console AWS
3. Configure as variáveis e parâmetros conforme especificado
4. Salve e teste o prompt
5. Use o ARN gerado no script `03_generate_metadata.py`

## Exemplo de Resultado Esperado
- **Título**: "AWS Bedrock Foundations: AI Models Made Simple"
- **Descrição**: Foca em por que aprender, benefícios práticos, e valor para carreira
- **Tags**: Mix de termos técnicos e acessíveis
