import csv
import json
import boto3
import os
import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# Configurações
S3_BUCKET = "randon-bucket-name"
PROMPT_ARN = "arn:aws:bedrock:us-east-1:471112955224:prompt/RR77CDGDJM"
REGION = "us-east-1"

# Configurações de agendamento
START_DATE = "2025-11-15"  # Data inicial no formato YYYY-MM-DD
INTERVAL_DAYS = 1  # Intervalo entre publicações (1=diário, 7=semanal)

def load_video_data():
    """Carrega dados dos vídeos do CSV"""
    videos = []
    with open("YouTube_Data/videos_table.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["file_name"] != "ADICIONAR_NOME_ARQUIVO_MANUALMENTE":
                videos.append({
                    "video_id": row["video_id"],
                    "video_title": row["video_title"],
                    "file_name": row["file_name"],
                    "file_type": row.get("file_type", "pdf").lower(),  # Normaliza para minúsculo
                    "reference_link": row.get("reference_link", "").strip()  # Link opcional
                })
    return videos

def generate_metadata_with_bedrock(bedrock_client, file_s3_key, file_type, video_title, video_id, scheduled_date, reference_link=""):
    """Gera metadados usando AWS Bedrock com document via S3"""
    
    print(f"  🔍 Iniciando geração de metadados...")
    print(f"     Arquivo: {file_s3_key} ({file_type.upper()})")
    print(f"     Título: {video_title}")
    print(f"     Video ID: {video_id}")
    print(f"     Data: {scheduled_date}")
    
    # Monta URI do S3
    s3_uri = f"s3://{S3_BUCKET}/{file_s3_key}"
    print(f"  📍 URI S3: {s3_uri}")
    
    # Nome do documento válido (sem underscores)
    document_name = file_s3_key.replace("_", "-").replace(f".{file_type}", "")
    print(f"  📄 Nome do documento: {document_name}")
    
    # Mensagem com documento via S3
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": "Please analyze the provided document and generate YouTube metadata according to the prompt instructions."
                },
                {
                    "document": {
                        "format": file_type,  # Usa o tipo correto (pdf ou txt)
                        "name": document_name,
                        "source": {
                            "s3Location": {
                                "uri": s3_uri
                            }
                        }
                    }
                }
            ]
        }
    ]
    
    # Variáveis do prompt
    reference_instruction = ""
    if reference_link:
        reference_instruction = f"Include at the end of all video descriptions this reference link: {reference_link}"
    
    prompt_variables = {
        "video_id": {"text": video_id},
        "scheduled_date": {"text": scheduled_date},
        "reference_link": {"text": reference_instruction}
    }
    
    print(f"  📝 Variáveis do prompt: {prompt_variables}")
    print(f"  🚀 Enviando requisição para Bedrock...")
    
    try:
        start_time = time.time()
        print(f"  ⏳ Aguardando resposta do Bedrock (pode demorar 1-2 minutos)...")
        
        response = bedrock_client.converse(
            modelId=PROMPT_ARN,
            messages=messages,
            promptVariables=prompt_variables
        )
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"  ⏱️  Resposta recebida em {duration:.2f} segundos")
        
        metadata_text = response["output"]["message"]["content"][0]["text"]
        print(f"  📊 Tamanho da resposta: {len(metadata_text)} caracteres")
        
        # Remove markdown code blocks se existirem
        if "```json" in metadata_text:
            metadata_text = metadata_text.split("```json")[1].split("```")[0]
            print(f"  🔧 Removido bloco markdown json")
        elif "```" in metadata_text:
            metadata_text = metadata_text.split("```")[1].split("```")[0]
            print(f"  🔧 Removido bloco markdown genérico")
        
        print(f"  🔍 Tentando fazer parse do JSON...")
        parsed_json = json.loads(metadata_text.strip())
        print(f"  ✅ JSON válido com {len(parsed_json)} chaves")
        
        return parsed_json
    
    except Exception as e:
        print(f"  ❌ Erro detalhado: {type(e).__name__}: {str(e)}")
        return None

