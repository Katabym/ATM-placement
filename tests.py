
from functions import optimize_atm_locations_ver_1_3 as ver1_3
from functions import optimize_atm_locations_2_2_1 as ver2_2_1
from functions import optimize_atm_locations_2_2_0 as ver2_2_0


def Test_versions(n, k, L, test_number=1):
    print(f"Test number {test_number}")
    print(f"Test parametrs: {n, k, L}")
    print('>>>>>>')
    try:
        result = ver1_3(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 1.3 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 1.3 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    try:
        result = ver2_2_1(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 2.2.1 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 2.2.1 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    try:
        result = ver2_2_0(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 2.2.0 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 2.2.0 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    print("~" * 50)

# Test 1
# 4 bankomat
n = 3
# 3 new bankomat
k = 3
L = [10, 5, 8]

Test_versions(n, k, L)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 2
# 6 bankomat
n = 5
# 8 new bankomat
k = 8
L = [10, 5, 8, 13, 2]

Test_versions(n, k, L, 2)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 3
# 6 bankomat
n = 5
# 4 new bankomat
k = 4
L = [15, 7, 12, 9, 6]

Test_versions(n, k, L, 3)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 4
# 3 bankomat
n = 2
# 5 new bankomat
k = 5
L = [20, 10]

Test_versions(n, k, L, 4)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 5
# 8 bankomat
n = 7
# 6 new bankomat
k = 6
L = [8, 12, 5, 9, 11, 7, 15]

Test_versions(n, k, L, 5)






import time
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Set, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from tqdm.auto import tqdm
import re
import os
def parse_months_ago_from_review_date(date_text: str) -> int:
    """
    Преобразует текст даты отзыва (например, '3 года назад', '2 недели назад')
    в количество месяцев назад.
    Возвращает:
        - 0, если < 1 месяца (часы, дни, недели)
        - N, если месяцы или годы
    """
    if not isinstance(date_text, str):
        return 999  # неизвестно → считаем старым

    # Убираем "Изменено"
    date_text = re.sub(r'^Изменено\s*', '', date_text, flags=re.IGNORECASE).strip()

    # Если есть часы, дни, недели → это < 1 месяца
    if any(word in date_text for word in ['час', 'день', 'дня', 'дней', 'недел', 'минут', 'секунд', 'вчера', 'сегодня']):
        return 0

    # Ищем годы/месяцы
    match = re.search(r'(\d+)\s*(год|лет|месяц|месяцев|месяца)', date_text)
    if not match:
        return 0  # например, "только что"

    num = int(match.group(1))
    unit = match.group(2)

    if 'год' in unit or 'лет' in unit:
        return num * 12
    elif 'месяц' in unit or 'месяцев' in unit or 'месяца' in unit:
        return num
    else:
        return 0

def select_sort_by_newest(driver):
    """
    Выбирает сортировку отзывов 'Сначала новые' на странице Google Maps.
    """
    try:
        # 1. Находим и кликаем по кнопке сортировки
        sort_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Самые релевантные"]'))
        )
        print("🔽 Кликаем по кнопке сортировки...")
        sort_button.click()
        time.sleep(1)

        # 2. Ждём появления выпадающего меню и ищем пункт "Сначала новые"
        # Ищем div с role="menuitemradio", внутри которого есть div.mLuXec с нужным текстом
        newest_option = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable(
                (By.XPATH, '//div[@role="menuitemradio"]//div[@class="mLuXec" and text()="Сначала новые"]')
            )
        )
        # Поднимаемся до кликабельного родителя (сам menuitemradio)
        clickable_item = newest_option.find_element(By.XPATH, './ancestor::div[@role="menuitemradio"]')
        print("🆕 Выбираем 'Сначала новые'...")
        clickable_item.click()
        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Не удалось выбрать сортировку 'Сначала новые': {e}")



def extract_name_in_quotes(text: str) -> str:

    if not isinstance(text, str):
        return ""
    
    pattern = r'(["«„‘‹])([^"»“’›]+?)\1|«([^»]+?)»|„([^“]+?)“|‹([^›]+?)›'
    match = re.search(pattern, text)
    
    if match:
        for group in match.groups():
            if group and isinstance(group, str):
                return group.strip()
    return ""

def configure_chrome_options():
    """
    Sets up chrome_options for selenium webdriver.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.71')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--headless')
    return chrome_options

def scroll_down(driver, down_keys: int = 50) -> None:

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    actions = ActionChains(driver)
    for _ in range(down_keys):
        actions.send_keys(Keys.DOWN)
        actions.perform()
        time.sleep(0.05)

def scroll_up(driver, up_keys: int = 5) -> None:

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    actions = ActionChains(driver)
    for _ in range(up_keys):
        actions.send_keys(Keys.UP)
        actions.perform()
        time.sleep(0.5)

def scroll_down_by_element(driver, scroll_by: str, scrolling_element_tag: str,
                           scroll_up_needed: bool = False,
                           scroll_index: int = 0) -> None:

    scrolling_element = driver.find_elements(scroll_by, scrolling_element_tag)[scroll_index]
    driver.execute_script('return arguments[0].scrollHeight', scrolling_element)
    time.sleep(2)
    last_height = -1
    while True:
        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scrolling_element)
        new_height = driver.execute_script('return arguments[0].scrollHeight', scrolling_element)
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(1.5)
        if scroll_up_needed:
            scroll_up(driver, 5)
        time.sleep(1.5)

def get_links_to_offices_google(driver, url: str, required_place_type: str = None) -> List[str]:
    """
    Автоматически определяет:
    - Если это страница поиска — скроллит и собирает ссылки на все офисы.
    - Если это страница одного офиса — возвращает список из одной текущей ссылки.
    """
    driver.get(url)
    time.sleep(2)  # Даём время на загрузку

    print("🔍 Анализируем страницу: это список офисов или карточка одного офиса?")

    # Проверяем, есть ли контейнер списка офисов — ПОЛНЫЙ НАБОР КЛАССОВ
    try:
        print("🔎 Ищем контейнер по полному классу: m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd")

        results_container = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd'
            ))
        )
        print("✅ Контейнер найден!")

        # 🔍 Ищем ВНУТРИ него  скроллящийся элемент
        try:
            inner_scroller = results_container.find_element(
                By.XPATH,
                './/div[contains(@class, "kA9KIf") and contains(@class, "dS8AEf")]'
            )
            print("🔍 Найден ВНУТРЕННИЙ скроллящийся элемент")
            results_container = inner_scroller
        except Exception as e_inner:
            print("ℹ️  Внутренний скроллер не найден")

        # Прокручиваем к началу
        driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", results_container)
        time.sleep(2)
        # ============ НАЧАЛО СКРОЛЛА И СБОРА ССЫЛОК ============
        print("Начинаем прокрутку для загрузки всех офисов...")

        collected_count = 0
        scroll_pause = 2  
        max_empty_scrolls = 3
        empty_scroll_count = 0

        while empty_scroll_count < max_empty_scrolls:
            print(f"\n--- Попытка #{empty_scroll_count + 1} ---")
            
            # 🆕 СКРОЛЛИМ ЧЕРЕЗ scrollTop — это КЛЮЧЕВО!
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", results_container)
            print("⬇️  Прокрутили вниз...")
            time.sleep(scroll_pause)

            # Отладка: позиция скролла
            current_scroll = driver.execute_script("return arguments[0].scrollTop;", results_container)
            print(f"📉 Текущая позиция scrollTop: {current_scroll}")

            # Собираем офисы
            current_offices = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb')
            current_count = len(current_offices)
            print(f"🏢 Загружено офисов: {current_count}")

            if current_count == collected_count:
                empty_scroll_count += 1
                print(f"⚠️  Новых офисов нет ({empty_scroll_count}/{max_empty_scrolls})")
            else:
                empty_scroll_count = 0
                collected_count = current_count
                print("✅ Новые офисы загружены!")

            # Кнопка "Загрузить больше"
            try:
                more_button = driver.find_element(By.XPATH, '//span[text()="Загрузить больше" or text()="More"]')
                print("🔘 Найдена кнопка 'Загрузить больше' — кликаем...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_button)
                time.sleep(1)
                try:
                    more_button.click()
                except:
                    driver.execute_script("arguments[0].click();", more_button)
                time.sleep(scroll_pause + 2)
                empty_scroll_count = 0
                continue
            except:
                pass

        print("✅ Прокрутка завершена. Собираем ссылки...")

        links_to_offices = []

        try:
            if required_place_type:
                # Поддержка как строки, так и списка
                if isinstance(required_place_type, str):
                    place_types = [required_place_type]
                else:
                    place_types = list(required_place_type)

                print(f"🔍 Фильтруем офисы по типам: {place_types}")

                # Собираем все офисы
                all_offices = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb')
                for office in all_offices:
                    try:
                        # Ищем все span с типами (обычно это второй или третий span в W4Efsd)
                        type_elements = office.find_elements(By.XPATH, './/div[@class="W4Efsd"]//span')
                        found_types = [el.text.strip() for el in type_elements if el.text.strip()]

                        # Проверяем: есть ли пересечение с целевыми типами
                        if any(pt in found_types for pt in place_types):
                            link_element = office.find_element(By.TAG_NAME, 'a')
                            href = link_element.get_attribute('href')
                            if href and 'google.com/maps' in href:
                                links_to_offices.append(href)
                    except Exception as e_inner:
                        continue
            else:
                print("📋 Собираем все офисы (без фильтрации по типу)")
                all_offices = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK.THOPZb')
                for office in all_offices:
                    try:
                        link_element = office.find_element(By.TAG_NAME, 'a')
                        href = link_element.get_attribute('href')
                        if href and 'google.com/maps' in href:
                            links_to_offices.append(href)
                    except:
                        continue

        except Exception as e:
            print(f"Ошибка при сборе ссылок: {e}")

        unique_links = list(set(links_to_offices))
        print(f"🔗 Собрано {len(unique_links)} ссылок.")
        return unique_links
        # ============ КОНЕЦ СКРОЛЛА И СБОРА ССЫЛОК ============
        
    except Exception as e:
        print(f"ℹ️  Контейнер списка офисов не найден. Проверяем, является ли это страницей одного офиса...")

        try:
            title_element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))
            )
            print("✅ Найден заголовок офиса")
            print(f"🏷️  Название: {title_element.text.strip()}")
            return [driver.current_url]

        except Exception as e2:
            print(f"❌ Это не страница списка и не страница офиса. Пропускаем: {url}")
            return []

def parse_one_office_google_maps(driver, url: str, expected_name: str = None, legal_name_cleaned: str = None, search_name: str = None, is_hotel: bool = False) -> List[Dict[str, Any]]:
    """
    Собираем отзывы со страницы.
    """
    driver.get(url)
    time.sleep(3)
    
    try:
        address = driver.find_element(By.CSS_SELECTOR, 'div.Io6YTe.fontBodyMedium.kR99db').text
    except NoSuchElementException:
        address = "Адрес не найден"
    
    all_reviews = []
    title_matched = False
    matched_by = None

    try:
        title_element = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))
        )
        actual_name = title_element.text.strip()
        print(f"🔍 Фактическое название на странице: '{actual_name}'")

        # 🧭 Проверка 1: по search_name (название, по которому искали в Google Maps)
        if search_name:
            print(f"🧭 Проверка 1: совпадает ли с названием для поиска: '{search_name}'")
            pattern_search = r'\b' + re.escape(search_name) + r'\b'
            match_search = re.search(pattern_search, actual_name, re.IGNORECASE)
            if match_search:
                print(f"✅ Название совпадает с поисковым: '{search_name}' — продолжаем парсинг.")
                title_matched = True
                matched_by = "search_name"

        # 🧭 Проверка 2: по expected_name (Бизнес наименование), если ещё не совпало
        if not title_matched and expected_name:
            print(f"🧭 Проверка 2: совпадает ли с бизнес-названием: '{expected_name}'")
            pattern_expected = r'\b' + re.escape(expected_name) + r'\b'
            match_expected = re.search(pattern_expected, actual_name, re.IGNORECASE)
            if match_expected:
                print(f"✅ Название совпадает с бизнес-названием: '{expected_name}' — продолжаем парсинг.")
                title_matched = True
                matched_by = "expected_name"

        # 🧭 Проверка 3: по legal_name_cleaned (Юр. название из кавычек), если ещё не совпало
        if not title_matched and legal_name_cleaned:
            print(f"🧭 Проверка 3: совпадает ли с юр. названием: '{legal_name_cleaned}'")
            pattern_legal = r'\b' + re.escape(legal_name_cleaned) + r'\b'
            match_legal = re.search(pattern_legal, actual_name, re.IGNORECASE)
            if match_legal:
                print(f"✅ Название совпадает с юр. названием: '{legal_name_cleaned}' — продолжаем парсинг.")
                title_matched = True
                matched_by = "legal_name_cleaned"

        # ❌ Если ничего не совпало — пропускаем
        if not title_matched:
            print("❌ Ни одно из названий не совпало — пропускаем офис.")
            return []

    except Exception as e:
        print(f"⚠️ Не удалось проверить название офиса: {e}")
    try:
        # Ищем ВНУТРЕННИЙ div с текстом "Отзывы", затем поднимаемся до родительского <button>
        review_tab = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable(
                (By.XPATH, '//button[@role="tab"]//div[contains(text(), "Отзывы")]/ancestor::button')
            )
        )
        # Прокручиваем к элементу
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", review_tab)
        time.sleep(0.5)

        # Пытаемся кликнуть обычным способом
        try:
            review_tab.click()
        except ElementClickInterceptedException:
            # Если перехватили клик — используем JS-клик
            print("Обычный клик не сработал, используем JS-клик...")
            driver.execute_script("arguments[0].click();", review_tab)

        time.sleep(2)
        select_sort_by_newest(driver)
    except Exception as e:
        print(f"Не удалось найти или кликнуть на вкладку 'Отзывы': {e}")
        return all_reviews
   

    try:
        reviews_container = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'DxyBCb'))
        )
        time.sleep(2)

        all_reviews = []
        last_review_count = 0
        max_empty_scrolls = 5
        empty_scroll = 0
        stop_parsing = False

        while empty_scroll < max_empty_scrolls and not stop_parsing:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", reviews_container)
            time.sleep(2.5)

            current_reviews = driver.find_elements(By.CLASS_NAME, 'jJc9Ad')
            current_count = len(current_reviews)

            new_reviews_found = False

            for i in range(last_review_count, current_count):
                if stop_parsing:
                    break

                review = current_reviews[i]

                # Извлечение даты
                try:
                    if is_hotel:
                        date_element = review.find_element(By.CSS_SELECTOR, 'span.xRkPPb')
                        full_text = date_element.text.strip()
                        date = full_text.split(',')[0].strip() if ',' in full_text else full_text
                    else:
                        date = review.find_element(By.CLASS_NAME, 'rsqaWe').text.strip()
                except:
                    date = "Дата не найдена"

                # Проверка возраста
                months_ago = parse_months_ago_from_review_date(date)
                if months_ago > 36:
                    print(f"📅 Отзыв старше 3 лет ('{date}') — останавливаем сбор.")
                    stop_parsing = True
                    break

                # Извлечение текста
                try:
                    text = review.find_element(By.CLASS_NAME, 'wiI7pd').text.strip()
                except:
                    text = "Текст не найден"

                if text == "Текст не найден":
                    continue

                # Извлечение автора
                try:
                    author = review.find_element(By.CLASS_NAME, 'd4r55').text.strip()
                except:
                    author = "Автор не найден"

                # Извлечение рейтинга
                try:
                    if is_hotel:
                        rating_element = review.find_element(By.CSS_SELECTOR, 'span.fontBodyLarge.fzvQIb')
                        rating_text = rating_element.text.strip()
                        match = re.search(r'^(\d+)', rating_text)
                        rating = float(match.group(1)) if match else 0.0
                    else:
                        rating_span = review.find_element(By.CLASS_NAME, 'kvMYJc')
                        aria_label = rating_span.get_attribute('aria-label')
                        rating = float(re.search(r'(\d+\.?\d*)', aria_label).group(1))
                except:
                    rating = 0.0

                # Полезность
                try:
                    helpful_count = int(review.find_element(By.CLASS_NAME, 'pkWtMe').text.strip())
                except:
                    helpful_count = 0

                # Раскрыть текст (если есть "Ещё")
                try:
                    more_btn = review.find_element(By.CLASS_NAME, 'w8nwRe')
                    driver.execute_script("arguments[0].scrollIntoView(true);", more_btn)
                    more_btn.click()
                    time.sleep(0.3)
                    text = review.find_element(By.CLASS_NAME, 'wiI7pd').text.strip()
                except:
                    pass

                # Ответ организации
                try:
                    response_element = review.find_element(By.CLASS_NAME, 'nM6d2c')
                    response = response_element.find_element(By.CLASS_NAME, 'wiI7pd').text.strip()
                    response_date = review.find_element(By.CSS_SELECTOR, 'span.DZSIDd').text
                except:
                    response, response_date = np.nan, np.nan

                # Добавляем отзыв
                all_reviews.append({
                    'download_date': datetime.today(),
                    'source': 'https://www.google.com/maps/',
                    'category': 'отзыв',
                    'product': driver.title,
                    'url': url,
                    'date': date,
                    'product_name': np.nan,
                    'author': author,
                    'text': text,
                    'response': response,
                    'response_date': response_date,
                    'rating': float(rating),
                    'helpful_count': helpful_count,
                    'address': address
                })
                new_reviews_found = True

            if current_count == last_review_count or not new_reviews_found:
                empty_scroll += 1
            else:
                empty_scroll = 0
                last_review_count = current_count

        print(f"✅ Собрано {len(all_reviews)} свежих отзывов.")
        return all_reviews

    except Exception as e:
        print(f"Ошибка при парсинге отзывов: {e}")
        return all_reviews

def format_and_save_dataframe(df_with_reviews: pd.DataFrame, search_years: Set[int]) -> pd.DataFrame:
    """

    """
    output_dir = "google_maps_towns_output"
    os.makedirs(output_dir, exist_ok=True)  
    if not df_with_reviews.empty:
        df_with_reviews.dropna(subset=['text'], inplace=True)
        df_with_reviews.drop_duplicates(inplace=True)
        df_with_reviews.reset_index(drop=True, inplace=True)
    
    print(f'Найдено {len(df_with_reviews)} отзывов.')
    
    if not df_with_reviews.empty:
        import re
        source = df_with_reviews['source'].unique().tolist()[0]
        src_name = re.search(r'https?://(.+?)/', source).group(1)
        src_name = re.sub(r'[^0-9a-zA-Zа-яА-ЯёЁ]', '_', src_name)
        src_name = re.sub(r'^www_', '', src_name)
        retr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        
        filename = f'google_maps_reviews_{retr_date}.xlsx'
        filepath = os.path.join(output_dir, filename)  # сохраняем в папку
        df_with_reviews.to_excel(filepath, index=False)
        print(f"Файл сохранен: {filepath}")

    return df_with_reviews

def parse_google_maps(
    link_to_offices: str,
    search_years: Set[int],
    required_place_type: Union[str, List[str], None] = None,
    business_name: str = None,
    legal_name_cleaned: str = None,
    search_name: str = None,
    is_hotel: bool = False
) -> pd.DataFrame:
    """
    Собирает отзывы с Google Maps.
    :param link_to_offices: URL поиска (например, "https://google.com/maps/search/...")
    :param search_years: Года для фильтрации (пока не используется в парсинге, но можно добавить)
    :param required_place_type: Тип места для фильтрации, например "Банк", "Кафе", "Аптека". Если None — собирает все.
    """
    chrome_options = configure_chrome_options()
    service = Service(r"C:\Users\23037335\Desktop\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:

        links_to_offices = get_links_to_offices_google(driver, link_to_offices, required_place_type)

        all_reviews = []
        
        for url in tqdm(links_to_offices):
            print(f'Парсим {url}')
            office_reviews = parse_one_office_google_maps(driver, url, expected_name=business_name, legal_name_cleaned=legal_name_cleaned, search_name=search_name, is_hotel=is_hotel)
            all_reviews.extend(office_reviews)
            print(f"Собрано {len(office_reviews)} отзывов для этого офиса")
        
        google_maps_df = pd.DataFrame(all_reviews)
        google_maps_df = format_and_save_dataframe(google_maps_df, search_years)
        return google_maps_df
        
    finally:
        driver.quit()

if __name__ == "__main__":
    import pandas as pd

    # 📂 Читаем Excel-файл
    try:
        df_input = pd.read_excel("ДЗО_города.xlsx", sheet_name=0)  # 0 = первый лист
        print(f"✅ Загружено {len(df_input)} строк из Excel.")
    except Exception as e:
        print(f"❌ Ошибка при чтении файла 'ДЗО.xlsx': {e}")
        exit(1)


    required_columns = ["Бизнес наименование", "Юридическое наименование", "пропускаем"]
    for col in required_columns:
        if col not in df_input.columns:
            print(f"❌ В файле нет столбца '{col}'. Проверь название столбца!")
            exit(1)

   # 🌍 Список целевых регионов
    RU_REGIONS = {
        'Амурская область', 'Архангельская область', 'Астраханская область', 'Белгородская область',
        'Брянская область', 'Владимирская область', 'Волгоградская область', 'Вологодская область',
        'Воронежская область', 'Ивановская область', 'Иркутская область', 'Калининградская область',
        'Калужская область', 'Кемеровская область - Кузбасс', 'Кировская область', 'Костромская область',
        'Курганская область', 'Курская область', 'Ленинградская область', 'Липецкая область',
        'Магаданская область', 'Москва', 'Московская область', 'Мурманская область',
        'Нижегородская область', 'Новгородская область', 'Новосибирская область', 'Омская область',
        'Оренбургская область', 'Орловская область', 'Пензенская область', 'Псковская область',
        'Ростовская область', 'Рязанская область', 'Самарская область', 'Санкт-Петербург',
        'Саратовская область', 'Сахалинская область', 'Свердловская область', 'Севастополь',
        'Смоленская область', 'Тамбовская область', 'Тверская область', 'Томская область',
        'Тульская область', 'Тюменская область', 'Ульяновская область', 'Челябинская область',
        'Ярославская область'
    }

    # 📂 Загружаем towns.csv
    try:
        df_towns = pd.read_csv("towns.csv", sep=",")
        print(f"✅ Загружено {len(df_towns)} городов из towns.csv.")
    except Exception as e:
        print(f"❌ Ошибка при загрузке towns.csv: {e}")
        exit(1)

    if "city" not in df_towns.columns or "region_name" not in df_towns.columns:
        print("❌ В towns.csv должны быть столбцы 'city' и 'region_name'")
        exit(1)


    df_towns_filtered = df_towns[df_towns["region_name"].isin(RU_REGIONS)]
    cities = df_towns_filtered["city"].dropna().unique().tolist()
    print(f"✅ Найдено {len(cities)} городов в целевых регионах.")


    df_filtered = df_input[df_input["пропускаем"] != 1].copy()
    print(f"📋 Всего строк после фильтрации (пропускаем != 1): {len(df_filtered)}")


    business_names = df_filtered["Бизнес наименование"].dropna().unique().tolist()
    print(f"📋 Найдено {len(business_names)} уникальных названий бизнесов для парсинга.")

    search_years = {2023, 2024}
    required_type = ["Банк", "Аптека"]

    print("🚀 Запускаем парсинг Google Maps...")

    all_reviews_df = pd.DataFrame()  

    for i, business in enumerate(business_names, 1):

        matching_rows = df_filtered[df_filtered["Бизнес наименование"] == business]
        if matching_rows.empty:
            print(f"⚠️  Для бизнеса '{business}' не найдено данных после фильтрации — пропускаем.")
            continue


        search_name_row = matching_rows["Название в google maps"].iloc[0] if "Название в google maps" in df_filtered.columns else None
        search_name = search_name_row.strip() if pd.notna(search_name_row) else business
        print(f"🔍 Используем для поиска: '{search_name}' (оригинальное название: '{business}')")


        legal_name_row = matching_rows["Юридическое наименование"].iloc[0]
        legal_name_cleaned = extract_name_in_quotes(legal_name_row) if pd.notna(legal_name_row) else None
        print(f"⚖️  Юр. название (очищенное из кавычек): '{legal_name_cleaned}'")


        is_hotel_row = matching_rows["Отель"].iloc[0] if "Отель" in df_filtered.columns else 0
        is_hotel = bool(is_hotel_row == 1)
        print(f"🏨 Это отель: {is_hotel}")


        search_name_clean = search_name.strip().replace(' ', '+')
        for city in cities:
            city_clean = city.strip().replace(' ', '+')
            url = f"https://www.google.com/maps/search/{search_name_clean}+{city_clean}"

            print(f"\n{'='*70}")
            print(f"🏢 Бизнес {i}/{len(business_names)}: {business}")
            print(f"🔍 Поиск по: {search_name} | 🌍 Город: {city} | 🏨 Отель: {is_hotel}")
            print(f"🔗 URL: {url}")
            print(f"{'='*70}")

            try:
                df = parse_google_maps(
                    link_to_offices=url,
                    search_years=search_years,
                    required_place_type=required_type,
                    business_name=business,
                    legal_name_cleaned=legal_name_cleaned,
                    search_name=search_name,
                    is_hotel=is_hotel
                )

                if not df.empty:
                    df['product'] = business
                    all_reviews_df = pd.concat([all_reviews_df, df], ignore_index=True)
                    print(f"✅ Добавлено {len(df)} отзывов. Всего: {len(all_reviews_df)}")
                else:
                    print("⚠️  Отзывов не найдено.")

            except Exception as e:
                print(f"❌ Ошибка при парсинге: {e}")
                continue

            # 🛑 Пауза между запросами 
            print("⏳ Пауза 8 секунд...")
            time.sleep(8)
    output_dir = "google_maps_towns_output"
    os.makedirs(output_dir, exist_ok=True)
    # 💾 Сохраняем общий файл
    if not all_reviews_df.empty:
        retr_date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        filename = f'google_maps_all_reviews_{retr_date}.xlsx'
        filepath = os.path.join(output_dir, filename)
        all_reviews_df.to_excel(filepath, index=False)
        print(f"\n🎉 ВСЕГО собрано {len(all_reviews_df)} отзывов.")
        print(f"📁 Файл сохранён: {filepath}")
    else:
        print("Ничего не собрано. Проверь параметры.")

    print("✅ Парсинг завершён!")
