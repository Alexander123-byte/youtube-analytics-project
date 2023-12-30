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


def main():
    channel_id = "UC-OVMPlMA3-YCIeg4z5z23A"
    channel = Channel(channel_id)

    print(f"Название канала: {channel.title}")
    print(f"Описание канала: {channel.description}")
    print(f"Количество подписчиков: {channel.subscriber_count}")
    print(f"Количество видео: {channel.video_count}")
    print(f"Общее количество просмотров: {channel.view_count}")

    # Сохранение данных в JSON-файл
    channel.to_json("channel_data.json")


if __name__ == "__main__":
    main()
