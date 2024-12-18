import math


class Solution:
    def __init__(self):#инициализирует списки для хранения
        self.segments = []
        self.intersections = []
        self.multiple_intersections = []

    def read_segments_from_file(self, filename):
        try:#в случае чего выведет ошибку, если таковая допущена
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        try:
                            x1, y1, x2, y2, segment_number = map(float, parts)
                            self.segments.append((x1, y1, x2, y2, int(segment_number)))
                        except ValueError:
                            print(f"Ошибка: неверный формат данных в строке: {line.strip()}. Строка пропущена.")
                    else:
                        print(f"Ошибка: неверное количество данных в строке: {line.strip()}. Строка пропущена.")
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")


    def calculate_area_ratio(self, x1, y1, x2, y2):
        if x1 == x2 == y1 == y2:
            return(0,0)
        if (x1 == x2) and (y1 != y2):  # Вертикальный отрезок
            if x1 == 0 or x1 == 1:
                return (0, 0)
            area1 = x1  # Левая площадь
            area2 = 1 - x1  # Правая площадь
            return(area1,area2)
        if (y1 == y2) and (x1 != x2):  # Горизонтальный отрезок
            if y1 == 0 or y1 == 1:
                return (0, 0)
            area1 = y1  # Нижняя площадь
            area2 = 1 - y1  # Верхняя площадь
            return (area1, area2)
        if ((y1 == x1 == 0) and (y2 == x2 == 1)) or ((y1 == x1 == 1) and (y2 == x2 == 0)):
            return(0.5,0.5)
        else:  # Наклонный отрезок
            intersections = []

            # пересечение с y = 0
            if (y1 * y2) <= 0:
                if y1 != y2:
                    x = x1 + (x2 - x1) * (-y1) / (y2 - y1)
                    if x >= 0 and x <= 1:
                        intersections.append((x, 0))

            # пересечение с y = 1
            if (1 - y1) * (1 - y2) <= 0:
                if y1 != y2:
                    x = x1 + (x2 - x1) * (1 - y1) / (y2 - y1)
                    if x >= 0 and x <= 1:
                        intersections.append((x, 1))

            # пересечение с x = 0
            if (x1 * x2) <= 0:
                if x1 != x2:
                    y = y1 + (y2 - y1) * (-x1) / (x2 - x1)
                    if y >= 0 and y <= 1:
                        intersections.append((0, y))

            # пересечение с x = 1
            if (1 - x1) * (1 - x2) <= 0:
                if x1 != x2:
                    y = y1 + (y2 - y1) * (1 - x1) / (x2 - x1)
                    if y >= 0 and y <= 1:
                        intersections.append((1, y))

            # Вычисление площадей по пересечениям
            if len(intersections) == 0 or len(intersections) == 1:
                return (0, 0)
            else:
                (x1_int, y1_int) = intersections[0]
                (x2_int, y2_int) = intersections[1]
                area = abs((x1_int * y2_int - x2_int * y1_int) / 2)

                area1 = area
                area2 = 1 - area
                return (area1, area2)


    def find_intersections(self):#находит точки пересечения у отрезков, всё находится с помощью определителя
        for i in range(len(self.segments)):
            x1, y1, x2, y2, seg1 = self.segments[i]
            for j in range(i + 1, len(self.segments)):
                x3, y3, x4, y4, seg2 = self.segments[j]

                det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

                if det == 0:  # Отрезки параллельны или совпадают
                    continue
                #точки пересечения
                px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
                py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

                #проверка, что точка пересечения находится на отрезках и в квадрате
                if 0 <= px <= 1 and 0 <= py <= 1:
                    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and min(x3, x4) <= px <= max(
                            x3, x4) and min(y3, y4) <= py <= max(y3, y4):

                        found = False
                        for intersection in self.intersections:
                            if math.isclose(intersection[0], px) and math.isclose(intersection[1], py):#смотрим, близки ли по значению наши точки с теми, которые находились в массиве
                                if seg1 not in intersection[2]:#дальше проверяем(точка в массиве такая есть), есть ли данные отрезки в массиве
                                    intersection[2].append(seg1)#если нет, то добавляем, если есть, то пропускаем
                                if seg2 not in intersection[2]:
                                    intersection[2].append(seg2)
                                found = True
                                break
                        if not found:#если в массиве ничего не задано было, либо таких точек ещё не было, то добавляем обе
                            self.intersections.append((px, py, [seg1, seg2]))#а также отрезки, которые в точке пересекаются


    def find_multiple_intersections(self):#находим те точки, где пересеклись 3 и больше отрезка
        for intersection in self.intersections:
            if len(intersection[2]) >= 3:
                self.multiple_intersections.append(intersection)


    def print_results(self):
        print("Соотношения площадей, в которых отрезки делят квадрат:")
        for x1, y1, x2, y2, segment_number in self.segments:
            area1, area2 = self.calculate_area_ratio(x1, y1, x2, y2)
            print(f"Отрезок {segment_number}: {area1:.4f} / {area2:.4f}")

        print("Точки пересечения отрезков:")
        if not self.intersections:
            print("Нет точек пересечения.")
        else:
            for x, y, segs in self.intersections:
                print(f"({x:.4f}, {y:.4f}) - Отрезки: {segs}")

        print("Точки, в которых пересекаются минимум три отрезка:")
        if not self.multiple_intersections:
            print("Таких точек не найдено")
        else:
            for x, y, segs in self.multiple_intersections:
                print(f"({x:.4f}, {y:.4f}) - Отрезки: {segs}")

solution = Solution()
solution.read_segments_from_file('segments.txt')
solution.find_intersections()
solution.find_multiple_intersections()
solution.print_results()