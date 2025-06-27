import requests
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s')

API_URL = 'https://ru.wikipedia.org/w/api.php'


def fetch_category_members(category_title):
    members = []
    cmcontinue = None

    while True:
        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': category_title,
            'cmlimit': '500',
            'format': 'json'
        }
        if cmcontinue:
            params['cmcontinue'] = cmcontinue

        response = requests.get(API_URL, params=params)
        data = response.json()

        batch = data.get('query', {}).get('categorymembers', [])
        logging.info(f'Получено {len(batch)} записей')
        members.extend(batch)

        if 'continue' in data:
            cmcontinue = data['continue']['cmcontinue']
        else:
            break
    return members


def count_by_first_letter(titles):
    counts = {}
    for title in titles:
        first_letter = title[0].upper()
        counts[first_letter] = counts.get(first_letter, 0) + 1
    return counts


def main():
    category = 'Категория:Животные_по_алфавиту'
    members = fetch_category_members(category)

    counts = {}
    for member in members:
        title = member['title']
        first_letter = title[0].upper()
        counts[first_letter] = counts.get(first_letter, 0) + 1

    sorted_counts = sorted(counts.items(), key=lambda x: x[0])

    #  Файла сохраняется в корень проекта
    with open('beasts.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for letter, count in sorted_counts:
            writer.writerow([letter, count])

    logging.info(
        f'Всего записей: {len(members)}. '
        f'Результат записан в beasts.csv'
        )


if __name__ == '__main__':
    main()
