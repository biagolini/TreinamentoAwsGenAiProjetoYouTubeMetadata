# 01_videos_table.py

## Propósito

Este script gera uma tabela CSV com os vídeos mais recentes do seu canal do YouTube, fornecendo uma base para o processo de automação de metadados.

## O que o código faz

1. **Conecta** à YouTube Data API usando credenciais OAuth 2.0
2. **Busca** os vídeos mais recentes do canal autenticado
3. **Extrai** informações básicas: video_id e video_title
4. **Ordena** os vídeos por título em ordem alfabética
5. **Gera** arquivo CSV com coluna adicional `file_name` para preenchimento manual

## Saída

- **Arquivo**: `YouTube_Data/videos_table.csv`
- **Colunas**:
  - `video_id`: ID único do vídeo no YouTube
  - `video_title`: Título atual do vídeo
  - `file_name`: Campo com texto "ADICIONAR_NOME_ARQUIVO_MANUALMENTE" para edição manual
  - `file_type`: Tipo de arquivo fonte (padrão: "pdf", pode ser editado para "txt")

## Configuração

- **MAX_VIDEOS**: Número de vídeos a buscar (padrão: 50)
- **Tipo de arquivo padrão**: PDF (pode ser alterado manualmente para TXT)

## Tipos de Arquivo Suportados

### PDF (Padrão)
- **Uso**: Documentação técnica complexa, manuais, guias detalhados
- **Vantagens**: Formatação preservada, imagens, tabelas
- **Desvantagens**: Processamento mais lento, maior uso de tokens

### TXT (Alternativa)
- **Uso**: Conteúdo textual simples, notas, resumos
- **Vantagens**: Processamento mais rápido, menor uso de tokens
- **Desvantagens**: Sem formatação, apenas texto puro

### Quando usar cada tipo:
- **PDF**: Para documentação oficial AWS, guias técnicos detalhados
- **TXT**: Para resumos, notas simplificadas, conteúdo que não requer formatação

## Pré-requisitos

### Credenciais Google
- Arquivo `client_secret.json` configurado (OAuth 2.0)
- Primeira execução gerará `token.json` automaticamente

### Dependências Python
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Permissões YouTube
- Canal do YouTube ativo
- Escopo: `https://www.googleapis.com/auth/youtube.readonly`

## Como usar

1. **Execute o script**:
   ```bash
   python 01_videos_table.py
   ```

2. **Edite o CSV gerado**:
   - Abra `YouTube_Data/videos_table.csv`
   - Substitua "ADICIONAR_NOME_ARQUIVO_MANUALMENTE" pelos nomes reais dos arquivos
   - Altere `file_type` de "pdf" para "txt" se necessário
   - Mantenha apenas as linhas dos vídeos que deseja processar

3. **Exemplo de edição**:
   ```csv
   video_id,video_title,file_name,file_type
   abc123,03 amazonq developer ug,03_amazonq-developer-ug.pdf,pdf
   def456,04 amazonq developer ug,04_amazonq-developer-ug.txt,txt
   ```

## Próximo passo

Após editar o CSV, execute `02_validate_files.py` para validar as correspondências entre vídeos e arquivos PDF.
