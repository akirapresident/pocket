"""
Instagram scraper service using Apify API
"""
import requests
import tempfile
import subprocess
import os
import whisper
from typing import Optional, Dict, Any
from app.config import settings

class InstagramScraper:
    """Instagram scraper service"""
    
    def __init__(self):
        self.apify_token = settings.APIFY_TOKEN
        self.apify_actor_id = settings.APIFY_ACTOR_ID
    
    def _download_video_temporarily(self, video_url: str) -> Optional[str]:
        """Download video temporarily for audio extraction"""
        try:
            print("📥 Baixando vídeo temporariamente...")
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_path = temp_file.name
            temp_file.close()
            
            # Download video
            response = requests.get(video_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Vídeo baixado: {temp_path}")
            return temp_path
            
        except Exception as e:
            print(f"❌ Erro ao baixar vídeo: {e}")
            return None
    
    def _extract_audio(self, video_path: str) -> Optional[str]:
        """Extract audio from video using FFmpeg"""
        try:
            print("🎵 Extraindo áudio...")
            
            # Create temporary file for audio
            audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio_path = audio_temp.name
            audio_temp.close()
            
            # FFmpeg command to extract audio
            cmd = [
                'ffmpeg', '-i', video_path, 
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # Audio codec
                '-ar', '16000',  # Sample rate
                '-ac', '1',  # Mono
                '-y',  # Overwrite file
                audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Áudio extraído: {audio_path}")
                return audio_path
            else:
                print(f"❌ Erro FFmpeg: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao extrair áudio: {e}")
            return None
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Whisper"""
        try:
            print("🎤 Transcrevendo áudio...")
            
            # Load Whisper model
            model = whisper.load_model("base")
            
            # Transcribe audio
            result = model.transcribe(audio_path, language="pt")
            
            transcription = result["text"].strip()
            print(f"✅ Transcrição concluída: {len(transcription)} caracteres")
            
            return transcription
            
        except Exception as e:
            print(f"❌ Erro na transcrição: {e}")
            return "ERRO_TRANSCRICAO"
    
    def _cleanup_temp_files(self, video_path: Optional[str], audio_path: Optional[str]):
        """Remove temporary files"""
        try:
            if video_path and os.path.exists(video_path):
                os.unlink(video_path)
                print("🗑️ Vídeo temporário removido")
            
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
                print("🗑️ Áudio temporário removido")
                
        except Exception as e:
            print(f"⚠️ Erro ao limpar arquivos: {e}")
    
    def _calculate_engagement_rates(self, likes: int, comments: int, views: int) -> tuple[float, float]:
        """Calculate engagement rates"""
        try:
            if views > 0:
                likes_rate = round((likes / views) * 100, 2)
                comments_rate = round((comments / views) * 100, 2)
            else:
                likes_rate = 0.0
                comments_rate = 0.0
            
            return likes_rate, comments_rate
        except:
            return 0.0, 0.0
    
    def scrape_video_data(self, instagram_url: str) -> Optional[Dict[str, Any]]:
        """Scrape data from Instagram video"""
        print(f"\n🔍 Processando: {instagram_url}")
        
        try:
            # Apify API configuration
            apify_url = f"https://api.apify.com/v2/acts/{self.apify_actor_id}/runs"
            
            payload = {
                "directUrls": [instagram_url],
                "resultsType": "posts",
                "resultsLimit": 1
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apify_token}"
            }
            
            # Execute scraper
            print("🚀 Executando scraper Apify...")
            response = requests.post(apify_url, json=payload, headers=headers, timeout=60)
            
            if response.status_code not in [200, 201]:
                print(f"❌ Erro HTTP {response.status_code}: {response.text}")
                return None
            
            run_data = response.json()
            run_id = run_data["data"]["id"]
            
            print(f"⏳ Aguardando conclusão... (Run ID: {run_id})")
            
            # Wait for completion
            import time
            max_attempts = 30
            for attempt in range(max_attempts):
                time.sleep(2)
                
                status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
                status_response = requests.get(status_url, headers=headers)
                status_data = status_response.json()
                
                if status_data["data"]["status"] == "SUCCEEDED":
                    print("✅ Scraper concluído!")
                    break
                elif status_data["data"]["status"] == "FAILED":
                    print("❌ Scraper falhou!")
                    return None
            else:
                print("⏰ Timeout aguardando scraper")
                return None
            
            # Get results
            dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items"
            dataset_response = requests.get(dataset_url, headers=headers)
            dataset_response.raise_for_status()
            
            items = dataset_response.json()
            
            if not items:
                print("❌ Nenhum item encontrado")
                return None
            
            item = items[0]
            
            # Verifica se há erro no resultado
            if "error" in item:
                print(f"❌ Erro do Apify: {item.get('error')} - {item.get('errorDescription', 'Sem descrição')}")
                return None
            
            # Extract basic data
            username = "ERRO_USERNAME"
            if 'ownerUsername' in item:
                username = f"@{item['ownerUsername']}"
            elif 'owner' in item and item['owner']:
                username = f"@{item['owner'].get('username', 'ERRO')}"
            elif 'username' in item:
                username = f"@{item['username']}"
            
            likes = item.get('likesCount', 0)
            comments = item.get('commentsCount', 0)
            views = item.get('videoViewCount', item.get('viewsCount', 0))
            
            # Extract posted date
            posted_at = None
            if 'timestamp' in item:
                from datetime import datetime
                try:
                    posted_at = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                except:
                    posted_at = None
            
            # Calculate engagement rates
            likes_rate, comments_rate = self._calculate_engagement_rates(likes, comments, views)
            
            data = {
                'url': instagram_url,
                'username': username,
                'likes': likes,
                'comments': comments,
                'views': views,
                'likes_rate': likes_rate,
                'comments_rate': comments_rate,
                'transcription': 'ERRO_TRANSCRICAO',
                'posted_at': posted_at
            }
            
            # Try to transcribe audio
            video_url = item.get('videoUrl') or item.get('video')
            if video_url:
                print("🎬 Encontrei URL do vídeo, vou transcrever...")
                
                # Download video temporarily
                video_temp = self._download_video_temporarily(video_url)
                audio_temp = None
                
                if video_temp:
                    # Extract audio
                    audio_temp = self._extract_audio(video_temp)
                    
                    if audio_temp:
                        # Transcribe
                        transcription = self._transcribe_audio(audio_temp)
                        data['transcription'] = transcription
                    else:
                        data['transcription'] = 'SEM_AUDIO'
                else:
                    data['transcription'] = 'ERRO_DOWNLOAD'
                
                # Cleanup temporary files
                self._cleanup_temp_files(video_temp, audio_temp)
            else:
                print("❌ URL do vídeo não encontrada")
                data['transcription'] = 'SEM_VIDEO_URL'
            
            return data
            
        except Exception as e:
            print(f"❌ Erro ao processar {instagram_url}: {e}")
            return None
