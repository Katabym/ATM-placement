import argparse
import subprocess
import sys
from functions import *

def main():
    atms = argparse.ArgumentParser(description='Расчет новых расстояний между банкоматами')
    atms.add_argument('--tests', action='store_true', help='Запускает тестовые варианты')
    atms.add_argument('--v1_3', action='store_true', help='Запускает тест для функции 1.3 версии')
    atms.add_argument('--v2_2_1', action='store_true', help='Запускает тест для функции 2.2.1 версии')
    atms.add_argument('--v2_2_0', action='store_true', help='Запускает тест для функции 2.2.0 версии')
    atms.add_argument('--n', type=int, default=3, help='Количество расстояний между банкоматами')
    atms.add_argument('--k', type=int, default=3, help='Количество новых банкоматов')
    atms.add_argument('--L', type=int, nargs='+', default=[10, 5, 8], help='Список расстояний')


    args = atms.parse_args()

    try:
        if args.n == len(args.L):
            if args.tests:
                # Запускаем tests.py
                subprocess.run([sys.executable, 'tests.py'])
            elif args.v1_3:
                # Запускаем функцию 1ю3 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_ver_1_3(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 1.3 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 1.3 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            elif args.v2_2_1:
                # Запускаем функцию 2.2.1 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_2_2_1(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 2.2.1 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 2.2.1 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            elif args.v2_2_0:
                # Запускаем функцию 2.2.0 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_2_2_0(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 2.2.0 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 2.2.0 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            else:
                print("Аргумент отсутствует.")
        else:
            # На случай если поменяли n или L по одиночке
            print("Количество промежутков n не соответствует списку длинн этих промежутков L")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
















json-to-e.....
import json
import pandas as pd
import os
import re


def clean_cons_text(text):
    """Очищает текст от лишних фраз в поле cons"""
    if not text:
        return text

    # Удаляем ненужные фразы
    patterns = [
        r'Преимущества и льготы.*',
        r'Полезный отзыв\d*',
        r'Ссылка на отзыв',
        r'Ответить от лица компании'
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text)

    # Убираем лишние пробелы и точки
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\.\.+', '.', text)
    text = re.sub(r'\s\.', '.', text)

    return text

def json_to_xlsx():
    """Обрабатывает все JSON файлы, преобразует в XLSX и удаляет исходные файлы"""

    # Находим все JSON файлы в текущей директории
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]

    if not json_files:
        print("Не найдено JSON файлов для обработки")
        return

    all_data = []

    for json_file in json_files:
        try:
            # Извлекаем название компании из имени файла
            company_name = re.sub(r'_\d+\.json$', '', json_file)
            company_id = re.search(r'_(\d+)\.json$', json_file)
            company_id = company_id.group(1) if company_id else "unknown"

            # Читаем JSON файл
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Обрабатываем каждый отзыв
            for review in data.get('reviews', []):
                # Очищаем поле cons
                if 'cons' in review:
                    review['cons'] = clean_cons_text(review['cons'])

                # Формируем полный текст отзыва
                full_text = ""
                if review.get('pros'):
                    full_text += f"Что нравится: {review['pros']}. "
                if review.get('cons'):
                    full_text += f"Что можно улучшить: {review['cons']}."

                # Формируем запись для XLSX
                record = {
                    'id': '',  # Уникальный номер статьи (нет данных)
                    'created_date': review.get('date', ''),  # Время публикации статьи
                    'title': '',  # Заголовок статьи (нет данных)
                    'url': f"https://dreamjob.ru/employers/{company_id}",  # Ссылка на статью
                    'source': 'DreamJob.ru',  # Источник статьи
                    'text': full_text,  # Текст отзыва/статьи
                    'download_date': data.get('parsed_date', ''),  # Дата загрузки
                    'author': review.get('position', ''),  # Автор
                    'address': '',  # Адрес (нет данных)
                    'rating': review.get('rating', ''),  # Рейтинг
                    'response': company_name,  # Ответ (название компании)
                    'response_date': ''  # Дата ответа (нет данных)
                }

                all_data.append(record)

            #print(f"Обработан файл: {json_file}")

        except Exception as e:
            print(f"Ошибка при обработке файла {json_file}: {e}")

    # Удаляем JSON файлы после успешного сохранения
    for json_file in json_files:
        try:
            os.remove(json_file)
            #print(f"Удален файл: {json_file}")
        except Exception as e:
            print(f"Ошибка при удалении файла {json_file}: {e}")

    # Возвращаем DataFrame
    if not all_data:
        print("Нет данных для сохранения")
        return # Завершаем функцию, если нет данных для сохранения

    return pd.DataFrame(all_data)





