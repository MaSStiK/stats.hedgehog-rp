#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vk_stats_report.py

Скрипт генерирует статистику по сообщениям ВКонтакте,
которые уже выгружены в файлы messages_<year>.json.

Выходной JSON (summary_stats.json) имеет структуру:
{
  "overview": {
    "total_messages": <int>,
    "messages_per_user_per_year": {"<user_id>": {"<year>": <int>, ...}, ...}
  },
  "years": {
    "<year>": {
      "total_messages": <int>,
      "messages_per_month": {"YYYY-MM": <int>, ...},
      "messages_per_user": {"<user_id>": <int>, ...},
      "messages_per_user_per_month": {"<user_id>": {"YYYY-MM": <int>, ...}, ...}
    },
    ...
  }
}

Требования:
    pip install pandas

Использование:
    python vk_stats_report.py
"""
import json
import glob
import os
from collections import defaultdict
import pandas as pd

# Параметры
INPUT_DIR     = 'messages'
INPUT_PATTERN = os.path.join(INPUT_DIR, 'messages_*.json')
SUMMARY_FILE  = 'summary_stats.json'

all_msgs = []
for filepath in glob.glob(INPUT_PATTERN):
    with open(filepath, 'r', encoding='utf-8') as f:
        msgs = json.load(f)
        all_msgs.extend(msgs)

if not all_msgs:
    print('Нет сообщений для анализа. Проверьте файлы messages_*.json.')
    exit(1)

# Шаг 2: Создание DataFrame
df = pd.DataFrame(all_msgs)
if 'date' not in df.columns or 'from_id' not in df.columns:
    print('Неправильный формат данных: отсутствуют поля date или from_id.')
    exit(1)

df['datetime'] = pd.to_datetime(df['date'], unit='s')
df['year'] = df['datetime'].dt.year
df['year_month'] = df['datetime'].dt.to_period('M').astype(str)

# --- Собираем статистику по годам ---
years_stats = {}
for year, group in df.groupby('year'):
    year_str = str(year)
    total_messages = int(len(group))

    # Полный список месяцев за год
    all_months = pd.period_range(
        start=f'{year}-01', end=f'{year}-12', freq='M'
    ).astype(str)

    # Сообщения по месяцам
    actual_month_counts = group.groupby('year_month').size()
    messages_per_month = {
        month: int(actual_month_counts.get(month, 0)) for month in all_months
    }

    # Сообщения по пользователям
    messages_per_user = group.groupby('from_id').size().to_dict()

    # Сообщения каждого пользователя по месяцам (заполняем пропущенные месяцы)
    user_monthly = defaultdict(dict)
    grouped = group.groupby(['from_id', 'year_month']).size()

    for user_id in group['from_id'].unique():
        for month in all_months:
            user_monthly[str(user_id)][month] = int(grouped.get((user_id, month), 0))

    years_stats[year_str] = {
        'total_messages': total_messages,
        'messages_per_month': messages_per_month,
        'messages_per_user': {str(uid): int(cnt) for uid, cnt in messages_per_user.items()},
        'messages_per_user_per_month': user_monthly
    }

# --- Общая статистика за все года ---
overall_total = len(df)
overall_user_year = defaultdict(lambda: defaultdict(int))
for (uid, yr), cnt in df.groupby(['from_id', 'year']).size().items():
    overall_user_year[str(uid)][str(yr)] = int(cnt)

overview = {
    'total_messages': int(overall_total),
    'messages_per_user_per_year': overall_user_year
}

# Итоговый словарь
summary = {
    'overview': overview,
    'years': years_stats
}

# Сохраняем в JSON
with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=4)

print(f"Сохранена статистика в {SUMMARY_FILE}")
