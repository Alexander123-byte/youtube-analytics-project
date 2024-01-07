from src.video import Video, PLVideo
from src.channel import Channel


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


if __name__ == '__main__':
    # Создаем два экземпляра класса
    video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
    video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    assert str(video1) == 'GIL в Python: зачем он нужен и как с этим жить'
    assert str(video2) == 'MoscowPython Meetup 78 - вступление'
