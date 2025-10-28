# 02_validate_files.py

## Propósito

Este script valida se existem correspondências entre os vídeos listados no CSV e os arquivos (PDF ou TXT) armazenados no Amazon S3, garantindo que todos os recursos necessários estejam disponíveis antes do processamento com IA.

## O que o código faz

1. **Lê** o arquivo `YouTube_Data/videos_table.csv` editado manualmente
2. **Filtra** apenas vídeos com `file_name` preenchido (ignora linhas com texto padrão)
3. **Detecta tipo de arquivo**: Usa coluna `file_type` (pdf|doc|docx|html|txt|md) para verificar extensão correta
4. **Verifica arquivos no S3**: Busca arquivos com extensão apropriada no bucket configurado
5. **Verifica vídeos no YouTube**: Usa `video_id` para confirmar existência via API
6. **Exibe relatório** detalhado de arquivos encontrados e faltando

## Validações realizadas

### Arquivos no Amazon S3
- **Todos os tipos**: Converte `.mp4` para extensão apropriada baseada em `file_type`
- Suporta: `.pdf`, `.doc`, `.docx`, `.html`, `.txt`, `.md`
- Verifica existência no bucket configurado
- Lista arquivos encontrados e faltando em ordem alfabética

### Vídeos no YouTube
- Usa `video_id` para buscar vídeo via API
- Confirma que o vídeo ainda existe e está acessível
- Lista vídeos encontrados e faltando

## Saída do script

```
=== Validação de Arquivos ===

Vídeos para validar: 4
Vídeos com file_name preenchido: 4

Verificando arquivos no S3...
✓ Arquivos encontrados:
  - 03_amazonq-developer-ug.pdf
  - 04_amazonq-developer-ug.txt

❌ Arquivos faltando:
  - 05_amazonq-developer-ug.pdf

Verificando vídeos no YouTube...
✓ Vídeos encontrados:
  - 03_amazonq-developer-ug.mp4
  - 04_amazonq-developer-ug.mp4

=== Resumo ===
Arquivos: 2 encontrados, 1 faltando
Vídeos: 2 encontrados, 0 faltando

⚠️  Alguns arquivos estão faltando.
```

## Tipos de Arquivo Suportados

O script valida todos os formatos compatíveis com o método `converse` do AWS Bedrock:

### MD (Markdown)
- **Uso**: Roteiros de vídeo, documentação técnica
- **Verificação**: Busca arquivo `.md` no S3

### TXT (Texto Simples)
- **Uso**: Roteiros simples, conteúdo direto
- **Verificação**: Busca arquivo `.txt` no S3

### DOC/DOCX (Microsoft Word)
- **Uso**: Roteiros elaborados, documentos formatados
- **Verificação**: Busca arquivo `.doc` ou `.docx` no S3

### PDF
- **Uso**: Documentação oficial AWS, artigos científicos
- **Verificação**: Busca arquivo `.pdf` no S3

### HTML
- **Uso**: Conteúdo web, documentação online
- **Verificação**: Busca arquivo `.html` no S3

## Pré-requisitos

### Arquivo CSV editado
- Execute `01_videos_table.py` primeiro
- Edite `YouTube_Data/videos_table.csv` com nomes reais dos arquivos
- Configure `file_type` como "pdf" ou "txt" conforme necessário
- Remova linhas de vídeos que não deseja processar

### Credenciais AWS
- Variáveis de ambiente AWS configuradas
- Acesso ao bucket S3: `randon-bucket-name`

### Credenciais Google
- Arquivo `client_secret.json` e `token.json` (gerado pelo script anterior)

### Dependências Python
```bash
pip install boto3 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Configuração

- **S3_BUCKET**: Nome do bucket S3 (padrão: "randon-bucket-name")
- **SCOPES**: Permissões YouTube (readonly)

## Como usar

1. **Certifique-se** que o CSV foi editado com nomes reais dos arquivos e tipos corretos

2. **Execute o script**:
   ```bash
   python 02_validate_files.py
   ```

3. **Analise o resultado**:
   - ✅ Se todos os arquivos estão disponíveis: prossiga para próxima etapa
   - ⚠️ Se há arquivos faltando: corrija antes de continuar

## Exemplo de CSV válido

```csv
video_id,video_title,file_name,file_type
abc123,03 amazonq developer ug,03_amazonq-developer-ug.mp4,pdf
def456,04 amazonq developer ug,04_amazonq-developer-ug.mp4,md
ghi789,05 tutorial completo,05_tutorial-completo.mp4,docx
```

## Próximo passo

Após validação bem-sucedida, você pode prosseguir com o processamento automatizado usando `03_generate_metadata.py` para gerar metadados otimizados.
