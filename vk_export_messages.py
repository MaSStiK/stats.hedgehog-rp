#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт выгружает все сообщения из беседы ВКонтакте и сохраняет их в отдельные JSON-файлы по годам,
с отображением прогресса загрузки сообщений, используя библиотеку vk_api.

Перед запуском внутри этого скрипта задайте следующие переменные:
    TOKEN   — ваш VK API access token
    PEER_ID — ID беседы (user_id или 2000000000+chat_id)

Требуется:
    pip install vk_api
"""

import json
import time
import os
from datetime import datetime
import vk_api
from dotenv import load_dotenv
load_dotenv()

# Задайте переменные здесь:
TOKEN = os.getenv("TOKEN")
PEER_ID = 2000000922

STATE_FILE = "vk_state.json"
FIELDS = ["id", "date", "from_id", "text"]
MESSAGES_DIR = "messages"
ACTIONS_DIR = "actions"
MESSAGES_FILE_TEMPLATE = os.path.join(MESSAGES_DIR, "messages_{year}.json")
ACTIONS_FILE_TEMPLATE = os.path.join(ACTIONS_DIR, "actions_{year}.json")
SAVE_INTERVAL = 5000

def ensure_dirs():
    os.makedirs(MESSAGES_DIR, exist_ok=True)
    os.makedirs(ACTIONS_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('offset', 0)
    return 0

def save_state(offset: int):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'offset': offset}, f)

def save_buffer(buffer: list):
    by_year = {}
    for msg in buffer:
        year = datetime.fromtimestamp(msg['date']).year
        by_year.setdefault(str(year), []).append(msg)

    for year, msgs in by_year.items():
        filename = MESSAGES_FILE_TEMPLATE.format(year=year)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = []
        existing.extend(msgs)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)

def save_actions_buffer(actions: list):
    by_year = {}
    for msg in actions:
        year = datetime.fromtimestamp(msg['date']).year
        by_year.setdefault(str(year), []).append(msg)

    for year, msgs in by_year.items():
        filename = ACTIONS_FILE_TEMPLATE.format(year=year)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = []
        existing.extend(msgs)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)

def fetch_and_save(vk, peer_id: int, delay: float = 0.34):
    ensure_dirs()
    offset = load_state()
    count = 200
    total = None
    fetched = offset
    buffer = []
    actions_buffer = []
    last_saved_offset = offset

    while True:
        resp = vk.messages.getHistory(peer_id=peer_id, offset=offset, count=count, rev=1)
        items = resp.get('items', [])

        if total is None:
            total = resp.get('count')

        if not items:
            break

        for msg in items:
            if 'action' in msg:
                action_msg = {key: msg.get(key) for key in FIELDS}
                action_msg['action'] = msg.get('action')
                actions_buffer.append(action_msg)
            else:
                filtered_msg = {key: msg.get(key) for key in FIELDS}
                buffer.append(filtered_msg)

        offset += len(items)
        fetched += len(items)

        if len(buffer) >= SAVE_INTERVAL or len(actions_buffer) >= SAVE_INTERVAL:
            print(f"Сохраняем {len(buffer)} обычных и {len(actions_buffer)} action-сообщений...")
            if buffer:
                save_buffer(buffer)
                buffer.clear()
            if actions_buffer:
                save_actions_buffer(actions_buffer)
                actions_buffer.clear()
            last_saved_offset = offset
            save_state(last_saved_offset)
            print(f"Состояние сохранено: offset={last_saved_offset}")

        if total:
            print(f"Загружено {fetched} из {total} сообщений")
        else:
            print(f"Загружено {fetched} сообщений...")

        if len(items) < count:
            break

        time.sleep(delay)

    if buffer or actions_buffer:
        print(f"Сохраняем оставшиеся {len(buffer)} обычных и {len(actions_buffer)} action-сообщений...")
        if buffer:
            save_buffer(buffer)
        if actions_buffer:
            save_actions_buffer(actions_buffer)
        save_state(offset)
        print(f"Состояние сохранено: offset={offset}")

    print("Выгрузка завершена.")

if __name__ == '__main__':
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    fetch_and_save(vk, PEER_ID)
