def pairwise(lst):
    """Разбивает список [a, b, c, d] на [(a, b), (c, d)]"""
    return list(zip(lst[::2], lst[1::2]))


def intersect(a, b):
    """Возвращает пересечение двух отрезков [start, end]"""
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    if start < end:
        return (start, end)
    return None


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals["lesson"]
    pupil_intervals = pairwise(intervals["pupil"])
    tutor_intervals = pairwise(intervals["tutor"])

    # Обрезаем интервалы по границам урока
    def clip_to_lesson(intervals):
        result = []
        for start, end in intervals:
            clipped = intersect((start, end), lesson)
            if clipped:
                result.append(clipped)
        return result

    pupil_clipped = clip_to_lesson(pupil_intervals)
    tutor_clipped = clip_to_lesson(tutor_intervals)

    # Собираем все пересечения между интервалами ученика и преподавателя
    intersections = []
    for ps, pe in pupil_clipped:
        for ts, te in tutor_clipped:
            inter = intersect((ps, pe), (ts, te))
            if inter:
                intersections.append(inter)

    # Объединяем пересекающиеся интервалы
    if not intersections:
        return 0
    intersections.sort()
    merged: list[list[int]] = []
    for interval in intersections:
        if not merged:
            merged.append(list(interval))
        else:
            last = merged[-1]
            if interval[0] <= last[1]:  # пересекаются или соприкасаются
                last[1] = max(last[1], interval[1])
            else:
                merged.append(list(interval))
    # Суммируем итоговую длительность без дублирующихся секунд
    total = sum(end - start for start, end in merged)
    return total


tests = [
    {
        'intervals': {
            'lesson': [1594663200, 1594666800],
            'pupil': [
                1594663340, 1594663389,
                1594663390, 1594663395,
                1594663396, 1594666472,
            ],
            'tutor': [
                1594663290, 1594663430,
                1594663443, 1594666473,
            ],
        },
        'answer': 3117,
    },
    {
        'intervals': {
            'lesson': [1594702800, 1594706400],
            'pupil': [
                1594702789, 1594704500,
                1594702807, 1594704542,
                1594704512, 1594704513,
                1594704564, 1594705150,
                1594704581, 1594704582,
                1594704734, 1594705009,
                1594705095, 1594705096,
                1594705106, 1594706480,
                1594705158, 1594705773,
                1594705849, 1594706480,
                1594706500, 1594706875,
                1594706502, 1594706503,
                1594706524, 1594706524,
                1594706579, 1594706641,
            ],
            'tutor': [
                1594700035, 1594700364,
                1594702749, 1594705148,
                1594705149, 1594706463,
            ],
        },
        'answer': 3577,
    },
    {
        'intervals': {
            'lesson': [1594692000, 1594695600],
            'pupil': [
                1594692033, 1594696347,
            ],
            'tutor': [
                1594692017, 1594692066,
                1594692068, 1594696341,
            ],
        },
        'answer': 3565,
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        expected = test['answer']
        assert test_answer == expected, (
            f'Test case {i} failed: got {test_answer}, expected {expected}'
        )
