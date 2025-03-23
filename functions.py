def optimize_atm_locations_ver_1_3(n, k, L):
    # Функция проверяет, можно ли достичь максимального расстояния max_dist,
    # добавив ровно k банкоматов
    def is_feasible(max_dist):
        atms_needed = 0
        for dist in L:
            # Сколько банкоматов нужно добавить в этот интервал
            atms_needed += max(0, (dist - 1) // max_dist)
        return atms_needed <= k

    # Бинарный поиск для нахождения минимально возможного максимального расстояния
    left, right = 1, max(L)
    while left < right:
        mid = (left + right) // 2
        if is_feasible(mid):
            right = mid
        else:
            left = mid + 1

    max_distance = left

    # Размещаем минимально необходимое количество банкоматов
    result = []
    atms_used = 0

    # Сохраняем информацию о каждом исходном сегменте
    segments_info = []

    for dist in L:
        # Сколько банкоматов нужно добавить в этот интервал
        atms_needed = max(0, (dist - 1) // max_distance)
        atms_used += atms_needed

        # Количество сегментов после добавления банкоматов
        segments = atms_needed + 1
        segment_length = dist / segments

        # Добавляем информацию о сегменте и его частях
        segments_info.append((segment_length, segments))

        # Добавляем все части в результат
        for _ in range(segments):
            result.append(segment_length)

    # Распределяем оставшиеся банкоматы
    remaining_atms = k - atms_used

    # Пока есть оставшиеся банкоматы
    while remaining_atms > 0:
        # Находим самый длинный сегмент
        max_length = 0
        max_idx = -1

        for i, (length, _) in enumerate(segments_info):
            if length > max_length:
                max_length = length
                max_idx = i

        # Делим самый длинный сегмент пополам
        old_length, segments_count = segments_info[max_idx]
        new_length = old_length * segments_count / (segments_count + 1)
        segments_info[max_idx] = (new_length, segments_count + 1)

        # Обновляем результат
        result = []
        for length, count in segments_info:
            for _ in range(count):
                result.append(length)

        remaining_atms -= 1

    return result


def optimize_atm_locations_2_2_1(n, k, L):
    # Функция проверки, можно ли добиться максимального расстояния не более max_dist
    def is_possible(max_dist):
        needed_atms = 0
        for dist in L:
            needed_atms += max(0, (dist + max_dist - 1) // max_dist - 1)
        return needed_atms <= k

    # Бинарный поиск для нахождения минимально возможного максимального расстояния
    left, right = 1, max(L) * 100  # Увеличиваем верхнюю границу для точности
    while right - left > 1e-6:  # Используем точность для дробных чисел
        mid = (left + right) / 2
        if is_possible(mid):
            right = mid
        else:
            left = mid

    max_dist = right

    # Распределяем банкоматы оптимально
    result = []
    total_atms_used = 0

    # Информация о каждом исходном интервале
    intervals = []

    for dist in L:
        # Минимальное количество банкоматов для этого интервала
        min_atms = max(0, int(dist / max_dist) - 1)
        total_atms_used += min_atms

        # Исходный интервал и минимальное количество банкоматов
        intervals.append((dist, min_atms))

    # Распределяем оставшиеся банкоматы
    remaining_atms = k - total_atms_used

    # Приоритизируем интервалы для добавления банкоматов
    while remaining_atms > 0:
        best_improvement = 0
        best_idx = -1

        for i, (dist, atms) in enumerate(intervals):
            # Текущая длина сегмента
            current_segments = atms + 1
            current_length = dist / current_segments

            # Длина после добавления еще одного банкомата
            new_segments = current_segments + 1
            new_length = dist / new_segments

            # Насколько уменьшится длина
            improvement = current_length - new_length

            if improvement > best_improvement:
                best_improvement = improvement
                best_idx = i

        # Добавляем банкомат в выбранный интервал
        dist, atms = intervals[best_idx]
        intervals[best_idx] = (dist, atms + 1)
        remaining_atms -= 1

    # Формируем итоговый список расстояний
    for dist, atms in intervals:
        segments = atms + 1
        segment_length = dist / segments
        for _ in range(segments):
            result.append(segment_length)

    return result




def optimize_atm_locations_2_2_0(n, k, L):
    def is_possible(max_dist):
        needed_atms = 0
        for dist in L:
            segments = (dist + max_dist - 1) // max_dist
            needed_atms += segments - 1
        return needed_atms <= k

    # Бинарный поиск для нахождения минимально возможного максимального расстояния
    left, right = 1, max(L)
    while left < right:
        mid = (left + right) // 2
        if is_possible(mid):
            right = mid
        else:
            left = mid + 1

    max_dist = left

    # Функция для распределения ровно k банкоматов
    def distribute_atms(max_dist):
        result = []
        total_atms_used = 0
        segments_per_interval = []

        for dist in L:
            segments = (dist + max_dist - 1) // max_dist
            atms_needed = segments - 1
            total_atms_used += atms_needed
            segments_per_interval.append(segments)
            segment_length = dist / segments
            for _ in range(segments):
                result.append(segment_length)

        # Если использовали меньше банкоматов, чем k, добавляем оставшиеся
        remaining_atms = k - total_atms_used
        if remaining_atms > 0:
            # Сортируем все сегменты по длине (в порядке убывания)
            segments_with_idx = [(i, result[i]) for i in range(len(result))]
            segments_with_idx.sort(key=lambda x: -x[1])  # Сортировка по убыванию длины

            # Добавляем оставшиеся банкоматы в самые длинные сегменты
            for i in range(min(remaining_atms, len(segments_with_idx))):
                idx, length = segments_with_idx[i]
                # Делим сегмент на две равные части
                new_length = length / 2
                result[idx] = new_length
                result.insert(idx + 1, new_length)

        return result

    result = distribute_atms(max_dist)

    return result
