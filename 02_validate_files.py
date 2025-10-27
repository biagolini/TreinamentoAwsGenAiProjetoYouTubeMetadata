import csv
import boto3
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from botocore.exceptions import ClientError
import os

# Configurações
S3_BUCKET = "randon-bucket-name"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def setup_youtube_client():
    """Configura cliente YouTube Data API"""
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

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
                    "file_type": row.get("file_type", "pdf")  # Default para PDF se não especificado
                })
    return videos

def check_pdfs_in_s3(videos):
    """Verifica se arquivos existem no S3"""
    s3 = boto3.client("s3")
    missing_files = []
    found_files = []
    
    for video in videos:
        # Usa a extensão correta baseada no file_type
        if video["file_type"] == "txt":
            file_name = video["file_name"].replace(".mp4", ".txt")
        else:  # Default para PDF
            file_name = video["file_name"].replace(".mp4", ".pdf")
            
        try:
            s3.head_object(Bucket=S3_BUCKET, Key=file_name)
            found_files.append(file_name)
        except ClientError:
            missing_files.append(file_name)
    
    return found_files, missing_files

def check_videos_in_youtube(videos):
    """Verifica se vídeos existem no YouTube usando video_id"""
    youtube = setup_youtube_client()
    missing_videos = []
    found_videos = []
    
    for video in videos:
        try:
            video_request = youtube.videos().list(
                part="snippet",
                id=video["video_id"]
            )
            video_response = video_request.execute()
            
            if video_response["items"]:
                found_videos.append(video["file_name"])
            else:
                missing_videos.append(video["file_name"])
        except:
            missing_videos.append(video["file_name"])
    
    return found_videos, missing_videos

def main():
    print("=== Validação de Arquivos ===\n")
    
    # Carrega dados dos vídeos
    videos = load_video_data()
    print(f"Vídeos para validar: {len(videos)}")
    
    if not videos:
        print("❌ Nenhum vídeo encontrado com file_name preenchido.")
        print("Execute youtube_videos_table.py e preencha a coluna file_name.")
        return
    
    print(f"Vídeos com file_name preenchido: {len(videos)}\n")
    
    # Verifica arquivos no S3
    print("Verificando arquivos no S3...")
    found_files, missing_files = check_pdfs_in_s3(videos)
    
    if found_files:
        print("✓ Arquivos encontrados:")
        for file in sorted(found_files):
            print(f"  - {file}")
    
    if missing_files:
        print("\n❌ Arquivos faltando:")
        for file in sorted(missing_files):
            print(f"  - {file}")
    
    # Verifica vídeos no YouTube
    print("\nVerificando vídeos no YouTube...")
    found_videos, missing_videos = check_videos_in_youtube(videos)
    
    if found_videos:
        print("✓ Vídeos encontrados:")
        for video in sorted(found_videos):
            print(f"  - {video}")
    
    if missing_videos:
        print("\n❌ Vídeos faltando:")
        for video in sorted(missing_videos):
            print(f"  - {video}")
    
    # Resultado final
    print(f"\n=== Resumo ===")
    print(f"Arquivos: {len(found_files)} encontrados, {len(missing_files)} faltando")
    print(f"Vídeos: {len(found_videos)} encontrados, {len(missing_videos)} faltando")
    
    if not missing_files and not missing_videos:
        print("\n✅ Todos os arquivos estão disponíveis!")
    else:
        print("\n⚠️  Alguns arquivos estão faltando.")

if __name__ == "__main__":
    main()
