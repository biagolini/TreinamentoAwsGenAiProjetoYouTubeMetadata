# extra_pdf_to_markdown.py

## Propósito

Este script converte arquivos PDF armazenados no S3 para formato Markdown, facilitando a edição e melhorando a qualidade do processamento com AWS Bedrock.

## O que o código faz

1. **Lê** o arquivo `YouTube_Data/videos_table.csv` 
2. **Filtra** apenas vídeos com `file_type = "pdf"`
3. **Localiza** arquivos PDF correspondentes no S3
4. **Converte** PDF para Markdown usando PyMuPDF
5. **Salva** arquivo `.md` no mesmo bucket S3
6. **Pula** arquivos já convertidos (evita duplicação)

## Vantagens da Conversão

### Markdown vs PDF para IA
- **Melhor processamento**: Markdown é mais facilmente interpretado por IAs
- **Estrutura preservada**: Títulos e seções são mantidos
- **Editável**: Permite ajustes manuais no conteúdo
- **Menor latência**: Processamento mais rápido no Bedrock
- **Menos tokens**: Formato mais eficiente

### Qualidade do Conteúdo
- **Formatação estruturada**: Títulos automáticos com `##`
- **Quebras de página**: Separadas com `---`
- **Texto limpo**: Remove elementos visuais desnecessários
- **Compatibilidade**: Funciona perfeitamente com método `converse`

## Saída do script

```
=== Conversão PDF para Markdown ===

Vídeos com PDFs encontrados: 3

[1/3] Processando: 03_amazonq-developer-ug.mp4
  📥 Baixando PDF: 03_amazonq-developer-ug.pdf
  🔄 Convertendo para Markdown...
  📤 Salvando Markdown: 03_amazonq-developer-ug.md
  ✅ Conversão concluída com sucesso

[2/3] Processando: 04_bedrock-guide.mp4
  ⏭️  Markdown já existe: 04_bedrock-guide.md

=== Conversão Concluída ===
PDFs convertidos com sucesso: 2/3

💡 Dica: Agora você pode alterar file_type de 'pdf' para 'md' no CSV para usar os arquivos Markdown.
```

## Características Técnicas

### Conversão Inteligente
- **Detecção de títulos**: Identifica automaticamente seções principais
- **Estrutura preservada**: Mantém hierarquia do documento
- **Quebras de página**: Adiciona separadores entre páginas
- **Encoding UTF-8**: Suporte completo a caracteres especiais

### Processamento Eficiente
- **Skip duplicados**: Não reconverte arquivos existentes
- **Streaming**: Processa arquivos diretamente na memória
- **Error handling**: Continua mesmo com falhas individuais
- **Feedback detalhado**: Log completo do progresso

### Integração S3
- **Download direto**: Baixa PDF do bucket configurado
- **Upload automático**: Salva Markdown no mesmo bucket
- **Verificação**: Confirma existência antes de processar
- **Metadados**: Define ContentType correto para Markdown

## Pré-requisitos

### Arquivo CSV editado
- Execute `01_videos_table.py` primeiro
- CSV deve ter vídeos com `file_type = "pdf"`
- PDFs devem existir no S3 (verifique com `02_validate_files.py`)

### Credenciais AWS
- Variáveis de ambiente AWS configuradas
- Permissões de leitura e escrita no bucket S3

### Dependências Python
```bash
pip install pymupdf  # Já incluído no requirements.txt atualizado
```

## Configuração

- **S3_BUCKET**: Nome do bucket S3 (padrão: "randon-bucket-name")
- **Conversão**: PDF → Markdown (extensão .pdf → .md)
- **Encoding**: UTF-8 para suporte internacional

## Como usar

1. **Certifique-se** que os PDFs estão no S3:
   ```bash
   python 02_validate_files.py
   ```

2. **Execute a conversão**:
   ```bash
   python extra_pdf_to_markdown.py
   ```

3. **Atualize o CSV** (opcional):
   - Altere `file_type` de "pdf" para "md" para usar Markdown
   - Ou mantenha "pdf" se preferir o original

4. **Continue o fluxo normal**:
   ```bash
   python 03_generate_metadata.py  # Usará o tipo especificado no CSV
   ```

## Exemplo de Conversão

### PDF Original
```
CHAPTER 3: AMAZON BEDROCK OVERVIEW

Amazon Bedrock is a fully managed service...

Key Features:
• Multiple AI models
• Serverless architecture
```

### Markdown Gerado
```markdown
## CHAPTER 3: AMAZON BEDROCK OVERVIEW

Amazon Bedrock is a fully managed service...

## Key Features:
• Multiple AI models
• Serverless architecture
```

## Casos de Uso

### Quando Converter
- **PDFs complexos**: Documentação técnica com muita formatação
- **Edição necessária**: Quando você quer ajustar o conteúdo
- **Melhor qualidade**: Para processamento mais preciso com IA
- **Velocidade**: Quando latência é importante

### Quando Manter PDF
- **Conteúdo visual**: PDFs com diagramas importantes
- **Formatação crítica**: Quando layout é essencial
- **Documentos finais**: Conteúdo que não precisa de edição

## Próximos passos

Após converter PDFs para Markdown:
1. Opcionalmente edite os arquivos `.md` no S3 ou localmente
2. Atualize `file_type` no CSV se desejar usar Markdown
3. Execute `03_generate_metadata.py` normalmente
4. O script usará automaticamente o tipo especificado no CSV

## Limitações

- **Texto apenas**: Não preserva imagens ou gráficos complexos
- **Formatação básica**: Converte para estrutura Markdown simples
- **PDFs escaneados**: Não funciona com PDFs que são imagens
- **Tabelas complexas**: Podem perder formatação original
