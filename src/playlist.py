# src/playlist.py
from googleapiclient.discovery import build
from datetime import timedelta
import re
import os


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = ""
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.videos = self.fetch_playlist_data()

    @property
    def total_duration(self):
        total_duration = sum(video["duration"].total_seconds() for video in self.videos)
        return timedelta(seconds=total_duration)

    def show_best_video(self):
        if not self.videos:
            return None

        best_video = max(self.videos, key=lambda video: video.get("likes", 0), default={})
        best_video_id = best_video.get("link", None)

        # Форматирование ссылки в ожидаемый формат
        if best_video_id:
            best_video_url = f"https://youtu.be/{best_video_id.split('=')[-1]}"
            return best_video_url
        else:
            return None

    def fetch_playlist_data(self):
        try:
            api_key = os.environ.get("YT_API_KEY")
            youtube = build("youtube", "v3", developerKey=api_key)

            # Получаем информацию о плейлисте
            playlist_info = youtube.playlists().list(
                part="snippet",
                id=self.playlist_id
            ).execute()

            # Заполняем название плейлиста
            self.title = playlist_info["items"][0]["snippet"]["title"]

            # Вывод информации о плейлисте (добавлено)
            print(f"Playlist Title: {self.title}")
            print(f"Playlist URL: {self.url}")

            # Получаем видео из плейлиста
            playlist_items = youtube.playlistItems().list(
                part="snippet",
                playlistId=self.playlist_id,
                maxResults=50  # Максимальное количество видео для запроса
            ).execute()

            videos = []
            for item in playlist_items["items"]:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_info = youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()

                snippet = video_info["items"][0]["snippet"]
                statistics = video_info["items"][0]["statistics"]
                content_details = video_info["items"][0]["contentDetails"]

                video_data = {
                    "title": snippet.get("title", ""),
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "likes": int(statistics.get("likeCount", 0)),
                    "duration": self.parse_duration(content_details.get("duration", "PT0S"))
                }

                videos.append(video_data)

            return videos
        except Exception as e:
            print(f"Error fetching playlist data: {e}")
            return []

    @staticmethod
    def parse_duration(duration_str):
        # Преобразование строкового представления продолжительности в объект timedelta
        match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration_str)
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        seconds = int(match.group(3)[:-1]) if match.group(3) else 0

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)


# Ваш код здесь (main.py)
