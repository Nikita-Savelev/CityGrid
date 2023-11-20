# CityGrid

## Демонстрация работы

1. Построение матрицы со случайным количеством заблокированных блоков (по умолчанию 30, но можно задать произвольное значение)

   ![Example 1](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_1.png)

2. Установка башни (радиус, бюджет и стоимость башни можно изменить)

   ![Example 2](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_2.png)

3. Покрытие свободных блоков башнями (для оптимизации использован жадный алгоритм для наилучшего покрытия за выделенный бюджет)

   ![Example 3](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_3.png)

4. Поиск кратчайшего пути (для этой задачи использован алгоритм "Поиск A*" с использованием графов)

   ![Example 4](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_4.png)

Пример со следующими входными значениями (radius=2, n=9, m=9, percent_blocked_blocks=50, budget=1020, tower_price=50)

   ![Example 5](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_5.png)

В следующем примере бюджет ограничен. Входные значения (radius=1, n=10, m=10, percent_blocked_blocks=40, budget=340, tower_price=54)
  ![Example 6](https://github.com/Nikita-Savelev/CityGrid/blob/main/example_6.png)

## Как запустить

1. Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv\bin\activate
```
2. установите все зависимости
```
pip install -r requirements.txt
```
3. Запустите скрипт CityGrid.py
```
python CityGrid.py
```
