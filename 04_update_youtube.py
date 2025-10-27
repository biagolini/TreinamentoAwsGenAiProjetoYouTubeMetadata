import os
import json
import datetime
from datetime import timezone
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

# Configurações
SCOPES = ["https://www.googleapis.com/auth/youtube"]
METADATA_FILE = "YouTube_Data/generated_metadata.json"

def setup_youtube_client():
    """Configura cliente YouTube Data API"""
    if os.path.exists("token.json"):
        try:
            # Tenta usar token existente
            creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
            return googleapiclient.discovery.build("youtube", "v3", credentials=creds)
        except Exception as e:
            print(f"🔄 Token inválido ({e}), gerando novo...")
            os.remove("token.json")
    
    # Gera novo token apenas se necessário
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def load_generated_metadata():
    """Carrega metadados gerados pelo script 03"""
    if not os.path.exists(METADATA_FILE):
        print(f"❌ Arquivo não encontrado: {METADATA_FILE}")
        print("Execute 03_generate_metadata.py primeiro")
        return {}
    
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def is_future_date(date_str):
    """Verifica se a data é futura"""
    try:
        scheduled_date_str = date_str.replace("Z", "+00:00")
        scheduled_date = datetime.datetime.fromisoformat(scheduled_date_str)
        current_date = datetime.datetime.now(timezone.utc)
        return scheduled_date > current_date
    except ValueError:
        print(f"❌ Formato de data inválido: {date_str}")
        return False

def update_video_metadata(youtube, video_id, metadata):
    """Atualiza metadados de um vídeo no YouTube"""
    
    print(f"🔄 Atualizando vídeo: {video_id}")
    
    try:
        # Busca dados atuais do vídeo
        video_request = youtube.videos().list(
            part="snippet,localizations,status",
            id=video_id
        )
        video_response = video_request.execute()
        
        if not video_response["items"]:
            print(f"  ❌ Vídeo não encontrado: {video_id}")
            return False
        
        print(f"  ✅ Vídeo encontrado")
        
        # Prepara atualizações
        body = {"id": video_id}
        
        # Atualiza snippet (título, descrição, tags)
        if "default" in metadata:
            default_info = metadata["default"]
            snippet = {
                "title": default_info.get("title"),
                "description": default_info.get("description"),
                "tags": default_info.get("tags", []),
                "defaultLanguage": "en",
                "categoryId": "27"  # Education
            }
            body["snippet"] = snippet
            print(f"  📝 Título: {snippet['title'][:50]}...")
        
        # Atualiza localizações
        if "localizations" in metadata:
            localizations = {}
            for lang, localization in metadata["localizations"].items():
                localizations[lang] = {
                    "title": localization.get("title"),
                    "description": localization.get("description")
                }
            body["localizations"] = localizations
            print(f"  🌍 Localizações: {len(localizations)} idiomas")
        
        # Atualiza status (agendamento)
        if "scheduledPublishTime" in metadata:
            scheduled_time = metadata["scheduledPublishTime"]
            if is_future_date(scheduled_time):
                status = {
                    "privacyStatus": "private",
                    "publishAt": scheduled_time,
                    "selfDeclaredMadeForKids": False
                }
                body["status"] = status
                print(f"  📅 Agendado para: {scheduled_time}")
            else:
                print(f"  ⚠️  Data de agendamento não é futura, ignorando")
        
        # Aplica atualizações
        parts = []
        if "snippet" in body:
            parts.append("snippet")
        if "localizations" in body:
            parts.append("localizations")
        if "status" in body:
            parts.append("status")
        
        if parts:
            youtube.videos().update(
                part=",".join(parts),
                body=body
            ).execute()
            print(f"  ✅ Vídeo atualizado com sucesso")
            return True
        else:
            print(f"  ⚠️  Nenhuma atualização necessária")
            return False
            
    except googleapiclient.errors.HttpError as e:
        print(f"  ❌ Erro HTTP: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
        return False

def main():
    print("=== Aplicação de Metadados no YouTube ===\n")
    
    # Carrega metadados gerados
    metadata_dict = load_generated_metadata()
    
    if not metadata_dict:
        return
    
    print(f"📊 Metadados carregados: {len(metadata_dict)} vídeos\n")
    
    # Setup cliente YouTube
    print("🔐 Configurando cliente YouTube...")
    youtube = setup_youtube_client()
    print("✅ Cliente configurado\n")
    
    # Processa cada vídeo
    success_count = 0
    total_videos = len(metadata_dict)
    
    for i, (video_id, metadata) in enumerate(metadata_dict.items(), 1):
        print(f"[{i}/{total_videos}] Processando vídeo: {video_id}")
        
        if update_video_metadata(youtube, video_id, metadata):
            success_count += 1
        
        print()  # Linha em branco para separar
    
    # Resultado final
    print("=== Processamento Concluído ===")
    print(f"Vídeos atualizados com sucesso: {success_count}/{total_videos}")
    
    if success_count == total_videos:
        print("🎉 Todos os vídeos foram atualizados!")
    elif success_count > 0:
        print("⚠️  Alguns vídeos foram atualizados com sucesso")
    else:
        print("❌ Nenhum vídeo foi atualizado")

if __name__ == "__main__":
    main()
