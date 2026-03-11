import asyncio
from telethon import TelegramClient
import csv
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
CHANNEL_USERNAME = '@LiveOnlain'


class ChannelExporter:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('export_session', api_id, api_hash)

    # async def export_to_csv(self, channel_username, limit=1000, filename='channel_messages.csv'):
    #     """Экспорт сообщений в CSV"""
    #     await self.client.start(phone=self.phone_number)
    #
    #     try:
    #         channel = await self.client.get_entity(channel_username)
    #
    #         with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    #             fieldnames = ['id', 'date', 'text', 'views', 'forwards', 'has_media', 'media_type']
    #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #             writer.writeheader()
    #
    #             async for message in self.client.iter_messages(channel, limit=limit):
    #                 media_type = None
    #                 if message.media:
    #                     if hasattr(message.media, 'photo'):
    #                         media_type = 'photo'
    #                     elif hasattr(message.media, 'document'):
    #                         media_type = 'document'
    #                     elif hasattr(message.media, 'video'):
    #                         media_type = 'video'
    #
    #                 writer.writerow({
    #                     'id': message.id,
    #                     'date': message.date.isoformat(),
    #                     'text': message.text.replace('\n', ' ') if message.text else '',
    #                     'views': message.views or 0,
    #                     'forwards': message.forwards or 0,
    #                     'has_media': bool(message.media),
    #                     'media_type': media_type or ''
    #                 })
    #
    #         print(f"Экспорт завершен! Сохранено в {filename}")
    #
    #     except Exception as e:
    #         print(f"Ошибка при экспорте: {e}")
    #     finally:
    #         await self.client.disconnect()

    async def export_to_json(self, channel_username, limit=1000,
                             filename=f'{datetime.now().strftime("%Y-%m-%d-%H-%m")}.json'):
        """Экспорт сообщений в JSON"""
        await self.client.start(phone=self.phone_number)

        try:
            channel = await self.client.get_entity(channel_username)
            messages = []

            async for message in self.client.iter_messages(channel, limit=limit):
                msg_data = {
                    'id': message.id,
                    'date': message.date.isoformat(),
                    'text': message.text,
                    'views': message.views,
                    'forwards': message.forwards,
                    'has_media': bool(message.media)
                }

                if message.media:
                    if hasattr(message.media, 'photo'):
                        msg_data['media_type'] = 'photo'
                    elif hasattr(message.media, 'document'):
                        msg_data['media_type'] = 'document'

                messages.append(msg_data)

            # with open(filename, 'w', encoding='utf-8') as f:
            #     json.dump(messages, f, ensure_ascii=False, indent=2)

            # print(f"Экспорт завершен! Сохранено в {filename}")
            return messages

        except Exception as e:
            print(f"Ошибка при экспорте: {e}")
        finally:
            await self.client.disconnect()

def create_json(msg_dict):
    """
    Запись результатов в json
    :param msg_dict: словарь с сообщениями
    """
    with open('message.json', 'w', encoding='utf-8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=2)

def import_json():
    """
    Распаковка json файла
    :return: Словарь с данными из json файла
    """
    with open('message.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


async def main():
    exporter = ChannelExporter(API_ID, API_HASH, PHONE_NUMBER)

    # Экспорт в CSV
    # await exporter.export_to_csv(CHANNEL_USERNAME, limit=100)

    # Экспорт в JSON
    res_tg = await exporter.export_to_json(CHANNEL_USERNAME, limit=5)
    json = import_json()
    # create_json(res)
    # print(res)
    # print(import_json())

if __name__ == '__main__':
    asyncio.run(main())