parse-dream
import requests
from bs4 import BeautifulSoup
import json
import time
from config import dzo_company
import re
import urllib3


# Отключаем предупреждения о SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_total_reviews_count(company_id):
    """
    Получает общее количество отзывов о компании на DreamJob.ru

    Args:
        company_id (int/str): ID компании в URL

    Returns:
        int: Количество отзывов или 0 при ошибке
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    try:
        url = f'https://dreamjob.ru/employers/{company_id}'
        response = requests.get(url, headers=headers, timeout=2, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем элемент с количеством отзывов
        reviews_count_element = soup.find('span', class_='tabs__count')
        if reviews_count_element:
            count_text = reviews_count_element.get_text()
            # Убираем неразрывные пробелы и преобразуем в число
            count_text = count_text.replace('&nbsp;', '').replace('\xa0', '')
            return int(count_text)

        return 0
    except Exception as e:
        #print(f"Нет отзывов {company_id}: {e}")
        return 0

def parse_dreamjob_reviews(company_id, max_reviews=None):
    """
    Парсит отзывы о компании с DreamJob.ru

    Args:
        company_id (int/str): ID компании в URL
        max_reviews (int): Максимальное количество отзывов для парсинга

    Returns:
        list: Список словарей с информацией об отзывах
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': f'https://dreamjob.ru/employers/{company_id}',
    }

    reviews = []
    page = 1
    max_pages = 50

    while page <= max_pages:
        # Прерываем парсинг, если достигли лимита отзывов
        if max_reviews and len(reviews) >= max_reviews:
            break

        url = f'https://dreamjob.ru/employers/{company_id}?page={page}'

        try:
            # print(f"Парсинг страницы {page}: {url}")
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.raise_for_status()

            # Проверяем не перенаправлены ли мы на главную (значит, страниц больше нет)
            if response.url == 'https://dreamjob.ru/':
                # print("Перенаправление на главную страницу - завершаем парсинг")
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            # Ищем контейнеры с отзывами
            review_elements = soup.find_all('div', class_='review')

            if not review_elements:
                # print(f"На странице {page} не найдено отзывов - завершаем парсинг")
                break

            # print(f"На странице {page} найдено {len(review_elements)} отзывов")

            for review in review_elements:
                try:
                    # Прерываем парсинг, если достигли лимита отзывов
                    if max_reviews and len(reviews) >= max_reviews:
                        break

                    # Извлекаем должность из h2 с классом review__header-title
                    position_element = review.find('h2', class_='review__header-title')
                    position = position_element.get_text(strip=True) if position_element else 'Должность не указана'


                    # Сначала находим элемент с классом, содержащим dj-rating
                    rating_element = review.find('div', class_=re.compile(r'dj-rating--\d+'))

                    # Проверяем наличие нужного элемента
                    if rating_element:
                        # Получаем текст элемента, очищенный от пробелов и переносов строк
                        rating_text = rating_element.get_text(strip=True)

                        # Используем регулярное выражение для нахождения числа формата X.X
                        rating_match = re.search(r'(\d+\.\d+|\d+,?\d*)', rating_text)

                        if rating_match:
                            # Преобразовываем строку в float, заменяя запятую точкой (если присутствует)
                            rating = float(rating_match.group().replace(',', '.'))

                    # Извлекаем дату из блока с классом tags__item tags__item_grey
                    date_element = review.find('div', class_='tags__item tags__item_grey')
                    date = date_element.get_text(strip=True) if date_element else 'Дата не указана'

                    # Очищаем дату от лишних пробелов и символов
                    date = re.sub(r'\s+', ' ', date).strip()

                    # Извлекаем текст отзыва из разделов "Что нравится?" и "Что можно улучшить?"
                    pros_text = ""
                    cons_text = ""

                    # Ищем раздел "Что нравится?"
                    pros_title = review.find('div', class_=re.compile(r'review__title.*'))
                    if pros_title and 'нравится' in pros_title.get_text():
                        # Берем следующий элемент после заголовка
                        next_element = pros_title.next_sibling
                        while next_element and (not hasattr(next_element, 'get') or
                                                (hasattr(next_element, 'get') and
                                                 'review__title' not in next_element.get('class', []))):
                            if hasattr(next_element, 'get_text'):
                                text = next_element.get_text(strip=True)
                                if text and not re.search(r'tags__item', str(next_element)):
                                    pros_text += text + " "
                            next_element = next_element.next_sibling

                    # Ищем раздел "Что можно улучшить?"
                    cons_title = None
                    for title in review.find_all('div', class_='review__title'):
                        if 'улучшить' in title.get_text():
                            cons_title = title
                            break

                    if cons_title:
                        # Берем следующий элемент после заголовка
                        next_element = cons_title.next_sibling
                        while next_element and (not hasattr(next_element, 'get') or
                                                (hasattr(next_element, 'get') and
                                                 'review__title' not in next_element.get('class', []))):
                            if hasattr(next_element, 'get_text'):
                                text = next_element.get_text(strip=True)
                                if text and not re.search(r'tags__item', str(next_element)):
                                    cons_text += text + " "
                            next_element = next_element.next_sibling

                    # Формируем полный текст отзыва
                    full_review_text = ""
                    if pros_text:
                        full_review_text += f"Что нравится: {pros_text.strip()}. "
                    if cons_text:
                        full_review_text += f"Что можно улучшить: {cons_text.strip()}."

                    review_data = {
                        'position': position,
                        'rating': rating,
                        'date': date,
                        'review_text': full_review_text.strip(),
                        'pros': pros_text.strip(),
                        'cons': cons_text.strip()
                    }

                    reviews.append(review_data)
                    # print(f"Добавлен отзыв для должности '{position}' с рейтингом {rating}, дата: {date}")

                except Exception as e:
                    print(f"Ошибка при парсинге отзыва: {e}")
                    continue

            page += 1
            # Задержка 2 секунды между запросами
            time.sleep(2)

        except requests.RequestException as e:
            print(f"Ошибка при запросе страницы {page}: {e}")
            break

    return reviews

