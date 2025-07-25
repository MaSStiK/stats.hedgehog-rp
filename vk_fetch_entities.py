#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vk_fetch_entities.py

Скрипт создает JSON-файл vk_entities.json, содержащий список всех участников (пользователей и групп)
с их именами и ссылками на аватарки в разрешении 100x100.

- Берет ID из summary_stats.json -> overview.messages_per_user_per_year
- Если ID > 0: пользователь, получаем через users.get (поле photo_100)
- Если ID < 0: группа, получаем через groups.getById (photo_100)

Требуется:
    pip install vk_api

Настройте переменные ниже перед запуском скрипта.
"""
import json
from vk_api import VkApi
import os
from dotenv import load_dotenv
load_dotenv()

# === Параметры ===
TOKEN = os.getenv("TOKEN")
INPUT_FILE = 'summary_stats.json'
OUTPUT_FILE = 'vk_entities.json'

# Размер чанка для запросов VK API
USERS_BATCH = 1000
GROUPS_BATCH = 1000


def chunked(seq, size):
    """Разбивает список на части длиной size"""
    return (seq[i:i+size] for i in range(0, len(seq), size))


def fetch_entities():
    # Загрузка summary
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        summary = json.load(f)

    user_year = summary.get('overview', {}).get('messages_per_user_per_year', {})
    all_ids = [int(uid) for uid in user_year.keys()]

    # Разделяем на пользователей (>0) и группы (<0)
    user_ids = [uid for uid in all_ids if uid > 0]
    group_ids = [abs(uid) for uid in all_ids if uid < 0]

    vk = VkApi(token=TOKEN).get_api()
    entities = []

    # Запрашиваем пользователей
    for batch in chunked(user_ids, USERS_BATCH):
        users = vk.users.get(user_ids=','.join(map(str, batch)), fields='photo_100')
        for u in users:
            entities.append({
                'id': u['id'],
                'type': 'user',
                'name': f"{u.get('first_name','')} {u.get('last_name','')}".strip(),
                'avatar': u.get('photo_100')
            })

    # Запрашиваем группы
    for batch in chunked(group_ids, GROUPS_BATCH):
        # Используем правильный параметр group_ids
        groups = vk.groups.getById(group_ids=','.join(map(str, batch)), fields='photo_100')
        for g in groups:
            entities.append({
                'id': -g['id'],
                'type': 'group',
                'name': g.get('name'),
                'avatar': g.get('photo_100')
            })

    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(entities, f, ensure_ascii=False, indent=4)

    print(f"Сохранено {len(entities)} entities в '{OUTPUT_FILE}'")


if __name__ == '__main__':
    fetch_entities()
