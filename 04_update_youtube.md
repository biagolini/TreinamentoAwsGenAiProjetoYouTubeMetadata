# 04_update_youtube.py

## Propósito

Este script aplica os metadados gerados pelo AWS Bedrock aos vídeos do YouTube, atualizando títulos, descrições, tags, localizações e configurações de agendamento automaticamente.

## O que o código faz

1. **Carrega** metadados do arquivo `YouTube_Data/generated_metadata.json`
2. **Autentica** com a YouTube Data API usando OAuth 2.0 (reutiliza token válido)
3. **Processa cada vídeo** individualmente:
   - Busca dados atuais do vídeo
   - Aplica novos metadados (título, descrição, tags)
   - Atualiza localizações em 8 idiomas
   - Configura agendamento de publicação
4. **Relatório** detalhado do progresso e resultados

## Funcionalidades

### Metadados Aplicados
- **Título**: Otimizado para SEO (60 caracteres)
- **Descrição**: Estruturada em parágrafos (1000-1500 caracteres)
- **Tags**: 15 tags únicas e relevantes
- **Categoria**: Education (ID: 27)
- **Idioma padrão**: Inglês

### Localizações Multilíngues
- **Chinês (zh)**: Simplificado
- **Holandês (nl)**
- **Francês (fr)**
- **Alemão (de)**
- **Italiano (it)**
- **Japonês (ja)**
- **Português (pt)**: Brasil
- **Espanhol (es)**: Internacional

### Configurações de Publicação
- **Status**: Privado (para vídeos agendados)
- **Agendamento**: Data/hora futura configurada
- **COPPA**: Não direcionado para crianças
- **Validação**: Verifica se data é futura

### Autenticação Inteligente
- **Reutilização**: Usa token existente se válido
- **Renovação automática**: Gera novo token apenas quando necessário
- **Transparência**: Informa quando renova credenciais
- **Eficiência**: Evita autenticação desnecessária

## Saída do script

```
=== Aplicação de Metadados no YouTube ===

📊 Metadados carregados: 4 vídeos

🔐 Configurando cliente YouTube...
✅ Cliente configurado

[1/4] Processando vídeo: 1qsgjjl3SaI
🔄 Atualizando vídeo: 1qsgjjl3SaI
  ✅ Vídeo encontrado
  📝 Título: Amazon Q Developer Overview: Getting Started with AI...
  🌍 Localizações: 8 idiomas
  📅 Agendado para: 2025-11-15T16:30:00Z
  ✅ Vídeo atualizado com sucesso

[2/4] Processando vídeo: 0Pu9NVZuj4k
🔄 Atualizando vídeo: 0Pu9NVZuj4k
  ✅ Vídeo encontrado
  📝 Título: Amazon Q Developer Basics: Free & Pro Tiers...
  🌍 Localizações: 8 idiomas
  📅 Agendado para: 2025-11-16T16:30:00Z
  ✅ Vídeo atualizado com sucesso

=== Processamento Concluído ===
Vídeos atualizados com sucesso: 4/4
🎉 Todos os vídeos foram atualizados!
```

## Validações e Segurança

### Verificações Automáticas
- **Existência do vídeo**: Confirma que o vídeo existe no canal
- **Data futura**: Valida agendamento apenas para datas futuras
- **Formato de data**: Verifica formato ISO 8601
- **Permissões**: Usa escopo `youtube` para atualizações completas

### Tratamento de Erros
- **Vídeo não encontrado**: Continua com próximo vídeo
- **Erro de API**: Log detalhado e continua processamento
- **Data inválida**: Ignora agendamento mas aplica outros metadados
- **Falha de autenticação**: Para execução com erro claro

### Autenticação Robusta
- **Token válido**: Reutiliza sem nova autenticação
- **Token inválido**: Remove e gera novo automaticamente
- **Primeira execução**: Gera token inicial
- **Tratamento de erros**: Informa motivo da renovação

## Pré-requisitos

### Arquivo de Metadados
- Execute `03_generate_metadata.py` primeiro
- Arquivo `YouTube_Data/generated_metadata.json` deve existir
- Metadados devem estar no formato correto

### Credenciais YouTube
- Arquivo `client_secret.json` configurado (OAuth 2.0)
- Token será gerado/reutilizado automaticamente
- Escopo: `https://www.googleapis.com/auth/youtube`

### Dependências Python
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Configuração

- **SCOPES**: Permissões YouTube (youtube)
- **METADATA_FILE**: Localização dos metadados gerados
- **Categoria padrão**: Education (ID: 27)
- **Idioma padrão**: Inglês (en)

## Como usar

1. **Certifique-se** que os metadados foram gerados:
   ```bash
   python 03_generate_metadata.py
   ```

2. **Execute o script**:
   ```bash
   python 04_update_youtube.py
   ```

3. **Autentique** quando solicitado (apenas se necessário)

4. **Monitore** o progresso no terminal

5. **Verifique** os vídeos no YouTube Studio

## Características Técnicas

### Processamento Individual
- **Isolado**: Cada vídeo é processado independentemente
- **Resiliente**: Falha em um vídeo não afeta os outros
- **Detalhado**: Log específico para cada operação
- **Incremental**: Pode ser executado múltiplas vezes

### Estrutura de Dados
- **Input**: JSON com video_id como chave
- **Validação**: Verifica estrutura antes de aplicar
- **Flexível**: Aplica apenas campos disponíveis
- **Compatível**: Formato padrão YouTube Data API

### Gerenciamento de Token
- **Inteligente**: Só autentica quando necessário
- **Persistente**: Salva token para reutilização
- **Robusto**: Trata expiração automaticamente
- **Transparente**: Informa status da autenticação

## Limitações

- **Rate Limits**: YouTube API tem limites de quota
- **Vídeos privados**: Apenas o proprietário pode atualizar
- **Agendamento**: Requer data futura e status privado
- **Localizações**: Limitado aos idiomas configurados

## Próximos passos

Após executar este script:
1. Verifique os vídeos no YouTube Studio
2. Confirme agendamentos de publicação
3. Teste visualizações em diferentes idiomas
4. Monitore performance dos metadados otimizados
5. Execute novamente se necessário (reutiliza token)
