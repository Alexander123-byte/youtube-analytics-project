import os
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = self.get_service()
        self.channel_id = channel_id
        self.fetch_channel_data()

    @classmethod
    def get_service(cls):
        api_key = os.environ.get("YT_API_KEY")
        return build("youtube", "v3", developerKey=api_key)

    def fetch_channel_data(self):
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=self.channel_id
        )
        response = request.execute()

        snippet = response["items"][0]["snippet"]
        statistics = response["items"][0]["statistics"]

        self.id = self.channel_id
        self.title = snippet.get("title", "")
        self.description = snippet.get("description", "")
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(statistics.get("subscriberCount", 0))
        self.video_count = int(statistics.get("videoCount", 0))
        self.view_count = int(statistics.get("viewCount", 0))

    def to_json(self, file_path):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()))

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count
