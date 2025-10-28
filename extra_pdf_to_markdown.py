import csv
import boto3
import fitz  # PyMuPDF
import io
import os
from botocore.exceptions import ClientError

# Configurações
S3_BUCKET = "randon-bucket-name"

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
                    "file_type": row.get("file_type", "pdf").lower()
                })
    return videos

def pdf_to_markdown(pdf_content):
    """Converte conteúdo PDF para Markdown"""
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    markdown_content = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        # Adiciona quebra de página
        if page_num > 0:
            markdown_content.append("\n---\n")
        
        # Processa o texto linha por linha
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detecta títulos (linhas em maiúscula ou com palavras-chave)
            if (line.isupper() and len(line) > 5) or any(keyword in line.lower() for keyword in ['chapter', 'section', 'overview']):
                markdown_content.append(f"## {line}")
            else:
                markdown_content.append(line)
        
        markdown_content.append("")  # Linha em branco após cada página
    
    doc.close()
    return "\n".join(markdown_content)

def convert_pdf_to_markdown(s3_client, pdf_key, md_key):
    """Converte PDF do S3 para Markdown e salva de volta no S3"""
    try:
        # Baixa PDF do S3
        print(f"  📥 Baixando PDF: {pdf_key}")
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=pdf_key)
        pdf_content = response['Body'].read()
        
        # Converte para Markdown
        print(f"  🔄 Convertendo para Markdown...")
        markdown_content = pdf_to_markdown(pdf_content)
        
        # Upload Markdown para S3
        print(f"  📤 Salvando Markdown: {md_key}")
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=md_key,
            Body=markdown_content.encode('utf-8'),
            ContentType='text/markdown'
        )
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na conversão: {e}")
        return False

def check_file_exists(s3_client, file_key):
    """Verifica se arquivo existe no S3"""
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=file_key)
        return True
    except ClientError:
        return False

def main():
    print("=== Conversão PDF para Markdown ===\n")
    
    # Setup cliente S3
    try:
        s3_client = boto3.client("s3")
    except Exception as e:
        print("❌ Erro ao configurar cliente S3:")
        print("   Verifique se as credenciais AWS estão configuradas no arquivo .env")
        print(f"   Erro: {e}")
        return
    
    # Carrega dados dos vídeos
    videos = load_video_data()
    pdf_videos = [v for v in videos if v["file_type"] == "pdf"]
    
    print(f"Vídeos com PDFs encontrados: {len(pdf_videos)}\n")
    
    if not pdf_videos:
        print("❌ Nenhum vídeo com tipo 'pdf' encontrado no CSV.")
        return
    
    success_count = 0
    
    for i, video in enumerate(pdf_videos, 1):
        print(f"[{i}/{len(pdf_videos)}] Processando: {video['file_name']}")
        
        # Gera nomes dos arquivos
        pdf_key = video["file_name"].replace(".mp4", ".pdf")
        md_key = video["file_name"].replace(".mp4", ".md")
        
        # Verifica se PDF existe
        if not check_file_exists(s3_client, pdf_key):
            print(f"  ❌ PDF não encontrado: {pdf_key}")
            continue
        
        # Verifica se Markdown já existe
        if check_file_exists(s3_client, md_key):
            print(f"  ⏭️  Markdown já existe: {md_key}")
            continue
        
        # Converte PDF para Markdown
        if convert_pdf_to_markdown(s3_client, pdf_key, md_key):
            success_count += 1
            print(f"  ✅ Conversão concluída com sucesso")
        
        print()  # Linha em branco
    
    print("=== Conversão Concluída ===")
    print(f"PDFs convertidos com sucesso: {success_count}/{len(pdf_videos)}")
    
    if success_count > 0:
        print("\n💡 Dica: Agora você pode alterar file_type de 'pdf' para 'md' no CSV para usar os arquivos Markdown.")

if __name__ == "__main__":
    main()