def verify_file_exists(s3_client, file_key):
    """Verifica se arquivo existe no S3"""
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=file_key)
        return True
    except ClientError:
        return False

def merge_metadata(existing_metadata, new_metadata):
    """Combina metadados novos com existentes"""
    if existing_metadata is None:
        return new_metadata
    
    existing_metadata.update(new_metadata)
    return existing_metadata

def main():
    print("=== Geração de Metadados com AWS Bedrock (Otimizado) ===\n")
    
    # Mostra configurações de agendamento
    print(f"📅 Configurações de agendamento:")
    print(f"   Data inicial: {START_DATE}")
    print(f"   Intervalo: {INTERVAL_DAYS} dia(s)")
    print(f"   Tipo: {'Diário' if INTERVAL_DAYS == 1 else 'Semanal' if INTERVAL_DAYS == 7 else f'A cada {INTERVAL_DAYS} dias'}\n")
    
    # Setup clientes AWS
    s3_client = boto3.client("s3", region_name=REGION)
    bedrock_client = boto3.client("bedrock-runtime", region_name=REGION)
    
    # Carrega dados dos vídeos
    videos = load_video_data()
    print(f"Vídeos para processar: {len(videos)}\n")
    
    if not videos:
        print("❌ Nenhum vídeo encontrado com file_name preenchido.")
        return
    
    # Carrega metadados existentes se houver
    metadata_file = "YouTube_Data/generated_metadata.json"
    existing_metadata = {}
    
    if os.path.exists(metadata_file):
        with open(metadata_file, "r", encoding="utf-8") as f:
            existing_metadata = json.load(f)
        print(f"📄 Carregados metadados existentes: {len(existing_metadata)} vídeos")
    
    # Processa cada vídeo
    success_count = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Processando: {video['file_name']}")
        
        # Converte nome do arquivo para extensão correta
        file_type = video["file_type"]
        if file_type in ["pdf", "doc", "docx", "html", "txt", "md"]:
            file_key = video["file_name"].replace(".mp4", f".{file_type}")
        else:
            file_key = video["file_name"].replace(".mp4", ".pdf")  # Default para PDF
        
        # Verifica se arquivo existe no S3
        if not verify_file_exists(s3_client, file_key):
            print(f"  ❌ Arquivo não encontrado no S3: {file_key}")
            continue
        
        print(f"  ✅ Arquivo encontrado no S3: {file_key}")
        
        # Gera video_id e data de agendamento
        video_id = video["video_id"]
        
        # Calcula data de agendamento baseada na configuração
        start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
        scheduled_date = (start_date + timedelta(days=(i-1) * INTERVAL_DAYS)).strftime("%Y-%m-%d")
        
        # Verifica se já foi processado
        if video_id in existing_metadata:
            print(f"  ⏭️  Vídeo já processado, pulando...")
            continue
        
        # Gera metadados com Bedrock
        new_metadata = generate_metadata_with_bedrock(
            bedrock_client, 
            file_key,
            file_type,
            video["video_title"],
            video_id,
            scheduled_date,
            video.get("reference_link", "")
        )
        
        if new_metadata:
            # Combina com metadados existentes
            existing_metadata = merge_metadata(existing_metadata, new_metadata)
            success_count += 1
            print(f"  ✅ Metadados gerados com sucesso")
            
            # Salva progresso a cada vídeo processado
            os.makedirs("YouTube_Data", exist_ok=True)
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(existing_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== Processamento Concluído ===")
    print(f"Vídeos processados com sucesso: {success_count}/{len(videos)}")
    print(f"Metadados salvos em: {metadata_file}")
    print(f"Total de vídeos no arquivo: {len(existing_metadata)}")

if __name__ == "__main__":
    main()
