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
  - `reference_link`: Link de referência opcional (padrão: vazio)

## Configuração

- **MAX_VIDEOS**: Número de vídeos a buscar (padrão: 50)
- **Tipo de arquivo padrão**: PDF (pode ser alterado manualmente para TXT)

## Tipos de Arquivo Suportados

O projeto suporta todos os formatos compatíveis com o método `converse` do AWS Bedrock:

### MD (Markdown) - Recomendado para Roteiros
- **Uso**: Roteiros de vídeo, documentação técnica, tutoriais
- **Vantagens**: Formatação estruturada, facilmente manipulado por IAs como Amazon Q
- **Integração IA**: Amazon Q (plugin VSCode) pode revisar e melhorar significativamente a qualidade do texto
- **Ideal para**: Criação colaborativa de roteiros com assistência de IA

### TXT (Texto Simples) - Recomendado para Simplicidade
- **Uso**: Roteiros simples, notas, conteúdo direto
- **Vantagens**: Processamento rápido, menor uso de tokens, máxima simplicidade
- **Ideal para**: Conteúdo sem formatação, rascunhos rápidos

### DOC/DOCX (Microsoft Word)
- **Uso**: Roteiros elaborados por usuários menos técnicos
- **Vantagens**: Interface amigável, formatação rica, amplamente conhecido
- **Ideal para**: Usuários com pouca habilidade técnica que preferem editores visuais

### PDF (Para Conteúdo Pronto)
- **Uso**: Documentação oficial AWS, artigos científicos, manuais técnicos
- **Vantagens**: Formatação preservada, conteúdo já finalizado
- **Ideal para**: Quando o texto já vem pronto e não precisa de edição

### HTML (Web Content)
- **Uso**: Conteúdo web, documentação online, artigos formatados
- **Vantagens**: Estrutura semântica, links, formatação web
- **Ideal para**: Artigos web, documentação online

### Recomendações por Caso de Uso:
- **Roteiros novos**: MD (com Amazon Q) > TXT > DOC/DOCX
- **Documentação existente**: PDF > HTML
- **Usuários não-técnicos**: DOC/DOCX > TXT
- **Máxima qualidade com IA**: MD + Amazon Q plugin

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
