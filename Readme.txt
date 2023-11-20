# CityGrid
## Демонстрация работы
1. Построение матрицы со случайным количеством заблокированных блоков (по умолчанию 30, но можно задать произвольное значение)
![Example №1](figures/example_1.png)

2. Установка башни (радиус, бюджет и стоимость башни можно поменять)
![Example №2](figures/example_2.png)

3. Покрытие свободных блоков башнями (для оптимизации был использован жадный алгоритм для наилучшего покрытия за выделенный бюджет)
![Example №3](figures/example_3.png)

4. Поиск кратчайшего пути (для этой задачи был использован алгоритм "Поиск A*" с использованием графов)
![Example №4](figures/example_4.png)

Вот пример со следующими входными значениями (radius=2, n=9, m=9, percent_blocked_blocks=50, budget=1020, tower_price=50)
![](figures/example_5.png)

В следующем примере бюджет ограничен. Входные значения (radius=1, n=10, m=10, percent_blocked_blocks=40, budget=340, tower_price=54)
![](figures/example_6.png)

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
