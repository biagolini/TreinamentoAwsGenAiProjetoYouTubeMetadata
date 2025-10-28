# 03_generate_metadata.py

## Propósito

Este script processa arquivos de documentação ou roteiros (PDF, DOC, DOCX, HTML, TXT, MD) armazenados no S3 e gera metadados otimizados para YouTube usando AWS Bedrock, criando títulos, descrições e tags multilíngues para vídeos baseados em conteúdo gerado por IA.

## O que o código faz

1. **Lê** o arquivo `YouTube_Data/videos_table.csv` editado com nomes de arquivos, tipos e links de referência
2. **Verifica** existência dos arquivos correspondentes no S3 (PDF, DOC, DOCX, HTML, TXT, MD)
3. **Processa cada vídeo** usando AWS Bedrock com document context apropriado
4. **Gera metadados** otimizados baseados no conteúdo do arquivo
5. **Salva progressivamente** em arquivo JSON para uso posterior
6. **Combina** novos metadados com existentes (permite retomar processamento)

## Configurações de Agendamento

### Variáveis Configuráveis
```python
START_DATE = "2025-11-15"  # Data inicial no formato YYYY-MM-DD
INTERVAL_DAYS = 1  # Intervalo entre publicações (1=diário, 7=semanal)
```

### Exemplos de Configuração

**Publicação Diária:**
```python
START_DATE = "2025-11-15"
INTERVAL_DAYS = 1
```
- Vídeo 1: 2025-11-15
- Vídeo 2: 2025-11-16
- Vídeo 3: 2025-11-17

**Publicação Semanal:**
```python
START_DATE = "2025-11-15"
INTERVAL_DAYS = 7
```
- Vídeo 1: 2025-11-15
- Vídeo 2: 2025-11-22
- Vídeo 3: 2025-11-29

## Tipos de Arquivo Suportados

O script processa todos os formatos compatíveis com o método `converse` do AWS Bedrock:

### MD (Markdown) - Recomendado para Roteiros
- **Uso**: Roteiros de vídeo, documentação técnica estruturada
- **Vantagens**: Formatação preservada, processamento eficiente, ideal para IA
- **Recomendado para**: Roteiros criados com Amazon Q, conteúdo estruturado

### TXT (Texto Simples) - Recomendado para Velocidade
- **Uso**: Roteiros simples, notas, conteúdo textual puro
- **Vantagens**: Processamento rápido (30-60s), menor uso de tokens, menos timeouts
- **Recomendado para**: Conteúdo simples ou quando velocidade é prioridade

### DOC/DOCX (Microsoft Word)
- **Uso**: Roteiros elaborados, documentos formatados
- **Vantagens**: Formatação rica, familiar para usuários não-técnicos
- **Recomendado para**: Usuários que preferem editores visuais

### PDF
- **Uso**: Documentação oficial AWS, artigos científicos, guias técnicos
- **Vantagens**: Formatação preservada, imagens, tabelas, conteúdo completo
- **Desvantagens**: Processamento mais lento (60-120s), maior uso de tokens
- **Recomendado para**: Documentação técnica complexa já finalizada

### HTML
- **Uso**: Conteúdo web, documentação online, artigos formatados
- **Vantagens**: Estrutura semântica, links, formatação web
- **Recomendado para**: Artigos web, documentação online

## Estratégia de Geração

### Abordagem Balanceada
- **Conectado ao arquivo**: Usa tema e conceitos principais do documento
- **Visão Geral**: Foca em benefícios e conceitos de alto nível
- **Adaptado para IA**: Considera que Google AI interpretará o conteúdo
- **Série Consciente**: Diferencia capítulos do mesmo serviço AWS
- **Engajamento**: Prioriza "por que assistir" vs "o que contém"

### Metadados Gerados
- **Título**: 60 caracteres, SEO otimizado, foco em benefícios
- **Descrição**: 1000-1500 caracteres, estruturada em parágrafos
- **Tags**: 15 tags únicas, mix técnico/acessível
- **Traduções**: 8 idiomas (zh, nl, fr, de, it, ja, pt, es)

## Saída do script

```
=== Geração de Metadados com AWS Bedrock (Otimizado) ===

📅 Configurações de agendamento:
   Data inicial: 2025-11-15
   Intervalo: 1 dia(s)
   Tipo: Diário

Vídeos para processar: 4
📄 Carregados metadados existentes: 2 vídeos

[1/4] Processando: 03_amazonq-developer-ug.mp4
  🔍 Iniciando geração de metadados...
     Arquivo: 03_amazonq-developer-ug.pdf (PDF)
     Título: 03 amazonq developer ug
     Video ID: abc123
     Data: 2025-11-15
  ✅ Arquivo encontrado no S3: 03_amazonq-developer-ug.pdf
  🤖 Gerando metadados usando PDF: s3://randon-bucket-name/03_amazonq-developer-ug.pdf
  ⏱️  Resposta recebida em 67.34 segundos
  ✅ Metadados gerados com sucesso

[2/4] Processando: 04_amazonq-developer-ug.mp4
  🔍 Iniciando geração de metadados...
     Arquivo: 04_amazonq-developer-ug.txt (TXT)
     Título: 04 amazonq developer ug
     Video ID: def456
     Data: 2025-11-16
  ✅ Arquivo encontrado no S3: 04_amazonq-developer-ug.txt
  🤖 Gerando metadados usando TXT: s3://randon-bucket-name/04_amazonq-developer-ug.txt
  ⏱️  Resposta recebida em 32.18 segundos
  ✅ Metadados gerados com sucesso

=== Processamento Concluído ===
Vídeos processados com sucesso: 2/4
Metadados salvos em: YouTube_Data/generated_metadata.json
Total de vídeos no arquivo: 4
```

