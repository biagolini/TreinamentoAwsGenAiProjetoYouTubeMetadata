import os
import csv
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

# Configuração
MAX_VIDEOS = 30
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Autenticação
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    # Obter playlist de uploads
    channel_request = youtube.channels().list(part="contentDetails", mine=True)
    channel_response = channel_request.execute()
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Obter vídeos recentes
    videos_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=MAX_VIDEOS
    )
    videos_response = videos_request.execute()

    # Preparar dados
    videos_data = []
    for item in videos_response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item["snippet"]["title"]
        videos_data.append([video_id, video_title, "ADICIONAR_NOME_ARQUIVO_MANUALMENTE", "pdf", ""])

    # Ordenar por título alfabeticamente
    videos_data.sort(key=lambda x: x[1])

    # Salvar CSV
    os.makedirs("YouTube_Data", exist_ok=True)
    csv_path = os.path.join("YouTube_Data", "videos_table.csv")
    
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["video_id", "video_title", "file_name", "file_type", "reference_link"])
        writer.writerows(videos_data)
    
    print(f"CSV salvo em: {csv_path}")
    print(f"Total de vídeos: {len(videos_data)}")

if __name__ == "__main__":
    main()
