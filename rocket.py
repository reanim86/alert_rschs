import asyncio
from telethon import TelegramClient, connection
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
        self.client = TelegramClient(
            'export_session', api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
            proxy=('win.sosproxy.space', 443, 'ee477ccce74a28c13a2ef6ec9e01510c3164726976652e676f6f676c652e636f6d')
        )

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

def comprassion(tg, json_file):
    """
    сравнение сообщений
    :param tg: полученные сообщения из канала ТГ
    :param json_file: сохраненные ранее сообщения
    :return: сообщение о РО
    """
    n = 15
    res = 'none'
    while n != 0:
        n -= 1
        if tg[n]['id'] > json_file[0]['id']:
            res = tg[n]['text']
    return res

def alarm(text):
    """
    анализ последнего сообщения
    :param text: текст последнего сообщения
    :return: уведомление
    """
    if 'Ракетная опасность' in text:
        return 'Ракетная опасность'
    if 'В укрытия' in text:
        return 'Ракетная опасность'
    if 'Авиационная опасность' in text:
        return 'Ракетная опасность'
    if 'Отбой ракетной опасности' in text:
        return 'Отбой ракетной опасности'
    return


async def main():
    exporter = ChannelExporter(API_ID, API_HASH, PHONE_NUMBER)
    res_tg = await exporter.export_to_json(CHANNEL_USERNAME, limit=15)
    json = import_json()
    tg_msg = comprassion(res_tg, json)
    print(alarm(tg_msg))

    create_json(res_tg)



if __name__ == '__main__':
    asyncio.run(main())