## Arquivo de Saída

**Localização**: `YouTube_Data/generated_metadata.json`

**Estrutura**:
```json
{
  "abc123": {
    "scheduledPublishTime": "2025-11-15T16:30:00Z",
    "default": {
      "title": "AWS Bedrock Foundations: AI Models Made Simple",
      "description": "Discover how AWS Bedrock...",
      "tags": ["AWS", "Bedrock", "AI", "Tutorial", ...]
    },
    "localizations": {
      "pt": {
        "title": "Fundamentos AWS Bedrock: Modelos IA Simplificados",
        "description": "Descubra como o AWS Bedrock..."
      }
    }
  }
}
```

## Características Técnicas

### Processamento Independente
- **Sem sessão**: Cada vídeo é processado isoladamente
- **Sem memória**: O modelo não "lembra" dos vídeos anteriores
- **Falhas isoladas**: Erro em um vídeo não afeta os outros
- **Consistência**: Cada vídeo recebe o mesmo tratamento inicial

### Document Context via S3
- **Acesso direto**: Bedrock lê arquivo diretamente do S3
- **Suporte múltiplo**: PDF e TXT nativamente suportados
- **Eficiência**: Sem transferência desnecessária de dados
- **URI S3**: Formato `s3://bucket/key`

### Processamento Incremental
- **Salva progresso**: Após cada vídeo processado
- **Skip duplicados**: Evita reprocessar vídeos existentes
- **Retomada**: Pode continuar de onde parou
- **Error handling**: Continua mesmo com falhas individuais

## Pré-requisitos

### Arquivo CSV editado
- Execute `01_videos_table.py` e `02_validate_files.py` primeiro
- CSV deve ter `file_name`, `file_type` e opcionalmente `reference_link` preenchidos corretamente

### Credenciais AWS
- Variáveis de ambiente AWS configuradas
- Acesso ao bucket S3: `randon-bucket-name`
- Permissões para AWS Bedrock Runtime

### Prompt configurado
- Use arquivos da pasta `prompt/` para configurar no console AWS
- Atualize `PROMPT_ARN` no script com o ARN correto

### Dependências Python
```bash
pip install boto3
```

## Link de Referência (Opcional)

### Funcionalidade
- **Coluna**: `reference_link` no CSV
- **Uso**: Link para documentação original, artigo ou fonte do conteúdo
- **Comportamento**: Se preenchido, será incluído automaticamente no final de todas as descrições

### Implementação
- **Vazio**: Nenhuma referência é adicionada
- **Preenchido**: Adiciona texto padrão: "Include at the end of all video descriptions this reference link: [URL]"
- **Automático**: O prompt processa e inclui o link nas descrições de todos os idiomas

### Exemplo de Uso
```csv
video_id,video_title,file_name,file_type,reference_link
abc123,AWS Bedrock Guide,bedrock-guide.mp4,pdf,https://docs.aws.amazon.com/bedrock/
def456,Lambda Tutorial,lambda-tutorial.mp4,md,
```

## Configuração

- **S3_BUCKET**: Nome do bucket S3 (padrão: "randon-bucket-name")
- **PROMPT_ARN**: ARN do prompt no Bedrock Prompt Manager
- **REGION**: Região AWS (padrão: "us-east-1")
- **START_DATE**: Data inicial de publicação (formato: "YYYY-MM-DD")
- **INTERVAL_DAYS**: Intervalo entre publicações em dias

## Como usar

1. **Configure o prompt** no AWS Bedrock usando arquivos da pasta `prompt/`

2. **Ajuste as configurações** no início do script:
   ```python
   START_DATE = "2025-11-15"  # Sua data desejada
   INTERVAL_DAYS = 7  # Para publicação semanal
   ```

3. **Atualize o ARN** no script se necessário

4. **Execute o script**:
   ```bash
   python 03_generate_metadata.py
   ```

5. **Monitore o progresso**: O script salva após cada vídeo processado

6. **Retome se necessário**: Vídeos já processados são automaticamente pulados

## Recomendações de Uso

### Para PDFs Grandes/Complexos:
- **Considere TXT**: Se houver timeouts frequentes
- **Monitore latência**: >120s pode indicar problema
- **Verifique tokens**: Limite de ~80k tokens de input

### Para Processamento Rápido:
- **Use TXT**: Quando velocidade é prioridade
- **Batch pequenos**: Processe poucos vídeos por vez
- **Horários off-peak**: Evite horários de pico do Bedrock

## Próximo passo

Após gerar os metadados, execute `04_update_youtube.py` para aplicar as atualizações nos vídeos do YouTube.
