# Configuração do Prompt no AWS Bedrock

## Arquivos de Prompt
O projeto oferece duas versões do prompt:

- **`prompt_en.txt`** - Versão em inglês (recomendada)
- **`prompt_pt.txt`** - Versão em português

Use o conteúdo do arquivo escolhido para criar/atualizar o prompt no AWS Bedrock Prompt Manager.

## Recomendação de Idioma

### Inglês (Recomendado)
- **Melhor performance**: Modelos de IA funcionam melhor em inglês
- **Consistência**: Variáveis e estrutura JSON em inglês
- **Compatibilidade**: Padrão da AWS e APIs
- **Qualidade**: Resultados mais precisos e consistentes

### Português
- **Facilidade**: Mais fácil para editar e entender
- **Localização**: Pode gerar conteúdo mais adaptado ao público brasileiro
- **Preferência**: Use se preferir trabalhar em português

## Estratégia do Prompt

### Contexto do Projeto
- **Arquivos fonte**: Documentação AWS ou roteiros personalizados (PDF, DOC, DOCX, HTML, TXT, MD)
- **Vídeos**: Conteúdo gerado por IA baseado nos arquivos fonte
- **Desafio**: Criar metadados conectados ao arquivo mas não muito específicos
- **Série**: Múltiplos vídeos cobrindo diferentes tópicos

### Abordagem Balanceada
- ✅ **Conectado ao arquivo**: Usa o tema e conceitos principais do documento
- ✅ **Visão Geral**: Foca em benefícios e conceitos de alto nível
- ✅ **Acessível**: Linguagem que não intimida iniciantes
- ✅ **Diferenciado**: Cada arquivo tem identidade própria na série
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
1. Escolha a versão do prompt (inglês recomendado)
2. Copie o conteúdo de `prompt_en.txt` ou `prompt_pt.txt`
3. Cole no campo de texto do prompt no console AWS
4. Configure as variáveis e parâmetros conforme especificado
5. Salve e teste o prompt
6. Use o ARN gerado no script `03_generate_metadata.py`

## Exemplo de Resultado Esperado
- **Título**: "AWS Bedrock Foundations: AI Models Made Simple"
- **Descrição**: Foca em por que aprender, benefícios práticos, e valor para carreira
- **Tags**: Mix de termos técnicos e acessíveis