def save_reviews_to_json(reviews, company_id, name='file'):
    """Сохраняет отзывы в JSON файл"""
    if not reviews:
        # print("Нет отзывов для сохранения")
        return

    filename = f'{name}_{company_id}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'company_id': company_id,
            'reviews': reviews,
            'total_reviews': len(reviews),
            'parsed_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, ensure_ascii=False, indent=2)

    # print(f"Данные сохранены в файл: {filename}")

def update_config_file(company, new_count):
    """Обновляет config.py файл с новым количеством отзывов"""
    try:
        # Читаем текущий config.py
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Находим и обновляем запись для компании
        pattern = re.compile(rf"'{company}':\s*\[[^]]*\]")
        replacement = f"'{company}': ['{dzo_company[company][0]}', {new_count}]"
        updated_content = re.sub(pattern, replacement, content)

        # Записываем обновленный контент обратно в файл
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # print(f"Обновлен config.py для {company}: новое количество отзывов = {new_count}")

        # Обновляем также глобальную переменную dzo_company
        dzo_company[company][1] = new_count

    except Exception as e:
        print(f"Ошибка при обновлении config.py: {e}")

# Использование
def start_parser():
    for company, data in dzo_company.items():
        company_id = data[0]
        last_review_count = data[1]

        # Получаем текущее количество отзывов
        current_review_count = get_total_reviews_count(company_id)
        #print(f"Компания: {company}, ID: {company_id}")
        #print(f"Последнее известное количество отзывов: {last_review_count}")
        #print(f"Текущее количество отзывов на сайте: {current_review_count}")

        # Если количество отзывов не изменилось, пропускаем
        if current_review_count == last_review_count:
            #print(f"Количество отзывов не изменилось, пропускаем {company}")
            continue

        # Если количество отзывов увеличилось, парсим разницу
        reviews_to_parse = current_review_count - last_review_count
        #print(f"Найдено {reviews_to_parse} новых отзывов для {company}")

        # Получаем отзывы (только новые)
        reviews = parse_dreamjob_reviews(company_id, max_reviews=reviews_to_parse)

        # Сохраняем результаты
        save_reviews_to_json(reviews, company_id, company)

        # Обновляем config.py с новым количеством отзывов
        update_config_file(company, current_review_count)
    print("Парсинг завершена.")
